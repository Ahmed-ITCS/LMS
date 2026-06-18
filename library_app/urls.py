from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('catalog/add/', views.add_book_view, name='add_book'),
    path('catalog/remove/<str:isbn>/', views.remove_book_view, name='remove_book'),
    path('search/', views.search_view, name='search'),
    path('transaction/issue/', views.issue_view, name='issue_book'),
    path('transaction/return/', views.return_view, name='return_book'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/register/', views.register_view, name='register'),
    path('account/', views.my_account_view, name='my_account'),
]
