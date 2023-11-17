from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    img = models.ImageField(upload_to='blog_img/', verbose_name='изображение', **NULLABLE)
    date = models.DateField(verbose_name='дата создания', **NULLABLE)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'запись в блоге'
        verbose_name_plural = 'записи в блоге'