import json
from src import formular_controller
from src import formular_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_delete_formular_item_ok(lambda_context, dynamodb_table):
    item = {
        'titel': "Test.pdf",
        'filename': "t.pdf",
        "beschreibung": "Eine Testdatei"
    }
    createdformular_item = formular_controller.create_formular_item(
        DEFAULT_TENANT_ID, item)

    formular_items = formular_controller.get_formular_items(DEFAULT_TENANT_ID)
    assert len(formular_items) == 1

    pathParameters = {
        "id": createdformular_item.id
    }
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'DELETE', None, pathParameters), lambda_context)
    
    assert response == lambda_response(204)
    formular_items = formular_controller.get_formular_items(DEFAULT_TENANT_ID)
    assert len(formular_items) == 0


def test_delete_formular_item_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": "abc123"
    }
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'DELETE', None, pathParameters), lambda_context)
   
    assert response == lambda_response(404)


def test_delete_formular_item_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": "abc123"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = formular_handler.handle(event(
        '/api/formular/{id}', 'DELETE', None, pathParameters, headers), lambda_context)
    
    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
