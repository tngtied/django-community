from django import forms
from pybo.models import Question, Answer, Comment, Category

category_choice = [ (category.id, category.name) for category in Category.objects.all() ]
class QuestionForm(forms.ModelForm):
    # category = forms.ChoiceField(choices=category_choice)
    class Meta:
        model = Question
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer 
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }