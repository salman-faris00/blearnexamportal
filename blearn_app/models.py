from django.db import models

# Create your models here.


class student(models.Model):
    Email=models.CharField(max_length=50,unique=True)
    Password=models.CharField(max_length=50)
    Name=models.CharField(max_length=50)
    phone_no=models.BigIntegerField(default=100)
    qualification=models.CharField(max_length=50)
    department=models.CharField(max_length=100)
    college=models.CharField(max_length=100)
    
class Question(models.Model):
    question_text = models.CharField(max_length=300)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)
    
    
class Result(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)
    
    