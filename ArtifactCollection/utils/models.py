__author__ = "reed@reedjones.me"


def get_or_create_generic(model_class, defaults=None, **kwargs):
    """
    Get a model instance based on the given lookup parameters.
    If the instance does not exist, create a new one with the provided defaults.

    Parameters:
    - model_class: The model class for which to perform the operation.
    - defaults: A dictionary of default values to use when creating a new instance.
    - kwargs: Lookup parameters to find an existing instance.

    Returns:
    - A tuple containing the model instance and a boolean indicating whether it was created.
    """
    instance, created = model_class.objects.get_or_create(defaults=defaults, **kwargs)
    return instance, created