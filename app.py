import os
import streamlit as st
from dotenv import load_dotenv

# Initialize environment variables first
load_dotenv()

# Set OpenAI API key from Streamlit secrets
if 'OPENAI_API_KEY' in st.secrets:
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
elif not os.getenv('OPENAI_API_KEY'):
    st.error('OpenAI API key not found! Please set it in your Streamlit secrets.')
    st.stop()

# Now import the rest of the dependencies
import pandas as pd
from typing import List
import time
import chardet
from models import ClinicalDocument
from main import analyze_clinical_trial

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .report-box {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e1e4e8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_config():
    try:
        with open('clinical_trial_ai.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("Configuration file not found. Using default settings.")
        return {}

def read_file_content(uploaded_file):
    """Safely read uploaded file content with encoding detection"""
    try:
        # Read the binary content
        bytes_data = uploaded_file.getvalue()
        
        # Detect the encoding
        result = chardet.detect(bytes_data)
        encoding = result['encoding']
        
        # If no encoding is detected, default to utf-8
        if not encoding:
            encoding = 'utf-8'
        
        # Try to decode with detected encoding
        try:
            content = bytes_data.decode(encoding)
        except UnicodeDecodeError:
            # If that fails, try with utf-8 and ignore errors
            content = bytes_data.decode('utf-8', errors='ignore')
            
        return content
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

def upload_documents():
    """Handle document uploads with proper encoding detection"""
    uploaded_files = st.file_uploader(
        "Upload Clinical Trial Documents",
        accept_multiple_files=True,
        type=['txt', 'pdf', 'doc', 'docx']
    )
    
    documents = []
    if uploaded_files:
        for idx, file in enumerate(uploaded_files):
            st.write(f"Processing file: {file.name}")
            
            doc_type = st.selectbox(
                f"Select document type for {file.name}",
                ["protocol", "safety_report", "case_report", "other"],
                key=f"doc_type_{idx}"
            )
            
            try:
                content = read_file_content(file)
                if content is not None:
                    documents.append(ClinicalDocument(
                        doc_id=f"DOC-{idx+1:03d}",
                        doc_type=doc_type,
                        content=content,
                        metadata={
                            "filename": file.name,
                            "size": len(content)
                        }
                    ))
                    st.success(f"Successfully processed {file.name}")
                else:
                    st.error(f"Failed to process {file.name}")
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
            finally:
                file.seek(0)
    
    return documents

def display_header():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("Clinical Trials AI Assistant")
        st.write("Powered by Multi-Agent AI System")

def display_analysis_settings():
    with st.expander("Analysis Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                "Analysis Mode",
                ["Comprehensive", "Safety Focus", "Quality Focus"]
            )
        with col2:
            st.slider(
                "Analysis Depth",
                min_value=1,
                max_value=5,
                value=3
            )

def display_progress():
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    st.success("Analysis Complete!")

def display_protocol_analysis(protocol_analysis):
    with st.expander("Protocol Analysis", expanded=True):
        if protocol_analysis:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Key Criteria")
                for criterion in protocol_analysis.key_criteria:
                    st.write(f"• {criterion}")
                
                st.subheader("Study Endpoints")
                for endpoint in protocol_analysis.study_endpoints:
                    st.write(f"• {endpoint}")
            
            with col2:
                st.subheader("Inclusion Criteria")
                for criterion in protocol_analysis.inclusion_criteria:
                    st.write(f"• {criterion}")
                
                st.subheader("Exclusion Criteria")
                for criterion in protocol_analysis.exclusion_criteria:
                    st.write(f"• {criterion}")
        else:
            st.warning("No protocol analysis available")

def display_safety_alerts(safety_alerts):
    with st.expander("Safety Alerts", expanded=True):
        if safety_alerts:
            for alert in safety_alerts:
                with st.container():
                    severity_color = {
                        "high": "red",
                        "medium": "orange",
                        "low": "green"
                    }.get(alert.severity.lower(), "gray")
                    
                    st.markdown(f"""
                    <div style='padding: 1rem; border-left: 5px solid {severity_color}; margin: 1rem 0;'>
                        <h4>{alert.alert_id}: {alert.description}</h4>
                        <p><strong>Severity:</strong> {alert.severity}</p>
                        <p><strong>Recommendations:</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for rec in alert.recommendations:
                        st.write(f"• {rec}")
        else:
            st.info("No safety alerts detected")

def display_quality_issues(quality_issues):
    with st.expander("Quality Issues", expanded=True):
        if quality_issues:
            issues_df = pd.DataFrame([
                {
                    "ID": issue.issue_id,
                    "Category": issue.category,
                    "Description": issue.description,
                    "Impact": issue.impact_level,
                    "Resolution": issue.suggested_resolution
                }
                for issue in quality_issues
            ])
            st.dataframe(issues_df, use_container_width=True)
        else:
            st.info("No quality issues detected")

def display_recommendations(recommendations):
    with st.expander("Recommendations", expanded=True):
        if recommendations:
            for idx, rec in enumerate(recommendations, 1):
                st.write(f"{idx}. {rec}")
        else:
            st.info("No recommendations available")

def display_final_report(final_report):
    with st.expander("Final Report", expanded=True):
        if final_report:
            st.markdown(final_report)
        else:
            st.info("Final report not yet generated")

def main():
    # Load configuration
    config = load_config()
    
    # Display header
    display_header()
    
    # Initialize session state if needed
    if 'nav' not in st.session_state:
        st.session_state.nav = "Document Upload"
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        st.session_state.nav = st.radio(
            "Select View",
            ["Document Upload", "Analysis Results", "Settings"]
        )
        
        st.header("Quick Actions")
        if st.button("New Analysis"):
            st.session_state.clear()
            st.session_state.nav = "Document Upload"
            st.rerun()
    
    # Main content
    if st.session_state.nav == "Document Upload":
        documents = upload_documents()
        
        if documents and st.button("Start Analysis"):
            st.session_state.documents = documents
            st.session_state.nav = "Analysis Results"
            
            with st.spinner("Analyzing documents..."):
                display_progress()
                results = analyze_clinical_trial("TRIAL-001", documents)
                st.session_state.results = results
            st.rerun()
    
    elif st.session_state.nav == "Analysis Results":
        if results := st.session_state.get("results"):
            tab1, tab2, tab3 = st.tabs(["Analysis", "Alerts", "Report"])
            
            with tab1:
                display_protocol_analysis(results.get("protocol_analysis"))
                display_recommendations(results.get("recommendations"))
            
            with tab2:
                display_safety_alerts(results.get("safety_alerts"))
                display_quality_issues(results.get("quality_issues"))
            
            with tab3:
                display_final_report(results.get("final_report"))
        else:
            st.warning("No analysis results available. Please upload documents first.")
    
    elif st.session_state.nav == "Settings":
        display_analysis_settings()

if __name__ == "__main__":
    main()