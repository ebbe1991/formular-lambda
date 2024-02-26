from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
import src.formular_controller as formular_controller
from src.formular_controller import FormularDTO
from lambda_utils.response_utils import response, empty_response, to_json_array
from lambda_utils.event_utils import extract_body, extract_tenant
from lambda_utils.exception import ValidationException
import urllib.parse
app = APIGatewayHttpResolver()


def handle(event: dict, context: dict):
    return app.resolve(event, context)


@app.post('/api/formular')
def post():
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    formular_item = formular_controller.create_formular_item(tenant_id, body)
    return response(201, formular_item.to_json())


@app.put('/api/formular/<id>')
def put(id):
    id = urllib.parse.quote(id)
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    formular_item = formular_controller.update_formular_item(tenant_id, id, body)
    return response(200, formular_item.to_json())


@app.get('/api/formularview/<id>')
def getView(id):
    return get(id)


@app.get('/api/formular/<id>')
def get(id):
    id = urllib.parse.quote(id)
    event = app.current_event
    tenant_id = extract_tenant(event)
    formular_item = formular_controller.get_formular_item(tenant_id, id)
    if formular_item:
        return response(200, formular_item.to_json())
    else:
        return empty_response(404)


@app.get('/api/formularview')
def getAllView():
    return getAll()


@app.get('/api/formular')
def getAll():
    event = app.current_event
    tenant_id = extract_tenant(event)
    formular_items = formular_controller.get_formular_items(tenant_id)
    body = to_json_array(list(map(FormularDTO.to_json, formular_items)))
    return response(200, body)


@app.delete('/api/formular/<id>')
def delete(id):
    id = urllib.parse.quote(id)
    event = app.current_event
    tenant_id = extract_tenant(event)
    deleted = formular_controller.delete_formular_item(tenant_id, id)
    if deleted:
        return empty_response(204)
    else:
        return empty_response(404)


@app.exception_handler(ValidationException)
def handle_http_exception(exception: ValidationException):
    return response(exception.http_status, exception.to_json())


@app.get('/api/formular/<id>/put-doc')
def request_put_doc(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    response = formular_controller.request_put_doc(tenant_id, id)
    return {
        'statusCode': 201,
        'body': response
    }

@app.get('/api/formular/<id>/get-doc')
def request_get_doc(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    response = formular_controller.request_get_doc(tenant_id, id)
    return {
        'statusCode': 201,
        'body': response
    }
