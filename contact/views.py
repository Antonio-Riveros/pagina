from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email
            subject = f"Nuevo mensaje de contacto de {contact.nombre}"
            message = f"Has recibido un nuevo mensaje de contacto en tu portafolio.\n\nNombre: {contact.nombre}\nEmail: {contact.email}\n\nMensaje:\n{contact.mensaje}"
            send_mail(
                subject,
                message,
                'no-reply@tu-portafolio.com',
                ['antonio.n.riveros18@gmail.com'],
                fail_silently=True,
            )
            
            if request.htmx:
                return render(request, 'contact/partials/_success.html')
            return render(request, 'contact/page.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
        
    return render(request, 'contact/page.html', {'form': form})
