from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Listing(models.Model):
    Categories = [
    ("fashion", "Fashion"),
    ("music", "Music"),
    ("electronics", "Electronics"),
    ("toys", "Toys"),

]
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=64,blank=True)
    description = models.TextField(blank=True)
    starting_bid = models.IntegerField()
    image_url = models.CharField(max_length=200,blank=True)
    category = models.CharField(max_length=64,choices=Categories,default="fashion")
    
    def __str__(self) -> str:
        return f"{self.title}"
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True,null=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2,null=True)

    def __str__(self) -> str:
        return f"{self.user } bid {self.price} on {self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    comment_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self) -> str:
        return f"{self.comment} on {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='watchlist')
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}'s watchlist"

