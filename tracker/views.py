import json
from datetime import date
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.utils import timezone

from .models import Category, Transaction

# Default categories to seed for new users
DEFAULT_CATEGORIES = [
    ('Salary',        'Income',  '💼', '#4ADE80'),
    ('Freelance',     'Income',  '💻', '#A78BFA'),
    ('Investment',    'Income',  '📈', '#2DD4BF'),
    ('Business',      'Income',  '🏢', '#60A5FA'),
    ('Food',          'Expense', '🍜', '#F87171'),
    ('Travel',        'Expense', '🚗', '#60A5FA'),
    ('Shopping',      'Expense', '🛍️', '#F472B6'),
    ('Bills',         'Expense', '🧾', '#FBBF24'),
    ('Health',        'Expense', '💊', '#34D399'),
    ('Entertainment', 'Expense', '🎬', '#FB923C'),
    ('Education',     'Expense', '📚', '#818CF8'),
    ('Other',         'Expense', '📦', '#94A3B8'),
]


def seed_categories(user):
    for name, type_, icon, color in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(user=user, name=name, type=type_, defaults={'icon': icon, 'color': color})


def seed_demo_transactions(user):
    today = date.today()
    salary_cat  = Category.objects.filter(user=user, name='Salary').first()
    free_cat    = Category.objects.filter(user=user, name='Freelance').first()
    food_cat    = Category.objects.filter(user=user, name='Food').first()
    travel_cat  = Category.objects.filter(user=user, name='Travel').first()
    bills_cat   = Category.objects.filter(user=user, name='Bills').first()
    shop_cat    = Category.objects.filter(user=user, name='Shopping').first()
    health_cat  = Category.objects.filter(user=user, name='Health').first()

    demos = [
        (salary_cat,  'Income',  45000, 'Monthly Salary',     '', today.replace(day=1)),
        (free_cat,    'Income',   8000, 'Freelance Project',  'React website', today.replace(day=10)),
        (food_cat,    'Expense',  2800, 'Grocery Shopping',   'Big Bazaar', today.replace(day=3)),
        (travel_cat,  'Expense',   500, 'Metro Monthly Pass', '', today.replace(day=4)),
        (bills_cat,   'Expense',  1450, 'Electricity Bill',   'TNEB', today.replace(day=7)),
        (shop_cat,    'Expense',  3600, 'Online Shopping',    'Amazon', today.replace(day=12)),
        (health_cat,  'Expense',   800, 'Doctor Visit',       'Clinic fee', today.replace(day=15)),
    ]
    for cat, typ, amt, note, extra, dt in demos:
        Transaction.objects.create(user=user, category=cat, type=typ, amount=amt, note=note, extra=extra, date=dt)


# ── AUTH ──────────────────────────────────────────────
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            seed_categories(user)
            seed_demo_transactions(user)
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account is ready.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})


# ── DASHBOARD ─────────────────────────────────────────
@login_required
def dashboard(request):
    today = date.today()
    year  = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    txns = Transaction.objects.filter(user=request.user, date__year=year, date__month=month)

    total_income  = txns.filter(type='Income').aggregate(s=Sum('amount'))['s'] or Decimal('0')
    total_expense = txns.filter(type='Expense').aggregate(s=Sum('amount'))['s'] or Decimal('0')
    balance       = total_income - total_expense

    recent = txns[:8]
    savings_rate = round(float(balance) / float(total_income) * 100, 1) if total_income > 0 else 0.0

    # Category breakdown for pie chart
    cat_data = (
        txns.filter(type='Expense')
        .values('category__name', 'category__color', 'category__icon')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # Month navigation
    import calendar
    month_name = calendar.month_name[month]
    prev_month = month - 1 if month > 1 else 12
    prev_year  = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year  = year if month < 12 else year + 1

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent': recent,
        'cat_data': list(cat_data),
        'savings_rate': savings_rate,
        'month_name': month_name,
        'year': year,
        'month': month,
        'prev_month': prev_month, 'prev_year': prev_year,
        'next_month': next_month, 'next_year': next_year,
        'txn_count': txns.count(),
    }
    return render(request, 'tracker/dashboard.html', context)


