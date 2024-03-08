# Generated by Django 3.2.24 on 2024-03-08 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='worker',
            name='skill',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='login.skill'),
        ),
    ]
