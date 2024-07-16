# Generated by Django 5.0.6 on 2024-07-16 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='extras',
        ),
        migrations.AddField(
            model_name='reservation',
            name='services',
            field=models.ManyToManyField(blank=True, to='reservations.service'),
        ),
    ]
