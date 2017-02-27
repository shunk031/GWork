from django.shortcuts import render

from predict_category.models import InputURLForm

# Create your views here.


def index(request):
    url_form = InputURLForm()
    context = {
        "url_form": url_form
    }

    return render(request, 'predict_category/index.html', context)
