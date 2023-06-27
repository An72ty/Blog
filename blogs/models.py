from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    """Пост в блоге."""
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.title
    

class Comment(models.Model):
    """Комментарий под постом."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text