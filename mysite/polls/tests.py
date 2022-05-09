import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    # timedeltaで取得
    return Question.objects.create(question_text=question_text, pub_data=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        # clientでurlsに対してアクセスをする
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # 過去の日付
    def test_past_question(self):
        question = create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse('polls:index'))
        # 追加した記事と同じ記事になるかどうか
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

    def test_future_question(self):
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        pass


# model_test
class QuestModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        # 30日後の
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_data=time)
        # Falseは予想される値
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_data=time)
        self.assertIs(old_question.was_published_recently(), False)

    # 現在よりも1日前
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_data=time)
        self.assertIs(recent_question.was_published_recently(), True)
