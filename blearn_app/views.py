from django.contrib import messages
import random
from django.shortcuts import get_object_or_404, render,redirect
# Create your views here.
from .models import*
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
import openpyxl
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from datetime import datetime, timedelta

from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


otp_storage = {}



def registration_page(request):
    return render(request,"register.html")

def register_student(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        name = request.POST.get('name', '').strip()
        phone_no = request.POST.get('phone_no', '').strip()
        qualification = request.POST.get('qualification', '').strip()
        department = request.POST.get('department', '').strip()
        college = request.POST.get('college', '').strip()
        year = request.POST.get('year', '').strip()

        # Check if any required field is empty
        if not all([email, password, confirm_password, name, phone_no, qualification, department, college, year]):
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        # Check if email already exists
        if student.objects.filter(Email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        # Check if phone number already exists
        if student.objects.filter(phone_no=phone_no).exists():
            messages.error(request, 'Phone number already registered.')
            return render(request, 'register.html')

        # Save to database
        student.objects.create(
            Email=email,
            Password=password,
            Name=name,
            phone_no=phone_no,
            qualification=qualification,
            department=department,
            college=college,
            year=year
        )

        return redirect('success')

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





def login_student(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        try:
            student_obj = student.objects.get(Email=email)
            if password == student_obj.Password:
                otp = str(random.randint(100000, 999999))

                request.session['otp_email'] = email
                request.session['otp_code'] = otp
                request.session['otp_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Send OTP via HTML email
                send_login_otp_html(student_obj.Name, email, otp)

                return redirect('verify_login_otp')
            else:
                return render(request, 'login.html', {'error': 'Invalid Password'})
        except student.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid Email'})

    return render(request, 'login.html')


def verify_login_otp(request):
    email = request.session.get('otp_email')
    stored_otp = request.session.get('otp_code')
    otp_time_str = request.session.get('otp_timestamp')

    if not email or not stored_otp or not otp_time_str:
        return redirect('login')

    otp_time = datetime.strptime(otp_time_str, '%Y-%m-%d %H:%M:%S')
    if datetime.now() > otp_time + timedelta(minutes=2):
        request.session.flush()
        return render(request, 'verify_otp.html', {'error': 'OTP expired. Please login again.'})

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == stored_otp:
            try:
                student_obj = student.objects.get(Email=email)
                request.session['student_id'] = student_obj.id
                request.session['student_name'] = student_obj.Name

                # Clear OTP session data
                request.session.pop('otp_email', None)
                request.session.pop('otp_code', None)
                request.session.pop('otp_timestamp', None)

                return redirect('dashboard')
            except student.DoesNotExist:
                return redirect('login')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html', {'email': email})


def resend_otp(request):
    email = request.session.get('otp_email')

    if not email:
        return redirect('login')

    try:
        student_obj = student.objects.get(Email=email)
    except student.DoesNotExist:
        return redirect('login')

    otp = str(random.randint(100000, 999999))
    request.session['otp_code'] = otp
    request.session['otp_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    send_login_otp_html(student_obj.Name, email, otp)

    messages.success(request, "OTP resent to your email.")
    return redirect('verify_login_otp')


# ==============================
# ✅ HTML Email Sender Function
# ==============================

def send_login_otp_html(name, email, otp):
    subject = "Your OTP for Login"
    from_email = "youremail@example.com"

    # Mask the email: show only last 4 characters
    masked_email = '*' * (len(email) - 16) + email[-16:]

    html_content = f"""
    <div style="max-width:600px; margin:auto; font-family:Arial, sans-serif; border:1px solid #ddd; padding:20px; border-radius:10px;">
        <div style="text-align:center;">
        </div>
        <h3 style="text-align:center; color:#333;">Hello {name},</h3>
        <p style="font-size:16px;">We received a request to log in to your BLEARN ACADEMY Exam Portal account using email verification.</p>
        <p style="font-size:18px;">Your OTP for contact details verification is:</p>
        <div style="text-align:center; margin:20px 0;">
            <span style="font-size:24px; font-weight:bold; background-color:#f0f0f0; padding:10px 20px; border-radius:5px; display:inline-block;">{otp}</span>
        </div>
        <p style="font-size:15px;">
            This OTP is valid for <strong>2 minutes</strong>.<br>
            Use this OTP along with the OTP sent to your registered <strong>{masked_email}</strong> to verify your contact details.
        </p>
        <p style="color:#a00;"><strong>Please do not share this OTP with anyone.</strong></p>
        <hr>
        <p style="font-size:13px; color:gray;">
            This is a system generated e-mail. Please do not reply.
        </p>
        <div style="text-align:center; margin-top:15px;">
            <small style="color:gray;">© 2025 BLEARN ACADEMY, India.</small>
        </div>
    </div>
    """

    plain_message = strip_tags(html_content)

    email_message = EmailMultiAlternatives(subject, plain_message, from_email, [email])
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()





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
        if username == 'Superadmin.Blearn' and password == 'Blearn#Admin@442288':
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


# def submit_exam(request):
#     if request.method == 'POST':
#         if 'student_id' not in request.session:
#             return redirect('login')

#         student_id = request.session.get('student_id')
#         student_obj = student.objects.get(id=student_id)

#         questions = Question.objects.all()
#         total_questions = questions.count()
#         correct_count = 0

#         for question in questions:
#             submitted_answer = request.POST.get(f'q{question.id}')  # Match HTML input name="q{{ q.id }}"
#             if submitted_answer and submitted_answer.strip() == question.correct_answer.strip():
#                 correct_count += 1

#         final_score = correct_count

#         # Save the result in DB
#         result = Result.objects.create(
#         student=student_obj,
#         score=final_score,
#         total_questions=total_questions,
#         correct_answers=correct_count
#         )

#         video_file = request.FILES.get('video')
#         if video_file:
#             ExamRecording.objects.create(student=student_obj, result=result, video=video_file)



#         return JsonResponse({'status': 'success'})
#         return render(request, 'result.html', {
#             'score': final_score,
#             'total': total_questions,
#             'correct': correct_count
#         })
        
        
        

#     return redirect('dashboard')








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
            submitted_answer = request.POST.get(f'q{question.id}')
            if submitted_answer and submitted_answer.strip() == question.correct_answer.strip():
                correct_count += 1

        final_score = correct_count

        # Save the result in DB
        result = Result.objects.create(
            student=student_obj,
            score=final_score,
            total_questions=total_questions,
            correct_answers=correct_count
        )

        # Save video (uploaded in the same form)
        video_file = request.FILES.get('video')
        if video_file:
            ExamRecording.objects.create(student=student_obj, result=result, video=video_file)

        return render(request,'result.html')  
    return redirect('dashboard')



def view_results(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    results = Result.objects.select_related('student').order_by('-date_taken')
    return render(request, 'view_results.html', {'results': results})



def send_html_otp_email(email, otp):
    subject = "Your OTP for Password Reset"
    html_content = render_to_string("otp_email.html", {"otp": otp})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, "youremail@example.com", [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = student.objects.get(Email=email)
            otp = str(random.randint(100000, 999999))
            expiry = datetime.now() + timedelta(minutes=2)
            otp_storage[email] = {'otp': otp, 'expires': expiry}

            send_html_otp_email(email, otp)
            return redirect('reset_password', email=email)

        except student.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': "Email not registered."})

    return render(request, 'forgot_password.html')

# Reset password: validate OTP and change password
def reset_password(request, email):
    otp_info = otp_storage.get(email)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        new_password = request.POST.get('new_password')

        if not otp_info or datetime.now() > otp_info['expires']:
            return render(request, 'reset_password.html', {
                'error': 'OTP expired. Please resend.',
                'email': email,
                'expired': True
            })

        if otp_input == otp_info['otp']:
            user = student.objects.get(Email=email)
            user.Password = new_password
            user.save()
            del otp_storage[email]
            return redirect('login')
        else:
            return render(request, 'reset_password.html', {
                'error': 'Invalid OTP.',
                'email': email
            })

    return render(request, 'reset_password.html', {'email': email})

# Resend OTP if expired
def resend_otp_password(request, email):
    try:
        user = student.objects.get(Email=email)
        otp = str(random.randint(100000, 999999))
        expiry = datetime.now() + timedelta(minutes=2)
        otp_storage[email] = {'otp': otp, 'expires': expiry}

        send_html_otp_email(email, otp)
        return redirect('reset_password', email=email)

    except student.DoesNotExist:
        return redirect('forgot_password')


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


def search_results(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    query = request.GET.get('query', '')
    results = Result.objects.select_related('student').all()

    if query:
        results = results.filter(
            Q(student__Name__icontains=query) |
            Q(student__Email__icontains=query) |
            Q(student__phone_no__icontains=query)
        )

    return render(request, 'view_results.html', {'results': results})





def delete_result(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    result = get_object_or_404(Result, id=id)

    # Also delete associated video if any
    recordings = ExamRecording.objects.filter(result=result)
    for rec in recordings:
        if rec.video:
            rec.video.delete()
        rec.delete()


    result.delete()
    return redirect('view_results')





@csrf_exempt
def save_recording(request):
    if request.method == 'POST' and request.FILES.get('recording'):
        if 'student_id' not in request.session:
            return JsonResponse({'error': 'Not authenticated'}, status=403)

        student_id = request.session['student_id']
        student_obj = student.objects.get(id=student_id)
        video_file = request.FILES['recording']

        ExamRecording.objects.create(
            student=student_obj,
            video=video_file
        )

        return JsonResponse({'message': 'Recording saved successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)





def view_students(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    students = student.objects.all()
    return render(request, 'view_students.html', {'students': students})


def delete_student(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    student_obj = student.objects.get(id=id)
    student_obj.delete()
    return redirect('view_students')


def clear_students(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    student.objects.all().delete()
    return redirect('view_students')


def edit_student(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    try:
        student_obj = student.objects.get(id=id)
    except student.DoesNotExist:
        return redirect('view_students')

    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ]

    if request.method == 'POST':
        student_obj.Name = request.POST.get('name')
        student_obj.Email = request.POST.get('email')
        student_obj.phone_no = request.POST.get('phone_no')
        student_obj.qualification = request.POST.get('qualification')
        student_obj.department = request.POST.get('department')
        student_obj.college = request.POST.get('college')
        student_obj.year = request.POST.get('year')
        student_obj.Password = request.POST.get('password')  # 🔐 Add password update
        student_obj.save()
        return redirect('view_students')

    return render(request, 'edit_student.html', {
        'student': student_obj,
        'year_choices': YEAR_CHOICES
    })





def download_students_pdf(request):
    students = student.objects.all()
    template_path = 'students_pdf.html'
    context = {'students': students}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('PDF generation failed.')
    return response


def download_students_excel(request):
    students = student.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Students"

    # Header
    ws.append(['Name', 'Email', 'Phone', 'Qualification', 'Department', 'College', 'Year'])

    # Data rows
    for stu in students:
        ws.append([
            stu.Name, stu.Email, stu.phone_no,
            stu.qualification, stu.department, stu.college, stu.year
        ])

    # Response
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'
    wb.save(response)
    return response












from .decorators import time_restricted  # adjust path if needed

@time_restricted(start_hour=2, start_minute=0, end_hour=3, end_minute=0)
def student_login_page(request):
    return render(request, 'login.html')
