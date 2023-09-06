import csv
from django.http import HttpResponse
from typing import Any, Dict
from django.contrib import messages
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.views import View
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .forms import AddCommentForm, AddFileForm
from .models import Lead


from client.models import Client, Comment as ClientComment
from team.models import Team


@login_required
def lead_export_csv(request):
    leads = Lead.objects.filter(created_by=request.user, converted=False)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="leads.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Leads', 'Description', 'Created at', 'Created by'])

    for lead in leads:
        writer.writerow([lead.name, lead.description,
                        lead.created_at, lead.created_by])

    return response


class LeadListView(ListView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(
            created_by=self.request.user, converted=False)


class LeadDetailView(DetailView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()

        return context


class LeadDeleteView(DeleteView):
    model = Lead

    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()

        messages.success(self.request, 'Deleted Successfully')
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class LeadCreateView(CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status', )

    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('leads:list')

    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user)[0]

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()

        messages.success(self.request, 'New Lead Added Successfully')

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user)[0]
        context['team'] = team
        context['title'] = 'Add Lead'

        return context


class LeadUpdateView(UpdateView):
    model = Lead

    fields = ('name', 'email', 'description', 'priority', 'status', )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        messages.success(self.request, 'Edited Successfully')
        return reverse_lazy('leads:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Lead'

        return context


class AddFileView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user)[0]
            file = form.save(commit=False)
            file.team = team
            file.lead_id = pk
            file.created_by = request.user
            file.save()

            messages.success(self.request, 'Upload Successful')

        return redirect('leads:detail', pk=pk)


class AddCommentView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        content = request.POST.get('content')

        form = AddCommentForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user)[0]
            comment = form.save(commit=False)

            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect('leads:detail', pk=pk)


class ConvertToCLientView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')

        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = Team.objects.filter(created_by=request.user)[0]

        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team=team
        )

        lead.converted = True
        lead.save()

        # This helps to convet the comments of the lead to the client
        # When the lead is converted to a client

        comments = lead.comments.all()

        for comment in comments:
            ClientComment.objects.create(
                client=client,
                content=comment.content,
                created_by=comment.created_by,
                team=team
            )

        # Show message and redirect

        messages.success(
            request, 'Lead has been added to clients successfully')

        return redirect('leads:list')
