from django.core.management.base import BaseCommand
from main.utils import generate_fake_resumes

class Command(BaseCommand):
    help = 'Generate fake Resumes with various details'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            type=int,
            default=3000,
            help='Number of resumes to generate'
        )
        parser.add_argument(
            '-c',
            '--clear',
            action='store_true',
            help='Clear existing resumes and related data before generating'
        )

    def handle(self, *args, **options):
        count = options['number']
        clear = options['clear']

        if clear:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Rating.objects.all().delete()
            PreviousJob.objects.all().delete()
            Education.objects.all().delete()
            Skill.objects.all().delete()
            Resume.objects.all().delete()
            User.objects.filter(is_staff=False, is_superuser=False).delete()
            Company.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared.'))

        self.stdout.write(f'Generating {count} resumes...')
        
        generated_count = generate_fake_resumes(count)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {generated_count} resumes.'))

