from django.shortcuts import redirect


def index(request):
    """Redirect url of 'polls:index'."""
    return redirect('polls:index')