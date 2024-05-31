from django.shortcuts import render, get_object_or_404, redirect
from .forms import StuffsForm
from .models import Stuffs
from .models import Category

def foodstuffs(request):
    stuffs = Stuffs.objects.all()
    return render(request, 'foodstuff/table-foodstuffs.html', {'stuffs': stuffs})

def addfoodstuffs(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = StuffsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('foodstuff:foodstuffs')  # Redirect to a list view or another page
    else:
        form = StuffsForm()
    
    return render(request, 'foodstuff/add-foodstuffs.html', {'categories': categories,'form': form})

def edit_stuff(request, pk):
    stuff = get_object_or_404(Stuffs, pk=pk)
    if request.method == "POST":
        form = StuffsForm(request.POST, instance=stuff)
        if form.is_valid():
            form.save()
            return redirect('foodstuff:foodstuffs')
    else:
        form = StuffsForm(instance=stuff)
    return render(request, 'foodstuff/edit_stuff.html', {'form': form})