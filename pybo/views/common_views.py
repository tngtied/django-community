from functools import wraps
from ..models import Category
from django.shortcuts import render

def render_with_common(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        request_data = func(request, *args, **kwargs)
        additional_data = {'category_list': Category.objects.all()}
        request_data['context'].update(additional_data)
        return render(request, request_data['template'], request_data['context'])
    return wrapper