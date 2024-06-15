from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ..models import Question, Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from pybo.decorators import render_with_common, log_time

# Create your views here.

@log_time
@render_with_common
def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    question_list = Question.objects.only('id').order_by('-create_date')
    print(f">> 쿼리: {question_list.query}")
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    print(f"type(int(page)) {type(int(page))}, value {int(page)}")

    paginator = Paginator(question_list, 10)
    try:
        page_object = paginator.get_page(page)
    except PageNotAnInteger:
        page_object = paginator.get_page(1)
    except EmptyPage:
        page_object = paginator.get_page(paginator.num_pages)
    context = {'question_list': page_object, 'page': page, 'kw' : kw}
    return {'context': context, 'template': 'pybo/question_list.html'}

@log_time
@render_with_common
def detail(request, question_id):
    page = request.GET.get('page', '1')
    question = get_object_or_404(Question, pk=question_id)
    question.hits += 1
    question.save()
    answer_list = question.answer_set.all().order_by('-voter_count', '-create_date')
    print(f"query of answer_list: {answer_list.query}")
    paginator = Paginator(answer_list, 10)
    page_object = paginator.get_page(page)
    # print("page object %s" % page_object.count)

    context = {'question': question, 'answer_list': page_object}
    return {'context': context, 'template': 'pybo/question_detail.html'}

@log_time
@render_with_common
def recent_comment(request):
    comment_list = Comment.objects.order_by('-create_date')
    paginator = Paginator(comment_list, 10)
    page_object = paginator.get_page(1)
    context = {'comment_list': page_object}
    return {'context': context, 'template': 'pybo/recent_comment.html'}
