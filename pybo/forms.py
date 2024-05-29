from django import forms
from pybo.models import Question, Answer, Comment, Category


class QuestionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='카테고리 선택')
    class Meta:
        model = Question
        fields = ['subject', 'content', 'category']
        labels = {
            'subject': '제목',
            'content': '내용',
            'category': '카테고리',
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