from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model
from .models import Transaction, ChildAccount
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.db.models.functions import TruncDay
from django.contrib import messages
from .forms import ChildExpenseForm
from django.core.paginator import Paginator

# ------------------------
# HOME
# ------------------------
def home(request):
    return render(request, "index.html")


# ------------------------
# DASHBOARD
# ------------------------
@login_required
def dashboard(request):
    # Transactions for all children of the parent
    transactions = Transaction.objects.filter(child__parent=request.user)
    spending = transactions.filter(transaction_type='debit')

    now = timezone.now()

    # ------------------------
    # PIE CHART (current month)
    # ------------------------
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_month_spending = spending.filter(date__gte=month_start)

    category_data = current_month_spending.values('category').annotate(total=Sum('amount'))
    categories = [item['category'] for item in category_data]
    category_totals = [float(item['total']) for item in category_data]

    # ------------------------
    # BAR CHART (last 6 months)
    # ------------------------
    six_months_ago = now - timedelta(days=180)
    monthly_data = spending.filter(date__gte=six_months_ago).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    months = [item['month'].strftime('%b %Y') for item in monthly_data]
    monthly_totals = [float(item['total']) for item in monthly_data]

    # Recent transactions
    recent_transactions = transactions.order_by('-date')[:3]

    context = {
        'categories': categories,
        'category_totals': category_totals,
        'months': months,
        'monthly_totals': monthly_totals,
        'recent_transactions': recent_transactions,
    }

    return render(request, "dashboard.html", context)



# ALL TRANSACTIONS
# ------------------------
@login_required
def all_transactions(request):
    transactions = Transaction.objects.filter(child__parent=request.user).order_by('-date')
    return render(request, "all_transactions.html", {"transactions": transactions})



# MY CHILDREN
@login_required
def mychildren(request):
    User = get_user_model()
    children = User.objects.filter(parent=request.user, role='child')

    children_data = []
    for child in children:
        transactions = Transaction.objects.filter(child=child)
        total_spent = transactions.filter(transaction_type='debit').aggregate(total=Sum('amount'))['total'] or 0

        # Get allowance from ChildAccount if exists
        allowance = getattr(getattr(child, 'account', None), 'allowance', 50000)
        balance = allowance - total_spent

        percentage_used = (total_spent / allowance) * 100 if allowance > 0 else 0

        children_data.append({
            "child": child,
            "allowance": allowance,
            "total_spent": total_spent,
            "balance": balance,
            "percentage_used": round(percentage_used, 1)
        })

    return render(request, "mychildren.html", {"children": children_data})



# ADD CHILD
@login_required
def Addchild(request):
    User = get_user_model()

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            error = "This username is already taken. Please choose another."
            return render(request, "Addchild.html", {"error": error})

        # Create child user
        child = User.objects.create_user(
            username=username,
            password=password,
            role="child",
            parent=request.user
        )

        child.first_name = full_name
        child.save()

        # Create child account
        ChildAccount.objects.create(child=child, allowance=50000)

        return redirect("mychildren")

    return render(request, "Addchild.html")

User = get_user_model()
def child_detail(request, child_id):
    child = get_object_or_404(User, id=child_id, parent=request.user)

    context = {
        "child": child
    }

    return render(request, "child_detail.html", context)


@login_required
def Fundwallet(request):

    if request.user.role != "parent":
        return redirect("dashboard")

    User = get_user_model()
    children = User.objects.filter(parent=request.user, role="child")

    if request.method == "POST":
        child_id = request.POST.get("child")
        amount = request.POST.get("amount")

        child = get_object_or_404(User, id=child_id, parent=request.user)

        # Create credit transaction
        Transaction.objects.create(
            child=child,
            category="Allowance",
            amount=amount,
            transaction_type="credit"
        )

        messages.success(request, "Wallet funded successfully!")

        return redirect("dashboard")

    return render(request, "Fundwallet.html", {"children": children})


# this is where child views start

# ------------------------
# CHILD LOGIN
# ------------------------
def child_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == "child":
            login(request, user)
            return redirect("childrendashboard")

        else:
            messages.error(request, "Invalid login details")

    return render(request, "child_login.html")


