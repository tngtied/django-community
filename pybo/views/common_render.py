from functools import wraps
from ..models import Category
from django.shortcuts import render

def render_with_common(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        print(">>function: ", func.__name__)
        request_data = func(request, *args, **kwargs)
        print(">>request_data: ", request_data)
        if isinstance(request_data, dict):
            additional_data = {'category_list': Category.objects.all()}
            request_data['context'].update(additional_data)
            return render(request, request_data['template'], request_data['context'])
        return request_data
    return wrapper