"""
Cost and Time Tracking Component for AutoDoc AI
Tracks API usage costs and generation time in real-time

FIXES:
- Correct Haiku 4.5 pricing ($1.00/$5.00 instead of $0.80/$4.00)
- Added Sonnet 4 pricing support ($3.00/$15.00)
- Model-specific cost calculation
"""

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class APICall:
    """Single API call record"""
    timestamp: datetime
    agent: str
    operation: str
    model: str  # NEW: Track which model was used
    input_tokens: int
    output_tokens: int
    cost_usd: float
    
class CostTracker:
    """
    Tracks API costs and time for documentation generation.
    
    Features:
    - Real-time cost calculation
    - Per-agent cost breakdown
    - Multi-model support (Haiku 4.5, Sonnet 4)
    - Generation time tracking
    - Recent activity log
    """
    
    # Anthropic Claude 4.5 Haiku pricing (Nov 2024)
    HAIKU_INPUT_COST = 1.00 / 1_000_000   # $1.00 per 1M tokens (FIXED from $0.80)
    HAIKU_OUTPUT_COST = 5.00 / 1_000_000  # $5.00 per 1M tokens (FIXED from $4.00)
    
    # Anthropic Claude 4 Sonnet pricing (Nov 2024)
    SONNET_INPUT_COST = 3.00 / 1_000_000   # $3.00 per 1M tokens (NEW)
    SONNET_OUTPUT_COST = 15.00 / 1_000_000 # $15.00 per 1M tokens (NEW)
    
    def __init__(self):
        """Initialize cost tracker"""
        self.calls: List[APICall] = []
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        
    def start_tracking(self):
        """Start timing the generation"""
        self.start_time = time.time()
        
    def stop_tracking(self):
        """Stop timing the generation"""
        self.end_time = time.time()
        
    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost based on model type.
        
        Args:
            model: Model identifier (haiku, sonnet, or full model string)
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost in USD
        """
        model_lower = model.lower()
        
        # Determine pricing based on model
        if 'sonnet' in model_lower:
            input_cost = self.SONNET_INPUT_COST
            output_cost = self.SONNET_OUTPUT_COST
        else:
            # Default to Haiku pricing
            input_cost = self.HAIKU_INPUT_COST
            output_cost = self.HAIKU_OUTPUT_COST
        
        return (input_tokens * input_cost) + (output_tokens * output_cost)
    
    def record_usage(
        self,
        agent: str,
        operation: str,
        input_tokens: int,
        output_tokens: int,
        model: str = "haiku"  # NEW: Default to Haiku for backward compatibility
    ):
        """
        Record an API call.
        
        Args:
            agent: Name of agent making the call
            operation: Description of operation
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model used (haiku, sonnet, or full model string)
        """
        cost_usd = self._calculate_cost(model, input_tokens, output_tokens)
        
        call = APICall(
            timestamp=datetime.now(),
            agent=agent,
            operation=operation,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd
        )
        
        self.calls.append(call)
        
    @property
    def total_calls(self) -> int:
        """Total number of API calls"""
        return len(self.calls)
        
    @property
    def total_input_tokens(self) -> int:
        """Total input tokens across all calls"""
        return sum(call.input_tokens for call in self.calls)
        
    @property
    def total_output_tokens(self) -> int:
        """Total output tokens across all calls"""
        return sum(call.output_tokens for call in self.calls)
        
    @property
    def total_tokens(self) -> int:
        """Total tokens (input + output)"""
        return self.total_input_tokens + self.total_output_tokens
        
    @property
    def total_cost_usd(self) -> float:
        """Total cost in USD"""
        return sum(call.cost_usd for call in self.calls)
        
    @property
    def generation_time_seconds(self) -> Optional[float]:
        """Total generation time in seconds"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
        
    @property
    def generation_time_formatted(self) -> str:
        """Formatted generation time"""
        if self.generation_time_seconds is None:
            return "In progress..."
        
        seconds = self.generation_time_seconds
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        else:
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            return f"{minutes}m {remaining_seconds}s"
            
    def get_cost_by_agent(self) -> dict:
        """Get cost breakdown by agent"""
        agent_costs = {}
        for call in self.calls:
            if call.agent not in agent_costs:
                agent_costs[call.agent] = 0.0
            agent_costs[call.agent] += call.cost_usd
        return agent_costs
    
    def get_cost_by_model(self) -> dict:
        """Get cost breakdown by model (NEW)"""
        model_costs = {}
        for call in self.calls:
            if call.model not in model_costs:
                model_costs[call.model] = 0.0
            model_costs[call.model] += call.cost_usd
        return model_costs
        
    def get_recent_calls(self, n: int = 5) -> List[APICall]:
        """Get n most recent API calls"""
        return self.calls[-n:] if self.calls else []
        
    def reset(self):
        """Reset all tracking data"""
        self.calls = []
        self.start_time = None
        self.end_time = None


def display_cost_dashboard(tracker: CostTracker):
    """
    Display cost tracking dashboard in Streamlit.
    
    Args:
        tracker: CostTracker instance
    """
    import streamlit as st
    
    st.success(f"✅ Tracking {tracker.total_calls} API calls with real cost data")
    
    # Main metrics
    st.subheader("📊 Actual Costs (Current Session)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cost", f"${tracker.total_cost_usd:.4f}")
    
    with col2:
        st.metric("Total Tokens", f"{tracker.total_tokens:,}")
    
    with col3:
        st.metric("API Calls", tracker.total_calls)
    
    with col4:
        # Show generation time instead of avg cost/call
        if tracker.generation_time_seconds:
            st.metric("Generation Time", tracker.generation_time_formatted)
        else:
            st.metric("Generation Time", "In progress...")
    
    # Cost breakdown by agent
    st.subheader("Cost by Agent")
    agent_costs = tracker.get_cost_by_agent()
    
    if agent_costs:
        for agent, cost in agent_costs.items():
            percentage = (cost / tracker.total_cost_usd * 100) if tracker.total_cost_usd > 0 else 0
            st.write(f"**{agent}:** ${cost:.4f} ({percentage:.1f}%)")
    else:
        st.info("No API calls recorded yet")
    
    # Cost breakdown by model (NEW)
    st.subheader("Cost by Model")
    model_costs = tracker.get_cost_by_model()
    
    if model_costs:
        for model, cost in model_costs.items():
            percentage = (cost / tracker.total_cost_usd * 100) if tracker.total_cost_usd > 0 else 0
            st.write(f"**{model}:** ${cost:.4f} ({percentage:.1f}%)")
    
    # Recent activity
    st.subheader("Recent Activity (Last 5)")
    recent_calls = tracker.get_recent_calls(5)
    
    if recent_calls:
        for call in reversed(recent_calls):  # Show most recent first
            time_str = call.timestamp.strftime("%H:%M:%S")
            st.write(f"▸ {time_str} - {call.agent} ({call.model}) - ${call.cost_usd:.4f}")
    else:
        st.info("No recent activity")
