__author__ = "reed@reedjones.me"

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProvenanceEvent, Collection


@receiver(post_save, sender=ProvenanceEvent)
def update_artifact_model_date(sender, instance, **kwargs):
    # Update the date of the associated ArtifactModel when a ProvenanceEvent is saved
    instance.artifact.save()


@receiver(post_save, sender=Collection)
def notify_collection_creation(sender, instance, **kwargs):
    if kwargs.get('created', False):
        print(f"New collection created: {instance.name}")
        # Implement your notification logic here


# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Artifact, Collection, Person, ProvenanceEvent


@receiver(post_save, sender=Artifact)
def create_artifact_events(sender, instance, created, **kwargs):
    # Trigger events for Artifact model
    if created:
        instance.create_initial_provenance_event()


@receiver(post_save, sender=Collection)
def create_collection_events(sender, instance, created, **kwargs):
    # Trigger events for Collection model
    if created:
        instance.create_initial_provenance_event()


@receiver(post_save, sender=Person)
def create_person_events(sender, instance, created, **kwargs):
    # Trigger events for Person model
    if created:
        instance.create_initial_provenance_event()


@receiver(post_save, sender=ProvenanceEvent)
def create_updated_provenance_event(sender, instance, created, **kwargs):
    # Trigger an updated event when a ProvenanceEvent is updated
    if not created:
        instance.update_provenance_event("Event updated")
