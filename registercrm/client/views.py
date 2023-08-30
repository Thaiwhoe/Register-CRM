from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import AddClientForm
from .models import Client


@login_required
def all_clients(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/all_clients.html', {
        'clients': clients
    })


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    # lead = Lead.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'client/client_detail.html', {
        'client': client
    })


@login_required
def add_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()

            messages.success(request, 'Client has been added successfully')

            return redirect('all_clients')

    else:
        form = AddClientForm()

    return render(request, 'client/add_client.html', {
        'form': form
    })


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()

    messages.success(request, 'Deleted Successfully')

    return redirect('all_clients')


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, 'Client details editted successfully')
            return redirect('all_clients')

    else:
        form = AddClientForm(instance=client)

    return render(request, 'client/edit_client.html', {
        'form': form
    })
