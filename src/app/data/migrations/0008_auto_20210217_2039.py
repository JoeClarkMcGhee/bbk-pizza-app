# Generated by Django 3.0.2 on 2021-02-17 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20210215_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='data.Post'),
        ),
    ]
