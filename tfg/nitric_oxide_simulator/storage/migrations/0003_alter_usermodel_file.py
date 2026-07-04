import storage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_alter_usermodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='file',
            field=models.FileField(upload_to=storage.models.user_model_upload_path),
        ),
    ]
