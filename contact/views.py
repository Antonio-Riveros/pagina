from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                return render(request, 'contact/partials/_success.html')
            return render(request, 'contact/page.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
        
    return render(request, 'contact/page.html', {'form': form})
