from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import UserCreationForm

@never_cache
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})
