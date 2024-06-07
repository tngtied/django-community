from django.test import TestCase
from pybo.models import Question
from django.utils import timezone
from django.contrib.auth.models import User
from ..decorators import log_time

# Create your tests here.
class QuestionTest(TestCase):

    @log_time
    def setUp(self):
        pass
    @classmethod
    @log_time
    def setUpTestData(cls):
        cls.author_instance = User.objects.create(
            username='testuser',
            password='1234',
            email = 'test@gmail.com'
        )
        questions = []
        for i in range(1000000):
            question = Question(
                subject='test subject',
                content='test content',
                author=cls.author_instance,
                create_date=timezone.now()
            )
            questions.append(question)
        Question.objects.bulk_create(questions)
    def test_get_question_page_1(self):
        print("test_get_question_page_1")
        response = self.client.get('/?page=1')
        self.assertEqual(response.status_code, 200)
    def test_get_question_page_100000(self):
        print("test_get_question_page_100000")
        response = self.client.get('/?page=100000')
        # print(response.body)
        # print(response.content)
        self.assertEqual(response.status_code, 200)