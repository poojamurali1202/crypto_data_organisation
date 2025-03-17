from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


def handle(self, *args, **kwargs):
        # Create interval schedule (every 5 minutes)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1, period=IntervalSchedule.MINUTES
        )

        # Create periodic task
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name="Fetch Crypto Prices",
            task="application.tasks.fetch_crypto_prices",
            defaults={"args": json.dumps([])},  # No arguments needed
        )

        self.stdout.write(self.style.SUCCESS("Successfully created scheduled tasks!"))
