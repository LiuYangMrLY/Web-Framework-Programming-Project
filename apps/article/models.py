from django.db import models


class Article(models.Model):
    author = models.ForeignKey('account.User', on_delete=models.PROTECT, verbose_name='作者')
    title = models.CharField(max_length=100, verbose_name='题目', null=False, blank=False)
    content = models.TextField(verbose_name='内容', null=False, blank=True, default='')
    clicks = models.BigIntegerField(verbose_name='点击量', null=False, blank=False, default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_edited_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.PROTECT, verbose_name='评论者')
    article = models.ForeignKey('Article', on_delete=models.PROTECT, verbose_name='文章', related_name='comments')
    content = models.TextField(verbose_name='内容', null=False, blank=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
