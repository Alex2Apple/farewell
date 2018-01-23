from django.template import loader
from django.http import HttpResponse

from article.models import Article


def home(request):
    latest_article_list = Article.objects.order_by('-pub_date')[:7]
    template = loader.get_template('articles/home.html')
    context = {
        'latest_article_list': latest_article_list,
        'archive_list': get_archives()
    }
    return HttpResponse(template.render(context, request))
    
def get_archives():
    from django.db.models.functions import TruncMonth
    from django.db.models import Count
    archive_list = Article.objects.annotate(month = TruncMonth('pub_date')).values('month').annotate(c = Count('id')).values('month', 'c')
    r = []
    for archive in archive_list:
        r.append(("%s年%s月" % (archive['month'].year, archive['month'].month), archive['month'].year, archive['month'].month, archive['c']))
    return r