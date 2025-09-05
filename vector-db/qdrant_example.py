import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_COLLECTION = os.getenv('QDRANT_COLLECTION')

client = QdrantClient(url=QDRANT_URL)


if not client.collection_exists(QDRANT_COLLECTION):
    print(f"Creating collection...")
    response = client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=4, distance=Distance.DOT),
    )

    print(f"The collection is created: {response}")
else:
    print(f"The collection: '{QDRANT_COLLECTION}' exists.")