# ── TRANSACTION LIST ──────────────────────────────────
@login_required
def transaction_list(request):
    today = date.today()
    year  = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    type_filter = request.GET.get('type', 'All')
    cat_filter  = request.GET.get('cat', 'All')

    txns = Transaction.objects.filter(user=request.user, date__year=year, date__month=month)

    if type_filter in ('Income', 'Expense'):
        txns = txns.filter(type=type_filter)
    if cat_filter != 'All':
        txns = txns.filter(category__name=cat_filter)

    categories = Category.objects.filter(user=request.user).order_by('type', 'name')

    import calendar
    month_name = calendar.month_name[month]
    prev_month = month - 1 if month > 1 else 12
    prev_year  = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year  = year if month < 12 else year + 1

    context = {
        'txns': txns,
        'categories': categories,
        'type_filter': type_filter,
        'cat_filter': cat_filter,
        'month_name': month_name,
        'year': year, 'month': month,
        'prev_month': prev_month, 'prev_year': prev_year,
        'next_month': next_month, 'next_year': next_year,
    }
    return render(request, 'tracker/transaction_list.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        type_  = request.POST.get('type')
        note   = request.POST.get('note', '').strip()
        amount = request.POST.get('amount')
        cat_id = request.POST.get('category')
        dt     = request.POST.get('date')
        extra  = request.POST.get('extra', '').strip()

        if not all([type_, note, amount, cat_id, dt]):
            messages.error(request, 'All fields are required.')
        else:
            try:
                cat = Category.objects.get(pk=cat_id, user=request.user)
                Transaction.objects.create(
                    user=request.user, category=cat,
                    type=type_, note=note, amount=Decimal(amount),
                    date=dt, extra=extra
                )
                messages.success(request, '✅ Transaction added successfully!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error: {e}')

    categories = Category.objects.filter(user=request.user).order_by('type', 'name')
    return render(request, 'tracker/add_transaction.html', {
        'categories': categories,
        'today': date.today().isoformat(),
    })


@login_required
def delete_transaction(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        txn.delete()
        messages.success(request, '🗑️ Transaction deleted.')
    return redirect(request.POST.get('next', 'dashboard'))


# ── CATEGORIES ────────────────────────────────────────
@login_required
def category_list(request):
    cats = Category.objects.filter(user=request.user).order_by('type', 'name')
    return render(request, 'tracker/category_list.html', {'cats': cats})


@login_required
def add_category(request):
    if request.method == 'POST':
        name  = request.POST.get('name', '').strip()
        type_ = request.POST.get('type')
        icon  = request.POST.get('icon', '📦')
        color = request.POST.get('color', '#94A3B8')
        if name and type_:
            Category.objects.get_or_create(user=request.user, name=name, type=type_, defaults={'icon': icon, 'color': color})
            messages.success(request, f'Category "{name}" added.')
        return redirect('category_list')
    return redirect('category_list')


@login_required
def delete_category(request, pk):
    cat = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category deleted.')
    return redirect('category_list')


# ── API ENDPOINTS ─────────────────────────────────────
@login_required
def api_monthly_summary(request):
    today = date.today()
    year  = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    txns = Transaction.objects.filter(user=request.user, date__year=year, date__month=month)
    income  = float(txns.filter(type='Income').aggregate(s=Sum('amount'))['s'] or 0)
    expense = float(txns.filter(type='Expense').aggregate(s=Sum('amount'))['s'] or 0)

    return JsonResponse({'income': income, 'expense': expense, 'balance': income - expense})


@login_required
def api_chart_data(request):
    today = date.today()
    year  = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Category pie data
    txns = Transaction.objects.filter(user=request.user, date__year=year, date__month=month)
    cat_data = list(
        txns.filter(type='Expense')
        .values('category__name', 'category__color')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # 6-month trend
    trend = []
    for i in range(5, -1, -1):
        m = month - i
        y = year
        while m <= 0: m += 12; y -= 1
        t = Transaction.objects.filter(user=request.user, date__year=y, date__month=m)
        inc = float(t.filter(type='Income').aggregate(s=Sum('amount'))['s'] or 0)
        exp = float(t.filter(type='Expense').aggregate(s=Sum('amount'))['s'] or 0)
        trend.append({'month': f"{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1]} {y}", 'income': inc, 'expense': exp})

    return JsonResponse({
        'cat_data': [{'name': d['category__name'], 'color': d['category__color'], 'total': float(d['total'])} for d in cat_data],
        'trend': trend,
    })
