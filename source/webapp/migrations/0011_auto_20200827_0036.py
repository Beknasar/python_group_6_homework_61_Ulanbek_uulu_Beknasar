# Generated by Django 2.2 on 2020-08-26 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_auto_20200823_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='webapp.Project', verbose_name='проект'),
        ),
    ]
