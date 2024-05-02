# Generated by Django 5.0.4 on 2024-05-02 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=300)),
            ],
            options={
                'ordering': ['-pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('short', models.TextField(blank=True, null=True, verbose_name='Short description')),
                ('description', models.TextField(blank=True, null=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
    ]
