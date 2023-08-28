from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import AddLeadForm
from .models import Lead


@login_required
def all_leads(request):
    leads = Lead.objects.filter(created_by=request.user)

    return render(request, 'lead/all_leads.html', {
        'leads': leads
    })


@login_required
def leads_detail(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    # lead = Lead.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'lead/leads_detail.html', {
        'lead': lead
    })


@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead.delete()

    messages.success(request, 'Deleted Successfully')

    return redirect('all_leads')


@login_required
def add_lead(request):
    if request.method == 'POST':
        form = AddLeadForm(request.POST)

        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()

            messages.success(request, 'New Lead Added Successfully')

            return redirect('all_leads')
    else:
        form = AddLeadForm()

    return render(request, 'lead/add_lead.html', {
        'form': form
    })


@login_required
def edit_lead(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()

            messages.success(request, 'Lead Editted Successfully')

            return redirect('all_leads')
    else:
        form = AddLeadForm()

    return render(request, 'leads/edit_lead.html', {
        'form': form
    })
