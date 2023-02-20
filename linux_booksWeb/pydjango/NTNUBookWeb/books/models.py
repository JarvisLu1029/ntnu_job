from django.db import models

# Create your models here.
# class Test(models.Model):
#     name = models.CharField(max_length=20)

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    published_year = models.IntegerField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_books_info'