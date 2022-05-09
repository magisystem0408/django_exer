from pyexpat import model

from django.shortcuts import render
from django.views.generic.base import View, TemplateView, RedirectView
from . import forms
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Books
from datetime import datetime


# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        book_form = forms.BookForm()
        return render(request, 'index.html', context={
            'book_form': book_form
        })

    def post(self, request, *args, **kwargs):
        book_form = forms.BookForm(request.POST or None)
        if book_form.is_valid():
            # saveする
            book_form.save()

        return render(request, 'index.html', context={
            'book_form': book_form
        })


class HomeView(TemplateView):
    template_name = "home.html"

    #     templateに値を渡したい場合
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)  # {'name': 'test'}

        context['name'] = kwargs.get('name')

        # timeを入れてcontextを返す
        context['time'] = datetime.now()
        return context


class BookDetailView(DetailView):
    model = Books
    # 詳細に指定したmodelを指定する
    template_name = 'book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['form'] = forms.BookForm()
        # {'object': <Books: Books object (1)>, 'books': <Books: Books object (1)>, 'view': <store.views.BookDetailView object at 0x1068ad8b0>}
        return context


class BookListView(ListView):
    model = Books
    template_name = 'book_list.html'

    # 順番の入れ替え
    def get_queryset(self):
        qs = super(BookListView, self).get_queryset()

        # 絞り込み
        if 'name' in self.kwargs:
            qs = qs.filter(name__startswith=self.kwargs['name'])

        # # nameがbookで始まるもののみを絞り込み
        # qs = qs.filter(name__startswith='Book')

        # 順番の並び替え
        qs = qs.order_by('-id')
        print(qs)
        return qs


class BookCreateView(CreateView):
    model = Books
    fields = ['name', 'description', 'price']
    template_name = 'add_book.html'
    success_url = reverse_lazy('store:list_book')

    def form_valid(self, form):
        form.instance.create_at = datetime.now()
        form.instance.update_at = datetime.now()
        return super(BookCreateView, self).form_valid(form)

    # formの初期値を制定
    def get_initial(self, **kwargs):
        initial = super(BookCreateView, self).get_initial(**kwargs)
        initial['name'] = 'sample'
        return initial


class BookUpdateView(SuccessMessageMixin, UpdateView):
    model = Books
    template_name = 'update_book.html'
    form_class = forms.BookUpdateForm
    success_message = "更新に成功しました"

    # 成功処理
    def get_success_url(self):
        print(self.object)
        return reverse_lazy('store:edit_book', kwargs={'pk': self.object.id})

    # success messageを更新できる
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return cleaned_data.get('name') + 'を更新しました'


class BookDeleteView(DeleteView):
    model = Books
    template_name = 'delete_book.html'
    success_url = reverse_lazy('store:list_book')


# indexviewを置き換える
class BookFormView(FormView):
    template_name = 'form_book.html'
    form_class = forms.BookForm
    success_url = reverse_lazy('store:list_book')

    def get_initial(self, **kwargs):
        initial = super(BookFormView, self).get_initial(**kwargs)
        initial['name'] = 'sample'
        return initial

    # formが送信された時の処理
    def form_valid(self, form):
        # データを保存する処理
        if form.is_valid():
            form.save()

        #     superクラスのform_validを実行した結果を返す
        return super(BookFormView, self).form_valid(form)


class BookRedirectView(RedirectView):
    url = 'http://google.co.jp'

    # 動的に遷移先
    def get_redirect_url(self, *args, **kwargs):
        book = Books.objects.first()
        if 'pk' in kwargs:
            return reverse_lazy('store:detail_book', kwargs={'pk': kwargs['pk']})

        print(book)
        return reverse_lazy('store:edit_book', kwargs={'pk': book.pk})
