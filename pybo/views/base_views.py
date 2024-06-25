from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ..models import Question, Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from pybo.decorators import render_with_common, log_time
from django.core.cache import cache
from django.conf import settings
import redis
from ..cache_functions import save_dict_to_redis_as_string, get_dict_from_redis_string, get_element_from_redis_dict, add_to_redis_dict
import pickle

redis_client = redis.StrictRedis.from_url(settings.CACHES["default"]["LOCATION"])
# Create your views here.
def cache_page(page_obj, key):
    serialized_page = pickle.dumps(page_obj)
    redis_client.set(key, serialized_page)

def get_cached_page(key):
    serialized_page = redis_client.get(key)
    if serialized_page:
        return pickle.loads(serialized_page)
    return None

@log_time
@render_with_common
def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    # redis_client.delete('index')
    # redis_client.delete('page_1')
    if not kw:
        cached_question_list = get_element_from_redis_dict("index", page)

        question_page_ids = cached_question_list
        page_object = get_cached_page(f"page_{page}")
    if kw or not cached_question_list:
        if kw:
            question_list = Question.objects.order_by('-create_date')
            question_list = question_list.filter(
                Q(subject__icontains=kw) |
                Q(content__icontains=kw) |
                Q(answer__content__icontains=kw) |
                Q(author__username__icontains=kw) |
                Q(answer__author__username__icontains=kw)
            ).distinct()
        else:
            question_list = Question.objects.only('id').order_by('-create_date')
        print(f">> 쿼리: {question_list.query}")

        paginator = Paginator(question_list, 10)

        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)
        print(f">> typeof page_object: {type(page_object)}")
        if not kw:
            question_page_ids = [q.id for q in page_object.object_list]
            add_to_redis_dict("index", page, question_page_ids)
            cache_page(page_object, f"page_{page}")
    else:
        print("using cache")

    questions = Question.objects.filter(id__in=question_page_ids).select_related('author').prefetch_related('answer_set').order_by('-create_date')
    print(f">> 쿼리: {questions.query}")
    context = {'pagination': page_object, 'question_list': questions, 'page': page, 'kw' : kw}

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
