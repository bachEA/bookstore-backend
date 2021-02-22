from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author_name = models.CharField(max_length=255)
    publiser_name = models.CharField(max_length=255)
    published_date = models.DateField(
        auto_now=False, auto_now_add=False)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.CharField(max_length=255)
    image = models.ImageField(upload_to='', blank=True, null=True)
    total_rating_value = models.DecimalField(
        max_digits=2, decimal_places=1)
    total_rating_count = models.IntegerField()
    # time at creation vs time at update
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
