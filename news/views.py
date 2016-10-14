from django.shortcuts import render, get_object_or_404
from .models import Article
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, InvalidPage

def latest(request):
	template = 'news/latest.html'
	page = request.GET.get('page')
	article_list = Article.objects.order_by('-created')
	cat_list = Article.objects.values_list('article_type', flat=True).distinct()
	paginator = Paginator(article_list, 10)

	try:
		articles = paginator.page(page)
	except InvalidPage:
		# Return first page for invalid input
		articles = paginator.page(1)

	context = {
		'articles_l': articles,
		'category_l': cat_list
	}

	return render(request, template, context)

def category(request):
	template = 'news/category.html'
	query = request.GET.get('query')
	if query is None:
		return HttpResponseRedirect(reverse('news:latest'))
	articles = Article.objects.filter(article_type=query).order_by('-created')
	cat_list = Article.objects.values_list('article_type', flat=True).distinct()

	context = {
		'articles_l': articles,
		'category_l': cat_list,
		'query': query
	}

	return render(request, template, context)

def article(request, article_slug):
	template = 'news/article.html'
	article = get_object_or_404(Article, slug=article_slug)
	context = {
		"article": article,
	}
	return render(request, template, context)
