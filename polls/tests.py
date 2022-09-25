import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Vote


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_old_question(self):
        """
        is_published() returns True for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_recent_question(self):
        """
        is_published() returns True for questions whose pub_date
        is  within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.is_published(), True)

    def test_can_vote_with_future_question(self):
        """
        can_vote() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_old_question(self):
        """
        can_vote() returns True for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.can_vote(), True)

    def test_can_vote_with_recent_question(self):
        """
        can_vote() returns True for questions whose pub_date
        is  within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        end_time = time + datetime.timedelta(days=1)
        recent_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(recent_question.can_vote(), True)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = \
            create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    class VoteTest(TestCase):
        def test_vote_count(self):
            """
            Test that the number of votes are counted correctly.
            """
            question1 = create_question(question_text='Past Question.',
                                        days=-5)
            choice1 = question1.choice_set.create(choice_text='Correct')
            self.user = User.objects.create_user(username='mymelody')
            Vote.objects.create(question=question1,
                                choice=choice1,
                                user=self.user)
            self.assertEqual(1, choice1.votes)

        def test_user_can_vote_one_choice_each_question(self):
            """Test for one user one vote."""
            question1 = create_question(question_text='Past Question.',
                                        days=-5)
            choice1 = question1.choice_set.create(choice_text="A lot")
            choice2 = question1.choice_set.create(choice_text="Not at all")
            self.user = User.objects.create_user(username='mymelody')
            self.client.post(reverse('polls:vote', args=(question1.id,)),
                             {'choice': choice1.id})
            self.assertEqual(question1.vote_set.get(user=self.user).choice,
                             choice1)
            self.assertEqual(Vote.objects.all().count(), 1)
            self.client.post(reverse('polls:vote', args=(question1.id,)),
                             {'choice': choice2.id})
            self.assertEqual(question1.vote_set.get(user=self.user).choice,
                             choice2)
            self.assertEqual(Vote.objects.all().count(), 1)

        def test_voter_is_authenticated(self):
            """Test that only authenticated user can vote."""
            question1 = create_question(question_text='Past Question.',
                                        days=-5)
            ans_a = self.client.post(reverse('polls:vote',
                                             args=(question1.id,)))
            self.assertEqual(ans_a.status_code, 200)
            self.client.logout()
            ans_b = self.client.post(reverse('polls:vote',
                                             args=(question1.id,)))
            self.assertEqual(ans_b.status_code, 302)
