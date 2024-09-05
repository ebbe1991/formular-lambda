import json
from datetime import date
from src import formular_handler
from src import formular_controller
from formular_dto import FormularDTO
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_update_formular_item_ok(lambda_context, dynamodb_table):
    item = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    createdformular_item = formular_controller.create_formular_item(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdformular_item.id
    }
    itemUpdate = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei (aktualisiert)"
    }
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, FormularDTO(
        "Test.pdf", "Fuhrpark", "t.pdf", "Eine Testdatei (aktualisiert)", createdformular_item.id).to_json())


def test_update_formular_item_required_field_to_null_not_ok(lambda_context, dynamodb_table):
    item = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    createdformular_item = formular_controller.create_formular_item(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdformular_item.id
    }
    itemUpdate = {
        'filename': "t.pdf",
        'kategorie': "Fuhrpark",
        "beschreibung": "Eine Testdatei"
    }
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'titel' not present."}))


def test_update_formular_item_with_unknown_id_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": 'unknown'
    }
    itemUpdate = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "unknown id 'unknown' (tenant='mytenant1')."}))


def test_update_formular_item_set_null_value(lambda_context, dynamodb_table):
    item = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    createdformular_item = formular_controller.create_formular_item(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdformular_item.id
    }

    itemUpdate = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
    }
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, FormularDTO(
        "Test.pdf", "Fuhrpark", "t.pdf", None, createdformular_item.id).to_json())


def test_update_formular_item_without_body_not_ok(lambda_context, dynamodb_table):
    item = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    createdformular_item = formular_controller.create_formular_item(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdformular_item.id
    }

    response = formular_handler.handle(
        event('/api/formular/{id}', 'PUT', None, pathParameters), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))


def test_update_formular_item_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    createdformular_item = formular_controller.create_formular_item(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdformular_item.id
    }
    itemUpdate = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei (aktualisiert)"
    }
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'PUT', json.dumps(itemUpdate), pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
