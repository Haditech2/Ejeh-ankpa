"""
Management command to seed initial data for Ejeh Ankpa Palace Platform.
This includes the current Ejeh biography and other essential data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from palace.models import EjehProfile
from datetime import date


User = get_user_model()


class Command(BaseCommand):
    help = 'Seed initial data for the Ejeh Ankpa Palace Platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin',
            action='store_true',
            help='Create a default admin user'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting data seeding...'))
        
        # Create present Ejeh profile
        self.create_present_ejeh()
        
        # Create admin user if requested
        if options['admin']:
            self.create_admin_user()
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))

    def create_present_ejeh(self):
        """Create or update the profile for the current Ejeh."""
        ejeh_data = {
            'full_name': 'Alhaji Abubakar Sadiq Ahmed Yakubu',
            'title': 'HRH',
            'royal_title': 'Ejeh Ankpa IV',
            'full_title_and_honours': 'His Royal Highness, Alhaji Abubakar Sadiq Ahmed Yakubu, The Ejeh Ankpa IV',
            'reign_status': 'present',
            'reign_start': date(2021, 10, 21),
            'reign_number': 4,
            'birth_date': date(1978, 4, 9),
            'birth_place': 'Kano State, North-west Nigeria',
            'biography': """The Ejeh Ankpa IV, His Royal Highness, Alhaji Abubakar Ahmed Yakubu was born into the family of Late Ejeh Ahmadu Yakubu on the 9th day of April, 1978 in Kano State, North-west Nigeria.

Alhaji Abubakar descends from a lineage marked with combination of royal blood and humanitarian service. Kings and philanthropists are found among his forebears as his father, the Late Ejeh Ahmadu Yakubu hails from the great Atiyele Omá Idoko dynasty of Igala Kingdom while his mother, Late Hajiya Rabi Yakubu (Nee Usman) hails from the family of Late Alhaji Usman Abubakar, a renowned fish farmer cum philanthropist of Angwa origin in Idah Local Government Area of Kogi State.""",
            
            'early_life': """He started his early life with a Primary Education at the Magwan Special Primary School, Kano, from 1983 to 1988 and a secondary education at the prestigious Government Secondary School, Kawaji, Kano State between 1989 to 1994.

Upon the completion of his secondary education, the young Prince who was destined to later become King took a short break to work and support his father, the Late Ejeh Ahmadu Yakubu as his Personal Assistant. By the virtue of his jurisdictions as a Personal Assistant, he was literally in charge of protocols, managing traditional engagements, planning visits and interfacing with high level stakeholders which no doubt, exposed him to the aura of royalty.

After about six years of diligent service in the Palace cum his determination to acquire a very sound education, Alhaji Abubakar proceeded to the Enugu State University of Science and Technology, Enugu where he bagged a first degree — Bachelor of Science (B.Sc) in Business Administration between the year 1999 to 2004. He thereafter proceeded to Meridian College Greenwich, London for his postgraduate studies in Management Information System (MIS) between 2006 to 2007.""",
            
            'education': """Primary Education: Magwan Special Primary School, Kano (1983-1988)
Secondary Education: Government Secondary School, Kawaji, Kano State (1989-1994)
B.Sc. Business Administration: Enugu State University of Science and Technology, Enugu (1999-2004)
Postgraduate Diploma in Management Information System (MIS): Meridian College Greenwich, London (2006-2007)

Professional Certifications:
• Member, UK Institute of Management Information Systems (IMIS)
• Courses in Business Analysis, Strategy and Management
• Leadership and Decision Making
• Private Sector Investment in Nigerian Railway Sector
• National Policy on Public Private Partnership (N4P)
• Proficiency Training In Management""",
            
            'occupation_before_throne': """2008-2010: Pioneer Sales Representative, Abercrombie & Fitch UK Limited, London - Part of the team that developed live model in-store mannequins, boosting sales and leading to expansion across Europe.

2010-2012: Business Development Manager, ZUMA Energy Nigeria Limited - Responsible for licenses, permits and liaising with Power sector stakeholders for three coal mining sites, two 1200MW Coal fired power plants in Itobe, and a 400MW Gas fired power plant in Egbema, Imo State.

