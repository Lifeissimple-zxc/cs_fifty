from django.contrib.auth.models import AbstractUser
from django.db import models


# misc
TITLE_CHAR_LIMIT = 228
LISTING_DESC_CHAR_LIMIT = 2000
LISTING_IMAGE_URL_CHAR_LIMIT = 1000
LISTING_STATUS_CHAR_LIMIT = 20

# Field names
LISTINGS_RELATED_NAME = "listings"
USER_RELATED_NAME = "user"


class User(AbstractUser):
    id = models.AutoField(primary_key=True)


class ListingCategory(models.Model):
    "An auction listing category"
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=TITLE_CHAR_LIMIT, unique=True)

    def __str__(self):
        return f"{self.title} category"
    
    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        super().save(*args, **kwargs)


# listing statuses
LISTING_STATUS_ACTIVE = "active"
LISTING_STATUS_INACTIVE = "inactive"

class Listing(models.Model):
    "An auction listing"
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=TITLE_CHAR_LIMIT)
    starting_bid = models.FloatField()
    description = models.CharField(max_length=LISTING_DESC_CHAR_LIMIT)
    image_url = models.CharField(max_length=LISTING_IMAGE_URL_CHAR_LIMIT)
    status = models.CharField(max_length=LISTING_STATUS_CHAR_LIMIT)
    # FKs
    category = models.ForeignKey(to=ListingCategory, on_delete=models.CASCADE, related_name=LISTINGS_RELATED_NAME)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name=USER_RELATED_NAME)

    def __str__(self):
        return f"{self.title} listing"



# TODO update the form's styling
# TODO update the site's styling overall
# TODO add an error page
# TODO add error handling on a model save

