from django.contrib.auth.models import User
from django.db import models
import uuid


class BaseModal(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True 


class Blog(BaseModal):
    blog_author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='blogs')
    blog_title = models.CharField(max_length=500)
    blog_text = models.TextField()
    blog_image = models.ImageField(upload_to="blogs")
    
    def __str__(self) -> str:
        return self.blog_title[:30]