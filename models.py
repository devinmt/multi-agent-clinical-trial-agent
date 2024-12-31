from typing import List, Optional, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator

class ClinicalDocument(BaseModel):
    doc_id: str
    doc_type: str = Field(description="Type of clinical document (protocol, case report, etc)")
    content: str
    metadata: dict

class ProtocolAnalysis(BaseModel):
    key_criteria: List[str]
    inclusion_criteria: List[str]
    exclusion_criteria: List[str]
    study_endpoints: List[str]
    safety_monitoring: List[str]

class SafetyAlert(BaseModel):
    alert_id: str
    severity: str
    description: str
    recommendations: List[str]
    related_criteria: List[str]

class DataQualityIssue(BaseModel):
    issue_id: str
    category: str
    description: str
    impact_level: str
    suggested_resolution: str

class TrialState(TypedDict):
    trial_id: str
    documents: List[ClinicalDocument]
    protocol_analysis: Optional[ProtocolAnalysis]
    safety_alerts: Annotated[List[SafetyAlert], operator.add]
    quality_issues: Annotated[List[DataQualityIssue], operator.add]
    recommendations: List[str]
    final_report: str