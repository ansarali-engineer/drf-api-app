import django.db.models.deletion
import django.contrib.auth.hashers
import user.models
from django.db import migrations, models


def hash_legacy_passwords(apps, schema_editor):
    User = apps.get_model('user', 'User')
    for user in User.objects.all().iterator():
        try:
            django.contrib.auth.hashers.identify_hasher(user.password)
        except (ValueError, TypeError):
            user.password = django.contrib.auth.hashers.make_password(user.password)
            user.save(update_fields=['password'])


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            hash_legacy_passwords,
            migrations.RunPython.noop,
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=user.models.generate_token_key, max_length=40, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='user.user')),
            ],
        ),
    ]
