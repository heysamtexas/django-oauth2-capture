# Generated by Django 5.1.1 on 2024-09-23 07:41

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("boom", "0005_oauthtoken_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="oauthtoken",
            name="slug",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet=None, length=22, max_length=22, prefix=""
            ),
        ),
        migrations.AlterField(
            model_name="oauthtoken",
            name="owner",
            field=models.ForeignKey(
                help_text="A reference to the local user this OAuth token is associated with.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="oauth_tokens",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
