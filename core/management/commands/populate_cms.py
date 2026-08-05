from django.core.management.base import BaseCommand
from cms.models import SiteSettings, Section, NavigationMenu

class Command(BaseCommand):
    help = 'Populates the CMS with default sections to avoid an empty site'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creando SiteSettings por defecto...")
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            settings.site_name = "Mi Portfolio"
            settings.hero_title = "Construyendo el futuro"
            settings.hero_subtitle = "línea por línea"
            settings.hero_description = "Desarrolladores Full Stack especializados en crear soluciones digitales robustas y escalables."
            settings.hero_btn1_text = "Ver Proyectos"
            settings.hero_btn1_url = "#proyectos"
            settings.hero_btn2_text = "Contactar"
            settings.hero_btn2_url = "/contacto/"
            settings.email = "hola@miportfolio.com"
            settings.estado_laboral = "disponible"
            settings.color_principal = "#8b5cf6"
            settings.color_secundario = "#11131a"
            settings.color_acento = "#d946ef"
            settings.footer_text = "Construyendo el futuro, línea por línea."
            settings.save()
            self.stdout.write(self.style.SUCCESS('SiteSettings creado.'))
        else:
            self.stdout.write('SiteSettings ya existía, omitiendo.')

        # Secciones por defecto
        sections_data = [
            {'tipo': 'hero', 'titulo': '', 'orden': 1, 'mostrar_fondo': False},
            {'tipo': 'projects', 'titulo': 'Proyectos Destacados', 'descripcion': 'Algunos de mis mejores trabajos', 'orden': 2, 'mostrar_fondo': False},
            {'tipo': 'technologies', 'titulo': 'Tecnologías que domino', 'descripcion': 'Las herramientas que utilizo día a día', 'orden': 3, 'mostrar_fondo': True},
            {'tipo': 'videos', 'titulo': 'Últimos Videos', 'descripcion': 'Tutoriales y demostraciones de proyectos', 'orden': 4, 'mostrar_fondo': False},
            {'tipo': 'cta', 'titulo': '¿Tienen un proyecto en mente?', 'descripcion': 'Estamos siempre abiertos a discutir nuevas oportunidades y crear soluciones increíbles juntos.', 'orden': 5, 'mostrar_fondo': True},
        ]

        self.stdout.write("Verificando secciones...")
        if not Section.objects.exists():
            for data in sections_data:
                Section.objects.create(
                    tipo=data['tipo'],
                    titulo=data['titulo'],
                    descripcion=data.get('descripcion', ''),
                    orden=data['orden'],
                    mostrar_fondo=data['mostrar_fondo'],
                    activo=True
                )
            self.stdout.write(self.style.SUCCESS('Secciones por defecto creadas.'))
        else:
            self.stdout.write('Las secciones ya existían, omitiendo creación.')

        # Menú de Navegación por defecto
        if not NavigationMenu.objects.exists():
            NavigationMenu.objects.create(nombre="Inicio", url="/", orden=1)
            NavigationMenu.objects.create(nombre="Proyectos", url="/proyectos/", orden=2)
            NavigationMenu.objects.create(nombre="Videos", url="/videos/", orden=3)
            NavigationMenu.objects.create(nombre="Contacto", url="/contacto/", orden=4)
            self.stdout.write(self.style.SUCCESS('Menú de navegación creado.'))

        self.stdout.write(self.style.SUCCESS('¡Población completada con éxito!'))
