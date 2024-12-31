from typing import List
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import os
from models import (
    TrialState,
    ProtocolAnalysis,
    SafetyAlert,
    DataQualityIssue
)

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",  
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)


# Define structured output models for lists
class SafetyAlertList(BaseModel):
    alerts: List[SafetyAlert]

class QualityIssueList(BaseModel):
    issues: List[DataQualityIssue]

class ProtocolAgent:
    @staticmethod
    def analyze_protocol(state: TrialState):
        """Analyzes clinical trial protocol documents"""
        
        system_prompt = """You are an expert clinical trial protocol analyzer. Review the protocol and extract:
        1. Key eligibility criteria
        2. Inclusion/exclusion criteria
        3. Study endpoints
        4. Safety monitoring requirements"""
        
        protocol_docs = [doc for doc in state["documents"] if doc.doc_type == "protocol"]
        if not protocol_docs:
            return {"protocol_analysis": None}
            
        protocol_content = "\n\n".join([doc.content for doc in protocol_docs])
        
        response = llm.with_structured_output(ProtocolAnalysis).invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Analyze this protocol: {protocol_content}")
            ]
        )
        
        return {"protocol_analysis": response}

class SafetyAgent:
    @staticmethod
    def monitor_safety(state: TrialState):
        """Monitors for safety concerns and generates alerts"""
        
        system_prompt = """You are an expert clinical trial safety monitor. Review the documents and:
        1. Identify potential safety concerns
        2. Assess severity levels
        3. Provide specific recommendations
        4. Link concerns to relevant protocol criteria"""
        
        docs_content = "\n\n".join([doc.content for doc in state["documents"]])
        protocol = state["protocol_analysis"]
        
        response = llm.with_structured_output(SafetyAlertList).invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Review these documents: {docs_content}\nProtocol analysis: {protocol}")
            ]
        )
        
        return {"safety_alerts": response.alerts}

class QualityAgent:
    @staticmethod
    def monitor_data_quality(state: TrialState):
        """Monitors for data quality issues"""
        
        system_prompt = """You are an expert clinical data quality analyst. Review the documents and:
        1. Identify potential data quality issues
        2. Categorize issues by type
        3. Assess impact levels
        4. Suggest resolutions"""
        
        docs_content = "\n\n".join([doc.content for doc in state["documents"]])
        
        response = llm.with_structured_output(QualityIssueList).invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Review these documents: {docs_content}")
            ]
        )
        
        return {"quality_issues": response.issues}

class RecommendationsAgent:
    @staticmethod
    def generate_recommendations(state: TrialState):
        """Generates overall trial recommendations"""
        
        system_prompt = """You are an expert clinical trial advisor. Based on the protocol analysis, 
        safety alerts, and quality issues, provide strategic recommendations for trial optimization."""
        
        response = llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"""Review this information:
                Protocol: {state['protocol_analysis']}
                Safety Alerts: {state['safety_alerts']}
                Quality Issues: {state['quality_issues']}""")
            ]
        )
        
        return {"recommendations": response.content.split('\n')}

class ReportGenerator:
    @staticmethod
    def generate_final_report(state: TrialState):
        """Generates comprehensive trial analysis report"""
        
        system_prompt = """You are an expert clinical trial report writer. Create a comprehensive 
        analysis report that includes protocol insights, safety concerns, data quality issues, 
        and strategic recommendations."""
        
        response = llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"""Generate report based on:
                Protocol: {state['protocol_analysis']}
                Safety: {state['safety_alerts']}
                Quality: {state['quality_issues']}
                Recommendations: {state['recommendations']}""")
            ]
        )
        
        return {"final_report": response.content}