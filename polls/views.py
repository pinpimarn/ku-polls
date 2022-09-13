from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


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


class DetailView(generic.DetailView):
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


def vote(request, question_id):
    """A voting page that conducts private voting and returns to the results page if successful."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
