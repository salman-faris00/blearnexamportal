from django.db import models

# Create your models here.

class student(models.Model):
    Email = models.CharField(max_length=50, unique=True)
    Password = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    phone_no = models.BigIntegerField(unique=True)
    qualification = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    college = models.CharField(max_length=100)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)

    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
        ('Graduated', 'Graduated'),
        ('Not Completed', 'Not Completed'),
    ]
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, null=True)

    

    COURSE_CHOICES = [
        ('Data Science', 'Data Science'),
        ('Data Analytics', 'Data Analytics'),
        ('Cloud Computing', 'Cloud Computing'),
        ('Cyber Security', 'Cyber Security'),
        ('Networking', 'Networking'),
        ('Python Fullstack', 'Python Fullstack'),
        ('MERN Stack', 'MERN Stack'),
        ('Java Fullstack', 'Java Fullstack'),
        ('Flutter', 'Flutter'),
        ('Software Testing', 'Software Testing'),
        ('DevOps', 'DevOps'),
        ('Other', 'Other'),
    ]
    interested_course = models.CharField(max_length=50, choices=COURSE_CHOICES, null=True)

    def __str__(self):
        return self.Name


class Question(models.Model):
    question_text = models.CharField(max_length=300)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question_text


class Result(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.Name} - {self.score}"


class ExamRecording(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    video = models.FileField(upload_to='recordings/')
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.ForeignKey(Result, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.student.Name} - {self.timestamp}"
