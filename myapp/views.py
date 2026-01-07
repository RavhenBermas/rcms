from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import DailyChart

from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.conf import settings


# Create your views here.

def registerUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        user_data_has_error = False

        if password != confirm:
            user_data_has_error = True
            messages.error(request, "Passwords do not match!")
        
        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exist!")

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already taken!")
        
        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect('register')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created. Please login.")
            return redirect("login")

    return render(request, "auth/register.html")

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("daily_charts")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "auth/login.html")

def logoutUser(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def daily_charts(request):

    if request.method == "POST":
        DailyChart.objects.create(
            station_name=request.POST.get("station_name"),
            station_id=request.POST.get("station_id"),
            station_code=request.POST.get("station_code"),
            assignment=request.POST.get("assignment"),
            date=request.POST.get("date"),
        )
        messages.success(request, "Daily Chart successfully added!")
        return redirect("daily_charts")

    charts = DailyChart.objects.all()

    charts_json = json.dumps(list(charts.values()), cls=DjangoJSONEncoder)

    paginator = Paginator(charts, 10)
    page_number = request.GET.get('page')
    charts_page = paginator.get_page(page_number)

    return render(request, "admin/scanned charts/daily.html", { "charts": charts_page,"charts_all": charts, "charts_json": charts_json})

@login_required(login_url="login")
def weekly_charts(request):
    return render(request, "admin/scanned charts/weekly.html")

@login_required(login_url="login")
def six_hourly(request):
    return render(request, "admin/hourly/6_hourly.html")

@login_required(login_url="login")
def twentyfour_hourly(request):
    return render(request, "admin/hourly/24_hourly.html")

@login_required(login_url="login")
def accounts(request):
    
    return render(request, "admin/accounts/accounts.html")    

@login_required(login_url="login")
def logs(request):
    return render(request, "admin/logs/logs.html")

@login_required(login_url="login")
def view_daily_charts(request, id):

    get_chart = get_object_or_404(DailyChart, pk=id)

    return render(request, 'admin/charts/view_chart.html', {'get_chart':get_chart})
