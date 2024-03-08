# Generated by Django 3.2.24 on 2024-03-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('age', models.IntegerField(blank=True, null=True)),
                ('overall_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('resume', models.FileField(upload_to='worker_resumes/')),
            ],
        ),
    ]
