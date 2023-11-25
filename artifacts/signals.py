__author__ = "reed@reedjones.me"

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProvenanceEvent, Collection, Artifact

@receiver(post_save, sender=ProvenanceEvent)
def update_artifact_model_date(sender, instance, **kwargs):
    # Update the date of the associated ArtifactModel when a ProvenanceEvent is saved
    instance.artifact.save()


@receiver(post_save, sender=Collection)
def notify_collection_creation(sender, instance, **kwargs):
    if kwargs.get('created', False):
        print(f"New collection created: {instance.name}")
        # Implement your notification logic here
