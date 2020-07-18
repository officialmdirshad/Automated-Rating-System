from django.db import models


# Customer Model
class Sentiment(models.Model):
    review = models.CharField(max_length=150)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.review