# Generated by Django 5.1 on 2024-08-30 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('SAVINGS', 'Savings Account'), ('CURRENT', 'Current Account'), ('DEBIT', 'Debit Card'), ('CREDIT', 'Credit Card')], max_length=10)),
                ('product_name', models.CharField(max_length=20)),
                ('description', models.TextField(null=True)),
            ],
        ),
    ]
