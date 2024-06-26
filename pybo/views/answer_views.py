from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..models import Question, Answer
from ..forms import AnswerForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_views import render_with_common
from django.core.paginator import Paginator

@render_with_common
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))

    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context=context)

@render_with_common
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
    resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context=context)

@render_with_common
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@render_with_common
@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 답변은 추천할 수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
    resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

@render_with_common
@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            answer.comment.add(comment)
            answer.save()
            return redirect('{}#comment_{}'.format(
    resolve_url('pybo:detail', question_id=answer.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'answer': answer, 'form': form}
    return {'context': context, 'template': 'pybo/answer_detail.html'}

@render_with_common
def recent_answer(request):
    answer_list = Answer.objects.order_by('-create_date')
    paginator = Paginator(answer_list, 10)
    page_object = paginator.get_page(1)
    context = {'answer_list': page_object}
    return {'context': context, 'template': 'pybo/recent_answer.html'}
