from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question, Category
from ..forms import QuestionForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_views import render_with_common
from django.db import transaction
import redis
from django.conf import settings
from django.core.cache import cache

# Redis 연결 설정
redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

@render_with_common
@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            # print(">>", form.cleaned_data['category'])
            question.category = form.cleaned_data['category']
            # question.category = Category.objects.get(pk = form.cleaned_data['category'])
            question.save()
            redis_client.rpush('index', question.id)
            redis_client.expire('index', 60)
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return {'context': context, 'template': 'pybo/question_form.html'}
@render_with_common
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('pybo:detail', question_id=question_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return {'context': context, 'template': 'pybo/question_form.html'}
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('pybo:detail', question_id=question_id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question_id)

@transaction.atomic
@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        question = get_object_or_404(Question, pk=question_id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            question.comment.add(comment)
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context=context)