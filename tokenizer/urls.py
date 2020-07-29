from django.urls import path
from . import views

urlpatterns = [
    path('', views.token_list, name='token_list'),
    path('keywords', views.select_keywords_first_page, name='select_keywords'),
    path('keywords/', views.select_keywords_first_page, name='select_keywords'),
    path('keywords/<int:current_page>', views.select_keywords, name='select_keywords'),
    path('keywords/<int:current_page>/', views.select_keywords, name='select_keywords'),
    path('ajaxUpdate', views.ajax_update, name='ajax_update'),
    path('export/<str:session_id>', views.export_users_csv, name='export_users_csv'),
]