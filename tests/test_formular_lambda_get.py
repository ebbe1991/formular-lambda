import json
from src import formular_controller
from src import formular_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_get_formular_item_not_found(lambda_context, dynamodb_table):
    pathParameters = {
        "id": "unknown_id"
    }
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(404)


def test_get_formular_item_ok(lambda_context, dynamodb_table):
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
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(200, createdformular_item.to_json())


def test_get_formular_item_with_introtext_ok(lambda_context, dynamodb_table):
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
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(200, createdformular_item.to_json())

def test_get_formular_item_without_tenant_id_not_ok(lambda_context, dynamodb_table):
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
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'GET', None, pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
