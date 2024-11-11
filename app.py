import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from model import EmbeddingManager  # Replace with the actual name of your backend code file

# Initialize the embedding manager (adjust the path as necessary)
folder_path = 'data/agents'  # Path to your folder containing JSON files
embedding_manager = EmbeddingManager(folder_path)

# Streamlit UI setup
st.title("Agent Query Interface")

# Text input field for search query
query_text = st.text_input(
    "Search",
    placeholder="Type a query..."
)

# Button to trigger the generation process
if st.button("Generate"):
    if query_text:
        # Generate embeddings and perform the search
        agents_df = embedding_manager.query_embedding(query_text)

        if agents_df is not None and not agents_df.empty:
            st.write("Results:")
            # Display the dataframe with relevant columns
            st.dataframe(agents_df[['filename', 'adjusted_score', 'similarity', 'distance']])
        else:
            st.write("No suitable agent found.")
    else:
        st.warning("Please enter a query before generating.")

# Add functionality for repeated runs by keeping the app responsive
st.button("Reset")
