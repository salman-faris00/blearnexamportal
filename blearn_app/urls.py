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
    
    
    path('B_ADMIN/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_question/', views.add_question, name='add_question'),
    path('edit_question/<int:id>/', views.edit_question, name='edit_question'),
    path('delete_question/<int:id>/', views.delete_question, name='delete_question'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('view_results/', views.view_results, name='view_results'),
     path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),
    path('resend_otp/<str:email>/', views.resend_otp_password, name='resend_otp_password'),
    path('download-results/', views.download_results_pdf, name='download_results'),
    path('download_excel/', views.download_excel, name='download_excel'),
    path('search-results/', views.search_results, name='search_results'),
    path('verify-login-otp/', views.verify_login_otp, name='verify_login_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('delete_result/<int:id>/', views.delete_result, name='delete_result'),
    path('save_recording/', views.save_recording, name='save_recording'),
    
    
    
    path('view_students/', views.view_students, name='view_students'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('clear_students/', views.clear_students, name='clear_students'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),





path('download_students_pdf/', views.download_students_pdf, name='download_students_pdf'),
path('download_students_excel/', views.download_students_excel, name='download_students_excel'),
path('resend_otp_password/<str:email>/', views.resend_otp_password, name='resend_otp_password'),






    
]
