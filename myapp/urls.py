from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerUser, name="register"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    path('daily-charts/', views.daily_charts, name="daily_charts"),
    path('weekly-charts/', views.weekly_charts, name="weekly_charts"),
    path('6-hourly/', views.six_hourly, name="6_hourly"),
    path('accounts/', views.accounts, name="accounts"),
    path('logs/', views.logs, name="logs"),

    path('view-charts/<int:id>/', views.view_daily_charts, name="view_daily_chart"),
]
