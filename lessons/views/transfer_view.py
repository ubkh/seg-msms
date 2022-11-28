"""
Views that will be used in the music school management system.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from lessons.forms import TransferForm
from lessons.models import Transfer
from lessons.helpers import administrator_restricted


@login_required
@administrator_restricted
def display_transfer(request):
    transfer_list = Transfer.objects.all()
    return render(request, "transfer/transfers.html", {'transfers': transfer_list})


@login_required
@administrator_restricted
def create_transfer(request):
    form = TransferForm()

    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = TransferForm()
    return render(request, "transfer/record_transfer.html", {'form': form})
