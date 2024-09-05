import json
from datetime import date
from src import formular_handler
from formular_dto import FormularDTO
from tests.helper import event, lambda_response, extract_id


def test_create_formular_item_ok(lambda_context, dynamodb_table):
    item = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    response = formular_handler.handle(
        event('/api/formular', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, FormularDTO(
        "Test.pdf", "Fuhrpark", "t.pdf", "Eine Testdatei", id).to_json())


def test_create_formular_item_missing_field_titel_bad_request(lambda_context, dynamodb_table):
    item = {
        'filename': "t.pdf",
        'kategorie': "Fuhrpark",
        "beschreibung": "Eine Testdatei"
    }
    response = formular_handler.handle(
        event('/api/formular', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'titel' not present."}))

def test_create_formular_item_missing_field_filename_bad_request(lambda_context, dynamodb_table):
    item = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        "beschreibung": "Eine Testdatei"
    }
    response = formular_handler.handle(
        event('/api/formular', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'filename' not present."}))



def test_create_formular_item_without_optional_parameters_ok(lambda_context, dynamodb_table):
    item = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf"
    }
    response = formular_handler.handle(
        event('/api/formular', 'POST', json.dumps(item)), lambda_context)
    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, FormularDTO(
        "Test.pdf", "Fuhrpark", "t.pdf", None, id).to_json())



def test_create_formular_item_without_body_not_ok(lambda_context, dynamodb_table):
    response = formular_handler.handle(
        event('/api/formular', 'POST'), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))

def test_create_formular_item_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    response = formular_handler.handle(
        event('/api/formular', 'POST', json.dumps(item), None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))