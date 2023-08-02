from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Note
from django.urls import reverse_lazy
from .forms import NoteCreationForm, NoteUpdateForm, AccountSettingsForm
from django.core.paginator import Paginator


class HomeView(TemplateView):
    template_name = 'notes/index.html'


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created successfully")
            return redirect('notes:login')
    context = {
        'form': form
    }
    return render(request, 'notes/register.html', context)


def home_page(request):
    notes = Note.objects.all()
    form = NoteCreationForm()
    get_page = request.GET.get('page', 1)
    stuff = Paginator(notes, 2)
    page = stuff.page(get_page)
    if request.method == "POST":
        form = NoteCreationForm(request.POST)
        if form.is_valid():
            note_obj = form.save(commit=False)
            note_obj.author = request.user
            note_obj.save()
            return redirect('notes:home_page')
    return render(request, 'notes/home.html', context={
        'notes': page,
        'form': form,
        'stuffs': stuff,
        'count': notes
    })


class AccountSettingsView(UpdateView):
    template_name = 'notes/settings.html'
    form_class = AccountSettingsForm
    success_url = '/home/'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Account Updated Successfully")
        return super().form_valid(form)


class LoggedoutView(TemplateView):
    template_name = 'notes/loggedout.html'


class NoteUpdateView(UpdateView):
    model = Note
    template_name = 'notes/update.html'
    fields = ['title', 'description']
    success_url = '/home/'


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'notes/delete.html'
    success_url = '/home/'
