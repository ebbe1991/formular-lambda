from src.formular_dto import FormularDTO, create
from lambda_utils.exception import UnknownIdException
from datetime import date
import dynamo_db_service
import os
import json
import boto3
from lambda_utils.exception import ValidationException

s3_bucket_name = os.getenv('FORMULAR_S3_BUCKET')
s3 = boto3.client('s3')


def create_formular_item(tenant_id: str, dto: dict) -> FormularDTO:
    formular_item = create(dto)
    dynamo_db_service.put_formular_item(tenant_id, formular_item)
    return formular_item


def update_formular_item(tenant_id: str, id: str, dto: dict) -> FormularDTO:
    dto.update({'id': id})
    formular_item = create(dto)
    to_update = get_formular_item(tenant_id, id)
    if to_update:
        dynamo_db_service.put_formular_item(tenant_id, formular_item)
        return formular_item
    else:
        raise UnknownIdException(id, tenant_id)


def get_formular_item(tenant_id: str, id: str) -> FormularDTO:
    item = dynamo_db_service.get_formular_item(tenant_id, id)
    if item:
        formular_item = create(item)
        return formular_item
    else:
        return None


def get_formular_items(tenant_id: str) -> list[FormularDTO]:
    formular_items = []
    items = dynamo_db_service.get_formular_items(tenant_id)
    for item in items:
        formular_item = create(item)
        formular_items.append(formular_item)

    return formular_items


def delete_formular_item(tenant_id: str, id: str) -> bool:
    formular_item = get_formular_item(tenant_id, id)
    if formular_item:
        try:
            delete_doc(tenant_id, id)
        except Exception:
            print("error: delete doc")
        dynamo_db_service.delete_formular_item(tenant_id, id)
        return True
    else:
        return False


def request_put_doc(tenant_id, id) -> str:
    doc_key = get_doc_key(tenant_id, id)

    url = s3.generate_presigned_url('put_object', Params={
                                    'Bucket': s3_bucket_name, 'Key': doc_key}, ExpiresIn=3600)
    return json.dumps(url)


def request_get_doc(tenant_id, id) -> str:
    doc_key = get_doc_key(tenant_id, id)

    url = s3.generate_presigned_url('get_object', Params={
                                    'Bucket': s3_bucket_name, 'Key': doc_key}, ExpiresIn=3600)
    return json.dumps(url)


def put_doc(tenant_id, id, filename: str, body):
    doc_key = get_doc_key(tenant_id, filename, id)

    s3.put_object(Body=body, Bucket=s3_bucket_name, Key=doc_key)
    item = get_formular_item(tenant_id=tenant_id, id=id)
    update_formular_item(tenant_id=tenant_id,
                     id=id,
                     dto=json.loads(item.to_json()))


def delete_doc(tenant_id, id, filename: str):
    doc_key = get_doc_key(tenant_id, id)
    s3.delete_object(Bucket=s3_bucket_name, Key=doc_key)
    item = get_formular_item(tenant_id=tenant_id, id=id)
    update_formular_item(tenant_id=tenant_id,
                     id=id,
                     dto=json.loads(item.to_json()))


def get_doc_key(tenant_id: str, id: str, filename: str) -> str:
    return f'formular/{tenant_id}/{id}/{filename}'
