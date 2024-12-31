from models import ClinicalDocument
from main import analyze_clinical_trial

def run_example():
    # Create sample documents
    documents = [
        ClinicalDocument(
            doc_id="PROTO-001",
            doc_type="protocol",
            content="Sample protocol content describing trial design and criteria",
            metadata={"version": "1.0"}
        ),
        ClinicalDocument(
            doc_id="SAFETY-001",
            doc_type="safety_report",
            content="Safety monitoring data and observations",
            metadata={"date": "2024-01-01"}
        ),
        # Add more documents as needed
    ]

    # Run analysis
    results = analyze_clinical_trial("TRIAL-001", documents)
    
    # Print results
    print("Analysis Results:")
    print(f"Trial ID: {results['trial_id']}")
    print("\nProtocol Analysis:")
    print(results['protocol_analysis'])
    print("\nSafety Alerts:")
    print(results['safety_alerts'])
    print("\nQuality Issues:")
    print(results['quality_issues'])
    print("\nRecommendations:")
    for rec in results['recommendations']:
        print(f"- {rec}")
    print("\nFinal Report:")
    print(results['final_report'])

if __name__ == "__main__":
    run_example()