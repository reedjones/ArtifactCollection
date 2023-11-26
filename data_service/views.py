__author__ = "reed@reedjones.me"

from django.apps import apps
from rest_framework.permissions import AllowAny
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import DataServiceImplementation  # Import your DataService implementation
from .serializers import DataServiceSerializer, get_fields_for_method_name

class DataServiceAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Get a list of available models and methods
        available_models = self.get_available_models()
        available_methods = self.get_available_methods()

        # Construct the response payload
        payload = {
            "available_models": available_models,
            "available_methods": available_methods,
        }

        return Response(payload, status=status.HTTP_200_OK)


    def get_available_models(self):
        # Dynamically retrieve available models
        models = apps.get_models()
        return [model.__name__ for model in models]

    def get_available_methods(self):
        # Dynamically retrieve available methods from DataServiceImplementation
        methods = dir(DataServiceImplementation)
        method_names = [method for method in methods if
                callable(getattr(DataServiceImplementation, method)) and not method.startswith("__")
                ]
        return [{method_name : self.get_params_for_method(method_name)} for method_name in method_names]

    def get_params_for_method(self, method_name):
        return get_fields_for_method_name(method_name=method_name)


    def post(self, request, *args, **kwargs):
        print(f"Got post with {request.data}")
        serializer = DataServiceSerializer(data=request.data)
        if serializer.is_valid():
            model_name = serializer.validated_data['model_name']
            method_name = serializer.validated_data['method_name']  # Add this field to your serializer
            print(f"Got model {model_name} amnd method {method_name}")
            data_service = DataServiceImplementation(app_name="artifacts", model_name=model_name)

            # get params
            print(f"Got validated data: {serializer.validated_data}")
            method_params = {k: v for k, v in serializer.validated_data.items() if k not in {'model_name', 'method_name'}}

            # Call the appropriate method based on the frontend request
            # Example: data_service.calculation(what, value, aggregation)
            # Adjust this part based on your frontend requirements
            print(f"Got method params : {method_params}")
            data = getattr(data_service, method_name)(
                # Add other method parameters here based on the serializer fields
                **method_params
            )
            serialized_data = data_service.serialize(data)
            return Response({"result": "success", "data": serialized_data}, status=status.HTTP_200_OK)

        else:
            return Response({"result": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
