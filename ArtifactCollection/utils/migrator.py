import sqlite3

from django.db import models


from django.apps import apps
from django.core.serializers import serialize
import json

def generate_field_name_fixture(output_file_path='field_names_fixture.json'):
    """
    Generate a fixture containing field names for all models in the old project.

    Parameters:
    - output_file_path: The path to save the generated fixture.

    Returns:
    - None
    """
    app_models = apps.get_models()

    field_names = {}
    for model in app_models:
        model_name = f"{model._meta.app_label}.{model.__name__}"
        field_names[model_name] = [field.name for field in model._meta.get_fields()]

    with open(output_file_path, 'w') as output_file:
        json.dump(field_names, output_file, indent=2)

    print(f"Field names fixture saved to {output_file_path}")

# Example usage
if __name__ == "__main__":
    generate_field_name_fixture('field_names_fixture.json')


def fetch_old_data_from_database(table_name, database_file):
    """
    Fetch data from a local SQLite database.

    Parameters:
    - table_name: The name of the table from which to fetch data.
    - database_file: The path to the SQLite database file.

    Returns:
    - A list of dictionaries representing rows from the specified table.
    """
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Fetch data from the specified table
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Close the connection
    connection.close()

    return data


class DataMigrator:
    def __init__(self, old_database_name='old_database'):
        self.old_database_name = old_database_name

    def load_model_table(self, model_class, etl_function):
        """
        Load data for the entire model from the old database using the provided ETL function.

        Parameters:
        - model_class: The Django model class for which to load data.
        - etl_function: A function that performs ETL on old database data.

        Returns:
        - A list of instances of the model with data loaded from the old database.
        """
        old_data = self._get_old_data(model_class)
        instances = [self._map_data_to_instance(model_class, entry, etl_function) for entry in old_data]
        return instances

    def load_model_column(self, model_class, column_name, etl_function):
        """
        Load data for a specific column of a model from the old database using the provided ETL function.

        Parameters:
        - model_class: The Django model class for which to load data.
        - column_name: The name of the column/field to load.
        - etl_function: A function that performs ETL on old database data.

        Returns:
        - A list of tuples containing the primary key and the ETL-transformed value for the specified column.
        """
        old_data = self._get_old_data(model_class)
        transformed_values = [(entry['id'], etl_function(entry[column_name])) for entry in old_data]
        return transformed_values

    def _get_old_data(self, model_class):
        """
        Get data for a model from the old database.

        Parameters:
        - model_class: The Django model class for which to get data.

        Returns:
        - A list of dictionaries representing rows from the old database.
        """
        # Assuming you have a function to connect to the old database and fetch data.
        # You can replace this with your own implementation.
        old_data = fetch_old_data_from_database(model_class._meta.db_table, self.old_database_name)
        return old_data

    def _map_data_to_instance(self, model_class, data, etl_function):
        """
        Map old database data to a new model instance using the provided ETL function.

        Parameters:
        - model_class: The Django model class for which to create an instance.
        - data: A dictionary representing a row from the old database.
        - etl_function: A function that performs ETL on old database data.

        Returns:
        - An instance of the model with data transformed using the ETL function.
        """
        transformed_data = etl_function(model_class, data)
        return model_class(**transformed_data)


# Example ETL function
def example_load(model_class, data):
    """
    Example ETL function for transforming data before loading.

    Parameters:
    - model_class: The Django model class.
    - data: A dictionary representing a row from the old database.

    Returns:
    - A dictionary with transformed data.
    """
    transformed_data = {
        'id': data['id'],
        'username': data['username'].upper(),  # Example transformation: Convert username to uppercase
        'email': data['email'],
        # Apply other transformations as needed
    }
    return transformed_data

# Example usage
def main():
    migrator = DataMigrator()

    # Dynamically call load_model_table with example_load function and any model class
    instances = migrator.load_model_table(UserModel, example_load)

    # Print the loaded instances
    for instance in instances:
        print(instance)

if __name__ == "__main__":
    main()