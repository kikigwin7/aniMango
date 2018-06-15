from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Board, Thread, Post

def index(request):
	context = {
		'board_list': Board.objects.order_by('order')
	}
	return render(request, 'forum/index.html', context)

def board(request, board_id):
	board = get_object_or_404(Board, id=board_id)
	threads = Thread.objects.filter(parent_board=board).order_by('-last_reply_time')
	context = {
		'board': board,
		'thread_list': threads
	}
	return render(request, 'forum/board.html', context)

def thread(request, thread_id):
	thread = get_object_or_404(Thread, id=thread_id)
	posts = Post.objects.filter(parent_thread=thread).order_by('created')
	context = {
		'thread': thread,
		'post_list': posts
	}
	return render(request, 'forum/thread.html', context)

@login_required
def new(request, board_id):
	board = get_object_or_404(Board, id=board_id)
	if request.method == 'POST':
		try:
			new_thread = create_thread(board, request.POST.get('title'), request.user.member)
			new_post = create_post(new_thread, request.POST.get('content'), request.user.member)
			messages.success(request, 'Thread created')
			return HttpResponseRedirect(reverse('forum:thread', args=[new_thread.id]))
		except Exception as e:
			messages.error(request, 'An error occured')
	return HttpResponseRedirect(reverse('forum:board', args=[board_id]))

@login_required
def reply(request, thread_id):
	thread = get_object_or_404(Thread, id=thread_id)
	if request.method == 'POST':
		try:
			new_post = create_post(thread, request.POST.get('reply_text'), request.user.member)
			messages.success(request, 'Reply posted')
		except Exception as e:
			messages.error(request, 'An error occured')
	return HttpResponseRedirect(reverse('forum:thread', args=[thread_id]))
		
@login_required
def edit(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	thread = post.parent_thread
	if not request.user.member == post.post_user:
		messages.error(request, 'This post does not belong to you')
	elif request.method == 'POST':
		try:
			post.edit(request.POST.get('reply_text'))
			messages.success(request, 'Edit succeeded')
		except Exception as e:
			messages.error(request, 'An error occured')
	return HttpResponseRedirect(reverse('forum:thread', args=[post.parent_thread.id]))
		
def create_thread(board, title, member):
	if board.locked:
		raise Warning('Board is locked')
	new_thread = Thread()
	new_thread.title = title
	new_thread.created = timezone.now()
	new_thread.last_reply_time = timezone.now()
	new_thread.parent_board = board
	new_thread.thread_user = member
	new_thread.save()
	return new_thread
	
def create_post(thread, content, member):
	if thread.locked:
		raise Warning('Thread is locked')
	new_post = Post()
	new_post.content = content
	new_post.post_user = member
	new_post.parent_thread = thread
	new_post.created = timezone.now()
	new_post.save()
	thread.last_reply_now()
	return new_post
