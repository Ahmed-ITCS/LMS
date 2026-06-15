from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('members/', views.member_list, name='member_list'), 
    path(
        'members/<int:member_id>/',
        views.member_detail,
        name='member_detail'
    ),
    
]