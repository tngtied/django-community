from functools import wraps
from pybo.models import Category, Answer, Comment
from django.shortcuts import render
import time

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f'[{start_time}] {func.__name__} 함수가 호출되었습니다.')
        request_data = func(*args, **kwargs)
        end_time = time.time()
        print(f'[{end_time}] {func.__name__} 함수가 종료되었습니다. 수행시간: {end_time - start_time}')
        return request_data
    return wrapper

def render_with_common(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        request_data = func(request, *args, **kwargs)
        if isinstance(request_data, dict):
            recent_answers = Answer.objects.order_by('-create_date')[:5]
            recent_comments = Comment.objects.order_by('-create_date')[:5]
            additional_data = {'category_list': Category.objects.all(), 'recent_answers': recent_answers, 'recent_comments': recent_comments}
            request_data['context'].update(additional_data)
            return render(request, request_data['template'], request_data['context'])
        return request_data
    return wrapper