import os
import boto3
from formular_dto import FormularDTO
from boto3.dynamodb.conditions import Key


def get_formular_items_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv('FORMULAR_TABLE_NAME')
    return dynamodb.Table(table_name)


def put_formular_item(tenant_id: str, formular_item: FormularDTO):
    table = get_formular_items_table()
    table.put_item(
        Item={
            'tenant-id': tenant_id,
            'id': formular_item.id,
            'kategorie': formular_item.kategorie,
            'titel': formular_item.titel,
            'filename': formular_item.filename,
            'beschreibung': formular_item.beschreibung
        }
    )


def get_formular_item(tenant_id: str, id: str):
    table = get_formular_items_table()
    result = table.get_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )
    return result.get('Item')


def get_formular_items(tenant_id: str) -> list:
    table = get_formular_items_table()
    items = []
    response = table.query(
        KeyConditionExpression=Key('tenant-id').eq(tenant_id),
        ScanIndexForward=False
    )
    items.extend(response['Items'])

    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=Key('tenant-id').eq(tenant_id),
            ScanIndexForward=False,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response['Items'])


    return items


def delete_formular_item(tenant_id: str, id: str):
    table = get_formular_items_table()
    table.delete_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )
