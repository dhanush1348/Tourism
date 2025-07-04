from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, null=True),
        ),
    ] 