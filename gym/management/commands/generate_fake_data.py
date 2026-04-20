from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from gym.models import Attendance, Member


class Command(BaseCommand):
    help = "Generate fake Attendance data only"

    def handle(self, *args, **kwargs):

        members = list(Member.objects.all())

        if not members:
            self.stdout.write(
                self.style.ERROR("لا يوجد أعضاء في النظام")
            )
            return

        # احذف الحضور القديم (اختياري)
        Attendance.objects.all().delete()

        created_count = 0

        # توليد 100 سجل حضور (تقدر تغير الرقم)
        for _ in range(100):

            random_days = random.randint(0, 30)   # آخر 30 يوم
            random_hours = random.randint(6, 22)  # أوقات الجيم

            fake_time = timezone.now() - timedelta(
                days=random_days,
                hours=random_hours,
                minutes=random.randint(0, 59)
            )

            Attendance.objects.create(
                member=random.choice(members),
                attendance_time=fake_time
            )

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"تم إنشاء {created_count} سجل حضور بنجاح"
            )
        )