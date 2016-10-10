from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Board, Thread, Post
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

def index(request):
	template = 'forum/index.html'
	boards = Board.objects.all()
	context = {
		'board_list': boards
	}
	return render(request, template, context)

def board(request, board_id):
	template = 'forum/board.html'
	board = get_object_or_404(Board, id=board_id)
	threads = Thread.objects.filter(parent_board=board)
	context = {
		'board': board,
		'thread_list': threads
	}
	return render(request, template, context)

def thread(request, thread_id):
	template = 'forum/thread.html'
	thread = get_object_or_404(Thread, id=thread_id)
	posts = Post.objects.filter(parent_thread=thread)

	# Change the content of the instance of a post if it is marked as deleted
	for post in posts:
		if post.deleted:
			post.content = '[POST DELETED]'

	context = {
		'thread': thread,
		'post_list': posts
	}
	return render(request, template, context)

def new(request, board_id):
	redir_url = reverse('forum:board', args=[board_id])
	if request.method == 'POST':
		if not request.user.is_authenticated():
			messages.error(request, 'You must be logged in to use the forum')
			return HttpResponseRedirect(redir_url)
		else:
			try:
				new_thread = Thread()
				new_thread.title = request.POST['title']
				new_thread.content = request.POST['content']
				new_thread.created = timezone.localtime(timezone.now())
				new_thread.parent_board = Board.objects.get(id=board_id)
				new_thread.thread_user = request.user.member
				new_thread.save()
				new_thread_url = reverse('forum:thread', args=[new_thread.id])
				messages.error(request, 'Thread created')
				return HttpResponseRedirect(new_thread_url)
			except ObjectDoesNotExist:
				messages.error(request, 'Board does not exist')
				return HttpResponseRedirect(redir_url)
	else:
		return HttpResponseRedirect(redir_url)

def reply(request, thread_id):
	redir_url = reverse('forum:thread', args=[thread_id])
	if request.method == 'POST':
		if not request.user.is_authenticated():
			messages.error(request, 'You must be logged in to use the forum')
			return HttpResponseRedirect(redir_url)
		else:
			try:
				new_post = Post()
				new_post.content = request.POST['reply_text']
				new_post.post_user = request.user.member
				new_post.parent_thread = Thread.objects.get(id=thread_id)
				new_post.created = timezone.localtime(timezone.now())
				new_post.save()
				messages.error(request, 'Reply posted')
				return HttpResponseRedirect(redir_url)
			except ObjectDoesNotExist:
				messages.error(request, 'Thread does not exist')
				return HttpResponseRedirect(redir_url)
	else:
		return HttpResponseRedirect(redir_url)