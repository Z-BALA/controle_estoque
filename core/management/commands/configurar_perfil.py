from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from core.models import Organizacao, Perfil

class Command(BaseCommand):
    help = 'Vincula usuário existente a uma organização e papel.'
    def add_arguments(self, parser):
        parser.add_argument('usuario')
        parser.add_argument('--organizacao', default='Organização padrão')
        parser.add_argument('--papel', choices=['admin','operador'], default='operador')
    def handle(self, *args, **options):
        try:
            user = get_user_model().objects.get(username=options['usuario'])
        except get_user_model().DoesNotExist:
            raise CommandError('Usuário não encontrado.')
        org, _ = Organizacao.objects.get_or_create(nome=options['organizacao'])
        Perfil.objects.update_or_create(usuario=user, defaults={'organizacao':org,'papel':options['papel']})
        self.stdout.write(self.style.SUCCESS('Perfil configurado.'))
