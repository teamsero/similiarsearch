from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import json

encoder = SentenceTransformer('all-MiniLM-L6-v2') # Model to create embeddings

client = QdrantClient("localhost", port=6333)
# Let's make a semantic search for Sci-Fi books! 


# Open the JSON file
with open('seek.json') as file:
    # Load the JSON data
     # Read the file contents
    file_contents = file.read()

    # Convert the file contents to JSON
    documents = json.loads(file_contents)


# Create collection to store books
client.recreate_collection(
    collection_name="my_books",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(), # Vector size is defined by used model
        distance=models.Distance.COSINE
    )
)

# Let's vectorize descriptions and upload to qdrant
client.upload_records(
    collection_name="my_books",
    records=[
        models.Record(
            id=idx,
            vector=encoder.encode(doc["title"] + " "+doc["desc"]).tolist(),
            payload=doc
        ) for idx, doc in enumerate(documents)
    ]
)
keyword =  "chăm sóc" 
print("keyword: ",keyword)

hits = client.search(
    collection_name="my_books",
    query_vector=encoder.encode(keyword).tolist(),
    limit=10,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="exp",
                range=models.Range(
                    gte=10
                )
            ),
            models.FieldCondition(
                key="star",
                range=models.Range(
                    gte=3
                )
            )
        ]
    ),
)
for hit in hits:
  print(hit.payload, "score:", hit.score)

