import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from model import EmbeddingManager  

folder_path = 'data/agents' 
embedding_manager = EmbeddingManager(folder_path)

st.title("Agent Query Interface")

query_text = st.text_input(
    "Search",
    placeholder="Type a query..."
)

if st.button("Generate"):
    if query_text:
        agents_df = embedding_manager.query_embedding(query_text)

        if agents_df is not None and not agents_df.empty:
            st.write("Results:")
            st.dataframe(agents_df[['filename', 'adjusted_score', 'similarity', 'distance']])
        else:
            st.write("No suitable agent found.")
    else:
        st.warning("Please enter a query before generating.")

st.button("Reset")
