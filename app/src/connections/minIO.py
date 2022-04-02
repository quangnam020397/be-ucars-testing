
from ..configs.configs import MINIO_ACCESS_KEY, MINIO_BUCKET, MINIO_SECRET_KEY, MINIO_URL

from minio import Minio

print(MINIO_URL)
minIO_client = Minio(
    endpoint=MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=True,
)

bucket_name = MINIO_BUCKET
