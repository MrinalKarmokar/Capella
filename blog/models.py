from django.db import models

# Create your models here.

class blogPost(models.Model):
    title = models.CharField(max_length=200, null=True)
    desc1 = models.TextField(null=True)
    desc2 = models.TextField(null=True, blank=True)
    link = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True ,null=True)

    def __str__(self):
            return f"{self.title}"