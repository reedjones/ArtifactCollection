# Generated by Django 4.2.7 on 2023-11-25 04:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("artifacts", "0004_geography_artifact_geography"),
    ]

    operations = [
        migrations.AddField(
            model_name="provenanceevent",
            name="level",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="provenanceevent",
            name="date",
            field=models.DateField(),
        ),
    ]
