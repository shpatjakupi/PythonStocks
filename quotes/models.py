from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10)

    def __self__(self):
        return self.ticker
