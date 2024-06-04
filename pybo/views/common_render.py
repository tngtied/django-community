from functools import wraps
from ..models import Category, Answer, Comment
from django.shortcuts import render

def render_with_common(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        print(">>function: ", func.__name__)
        request_data = func(request, *args, **kwargs)
        print(">>request_data: ", request_data)
        if isinstance(request_data, dict):
            recent_answers = Answer.objects.order_by('-create_date')[:5]
            recent_comments = Comment.objects.order_by('-create_date')[:5]
            additional_data = {'category_list': Category.objects.all(), 'recent_answers': recent_answers, 'recent_comments': recent_comments}
            request_data['context'].update(additional_data)
            return render(request, request_data['template'], request_data['context'])
        return request_data
    return wrapper