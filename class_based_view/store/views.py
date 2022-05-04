from django.shortcuts import render
from django.views.generic.base import View


# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', )

    def post(self, request, *args, **kwargs):
        return render(request, 'index.html', )
