# Generated by Django 5.2 on 2025-05-13 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("blearn_app", "0006_delete_question_delete_result_delete_student"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question_text", models.CharField(max_length=300)),
                ("option1", models.CharField(max_length=100)),
                ("option2", models.CharField(max_length=100)),
                ("option3", models.CharField(max_length=100)),
                ("option4", models.CharField(max_length=100)),
                ("correct_answer", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Email", models.CharField(max_length=50, unique=True)),
                ("Password", models.CharField(max_length=50)),
                ("Name", models.CharField(max_length=50)),
                ("phone_no", models.BigIntegerField(default=100)),
                ("qualification", models.CharField(max_length=50)),
                ("department", models.CharField(max_length=100)),
                ("college", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.IntegerField()),
                ("total_questions", models.IntegerField()),
                ("correct_answers", models.IntegerField()),
                ("date_taken", models.DateTimeField(auto_now_add=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blearn_app.student",
                    ),
                ),
            ],
        ),
    ]
