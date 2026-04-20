from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Member, Attendance, Expense, Sub

def statistics_view(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # --- الإحصائيات اليومية ---
    daily_attendance = Attendance.objects.filter(
        attendance_time__date=today
    ).count()

    daily_expenses = Expense.objects.filter(
        expense_date=today
    ).aggregate(total=Sum("expense_cost"))["total"] or 0

    # --- الإحصائيات الأسبوعية ---
    weekly_attendance = Attendance.objects.filter(
        attendance_time__date__gte=week_ago,
        attendance_time__date__lte=today
    ).count()

    weekly_expenses = Expense.objects.filter(
        expense_date__gte=week_ago,
        expense_date__lte=today
    ).aggregate(total=Sum("expense_cost"))["total"] or 0

    # --- إجمالي الإيرادات من الاشتراكات (بناءً على تكلفة اشتراك كل عضو) ---
    # نفترض أن كل Member مرتبط بـ Sub له sub_cost
    total_revenue = Member.objects.aggregate(
        total=Sum('sub__sub_cost')
    )['total'] or 0

    # --- إجمالي المصروفات ---
    total_expenses = Expense.objects.aggregate(
        total=Sum("expense_cost")
    )["total"] or 0

    # --- صافي الربح ---
    net_profit = total_revenue - total_expenses

    # --- بيانات الأيام السبعة الماضية للرسم البياني ---
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    attendance_labels = [d.strftime("%Y-%m-%d") for d in last_7_days]
    attendance_data = [
        Attendance.objects.filter(attendance_time__date=d).count()
        for d in last_7_days
    ]

    expenses_labels = [d.strftime("%Y-%m-%d") for d in last_7_days]
    expenses_data = [
        float(Expense.objects.filter(expense_date=d).aggregate(
            total=Sum("expense_cost")
        )["total"] or 0)
        for d in last_7_days
    ]

    # إجمالي الأعضاء والحضور (للإشارة)
    total_members = Member.objects.count()
    total_attendance = Attendance.objects.count()

    context = {
        "total_members": total_members,
        "total_attendance": total_attendance,
        "total_expenses": total_expenses,
        "total_revenue": total_revenue,
        "net_profit": net_profit,
        "daily_attendance": daily_attendance,
        "daily_expenses": daily_expenses,
        "weekly_attendance": weekly_attendance,
        "weekly_expenses": weekly_expenses,
        "attendance_labels": attendance_labels,
        "attendance_data": attendance_data,
        "expenses_labels": expenses_labels,
        "expenses_data": expenses_data,
    }

    return render(request, "statistics.html", context)