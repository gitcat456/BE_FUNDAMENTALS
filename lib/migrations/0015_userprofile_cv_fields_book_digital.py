from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0014_alter_loan_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cv_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cv_object_name',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cv_filename',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='digital_object_name',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='digital_filename',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