2012-2016: Project Coordinator, ZIMCO Nigeria Limited - Engaged foreign investors from Russia, China, Korea and India for rail projects on B.O.T basis with Nigeria Railway Corporation (NRC). Facilitated Federal Government's approval of the Company's railway development project.

Current Positions:
• Managing Director, Ashkar Integrated Services Limited
• Executive Director of Business Development, Softcom
• Board Director, Maidpro Nigeria Limited
• Board Director, Acceloron Technologies Limited""",
            
            'achievements': """Being a self motivated, highly enthusiastic, digitally inclined and professionally groomed young man with sufficient industrious acumen; He was in 2008 employed as a pioneer sales representative staff of Abercrombie & Fitch UK Limited, a couture firm in London. He was part of the team that developed live model in-store mannequins. This initiative attracted more customers, boosted sales and led to his team opening up more Abercrombie flagship stores across other European countries.

In 2010, he returned to Nigeria to join the ZUMA Energy Nigeria Limited as Business Development Manager, responsible for preparing action and business plans for licenses, permits and liaising with Power sector Stakeholders towards the success of the company's long term lease operations including three coal mining sites in Kogi State, two 1200MW Coal fired power plant in Itobe, and a 400MW Gas fired power plant in Egbema, Imo State.

In 2012, he was transferred to Zuma Infrastructure Management Company (ZIMCO) Nigeria Limited as Project Coordinator where he engaged foreign investors from Russia, China, Korea and India for rail projects on B.O.T basis with Nigeria Railway Corporation (NRC). He also facilitated Federal Government's approval of the Company's railway development project.

Awards and Recognition:
• Award of Stewardship from Coalition of Progressive Political Parties in Kogi State
• Board Membership Certificate of Kogi Chamber of Commerce, Industry, Mines and Agriculture
• Humanitarian Award from Omataina Empire
• Plaque of Honour from the author of 'The Buhari in Us'""",
            
            'legacy': """Alhaji Abubakar's philosophy to life is the equality of all men before God. He believes in the possibility of change occurring at any time, has a firm belief in the reality of people's dreams and has always disposed himself as a catalyst to the growth of many youths.

His words are his bond and he has been using his networks to facilitate assistances within his might for many young people within and outside Kogi State. The aged and people living with disabilities (PLWD) are also not left out of his humanitarian services as he has been positively affecting their lives through partnership with both local and international Non Governmental Organizations (NGO).

Alhaji Abubakar was a cherished child of his father, Late Ejeh Ahmadu Yakubu. More so that he is known for a strength of character and humility, his announcement as the fourth Ejeh Ankpa on Thursday 21st October, 2021 reinvigorated his father by signaling an uninterrupted continuity between his and his father's reigns.

As he said in his note of appreciation and acceptance of appointment as Ejeh Ankpa IV: 'He will bequeath a greater Ankpa to generations to come.'

Indeed, it's a new dawn in Ankpa. All hail His Royal Highness... Agaaaaaaaagwu!!!""",
            
            'motto': 'He will bequeath a greater Ankpa to generations to come',
            'hobbies': 'Charity works, reading and intelligent interactions',
            'countries_visited': 'UK, Germany, Kenya, Russia, India, Qatar, USA, Saudi Arabia, Ethiopia, Australia, Spain, Turkey',
            'is_active': True,
            'display_order': 1,
        }
        
        ejeh, created = EjehProfile.objects.update_or_create(
            reign_status='present',
            defaults=ejeh_data
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Created profile for {ejeh.full_name} (Ejeh Ankpa IV)'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Updated profile for {ejeh.full_name} (Ejeh Ankpa IV)'
            ))

    def create_admin_user(self):
        """Create a default admin user if it doesn't exist."""
        admin_email = 'admin@ejehankpa.com'
        
        if not User.objects.filter(email=admin_email).exists():
            user = User.objects.create_superuser(
                email=admin_email,
                password='admin123',  # Change this in production!
                first_name='Palace',
                last_name='Administrator',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created admin user: {admin_email}'
            ))
            self.stdout.write(self.style.WARNING(
                'Remember to change the default admin password!'
            ))
        else:
            self.stdout.write(self.style.NOTICE(
                f'Admin user {admin_email} already exists'
            ))
