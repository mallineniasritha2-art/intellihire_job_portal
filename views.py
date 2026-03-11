from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import Job,Application
from django.contrib import messages
from django.shortcuts import get_object_or_404


# ------------------ SIGNUP VIEW ------------------

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        contact_number = request.POST.get("contact_number")
        role = request.POST.get("role")

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Save extra fields
        user.contact_number = contact_number

        if role == "candidate":
            user.is_candidate = True
        elif role == "interviewer":
            user.is_interviewer = True

        user.save()

        return redirect("login")

    return render(request, "signup.html")


# ------------------ LOGIN VIEW ------------------



def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_candidate:
                return redirect("candidate_dashboard")

            elif user.is_interviewer:
                return redirect("interviewer_dashboard")

        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

# ------------------ LOGOUT VIEW ------------------

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------ DASHBOARDS ------------------





@login_required

def candidate_dashboard(request):

    if not request.user.is_candidate:
        return redirect('interviewer_dashboard')

    jobs = Job.objects.all()
    applications = Application.objects.filter(candidate=request.user)

    return render(request, "candidate_dashboard.html", {
        "jobs": jobs,
        "applications": applications
    })

@login_required
def interviewer_dashboard(request):

    # If candidate tries to access interviewer page
    if not request.user.is_staff:
        return redirect("candidate_dashboard")

    jobs = Job.objects.all()
    return render(request, "interviewer_dashboard.html", {"jobs": jobs})
def add_job(request):
    if request.method == "POST":
        title = request.POST.get("title")
        company_name = request.POST.get("company_name")
        description = request.POST.get("description")
        location = request.POST.get("location")
        salary = request.POST.get("salary")

        Job.objects.create(
            title=title,
            company_name=company_name,
            description=description,
            location=location,
            salary=salary,
        )

        return redirect("interviewer_dashboard")

    return render(request, "add_job.html")


@login_required
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You already applied for this job.")
        return redirect("candidate_dashboard")

    Application.objects.create(
        job=job,
        candidate=request.user,
        status="Pending"
    )

    messages.success(request, "Application submitted successfully!")

    return redirect("candidate_dashboard")



@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id)

    application.status = status
    application.save()

    return redirect("interviewer_dashboard")
@login_required
def schedule_interview(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == "POST":
        application.interview_date = request.POST.get("date")
        application.interview_time = request.POST.get("time")
        application.meeting_link = request.POST.get("link")
        application.status = "Interview Scheduled"
        application.save()

        return redirect("interviewer_dashboard")

    return render(request, "schedule_interview.html", {"application": application})