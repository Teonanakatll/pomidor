from django.db import models


class Category(models.Model):
    name = models.CharField('Категория',max_length=100, db_index=True)

    def __str__(self):
        return self.name

class Women(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    content = models.TextField('Контент', blank=True)
    created = models.DateTimeField('Время создания', auto_now_add=True)
    updated = models.DateTimeField('Время изменения', auto_now=True)
    is_published = models.BooleanField('Опубликованно', default=True)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

