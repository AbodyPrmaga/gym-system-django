from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count, Sum
from .models import Member, Sub, Attendance, Expense
from .forms import AttendanceForm
from django.core.exceptions import ValidationError
from django.utils import timezone


import qrcode, base64
from io import BytesIO


def generate_qr_image(data):

    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


admin.site.unregister([Group, User])


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "phonenum", "age", "sub", "start_date", "end_date")
    search_fields = ("name", "phonenum")
    list_filter = ("sub","end_date","start_date","age")
    readonly_fields = ("qr_preview",)

    def qr_preview(self, obj):
        if obj.qr_code:
            image = generate_qr_image(obj.qr_code)
            return format_html('<img src="{}" width="150" height="150"/>', image)

        return "No QR"

    qr_preview.short_description = "QR Code"


@admin.register(Sub)
class SubAdmin(admin.ModelAdmin):
    list_display = ("sub_name", "sub_cost", "end_after")



@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    form = AttendanceForm

    list_display = ("member", "attendance_time")
    list_filter = ["attendance_time"]

    def save_model(self, request, obj, form, change):

        member = form.cleaned_data["qr_input"]

        today = timezone.now().date()

        # منع تكرار الحضور في نفس اليوم
        if Attendance.objects.filter(
            member=member,
            attendance_time__date=today
        ).exists():

            raise ValidationError("تم تسجيل الحضور اليوم بالفعل")

        obj.member = member

        super().save_model(request, obj, form, change)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("expense_name", "expense_cost", "expense_date")
    list_filter = ("expense_date",)