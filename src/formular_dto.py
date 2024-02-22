import json, uuid
import urllib.parse
import re

from lambda_utils.validation import check_required_field


def create(item: dict):
    titel = item.get('titel')
    check_required_field(titel, 'titel')
    filename = item.get('filename')
    check_required_field(filename, 'filename')
    beschreibung = item.get('beschreibung')
    return FormularDTO(
        titel,
        filename,
        beschreibung,
        item.get('id')
    )


class FormularDTO:

    def __init__(self, titel: str, filename: str, beschreibung: str, id: str = None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.titel = titel
        self.filename = filename
        self.beschreibung = beschreibung

    def to_json(self):
        return json.dumps(self.__dict__)