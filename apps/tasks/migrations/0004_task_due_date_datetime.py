import datetime

from django.db import migrations, models
from django.utils import timezone


def dates_to_datetimes(apps, schema_editor):
    # prazos antigos eram só data: viram 23:59 daquele dia, no fuso do projeto (TIME_ZONE)
    Task = apps.get_model('tasks', 'Task')
    for task in Task.objects.exclude(due_date=None):
        end_of_day = datetime.datetime.combine(task.due_date, datetime.time(23, 59))
        task.due_at = timezone.make_aware(end_of_day)
        task.save(update_fields=['due_at'])


def datetimes_to_dates(apps, schema_editor):
    # para desfazer a migration (migrate tasks 0003): guarda só a data local
    Task = apps.get_model('tasks', 'Task')
    for task in Task.objects.exclude(due_at=None):
        task.due_date = timezone.localtime(task.due_at).date()
        task.save(update_fields=['due_date'])


class Migration(migrations.Migration):
    # Um AlterField direto de DateField para DateTimeField perderia os prazos no SQLite,
    # então criamos um campo novo, convertemos os valores e trocamos os nomes.

    dependencies = [
        ('tasks', '0003_task_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='due_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(dates_to_datetimes, datetimes_to_dates),
        migrations.RemoveField(
            model_name='task',
            name='due_date',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='due_at',
            new_name='due_date',
        ),
    ]
