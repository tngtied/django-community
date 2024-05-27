from django.core.paginator import Paginator
from ..models import Question
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

# Create your views here.

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

    context = {'question_list': page_object, 'page' : page, 'kw' : kw}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer_list = question.answer_set.all().annotate(num_voter = Count('voter')).order_by('-num_voter', '-create_date')
    print(answer_list)
    paginator = Paginator(answer_list, 10)
    page_object = paginator.get_page(1)
    # print("page object %s" % page_object.count)

    context = {'question': question, 'answer_list': page_object}
    return render(request, 'pybo/question_detail.html', context)