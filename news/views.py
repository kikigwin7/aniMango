from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render, get_object_or_404

from .models import Article


def latest(request, category, page):
    if category == 'All':
        articles = Article.objects.order_by('-created')
    else:
        articles = Article.objects.filter(article_type=category).order_by('-created')

    paginator = Paginator(articles, 10)
    try:
        articles = paginator.page(page)
    except InvalidPage:
        articles = paginator.page(1)

    context = {
        'articles_l': articles,
        'category': category
    }
    return render(request, 'news/latest.html', context)


def article(request, article_id, article_slug):
    context = {
        "article": get_object_or_404(Article, id=article_id),
    }
    return render(request, 'news/article.html', context)
