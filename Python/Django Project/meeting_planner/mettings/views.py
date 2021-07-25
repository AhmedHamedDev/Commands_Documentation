from django.shortcuts import render, get_object_or_404, redirect
from .models import Metting
from django.forms import modelform_factory

# Create your views here.

def mettings(request):
    return render(request,"mettings/mettings-list.html",{"mettings_number": Metting.objects.count(), "mettings": Metting.objects.all() })

def detail(request, id):
    # metting = Metting.objects.get(pk=id)
    metting = get_object_or_404(Metting, pk=id)
    return render(request,"mettings/metting-detail.html",{"metting": metting })

MettingForm = modelform_factory(Metting, exclude=[])

def new(request):
    if request.method == "POST":
        form = MettingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("mettings")
    else:
        form = MettingForm()
    return render(request, "mettings/new.html", {"form":form})
