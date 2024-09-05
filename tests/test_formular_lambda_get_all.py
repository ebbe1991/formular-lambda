import json
from src import formular_controller
from src import formular_handler
from tests.helper import event, extract_body, extract_status_code, lambda_response, DEFAULT_TENANT_ID


def test_get_formular_items_ok(lambda_context, dynamodb_table):
    item1 = {
        'titel': "Test.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    item2 = {
        'titel': "Test2.pdf",
        'kategorie': "Fuhrpark",
        'filename': "t2.pdf",
        "beschreibung": "Eine Testdatei"
    }
    formular_controller.create_formular_item(DEFAULT_TENANT_ID, item1)
    formular_controller.create_formular_item(DEFAULT_TENANT_ID, item2)

    response = formular_handler.handle(
        event('/api/formular', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 2


def test_get_formular_items_empty_ok(lambda_context, dynamodb_table):
    response = formular_handler.handle(
        event('/api/formular', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 0


def test_get_formular_items_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    response = formular_handler.handle(
        event('/api/formular', 'GET', None, None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))