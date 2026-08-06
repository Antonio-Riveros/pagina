import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from projects.models import Technology

techs = [
    ('Django', '<i class="fa-brands fa-python"></i>', '#44b78b'),
    ('React', '<i class="fa-brands fa-react"></i>', '#61dafb'),
    ('Python', '<i class="fa-brands fa-python"></i>', '#3776ab'),
    ('JavaScript', '<i class="fa-brands fa-js"></i>', '#f7df1e'),
    ('IA / Desarrollo Acelerado', '<i class="fa-solid fa-brain"></i>', '#8b5cf6'),
    ('HTML & CSS', '<i class="fa-brands fa-html5"></i>', '#e34f26'),
]

for nombre, icono, color in techs:
    Technology.objects.get_or_create(nombre=nombre, defaults={'icono': icono, 'color': color})

print("Tecnologías creadas!")
