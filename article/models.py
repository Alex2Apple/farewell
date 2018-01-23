from django.db import models
from django.utils.html import format_html
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from accessor.models import Accessor

import time

class Category(models.Model):
    category_name = models.CharField(max_length = 20)
    category_desc = models.TextField(max_length = 100)
    last_updated = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.category_name
        
    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'

class Article(models.Model):
    PUB_STATE = 10
    DRAFT_STATE = 11
    HIDEN_STATE = 12

    ARTICLES_STATES = (
        (PUB_STATE, '已发布'),
        (DRAFT_STATE, '草稿'),
        (HIDEN_STATE, '隐藏'),
    )

    title = models.CharField("标题", max_length = 30)
    subhead = models.CharField("副标题", max_length = 50)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, verbose_name = "分类", null = True)
    tags = models.CharField("标签", max_length = 30)
    read_count = models.PositiveIntegerField("阅读量", default = 2)
    pub_date = models.DateTimeField("发布时间", auto_now_add = True)
    last_updated = models.DateTimeField("最后更新时间", auto_now = True)
    summary = RichTextField(config_name='custom', verbose_name = '摘要', default = '')
    context = RichTextUploadingField(config_name='default', verbose_name = '正文')
    state = models.PositiveSmallIntegerField(
        verbose_name = '状态',
        choices = ARTICLES_STATES, 
        default = PUB_STATE,
    )
    
    def __str__(self):
        return self.title
    
    def is_published(self):
        return self.state == self.PUB_STATE
        
    def is_hiden(self):
        return self.state == self.HIDEN_STATE
        
    def is_draft(self):
        return self.state == self.DRAFT_STATE
    
    def color_state(self):
        if self.is_published:
            color = 'green'
        elif self.is_hiden:
            color = 'red'
        else:
            color = 'gray'
        
        state_desc = '草稿'
        for s in self.ARTICLES_STATES:
            if s[0] == self.state:
                state_desc = s[1]
        
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            state_desc
        )
    color_state.short_description = '状态'
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
    
class ArticleComment(models.Model):
    STATE_SHOW = False
    STATE_HIDEN = True
    
    COMMENT_STATE = (
        (STATE_SHOW, '显示'),
        (STATE_HIDEN, '隐藏'),
    )
    
    TYPE_ACK_ARTICLE = 1
    TYPE_ACK_COMMENT = 2

    article = models.ForeignKey(Article, on_delete = models.CASCADE, editable = False)
    state = models.BooleanField(
        choices = COMMENT_STATE,
        default = STATE_HIDEN,
    )
    comment = models.TextField("评论正文")
    comment_type = models.PositiveSmallIntegerField(editable = False, default = TYPE_ACK_ARTICLE)
    parent_id = models.IntegerField(default = 0, editable = False)
    pub_time = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(Accessor)
    
    def __str__(self):
        return str(self.id)
    
    def is_show(self):
        return self.state == self.STATE_SHOW
        
    def is_hiden(self):
        return self.state == self.STATE_HIDEN
        
    def is_ack_article(self):
        return self.comment_type == self.TYPE_ACK_ARTICLE
        
    def is_ack_comment(self):
        return self.comment_type == self.TYPE_ACK_COMMENT
        
    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = '文章评论'    
    
    @classmethod
    def create_comment(cls, article, comment, parent_id, user):
        co = cls(article = article, comment = comment, parent_id = parent_id, user = user)
        co.save()
        return co
        
