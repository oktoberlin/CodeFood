# Generated by Django 3.2.11 on 2022-03-10 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20220310_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Steps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stepOrder', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
    ]
