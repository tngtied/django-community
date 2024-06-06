from django.test import TestCase
from pybo.models import Question
from django.utils import timezone
from django.contrib.auth.models import User
# Create your tests here.
class QuestionTest(TestCase):
    def setUp(self):
        self.author_instance = User.objects.create(
            username='testuser',
            password='1234',
            email = 'email@gmail.com'
        )
        self.question_instance = Question.objects.create(
            subject='test subject',
            content='test content',
            author = self.author_instance,
            create_date=timezone.now()
        )

    def test_index(self):
        response = self.client.get('/pybo/')
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.get('/pybo/1/')
        self.assertEqual(response.status_code, 200)