@login_required
def childrendashboard(request):

    if request.user.role != "child":
        return redirect("dashboard")

    child = request.user

    # -------------------------
    # CHILD TRANSACTIONS
    # -------------------------
    transactions = Transaction.objects.filter(child=child)

    # -------------------------
    # TOTAL SPENT
    # -------------------------
    total_spent = transactions.filter(
        transaction_type="debit"
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    # -------------------------
    # ACCOUNT INFO
    # -------------------------
    allowance = child.transactions.filter(
    transaction_type="credit"
    ).aggregate(Sum("amount"))["amount__sum"] or 0
    balance = allowance - total_spent

    # -------------------------
    # RECENT TRANSACTIONS
    # -------------------------
    recent_transactions = transactions.order_by("-date")[:5]

    # -------------------------
    # LINE CHART DATA (LAST 7 DAYS)
    # -------------------------
    today = timezone.now().date()
    day_objects = [today - timedelta(days=i) for i in range(6, -1, -1)]
    days = [(day).strftime("%a") for day in day_objects]  # labels for Chart.js

    # Get spending grouped by day & category
    weekly_data = (
        transactions.filter(
            transaction_type="debit",
            date__date__gte=day_objects[0]  # 7 days ago
        )
        .annotate(day=TruncDay("date"))
        .values("day", "category")
        .annotate(total=Sum("amount"))
        .order_by("day")
    )

    # Build a dictionary of category -> day -> amount
    datasets_dict = {}
    for item in weekly_data:
        category = str(item["category"])
        day = item["day"].date()
        total = float(item["total"])

        if category not in datasets_dict:
            datasets_dict[category] = {d: 0 for d in day_objects}

        datasets_dict[category][day] = total

    # If there’s no data at all, create a default "No Spending" dataset
    if not datasets_dict:
        datasets_dict["No Spending"] = {d: 0 for d in day_objects}

    # Build the final datasets list for Chart.js
    datasets = []
    for category, values in datasets_dict.items():
        data_ordered = [values[day] for day in day_objects]
        datasets.append({
            "label": category,
            "data": data_ordered
        })

    context = {
        "child": child,
        "allowance": allowance,
        "total_spent": total_spent,
        "balance": balance,
        "recent_transactions": recent_transactions,
        "chart_days": days,
        "chart_datasets": datasets,
    }

    return render(request, "childrendashboard.html", context)


@login_required
def Addexpense(request):

    if request.user.role != "child":
        return redirect("dashboard")

    if request.method == "POST":
        form = ChildExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.child = request.user
            expense.transaction_type = "debit"

            # handle other category
            other_category = request.POST.get("other_category")

            if expense.category == "Other" and other_category:
                expense.category = other_category

            expense.save()

            messages.success(request, "Expense added successfully!")

            return redirect("Addexpense")

    else:
        form = ChildExpenseForm()

    return render(request, "Addexpense.html", {"form": form})




@login_required
def Mytransactions(request):

    if request.user.role != "child":
        return redirect("dashboard")

    child = request.user

    transactions = Transaction.objects.filter(
        child=child
    ).order_by("-date")

    # GET FILTER VALUES
    category = request.GET.get("category")
    date_filter = request.GET.get("date")

    # CATEGORY FILTER
    if category:
        transactions = transactions.filter(category=category)

    # DATE FILTER
    if date_filter == "today":
        transactions = transactions.filter(date__date=timezone.now().date())

    elif date_filter == "week":
        week_ago = timezone.now() - timedelta(days=7)
        transactions = transactions.filter(date__gte=week_ago)

    elif date_filter == "month":
        month_ago = timezone.now() - timedelta(days=30)
        transactions = transactions.filter(date__gte=month_ago)

    # PAGINATION
    paginator = Paginator(transactions, 10)  # 10 transactions per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # GET UNIQUE CATEGORIES
    categories = Transaction.objects.filter(
        child=child
    ).values_list("category", flat=True).distinct()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "selected_category": category,
        "selected_date": date_filter,
    }

    return render(request, "Mytransactions.html", context)




@login_required
def Childprofile(request):
    now = timezone.now()

    # All debit transactions this month
    transactions = Transaction.objects.filter(
        child=request.user,
        transaction_type="debit",
        date__month=now.month,
        date__year=now.year
    ).order_by("date")

    # Daily points (each transaction amount)
    daily_labels = [tx.date.strftime("%d %b") for tx in transactions]
    daily_data = [float(tx.amount) for tx in transactions]

    # Weekly points (sum per week, but keep each week as its own point)
    weekly_spending = {}
    for tx in transactions:
        week_label = f"Week {tx.date.isocalendar()[1]}"
        weekly_spending[week_label] = weekly_spending.get(week_label, 0) + float(tx.amount)

    # Sort weeks so they appear in order
    weekly_labels = sorted(weekly_spending.keys(), key=lambda w: int(w.split()[1]))
    weekly_data = [weekly_spending[w] for w in weekly_labels]

    context = {
        "monthly_spending": sum(daily_data) if daily_data else 0,
        "daily_labels": daily_labels,
        "daily_data": daily_data,
        "weekly_labels": weekly_labels,
        "weekly_data": weekly_data,
    }
    return render(request, "Childprofile.html", context)