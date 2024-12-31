from IPython.display import Image, display
import streamlit as st
from main import create_trial_graph

def display_langgraph_visualization():
    """Display the LangGraph visualization using draw_mermaid_png"""
    try:
        # Create the graph
        graph = create_trial_graph()
        
        # Get the mermaid PNG visualization
        mermaid_png = graph.get_graph(xray=1).draw_mermaid_png()
        
        # Display in Streamlit
        st.image(mermaid_png, caption="LangGraph Workflow Visualization", use_column_width=True)
        
        # Add explanation
        with st.expander("Graph Structure Details"):
            st.write("""
            This graph visualization shows:
            - Node connections and dependencies
            - Data flow between agents
            - Parallel processing paths
            - Full system architecture
            """)
    except Exception as e:
        st.error(f"Error generating graph visualization: {str(e)}")

def display_notebook_visualization():
    """Display the visualization in a Jupyter notebook"""
    graph = create_trial_graph()
    display(Image(graph.get_graph(xray=1).draw_mermaid_png()))