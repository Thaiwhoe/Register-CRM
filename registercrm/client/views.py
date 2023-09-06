from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import AddClientForm, AddCommentForm, AddFileForm
from .models import Client
from team.models import Team


@login_required
def all_clients(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/all_clients.html', {
        'clients': clients
    })


@login_required
def clients_add_file(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = team
            file.client_id = pk
            file.created_by = request.user
            file.save()

            messages.success(request, 'Upload successfull')

            return redirect('clients:detail', pk=pk)

    return redirect('clients:detail', pk=pk)


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    # lead = Lead.objects.filter(created_by=request.user).get(pk=pk)

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        team = Team.objects.filter(created_by=request.user)[0]

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.client = client
            comment.save()

            return redirect('clients:detail', pk=pk)

    else:
        form = AddCommentForm

    return render(request, 'client/client_detail.html', {
        'client': client,
        'form': form,
        'fileform': AddFileForm(),
    })


@login_required
def add_client(request):
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]

            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()

            messages.success(request, 'Client has been added successfully')

            return redirect('clients:list')

    else:
        form = AddClientForm()

    return render(request, 'client/add_client.html', {
        'form': form,
        'team': team
    })


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()

    messages.success(request, 'Deleted Successfully')

    return redirect('clients:list')


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, 'Client details editted successfully')
            return redirect('clients:list')

    else:
        form = AddClientForm(instance=client)

    return render(request, 'client/edit_client.html', {
        'form': form
    })
