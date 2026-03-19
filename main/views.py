from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import transaction as db_transaction
from django.db.models.functions import TruncMonth, TruncDay
from django.contrib.auth import get_user_model, authenticate, login
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.core.paginator import Paginator
from decimal import Decimal
from .models import Transaction, ChildAccount
from .models import CustomUser
from .forms import ChildExpenseForm


# ------------------------
# HOME
# ------------------------
def home(request):
    if request.user.is_authenticated:
        if request.user.role == "parent":
            return redirect("mychildren")
        elif request.user.role == "child":
            return redirect("children")
    return render(request, "index.html")


# ------------------------
# DASHBOARD ROUTER
# ------------------------
@login_required
def dashboard(request):

    if request.user.role == "parent":
        return redirect("mychildren")

    if request.user.role == "child":
        return redirect("childrendashboard")


# ------------------------
# MY CHILDREN (PARENT MAIN PAGE)
# ------------------------
@login_required
def mychildren(request):

    if request.user.role != "parent":
        return redirect("childrendashboard")

    User = get_user_model()
    children = User.objects.filter(parent=request.user, role="child")

    children_data = []

    for child in children:

        transactions = Transaction.objects.filter(child=child)

        total_spent = transactions.filter(
            transaction_type="debit"
        ).aggregate(total=Sum("amount"))["total"] or 0

        account = getattr(child, "account", None)

        allowance = account.allowance if account else 0

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


# ------------------------
# ADD CHILD
# ------------------------
@login_required
def Addchild(request):

    if request.user.role != "parent":
        return redirect("childrendashboard")

    User = get_user_model()

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            error = "This username is already taken. Please choose another."
            return render(request, "Addchild.html", {"error": error})

        child = User.objects.create_user(
            username=username,
            password=password,
            role="child",
            parent=request.user
        )

        child.first_name = full_name.title()
        child.save()

        # Child wallet starts at ₦0
        ChildAccount.objects.create(child=child)

        return redirect("mychildren")

    return render(request, "Addchild.html")


@login_required
def reset_child_password(request, child_id):

    child = get_object_or_404(CustomUser, id=child_id, parent=request.user)

    if request.method == "POST":

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")

        else:
            child.set_password(password1)
            child.save()

            messages.success(request, "Child password reset successfully")

            return redirect("mychildren")

    return render(request, "reset_child_password.html", {"child": child})

# ------------------------
# CHILD DETAIL
# ------------------------
@login_required
def child_detail(request, child_id):

    if request.user.role != "parent":
        return redirect("childrendashboard")

    User = get_user_model()

    child = get_object_or_404(User, id=child_id, parent=request.user)

    context = {
        "child": child
    }

    return render(request, "child_detail.html", context)


# ------------------------
# FUND WALLET
# ------------------------



@login_required
def Fundwallet(request):
    if request.user.role != "parent":
        return redirect("childrendashboard")

    User = get_user_model()
    children = User.objects.filter(parent=request.user, role="child")

    if request.method == "POST":
        child_id = request.POST.get("child")
        amount_str = request.POST.get("amount")

        # Convert amount safely to Decimal
        try:
            amount = Decimal(amount_str)
        except Exception:
            messages.error(request, "Invalid amount entered.")
            return redirect("Fundwallet")

        child = get_object_or_404(User, id=child_id, parent=request.user)

        # Add credit transaction
        Transaction.objects.create(
            child=child,
            category="Allowance",
            amount=amount,  # store as Decimal
            transaction_type="credit"
        )

        # Update allowance
        account = child.account
        account.allowance += amount  # both are Decimal now
        account.save()

        messages.success(request, "Wallet funded successfully!")
        return redirect("mychildren")

    return render(request, "Fundwallet.html", {"children": children})



# ======================================================
# CHILD SIDE
# ======================================================

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


# ------------------------
# CHILD DASHBOARD
# ------------------------
@login_required
def childrendashboard(request, child_id=None):

    # CHILD VIEWING THEIR OWN DASHBOARD
    if request.user.role == "child":
        child = request.user
        readonly = False

    # PARENT VIEWING CHILD DASHBOARD
    else:
        if not child_id:
            return redirect("mychildren")

        User = get_user_model()
        child = User.objects.get(id=child_id, parent=request.user)
        readonly = True


    transactions = Transaction.objects.filter(child=child)

    total_spent = transactions.filter(
        transaction_type="debit"
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    allowance = transactions.filter(
        transaction_type="credit"
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    balance = allowance - total_spent

    recent_transactions = transactions.order_by("-date")[:5]

    # CHART DATA
    today = timezone.now().date()
    day_objects = [today - timedelta(days=i) for i in range(6, -1, -1)]
    days = [(day).strftime("%a") for day in day_objects]

    weekly_data = (
        transactions.filter(
            transaction_type="debit",
            date__date__gte=day_objects[0]
        )
        .annotate(day=TruncDay("date"))
        .values("day", "category")
        .annotate(total=Sum("amount"))
        .order_by("day")
    )

    datasets_dict = {}

    for item in weekly_data:

        category = str(item["category"])
        day = item["day"].date()
        total = float(item["total"])

        if category not in datasets_dict:
            datasets_dict[category] = {d: 0 for d in day_objects}

        datasets_dict[category][day] = total

    if not datasets_dict:
        datasets_dict["No Spending"] = {d: 0 for d in day_objects}

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
        "readonly": readonly
    }

    return render(request, "childrendashboard.html", context)


# ------------------------
# ADD EXPENSE
# ------------------------
@login_required
def Addexpense(request):

    if request.user.role != "child":
        return redirect("mychildren")

    if request.method == "POST":

        form = ChildExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)
            expense.child = request.user
            expense.transaction_type = "debit"

            other_category = request.POST.get("other_category")

            if expense.category == "Other" and other_category:
                expense.category = other_category

            expense.save()

            messages.success(request, "Expense added successfully!")

            return redirect("Addexpense")

    else:
        form = ChildExpenseForm()

    return render(request, "Addexpense.html", {"form": form})


# ------------------------
# CHILD TRANSACTIONS
# ------------------------
@login_required
def Mytransactions(request):

    if request.user.role != "child":
        return redirect("mychildren")

    child = request.user

    transactions = Transaction.objects.filter(
        child=child
    ).order_by("-date")

    category = request.GET.get("category")
    date_filter = request.GET.get("date")

    if category:
        transactions = transactions.filter(category=category)

    if date_filter == "today":
        transactions = transactions.filter(date__date=timezone.now().date())

    elif date_filter == "week":
        week_ago = timezone.now() - timedelta(days=7)
        transactions = transactions.filter(date__gte=week_ago)

    elif date_filter == "month":
        month_ago = timezone.now() - timedelta(days=30)
        transactions = transactions.filter(date__gte=month_ago)

    paginator = Paginator(transactions, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

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


# ------------------------
# CHILD PROFILE
# ------------------------
@login_required
def Childprofile(request):

    if request.user.role != "child":
        return redirect("mychildren")

    now = timezone.now()

    transactions = Transaction.objects.filter(
        child=request.user,
        transaction_type="debit",
        date__month=now.month,
        date__year=now.year
    ).order_by("date")

    daily_labels = [tx.date.strftime("%d %b") for tx in transactions]
    daily_data = [float(tx.amount) for tx in transactions]

    weekly_spending = {}

    for tx in transactions:
        week_label = f"Week {tx.date.isocalendar()[1]}"
        weekly_spending[week_label] = weekly_spending.get(week_label, 0) + float(tx.amount)

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