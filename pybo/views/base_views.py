from django.core.paginator import Paginator
from ..models import Question, Comment
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .common_render import render_with_common

# Create your views here.

@render_with_common
def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    paginator = Paginator(question_list, 10)
    page_object = paginator.get_page(page)

    context = {'question_list': page_object, 'page': page, 'kw' : kw}
    return {'context': context, 'template': 'pybo/question_list.html'}
    # return render(request, 'pybo/question_list.html', context=context)

@render_with_common
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer_list = question.answer_set.all().annotate(num_voter = Count('voter')).order_by('-num_voter', '-create_date')
    
    paginator = Paginator(answer_list, 10)
    page_object = paginator.get_page(1)
    # print("page object %s" % page_object.count)

    context = {'question': question, 'answer_list': page_object}
    return {'context': context, 'template': 'pybo/question_detail.html'}

@render_with_common
def recent_comment(request):
    comment_list = Comment.objects.order_by('-create_date')
    paginator = Paginator(comment_list, 10)
    page_object = paginator.get_page(1)
    context = {'comment_list': page_object}
    return {'context': context, 'template': 'pybo/recent_comment.html'}
