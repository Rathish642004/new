# Generated by Django 4.2.6 on 2024-02-19 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0005_alter_student_phone_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_num',
            field=models.BigIntegerField(),
        ),
    ]
