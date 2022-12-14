"""All views of polls for polls app."""
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Choice, Question, Vote
import logging
logger = logging.getLogger("polls")


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_queryset(self):
    """Give the last five published questions."""
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]


class IndexView(generic.ListView):
    """The view of index page which shows the list of all questions."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.localtime()
                                       ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """ The view of detail page which shows the detail of question, including the question and choices."""

    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        question = Question.objects.get(pk=self.question_id)
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            try:
                selected_choice = Vote.objects.get(
                    user=user, choice__in=question.choice_set.all()
                ).choice.choice_text
                context["selected_choice"] = selected_choice
            except Vote.DoesNotExist:
                pass
        return context

    def get(self, request, *args, **kwargs):
        """
        Send the error message for poll that is not allow for voting,
        but if the poll is allowed for voting, it will send to vote normally.
        """
        self.question_id = kwargs["pk"]
        self.object = Question.objects.get(pk=self.question_id)
        if not self.object.is_published():
            raise Http404("You are not allow to vote on this question")
        if not self.object.can_vote():
            messages.error(request,
                           f'You are not allow to vote on question "'
                           f'{self.object.question_text}"')
            return redirect("polls:results", pk=self.question_id)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ResultsView(generic.DetailView):
    """
    The view of result page which shows the result that count
    each vote for each choice.
    """

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """
    A voting page that conducts private voting and
    returns to the results page if successful.
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
    user = request.user
    try:
        vote_object = Vote.objects.get(user=user,
                                       choice__in=question.choice_set.all())
    except Vote.DoesNotExist:
        vote_object = Vote.objects.create(choice=selected_choice,
                                          user=user)
        vote_object.save()
    vote_object.choice = selected_choice
    vote_object.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return redirect("polls:results", pk=question_id)
