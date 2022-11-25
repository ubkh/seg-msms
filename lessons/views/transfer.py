"""
Views that will be used in the music school management system.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from lessons.forms import TransferForm


@login_required
# @admin_restricted
def transfer(request):
    form = TransferForm()

    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = TransferForm()
    return render(request, "admin/record_transfer.html", {'form': form})
