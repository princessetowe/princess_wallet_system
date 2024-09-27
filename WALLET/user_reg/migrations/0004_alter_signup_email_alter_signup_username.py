# Generated by Django 5.0.3 on 2024-09-27 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_reg', '0003_signup_other_name_alter_signup_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='signup',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
