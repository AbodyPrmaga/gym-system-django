from django import forms
from django.utils import timezone
from .models import Attendance, Member

class AttendanceForm(forms.ModelForm):

    qr_input = forms.CharField(label="Scan QR Code")

    class Meta:
        model = Attendance
        fields = ["qr_input"]

    def clean_qr_input(self):
        qr_code = self.cleaned_data["qr_input"]

        try:
            member = Member.objects.get(qr_code=qr_code)
        except Member.DoesNotExist:
            raise forms.ValidationError("QR Code غير موجود")

        # ========== التحقق الجديد: هل الاشتراك منتهي؟ ==========
        if member.end_date and member.end_date < timezone.now():
            raise forms.ValidationError("عذراً، اشتراك هذا العضو قد انتهى")
        # ====================================================

        today = timezone.now().date()

        already_attended = Attendance.objects.filter(
            member=member,
            attendance_time__date=today
        ).exists()

        if already_attended:
            raise forms.ValidationError("هذا العضو مسجل حضور بالفعل اليوم")

        return member