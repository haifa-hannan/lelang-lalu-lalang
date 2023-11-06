from typing import Type
from django.db import models

ModelType = Type[models.Model]


def insert_data(model_class: ModelType, data: dict):
    if model_class.objects.filter(**data).exists():
        raise ValueError("data already exists")
    try:
        obj, created = model_class.objects.get_or_create(**data)
        if not created:
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
    except(Exception)as e:
        raise ValueError(f"Error: {str(e)}") from e

def validate_payload_credentials(data, keys):
    creds = {}
    missing_fields = []

    for key in keys:
        if key in data:
            creds[key] = data[key]
        else:
            missing_fields.append(key)
    if missing_fields:
        return {"creds": None, "missing_fields": missing_fields}
    else:
        return{"creds":creds, "missing_fields":[]}

def result_covert_simple(data_master):
    data = {
        'data': data_master,
        'meta': {
            'pagination' : {
                'total' : 1,
                'count' : 1,
                'per_page' : 1,
                'current_page': 1,
                'total_pages': 1,
                'links': []
            }
        }
    }
    return data
    
def update_data(model: ModelType, lookup: str, lookup_value: str, data: dict):
    """
    dynamicaly update passed model data.
    input:
        model: ModelType, django orm class
        lookup: str, lookup field
        lookup_value: str, what to look in lookup
        data: dict, new data to be inputed
    """
    lookup_field = f"{lookup}__exact"
    query = {lookup_field : lookup_value, "endda__gt" : today}
    if not model.objects.filter(**query).exists():
        raise ValueError("data not found")

    try:
        new_data = model.objects.get(**query)
        for k,v in data.items():
            setattr(new_data, k, v)
        new_data.save()
    except Exception as e:
        raise ValueError(f"Error: {str(e)}") from e