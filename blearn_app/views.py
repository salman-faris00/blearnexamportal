from django.contrib import messages
import random
from django.shortcuts import render,redirect
# Create your views here.
from .models import*
from django.core.mail import send_mail
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
import openpyxl


def registration_page(request):
    return render(request,"register.html")

def register_student(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        qualification = request.POST.get('qualification')
        department = request.POST.get('department')
        college = request.POST.get('college')

         # Check if email already exists
        if student.objects.filter(Email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        # Save to database
        student.objects.create(
            Email=email,
            Password=password,
            Name=name,
            phone_no=phone_no,
            qualification=qualification,
            department=department,
            college=college
        )
        return redirect('success')  # After registration, redirect to success page

    return render(request, 'register.html')

def success_page(request):
    return render(request, 'success.html')


# def login_student(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             student_obj = student.objects.get(Email=email, Password=password)
#             # If email and password match
#             request.session['student_id'] = student_obj.id
#             request.session['student_name'] = student_obj.Name
#             return redirect('dashboard')
#         except student.DoesNotExist:
#             # If email and password are wrong
#             return render(request, 'login.html', {'error': 'Invalid Email or Password'})

#     return render(request, 'login.html')




from django.contrib.auth.hashers import check_password

def login_student(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')  # DO NOT strip password for strict match

        try:
            student_obj = student.objects.get(Email=email)

            db_password = student_obj.Password  # Use stored password as-is

            print("Entered password:", repr(password))
            print("Stored password:", repr(db_password))

            # Case-sensitive match
            if password == db_password:
                request.session['student_id'] = student_obj.id
                request.session['student_name'] = student_obj.Name
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'error': 'Invalid  Password'})
        except student.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid Email'})

    return render(request, 'login.html')








def dashboard(request):
    if 'student_id' in request.session:
        name = request.session.get('student_name')
        return render(request, 'dashboard.html', {'name': name})
    else:
        return redirect('login')

def logout_student(request):
    request.session.flush()  # This will clear all session data
    return redirect('login')




# def exam_portal(request):
#     if 'student_id' not in request.session:
#         return redirect('login')

#     student_id = request.session.get('student_id')
#     student_obj = student.objects.get(id=student_id)

#     # Check if the student has already taken the exam
#     if Result.objects.filter(student=student_obj).exists():
#         return render(request, 'already_attempted.html')  # Show a message or redirect

#     if request.method == 'POST':
#         questions = Question.objects.all()
#         score = 0
#         total = questions.count()

#         for question in questions:
#             selected_answer = request.POST.get('q' + str(question.id))
#             if selected_answer == question.correct_answer:
#                 score += 1

#         Result.objects.create(
#             student=student_obj,
#             score=score,
#             total_questions=total,
#             correct_answers=score
#         )

#         return render(request, 'result.html', {'score': score, 'total': total, 'correct': score})

#     questions = list(Question.objects.all())
#     random.shuffle(questions)
#     selected_questions = questions[:25]
#     return render(request, 'exam_portal.html', {'questions': selected_questions})






def exam_portal(request):
    if 'student_id' not in request.session:
        return redirect('login')

    student_id = request.session.get('student_id')
    try:
        student_obj = student.objects.get(id=student_id)
    except student.DoesNotExist:
        return redirect('login')

    # Check if the student has already taken the exam
    if Result.objects.filter(student=student_obj).exists():
        return render(request, 'already_attempted.html')

    if request.method == 'POST':
        questions = Question.objects.all()
        score = 0
        total = questions.count()

        for question in questions:
            selected_answer = request.POST.get('q' + str(question.id))
            if selected_answer == question.correct_answer:
                score += 1

        Result.objects.create(
            student=student_obj,
            score=score,
            total_questions=total,
            correct_answers=score
        )

        return render(request, 'result.html', {
            'score': score,
            'total': total,
            'correct': score,
            'mark': score  # Pass score as 'mark' to trigger sparkles
        })

    questions = list(Question.objects.all())
    random.shuffle(questions)
    selected_questions = questions[:25]

    return render(request, 'exam_portal.html', {
        'questions': selected_questions
    })




# Admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Hardcoded admin credentials
        if username == 'admin' and password == 'admin123':
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid username or password'})

    return render(request, 'admin_login.html')


# Admin dashboard view
def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    questions = Question.objects.all()
    return render(request, 'admin_dashboard.html', {'questions': questions})


# Add Question
def add_question(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    if request.method == 'POST':
        question_text = request.POST['question_text']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        correct_answer = request.POST['correct_answer']

        Question.objects.create(
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer=correct_answer
        )
        return redirect('admin_dashboard')

    return render(request, 'add_question.html')


# Edit Question
def edit_question(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    question = Question.objects.get(id=id)

    if request.method == 'POST':
        question.question_text = request.POST['question_text']
        question.option1 = request.POST['option1']
        question.option2 = request.POST['option2']
        question.option3 = request.POST['option3']
        question.option4 = request.POST['option4']
        question.correct_answer = request.POST['correct_answer']
        question.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_question.html', {'question': question})


# Delete Question
def delete_question(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    question = Question.objects.get(id=id)
    question.delete()
    return redirect('admin_dashboard')


# Admin logout
def admin_logout(request):
    try:
        del request.session['admin_logged_in']
    except KeyError:
        pass
    return redirect('admin_login')


def submit_exam(request):
    if request.method == 'POST':
        if 'student_id' not in request.session:
            return redirect('login')

        student_id = request.session.get('student_id')
        student_obj = student.objects.get(id=student_id)

        questions = Question.objects.all()
        total_questions = questions.count()
        correct_count = 0

        for question in questions:
            submitted_answer = request.POST.get(f'q{question.id}')  # Match HTML input name="q{{ q.id }}"
            if submitted_answer and submitted_answer.strip() == question.correct_answer.strip():
                correct_count += 1

        final_score = correct_count

        # Save the result in DB
        Result.objects.create(
            student=student_obj,
            score=final_score,
            total_questions=total_questions,
            correct_answers=correct_count
        )

        return render(request, 'result.html', {
            'score': final_score,
            'total': total_questions,
            'correct': correct_count
        })

    return redirect('dashboard')


def view_results(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    results = Result.objects.select_related('student').order_by('-date_taken')
    return render(request,'view_results.html', {'results': results})


otp_storage = {}

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = student.objects.get(Email=email)
            otp = str(random.randint(100000, 999999))
            otp_storage[email] = otp

            send_mail(
                subject="Your OTP for Password Reset",
                message=f"Your OTP is: {otp}",
                from_email="youremail@example.com",  # replace with your Gmail
                recipient_list=[email],
                fail_silently=False,
            )
            return redirect('reset_password', email=email)

        except student.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': "Email not registered."})

    return render(request, 'forgot_password.html')


def reset_password(request, email):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        new_password = request.POST.get('new_password')

        if otp_input == otp_storage.get(email):
            user = student.objects.get(Email=email)
            user.Password = new_password
            user.save()
            del otp_storage[email]
            return redirect('login')
        else:
            return render(request, 'reset_password.html', {'error': 'Invalid OTP', 'email': email})

    return render(request, 'reset_password.html', {'email': email})



def download_results_pdf(request):
    results = Result.objects.all()  # Fetch result data
    template_path = 'result_pdf.html'
    context = {'results': results}

    # Render template to HTML
    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="exam_results.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error while generating PDF')
    return response




def download_excel(request):
    # Create a workbook and add a worksheet.
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Exam Results'

    # Header row
    headers = ['Student Name', 'Email', 'Score', 'Correct Answers', 'Total Questions', 'Date']
    sheet.append(headers)

    # Data rows
    results = Result.objects.select_related('student').all()
    for result in results:
        sheet.append([
            result.student.Name,
            result.student.Email,
            result.score,
            result.correct_answers,
            result.total_questions,
            result.date_taken.strftime('%Y-%m-%d %H:%M'),
        ])

    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=exam_results.xlsx'
    workbook.save(response)
    return response





