from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F, QuerySet, Subquery, Count

from django.db.models import OuterRef


class EventActorMixin:
    @property
    def event_model(self):
        raise NotImplemented

    @property
    def pk(self):
        raise NotImplemented

    def fire_event(self):
        c = ContentType.objects.get_for_model(self)
        return self.event_model(object_id=self.pk, content_type=c)


from django.utils.functional import cached_property


# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=255)
    short = models.CharField(max_length=4, unique=True)
    description = models.TextField(default="no description")

    # location = models.ForeignKey(Location, on_delete=models.CASCADE)

    @cached_property
    def flag_url(self):
        return f"/static/flags/Flag_of_{self.name}.svg"


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


class Geography(models.Model):
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, default=None)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, default=None)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, default=None)


class Physical(models.Model):
    """


    """

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
    """
       Manager for `Artifact` model
        """

    def get_by_category(self, category):
        """
        artifacts_by_category = ArtifactModel.objects.get_by_category('Projectile Point')

        :param category:
        :return:
        """
        return self.filter(artifact_category__category=category)

    def with_photos(self):
        return self.prefetch_related('photos').annotate(
            photo_url=Subquery(
                Photo.objects.get_for_artifact().values('filename')[0]
            )
        )

    def with_related(self, *args):
        return self.select_related(*args)

    def with_photos_and_categories(self):
        main_photo_subquery = Photo.objects.filter(
            artifact=OuterRef('pk')
        ).order_by('pk').values('filename')[:1]
        qs = self.with_related('category', 'geography').prefetch_related('photos').annotate(
            photo_url=Subquery(main_photo_subquery),
            photo_count=Count('photos'),
            subcategory=F('category__parent__name'),
            maincategory=F('category__name'),
            category_attribute=F('category__attribute__name'),
            from_state=F('geography__state__name')
        )
        return qs

    def with_categories(self, use_values=False, initial_qs: QuerySet = None):
        if initial_qs:
            qs = initial_qs.annotate(
                subcategory=F('category__parent__name'),
                maincategory=F('category__name'),
                category_attribute=F('category__attribute__name'))
        else:
            qs = self.with_related('category') \
                .annotate(
                subcategory=F('category__parent__name'),
                maincategory=F('category__name'),
                category_attribute=F('category__attribute__name')
            )
        if not use_values:
            return qs
        return qs.values('aw_item_number', 'category_attribute', 'maincategory', 'subcategory')

    def with_materials(self):
        return self.prefetch_related('materials')


class Artifact(Physical):
    """
        Represents information about artifacts.

        Attributes:
            name (str): The name of the artifact.
            ... (add descriptions for other fields)
        """
    name = models.CharField(max_length=255, db_index=True)
    provenance_details = models.TextField(default="na")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, default=None, null=True)
    finder = models.ForeignKey('Person', on_delete=models.SET_NULL, default=None, null=True)
    aw_item_number = models.IntegerField(default=None, null=True)
    geography = models.ForeignKey(Geography, on_delete=models.SET_NULL, null=True, default=None)
    objects = ArtifactModelManager()

    @property
    def category_hierarchy(self):
        return f"{self.category} > {self.category.parent} > {self.category.attribute}"

    def get_provenance_events(self):
        return ProvenanceEvent.objects.filter(artifact=self).order_by('date')

    def get_owner(self):
        ownership = ArtifactOwnership.objects.filter(artifact=self).first()
        return ownership.collection.owner if ownership else None

    def get_event_for(self):
        c = ContentType.objects.get_for_model(self)
        e = ProvenanceEvent(content_type=c, object_id=self.pk)
        return e

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"unnamed artifact"
        super(Artifact, self).save(*args, **kwargs)


class PhotoManger(models.Manager):
    def get_for_artifact(self):
        return self.filter(
            artifact_id=OuterRef('id')
        )


class Photo(models.Model):
    objects = PhotoManger()

    class PhotoType(models.TextChoices):
        artifact = "artifact"
        document = "document"
        other = "other"

    artifact = models.ForeignKey(Artifact,
                                 on_delete=models.SET_NULL, null=True, default=None, related_name='photos')
    file = models.FileField(null=True, default=None)
    filename = models.CharField(max_length=255)
    title = models.TextField(default="no caption")
    photo_type = models.CharField(max_length=30, default=PhotoType.other, choices=PhotoType.choices)




class MaterialTag(models.Model):
    name = models.CharField(max_length=255, db_index=True)


class Attribute(models.Model):
    name = models.CharField(max_length=30, default="na")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey('self', related_name='sub_categories', on_delete=models.SET_NULL, null=True,
                               default=None)
    attribute = models.ForeignKey(
        Attribute, null=True,
        blank=True, on_delete=models.SET_NULL)

    primary = models.BooleanField(
        default=True)
    __current_parent = None

    # def __init__(self, *args, **kwargs):
    #     self.__current_parent = self.parent
    #     super(Category, self).__init__(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     changed = self.__current_parent != self.parent
    #     if self._state.adding or changed:
    #         if self.parent is not None:
    #             self.primary = False
    #     super(Category, self).save(*args, **kwargs)

    def get_related_artifacts(self):
        return Artifact.objects.filter(category=self)

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


class ProvenanceEventManager(models.Manager):
    def with_dates(self):
        return self.exclude(date=None)

    def without_dates(self):
        return self.filter(date=None)


class ProvenanceEvent(models.Model):
    artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=255, db_index=True)  # E.g., Found, Acquired, Sold
    description = models.TextField()
    date = models.DateField(db_index=False, null=True, default=None)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)  # Use AutoField for insertion order
    level = models.IntegerField(default=1)
    objects = ProvenanceEventManager()

    @classmethod
    def trigger(cls, actor, event_type: str, artifact: Artifact, **kwargs):
        c = ContentType.objects.get_for_model(actor)
        i = actor.pk
        return cls(object_id=i, content_type=c, event_type=event_type, artifact=artifact, **kwargs)

    class Meta:
        ordering = ['created_at']
        # order_with_respect_to = ['artifact']
        indexes = [
            models.Index(fields=['artifact', 'event_type', 'date']),
        ]

    def save(self, *args, **kwargs):
        if self._state.adding:
            f = self.artifact.provenanceevent_set.count() + 1
            self.level = f
        super(ProvenanceEvent, self).save(*args, **kwargs)


class Trade(models.Model):
    artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE)
    from_collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='from_trades')
    to_collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='to_trades')
    date = models.DateField(default=None, null=True)


class PersonManager(models.Manager):
    pass


class Person(models.Model, EventActorMixin):
    name = models.CharField(max_length=255, db_index=True, unique=True)

    event_model = ProvenanceEvent

    def __str__(self):
        return self.name

    def collections(self):
        return Collection.objects.filter(owner=self)

    def certifications(self):
        return COA.objects.filter(signer=self)

    def events(self):
        return ProvenanceEvent.objects.filter(content_object=self)

    def create_collection_for(self):
        c = Collection(owner=self)
        return c


class Date(models.Model):
    date = models.DateField(db_index=True)

    def __str__(self):
        if not self.date:
            return "not specified"
        return str(self.date)


class COA(models.Model):
    signer = models.ForeignKey('Person', on_delete=models.SET_NULL, default=None, null=True)
    details = models.TextField(default="na")
    artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE)


