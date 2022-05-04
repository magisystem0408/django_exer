from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.views import generic


def index(request):
    latest_question_list = Question.objects.order_by('-pub_data')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    # 第三引数に送りたい変数を書く
    return render(request, 'polls/index.html', context)

# listViewは複数のオブジェクトを返してくれる
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # object_list
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by('-pub_data')[:5]


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question
#     }
#     return render(request, 'polls/detail.html', context)

# 個別のviewで使用する
class DetailView(generic.DetailView):
    # 個別の内容を取得することができる
    model = Question
    template_name = 'polls/detail/detail.html'


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context ={'question':question}
#     return render(request, 'polls/results.html', context)

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        print('@@@@', request.POST['choice'])
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "選択できていない"
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
