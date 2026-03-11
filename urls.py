from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("candidate/", views.candidate_dashboard, name="candidate_dashboard"),
    path("interviewer/", views.interviewer_dashboard, name="interviewer_dashboard"),
    path("add-job/", views.add_job, name="add_job"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("update-status/<int:app_id>/<str:status>/", views.update_application_status, name="update_status"),
    path('schedule/<int:application_id>/', views.schedule_interview, name='schedule_interview'),
]