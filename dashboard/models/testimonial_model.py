from django.db import models
from dashboard.models.base_model import Base
from dashboard.models.user_model import CustomUser

class Testimonial(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='testimonial')
    rating = models.PositiveIntegerField(default=5)
    content = models.TextField()
    author_name = models.CharField(max_length=255)
    author_title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Depoimento"
        verbose_name_plural = "Depoimentos"
        indexes = [
                models.Index(fields=['author_name']),
            ]

    def __str__(self):
        return self.author_name


          