from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path('^$', views.registration_page, name='registration_page'),

    path('register/', views.register_student, name='register'),
    path('success/', views.success_page, name='success'),
    path('login/', views.login_student, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_student, name='logout'),
    path('exam_portal/', views.exam_portal, name='exam_portal'),
      path('submit_exam/', views.submit_exam, name='submit_exam'),
      
      # path('log_violation/', views.log_violation, name='log_violation'),
    
    
    #admin tasks 
    
    
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_question/', views.add_question, name='add_question'),
    path('edit_question/<int:id>/', views.edit_question, name='edit_question'),
    path('delete_question/<int:id>/', views.delete_question, name='delete_question'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('view_results/', views.view_results, name='view_results'),
     path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:email>/', views.reset_password, name='reset_password'),
    path('download-results/', views.download_results_pdf, name='download_results'),
    path('download_excel/', views.download_excel, name='download_excel'),
path('results/delete/<int:id>/', views.delete_result, name='delete_result'),
path('list_students/', views.list_students, name='list_students'),






    
]
