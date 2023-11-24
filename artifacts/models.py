from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=255)
    short = models.CharField(max_length=4, unique=True)
    description = models.TextField(default="no description")
    # location = models.ForeignKey(Location, on_delete=models.CASCADE)


class County(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100, default="na")
    description = models.TextField(default="no description")

    class Meta:
        ordering = ('state__name', 'name')


class Region(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=None, null=True, db_index=True)
    name = models.CharField(max_length=100, default="na")
    description = models.TextField(default="no description")

    class Meta:
        ordering = ('state__name', 'name')


from django.db import models


class Physical(models.Model):
    class ConditionType(models.TextChoices):
        excellent = "excellent"
        good = "good"
        ok = "ok"
        damaged = "damaged"

    condition = models.CharField(max_length=12, default=ConditionType.ok, choices=ConditionType.choices)
    characteristics = models.TextField(default="not specified")
    attributes = models.CharField(max_length=100, default="none")
    materials = models.ManyToManyField('MaterialTag')


    class Meta:
        abstract = True


class ArtifactModelManager(models.Manager):
    def get_by_category(self, category):
        """
        artifacts_by_category = ArtifactModel.objects.get_by_category('Projectile Point')

        :param category:
        :return:
        """
        return self.filter(artifact_category__category=category)
class Artifact(Physical):
    name = models.CharField(max_length=255, db_index=True)
    provenance_details = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    finder = models.ForeignKey('Person', on_delete=models.SET_NULL, default=None, null=True)

    objects = ArtifactModelManager()
    @property
    def category_hierarchy(self):
        return f"{self.category.parent} > {self.artifact_category.sub_category} > {self.artifact_category.attribute}"

    def get_provenance_events(self):
        return ProvenanceEvent.objects.filter(artifact=self).order_by('date')

    def get_owner(self):
        ownership = ArtifactOwnership.objects.filter(artifact=self).first()
        return ownership.collection.owner if ownership else None




class MaterialTag(models.Model):
    name = models.CharField(max_length=255, db_index=True)


class Attribute(models.Model):
    name = models.CharField(max_length=30, default="na")

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey('self', related_name='sub_categories', on_delete=models.SET_NULL, null=True, default=None)
    attribute = models.ForeignKey(
        Attribute, null=True,
        blank=True, on_delete=models.SET_NULL)

    primary = models.BooleanField(
        default=True)
    __current_parent = None
    def __init__(self, *args, **kwargs):
        self.__current_parent = self.parent
        super(Category, self).__init__(*args, **kwargs)
    def save(self,*args, **kwargs):
        changed = self.__current_parent != self.parent
        if self._state.adding or changed:
            if self.parent is not None:
                self.primary = False
        super(Category, self).save(*args, **kwargs)

    def get_related_artifacts(self):
        return Artifact.objects.filter(artifact_category=self)

    def __str__(self):
        return self.name




class Period(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    date_range = models.CharField(max_length=255, db_index=True)



class CollectionManager(models.Manager):
    def get_owned_by_person(self, person):
        return self.filter(owner=person)


class Collection(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    owner = models.ForeignKey('Person', on_delete=models.CASCADE)

    objects = CollectionManager()
    def get_artifacts(self):
        return Artifact.objects.filter(artifactownership__collection=self)

    def get_trades(self):
        return Trade.objects.filter(Q(from_collection=self) | Q(to_collection=self)).order_by('date')





class ArtifactOwnership(models.Model):
    artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    owner = models.ForeignKey('Person', on_delete=models.SET_NULL, default=None, null=True)
    certification = models.ForeignKey('COA', on_delete=models.CASCADE)
    date_range = models.CharField(max_length=255, default="not specifed")
    acquisition_date = models.ForeignKey('Date', on_delete=models.SET_NULL, default=None, null=True)



from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.contenttypes.models import ContentType

class ProvenanceEventManager(models.Manager):
    def with_dates(self):
        return self.exclude(date=None)

    def without_dates(self):
        return self.filter(date=None)
class ProvenanceEvent(models.Model):
    artifact = models.ForeignKey('ArtifactModel', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=255, db_index=True)  # E.g., Found, Acquired, Sold
    description = models.TextField()
    date = models.DateField(db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)  # Use AutoField for insertion order

    objects = ProvenanceEventManager()
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['artifact', 'event_type', 'date']),
        ]

@receiver(post_save, sender=ProvenanceEvent)
def update_artifact_model_date(sender, instance, **kwargs):
    # Update the date of the associated ArtifactModel when a ProvenanceEvent is saved
    instance.artifact.save()
@receiver(post_save, sender=Collection)
def notify_collection_creation(sender, instance, **kwargs):
    if kwargs.get('created', False):
        print(f"New collection created: {instance.name}")
        # Implement your notification logic here


class Trade(models.Model):
    artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE)
    from_collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='from_trades')
    to_collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='to_trades')
    date = models.DateField(default=None, null=True)
class Person(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def get_owned_collections(self):
        return Collection.objects.filter(owner=self)

    def get_certifications(self):
        return COA.objects.filter(signer=self)
    def get_found_artifacts(self):
        return Artifact.objects.filter(provenanceevent__event_type='Found', provenanceevent__artifact=self)
class Date(models.Model):
    date = models.DateField(db_index=True)
    def __str__(self):
        if not self.date:
            return "not specified"
        return str(self.date)

class COA(models.Model):
    signer = models.ForeignKey('Person', on_delete=models.SET_NULL,default=None, null=True)
    details = models.TextField(default="na")
    artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE)


class Photo(models.Model):
    class PhotoType(models.TextChoices):
        artifact = "artifact"
        document = "document"
        other = "other"
    artifact = models.ForeignKey(Artifact, on_delete=models.SET_NULL, null=True, default=None)
    file = models.FileField()
    filename = models.CharField(max_length=255)
    title = models.TextField(default="no caption")
    photo_type = models.CharField(max_length=30, default=PhotoType.other, choices=PhotoType.choices)