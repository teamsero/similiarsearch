from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import json

# Model to create embeddings
encoder = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

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
    collection_name="my_books2",
    vectors_config=models.VectorParams(
        # Vector size is defined by used model
        size=encoder.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE
    )
)

# Let's vectorize descriptions and upload to qdrant
client.upload_records(
    collection_name="my_books2",
    records=[
        models.Record(
            id=idx,
            # vector=encoder.encode(doc["title"] + " "+doc["desc"]).tolist(),
            vector=encoder.encode(doc["title"]).tolist(),
            payload=doc
        ) for idx, doc in enumerate(documents)
    ]
)

keyword = "mentor"
print("keyword: ", keyword)

hits = client.search(
    collection_name="my_books2",
    query_vector=encoder.encode(keyword).tolist(),
    limit=10,
    query_filter=models.Filter(
        should=[
            models.FieldCondition(
                key="star",
                range=models.Range(
                    gte=2
                )
            )
        ],
        must=[
            models.FieldCondition(
                key="reputation_level",
                match=models.Match(
                    any=["mentor"]
                )
            )
        ]
    ),
)
for hit in hits:
    print(hit.payload, "score:", hit.score)
