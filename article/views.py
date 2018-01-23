from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.http import Http404

from .models import *
from .forms import CommentForm
from accessor.models import Accessor


def index(request):
    latest_article_list = Article.objects.order_by('-pub_date')[:7]
    template = loader.get_template('articles/index.html')
    context = {
        'latest_article_list': latest_article_list,
        'archive_list': get_archives()
    }
    return HttpResponse(template.render(context, request))
    
def detail(request, article_id):
    try:
        article = Article.objects.get(pk = article_id)
        form = CommentForm()
        comment_list = ArticleComment.objects.filter(article = article).order_by('-pub_time')[:10]
        previous_articles = Article.objects.filter(pub_date__gt = article.pub_date).order_by('pub_date')[:1]
        next_articles = Article.objects.filter(pub_date__lt = article.pub_date).order_by('-pub_date')[:1]
    except:
        raise Http404('迷路了, 招贴寻人启事')
        
    data = {
            'article' : article, 
            'form': form, 
            'comment_list' : comment_list, 
            'archive_list': get_archives(),
        }
    
    if len(previous_articles) > 0:
        data['previous_article'] = previous_articles[0]
        
    if len(next_articles) > 0:
        data['next_article'] = next_articles[0]
    
    return render(request, 'articles/detail.html', data)

def archive(request, year, month):
    begin_date = datetime.strptime('%s-%s-%s' % (year, month, '01'), '%Y-%m-%d')
    end_date = begin_date + relativedelta(months = +1)
    article_list = Article.objects.filter(pub_date__gte = begin_date).filter(pub_date__lt = end_date).order_by('-pub_date')[:7]
    template = loader.get_template('articles/index.html')
    context = {
        'latest_article_list': article_list,
        'archive_list': get_archives()
    }
    return HttpResponse(template.render(context, request))
    
def post_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            article_id = form.cleaned_data['article_id']
            article = Article.objects.get(pk = article_id)
            user = Accessor.objects.get(email = form.cleaned_data['email'])
            article_comment = ArticleComment.create_comment(article, form.cleaned_data['comment'], form.cleaned_data['comment_parent_id'], user)
            article_comment.save()
            return redirect('/article/%s/' % article_id)
    return HttpResponse(form.errors.as_data())
    
def get_archives():
    from django.db.models.functions import TruncMonth
    from django.db.models import Count
    archive_list = Article.objects.annotate(month = TruncMonth('pub_date')).values('month').annotate(c = Count('id')).values('month', 'c')
    r = []
    for archive in archive_list:
        r.append(("%s年%s月" % (archive['month'].year, archive['month'].month), archive['month'].year, archive['month'].month, archive['c']))
    return r