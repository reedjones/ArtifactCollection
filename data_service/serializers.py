__author__ = "reed@reedjones.me"

import inspect
from typing import Type, Any, Union

from django import forms
from django.db import models
from rest_framework import serializers

from data_service import services


class DataServiceSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    method_name = serializers.CharField()

    # Add fields for other method parameters as needed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method_name = self.initial_data.get('method_name', None)
        if method_name:
            fields = get_fields_for_method_name(self.initial_data['method_name'])
            for k,v in fields.items():
                self.fields[k] = v

    def method_param_fields(self):
        return get_fields_for_method_name(self.data.get('method_name', None))

    def validate(self, data):
        # Perform additional validation if needed
        return data


def get_fields_for_method_name(method_name: str,
                               serializer_type: bool = True,
                               form_type: bool = False,
                               model_type: bool = False) -> Union[dict, None]:
    """

    :param method_name:
    :param serializer_type: bool, return serializers.Field type
    :param form_type: bool, return forms.Field type
    :param model_type: bool, return models.Field type
    :return: Union[dict, None] dict is key:str: value:Type[(serializers|models|forms).Field]],
        (if none of [serializer_type, form_type, model_type] defaults to serializer_type
    """
    # Dynamically add fields based on the method signature
    if method_name is None or method_name.strip() == '':
        return
    fields = {
    }
    data_service_class = services.DataServiceImplementation
    method = getattr(data_service_class, method_name, None)
    if method and callable(method):
        method_params = inspect.signature(method).parameters
        for param_name, param_info in method_params.items():
            if param_name not in {'self', 'model_class'}:
                if serializer_type:
                    field_type = serializers.CharField  # Adjust based on your method parameter types
                elif form_type:
                    field_type = forms.CharField
                elif model_type:
                    field_type = models.CharField
                else:
                    flist = f"{[form_type,model_type,serializer_type]}"
                    raise Exception(
                        f"one of these must be true\nform_type|model_type|serializer_type|\n{flist}"
                    )
                fields[param_name] = field_type()
    return fields


def get_serial_for_model(model_class: Type[models.Model], field_set: Any = '__all__'):
    class DynamicQuerySetSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = field_set

    return DynamicQuerySetSerializer
