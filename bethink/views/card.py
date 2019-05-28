from django.views import generic
from bethink.models.card import Card
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from bethink.forms.card import CardForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class CardView(generic.DetailView):
    model = Card
    template_name = 'bethink/card.djt'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the username
        #comments = Comment.objects.filter(post=self.kwargs['pk'])
        #context['comments'] = comments
        return context


class CardCreate(LoginRequiredMixin, CreateView):
    model = Card
    fields = ['title', 'body', 'notification_date']
    template_name = 'bethink/create_card.djt'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def card_new(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            # return redirect('bethink:card', pk=card.pk)
            messages.success(request, 'Напомнинание успешно создано')
            return redirect('bethink:home')
    else:
        form = CardForm()
    return render(request, 'bethink/card_new.djt', {'form': form})


def card_edit(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            #card.pub_date = tim
            card.save()
            #return redirect('bethink:card', pk=card.pk)
            return redirect('bethink:home')
    else:
        form = CardForm(instance=card)
    return render(request, 'bethink/card_new.djt', {'form': form})


class CardUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Card
    fields = ['title', 'body']
    template_name = 'bethink/create_card.djt'
    login_url = reverse_lazy('login')

    def test_func(self):
        return Card.objects.get(id=self.kwargs['pk']).user == self.request.user


class CardDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('bethink:home')
    login_url = reverse_lazy('login')
    success_message = "Напоминание с заголовоком: %(title)s удалено"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(CardDelete, self).delete(request, *args, **kwargs)

    def test_func(self):
        return Card.objects.get(id=self.kwargs['pk']).user == self.request.user
