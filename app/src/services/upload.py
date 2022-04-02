

from datetime import datetime, timedelta
from io import BytesIO
from fastapi import File, UploadFile
from pydantic import BaseModel
import random

from ..connections.minIO import minIO_client, bucket_name


class UploadFileResponse(BaseModel):
    bucket_name: str
    file_name: str
    url: str


async def uploadFile(file: UploadFile = File(...)):
    try:
        data = file.file.read()

        file_name = " ".join(file.filename.strip().split())

        data_file = put_object(
            file_name=file_name,
            file_data=BytesIO(data),
            content_type=file.content_type
        )
        return data_file
    except print(0):
        return None


def put_object(file_data, file_name, content_type):
    try:
        datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        object_name = f"{datetime_prefix}___{file_name}"
        while check_file_name_exists(bucket_name=bucket_name, file_name=object_name):
            random_prefix = random.randint(1, 1000)
            object_name = f"{datetime_prefix}___{random_prefix}___{file_name}"

        minIO_client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=file_data,
            content_type=content_type,
            length=-1,
            part_size=10 * 1024 * 1024
        )
        url = presigned_get_object(
            bucket_name=bucket_name, object_name=object_name)
        data_file = {
            'bucket_name': bucket_name,
            'file_name': object_name,
            'url': url
        }
        return data_file
    except Exception as e:
        raise Exception(e)


def presigned_get_object(bucket_name, object_name):
    # Request URL expired after 7 days
    url = minIO_client.presigned_get_object(
        bucket_name=bucket_name,
        object_name=object_name,
        # expires=timedelta(days=7)
    )
    return url


def check_file_name_exists(bucket_name, file_name):
    try:
        minIO_client.stat_object(
            bucket_name=bucket_name, object_name=file_name)
        return True
    except Exception as e:
        print(f'[x] Exception: {e}')
        return False
