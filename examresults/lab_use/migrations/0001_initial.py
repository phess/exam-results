# Generated by Django 3.0.5 on 2020-04-05 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.SlugField(max_length=15)),
                ('full_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ExamResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_full_name', models.CharField(max_length=200)),
                ('patient_id', models.CharField(max_length=20)),
                ('sample_received', models.DateField(verbose_name='date received')),
                ('sample_id', models.CharField(max_length=40)),
                ('exam_result', models.BooleanField(choices=[('POSITIVE', True), ('NEGATIVE', False)])),
                ('exam_date', models.DateTimeField(auto_now_add=True, verbose_name='date issued')),
                ('result_submitted', models.BooleanField()),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab_use.Institution')),
            ],
        ),
    ]
