# Generated by Django 5.0.6 on 2024-08-24 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('coupon_code', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('coupon_used', models.BooleanField(default=False)),
            ],
        ),
    ]
