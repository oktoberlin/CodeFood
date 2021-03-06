# Generated by Django 3.2.11 on 2022-03-12 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_servehistory_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servehistory',
            name='id',
            field=models.CharField(default='V4RO', editable=False, max_length=4, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='servehistory',
            name='recipeId',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='serveHistory', to='api.recipelist'),
        ),
    ]
