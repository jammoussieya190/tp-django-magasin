# Generated by Django 5.0.2 on 2024-04-20 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0006_commande_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='type',
            field=models.CharField(choices=[('Al', 'Alimentaire'), ('Mb', 'Meuble'), ('Sn', 'Sanitaire'), ('Vs', 'Vaisselle'), ('Vt', 'Vêtement'), ('Jx', 'Jouets'), ('Lg', 'Linge de Maison'), ('Bj', 'Bijoux'), ('Dc', 'Décor')], default='em', max_length=2),
        ),
    ]
