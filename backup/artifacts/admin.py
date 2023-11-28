from django.contrib import admin
from django import forms

# Register your models here.
from .models import Artifact, MaterialTag, Physical, Category, Period, Collection, ArtifactOwnership, Trade, Person, Date, COA, Photo
from django.contrib.admin import AdminSite

#
#
class CustomAdminSite(AdminSite):
    site_header = 'Artifact Tracking Admin'
    site_title = 'Artifact Tracking Admin'

admin_site = CustomAdminSite(name='custom_admin')

#
# admin.site.register(MaterialTag)
# # admin.site.register(Physical)
# admin.site.register(Category)
# # admin.site.register(Location)
# admin.site.register(Period)
# admin.site.register(Collection)
# admin.site.register(ArtifactOwnership)
# admin.site.register(Trade)
# admin.site.register(Person)
# admin.site.register(Date)
# admin.site.register(COA)
# admin.site.register(Photo)
#
#
#
#
# class ArtifactAdminForm(forms.ModelForm):
#     class Meta:
#         model = Artifact
#         fields = '__all__'
#
#     # Add custom form fields or validation if needed
#
#
# def mark_as_certified(modeladmin, request, queryset):
#     queryset.update(is_certified=True)
#
# mark_as_certified.short_description = "Mark selected artifacts as certified"
#
#
#
#
# class ArtifactAdmin(admin.ModelAdmin):
#     actions = [mark_as_certified]
#     search_fields = ['name', 'type']
#     list_filter = ['location', 'period', 'collection']
#     form = ArtifactAdminForm
#
# admin.site.register(Artifact, ArtifactAdmin)