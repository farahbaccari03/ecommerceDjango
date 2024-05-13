# Generated by Django 4.1.7 on 2023-02-28 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100)),
                ('description', models.TextField(default='non definie')),
                ('prix', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('type', models.CharField(choices=[('Em', 'emballe'), ('fr', 'frais'), ('cs', 'conserve')], default='em', max_length=2)),
            ],
        ),
    ]
