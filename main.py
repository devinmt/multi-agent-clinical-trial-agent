from typing import List
from langgraph.graph import StateGraph, START, END

from models import TrialState, ClinicalDocument
from agents import (
    ProtocolAgent,
    SafetyAgent,
    QualityAgent,
    RecommendationsAgent,
    ReportGenerator
)

def create_trial_graph():
    """Creates and returns the clinical trial analysis graph"""
    
    # Build the graph
    builder = StateGraph(TrialState)

    # Add nodes
    builder.add_node("analyze_protocol", ProtocolAgent.analyze_protocol)
    builder.add_node("monitor_safety", SafetyAgent.monitor_safety)
    builder.add_node("monitor_quality", QualityAgent.monitor_data_quality)
    builder.add_node("generate_recommendations", RecommendationsAgent.generate_recommendations)
    builder.add_node("generate_report", ReportGenerator.generate_final_report)

    # Add edges - Fixed to handle parallel paths correctly
    builder.add_edge(START, "analyze_protocol")
    builder.add_edge("analyze_protocol", "monitor_safety")
    builder.add_edge("analyze_protocol", "monitor_quality")
    builder.add_edge("monitor_safety", "generate_recommendations")
    builder.add_edge("monitor_quality", "generate_recommendations")
    builder.add_edge("generate_recommendations", "generate_report")
    builder.add_edge("generate_report", END)

    # Compile the graph
    return builder.compile()

def analyze_clinical_trial(trial_id: str, documents: List[ClinicalDocument]):
    """Process a clinical trial through the multi-agent system"""
    
    # Create initial state
    initial_state = {
        "trial_id": trial_id,
        "documents": documents,
        "protocol_analysis": None,
        "safety_alerts": [],
        "quality_issues": [],
        "recommendations": [],
        "final_report": ""
    }
    
    # Get the graph
    graph = create_trial_graph()
    
    # Run the analysis
    final_state = graph.invoke(initial_state)
    return final_state