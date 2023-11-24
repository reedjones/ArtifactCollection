__author__ = "reed@reedjones.me"


from storages.backends.s3boto3 import S3Boto3Storage

"""

class YourModel(models.Model):
    public_file = models.FileField(upload_to='public_media/')
    private_file = models.FileField(upload_to='private_media/')
"""

class PrivateMediaStorage(S3Boto3Storage):
    location = 'private_media'  # S3 path where private media files are stored
    default_acl = 'private'  # Set default ACL to private


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'  # S3 path where media files are stored
    default_acl = 'public-read'  # Make files publicly readable