from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Choice, Question, Vote


def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]


class IndexView(generic.ListView):
    """The view of index page which shows the list of all questions."""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte = timezone.localtime()).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """
    The view of detail page which shows the detail of question
    including the question and choices.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        """Send the error message for poll that is not allow for voting,
        but if the poll is allowed for voting, it will send to vote normally."""
        self.object = Question.objects.filter(pk=kwargs['pk'])[0]
        if not self.object.can_vote():
            messages.error(request, f'You are not allow to vote on question "{self.object.question_text}"')
            return HttpResponseRedirect(reverse('polls:index'))

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
    """A voting page that conducts private voting and returns to the results page if successful."""
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
        vote_object = Vote.objects.get(user=user, choice__in=question.choice_set.all())
    except Vote.DoesNotExist:
        vote_object = Vote.objects.create(choice=selected_choice, user=user)
        vote_object.save()
    vote_object.choice = selected_choice
    vote_object.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return redirect("polls:results", pk=question_id)