import json
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from data.queries import QUERIES, ADDITIONAL_QUERIES

# Load the pre-trained model
model = SentenceTransformer('all-mpnet-base-v2')

class EmbeddingManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.client = chromadb.Client()  
        
        existing_collections = [collection.name for collection in self.client.list_collections()]
        if "agent_descriptions" in existing_collections:
            self.collection = self.client.get_collection(name="agent_descriptions")
        else:
            self.collection = self.client.create_collection(name="agent_descriptions")


    def get_descriptions_from_folder(self):
        descriptions = {}
        try:
            for filename in os.listdir(self.folder_path):
                if filename.endswith(".json"):
                    json_file_path = os.path.join(self.folder_path, filename)
                    with open(json_file_path, 'r') as file:
                        agent_data = json.load(file)

                    description = agent_data.get('description')
                    if description:
                        descriptions[filename] = description
                    else:
                        descriptions[filename] = "Description not available"

            if not descriptions:
                print("No JSON files with valid descriptions found in the folder.")
                return {}

            return descriptions
        except FileNotFoundError:
            print(f"Error: Folder '{self.folder_path}' not found.")
            return {}
        except json.JSONDecodeError:
            print("Error decoding JSON from one of the files. Ensure all files have valid JSON.")
            return {}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

    def generate_and_store_embeddings(self, batch_size=10):
        descriptions = self.get_descriptions_from_folder()

        if isinstance(descriptions, dict) and descriptions:
            batch_embeddings = []
            batch_documents = []
            batch_metadata = []
            batch_ids = []

            for idx, (filename, description) in enumerate(descriptions.items()):
                agent_embedding = model.encode(description)

                # Append to batch lists
                batch_embeddings.append(agent_embedding.tolist())
                batch_documents.append(description)
                batch_metadata.append({"filename": filename})
                batch_ids.append(filename)

                # Store in batches
                if (idx + 1) % batch_size == 0 or (idx + 1) == len(descriptions):
                    self.collection.add(
                        embeddings=batch_embeddings,
                        documents=batch_documents,
                        metadatas=batch_metadata,
                        ids=batch_ids
                    )
                    batch_embeddings.clear()
                    batch_documents.clear()
                    batch_metadata.clear()
                    batch_ids.clear()

            print("All embeddings have been processed and stored.")
        else:
            print("No valid descriptions available for embedding generation.")

    def calculate_weight(self, query_embedding, agent_embedding):
        similarity_distance = self.calculate_similarity(query_embedding, agent_embedding)
        weight = 1 / (1 + similarity_distance)
        return weight

    def calculate_similarity(self, query_embedding, agent_embedding):
        dot_product = sum(q * a for q, a in zip(query_embedding, agent_embedding))
        norm_q = sum(q * q for q in query_embedding) ** 0.5
        norm_a = sum(a * a for a in agent_embedding) ** 0.5
        return 1 - (dot_product / (norm_q * norm_a))

    def query_embedding(self, query_text, n_results=10):
        query_embedding = model.encode(query_text)
        results = self.collection.query(query_embeddings=[query_embedding.tolist()], n_results=n_results)

        if results and 'distances' in results and results['distances']:
            agent_results = []
            for idx in range(len(results['distances'][0])):
                agent_filename = results['metadatas'][0][idx]['filename']
                agent_description = results['documents'][0][idx]
                similarity_distance = results['distances'][0][idx]

                agent_file_path = os.path.join(self.folder_path, agent_filename)
                with open(agent_file_path, 'r') as file:
                    agent_data = json.load(file)

                agent_embedding = model.encode(agent_description)

                # Calculate cosine similarity
                dot_product = sum(q * a for q, a in zip(query_embedding, agent_embedding))
                norm_q = sum(q * q for q in query_embedding) ** 0.5
                norm_a = sum(a * a for a in agent_embedding) ** 0.5
                similarity = dot_product / (norm_q * norm_a)

                weight = self.calculate_weight(query_embedding, agent_embedding)
                adjusted_score = similarity_distance * weight

                agent_results.append({
                    'filename': agent_filename,
                    'description': agent_description,
                    'similarity': similarity,
                    'distance': similarity_distance,
                    'weight': weight,
                    'adjusted_score': adjusted_score
                })

            df = pd.DataFrame(agent_results)
            df = df.sort_values(by='adjusted_score', ascending=True)
            return df
        else:
            print("No suitable agent found.")
            return None

folder_path = 'data/agents'  
embedding_manager = EmbeddingManager(folder_path)
embedding_manager.generate_and_store_embeddings()

query_text = "Explain quantum key distribution and the BB84 protocol."
agents_df = embedding_manager.query_embedding(query_text)

if agents_df is not None and not agents_df.empty:
    best_agent = agents_df.head(1)
    print(f"Best agent for query: '{query_text}'\n")
    print(best_agent[['filename', 'adjusted_score', 'similarity', 'distance']])
else:
    print("No suitable agent found.")
