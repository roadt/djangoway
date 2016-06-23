

import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import *

# Create your tests here.

class QuestionMethodTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() should return False for questions whose pub_date is in the future

        '''
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)


    def test_was_published_recently_with_old_question(self):
        '''
        pub_date is older than one day
        '''
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''
        recently question, should pass
        '''
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


        
def create_question(question_text, days):
    '''
    create question with text and days, helper func
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return  Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):
        
    def test_index_view_with_no_question(self):
        resp  = self.client.get(reverse('polls:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No polls are available")
        self.assertQuerysetEqual(resp.context['latest_question_list'], [])

    def test_index_view_with_a_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
    

        

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        '''
        should return 404
        '''
        q = create_question(question_text='Future question', days=5)
        url = reverse('polls:detail', args(q.id,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)


    def test_detail_view_with_a_past_question(self):
        '''
        should display question's text
        '''
        q = create_question(question_text='Past Question', days=-5)
        url = reverse('polls:detail', args=(q.id,))
        resp = self.client.get(url)
        self.assertContains(resp, q.question_text)


    
        

