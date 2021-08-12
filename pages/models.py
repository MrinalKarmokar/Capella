from django.db import models

# Create your models here.

# class cardDataHome(models.Model):
#     image_url = models.ImageField(upload_to='pages/images', default="")
#     title = models.CharField(max_length=50, blank=False, null=False)
#     desc = models.CharField(max_length=50, blank=False, null=False)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#          return self.title


# class carouselDataHome(models.Model):
#     image_url = models.ImageField(upload_to='pages/images', default="")
#     title = models.CharField(max_length=50, blank=False, null=False)
#     desc = models.CharField(max_length=50, blank=False, null=False)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#          return self.title


# class scrollCarouselLoop(models.Model):
#     image_url1 = models.ImageField(upload_to='pages/images', default="")
#     image_url2 = models.ImageField(upload_to='pages/images', default="")
#     image_url3 = models.ImageField(upload_to='pages/images', default="")
#     image_url4 = models.ImageField(upload_to='pages/images', default="")
#     image_url5 = models.ImageField(upload_to='pages/images', default="")
#     title = models.CharField(max_length=50, blank=False, null=False)
#     desc = models.CharField(max_length=50, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#          return self.title