from django.db import models
import uuid
from datetime import timedelta
from django.utils import timezone

def gen_qr():
    return str(uuid.uuid4())


class Sub(models.Model):

    sub_name = models.CharField(max_length=100, verbose_name="اسم الاشتراك")
    sub_cost = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="سعر الاشتراك"
    )
    end_after = models.IntegerField(verbose_name="مدة الاشتراك بالأيام")

    class Meta:
        db_table = "subs"
        verbose_name = "اشتراك"
        verbose_name_plural = "الأشتراكات"

    def __str__(self):
        return self.sub_name


class Member(models.Model):

    name = models.CharField(max_length=250, verbose_name="الاسم")
    phonenum = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    age = models.IntegerField(verbose_name="العمر")

    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, verbose_name="نوع الاشتراك")

    start_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ البداية")
    end_date = models.DateTimeField(
        blank=True, null=True, verbose_name="تاريخ الانتهاء"
    )

    qr_code = models.CharField(
        max_length=40,
        unique=True,
        editable=False,
        default=gen_qr,
        verbose_name="كود QR",
    )

    class Meta:
        db_table = "members"
        verbose_name = "عضو"
        verbose_name_plural = "الأعضاء"

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(days=self.sub.end_after)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Attendance(models.Model):

    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="العضو")

    # attendance_time = models.DateTimeField(auto_now_add=True, verbose_name="وقت الحضور")
    attendance_time = models.DateTimeField(default=timezone.now, verbose_name="وقت الحضور")

    class Meta:
        db_table = "attendances"
        verbose_name = "حضور"
        verbose_name_plural = "سجل الحضور"

    def __str__(self):
        return self.member.name


class Expense(models.Model):

    expense_name = models.CharField(max_length=200, verbose_name="اسم المصروف")

    expense_cost = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name="قيمة المصروف"
    )

    expense_date = models.DateField(verbose_name="تاريخ المصروف")

    class Meta:
        db_table = "expenses"
        verbose_name = "مصروف"
        verbose_name_plural = "المصروفات"

    def __str__(self):
        return self.expense_name
