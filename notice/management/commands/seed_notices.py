"""
Fills the notice board with realistic demo data so the site is not empty
during development.

    python manage.py seed_notices
    python manage.py seed_notices --flush    # delete existing first

Safe to re-run: it updates notices that match on title rather than creating
duplicates.
"""

import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from notice.models import Notice, NoticeCategory

CATEGORIES = [
    ('Examination', 1),
    ('Admission', 2),
    ('Research', 3),
    ('Campus', 4),
    ('General', 5),
]

NOTICES = [
    {
        'title': 'Mid-Term Examination Schedule — Spring Semester',
        'category': 'Examination',
        'reference_code': 'JU/REG/2026/041',
        'published_date': datetime.date(2026, 9, 18),
        'has_pdf': True,
        'is_pinned': True,
        'description': (
            'The mid-term examination schedule for all programmes is now available. '
            'Papers are grouped by faculty and scheduled across two weeks beginning '
            '5 October 2026.\n\n'
            'Students must carry their registration card to every paper. Entry to the '
            'examination hall closes fifteen minutes before the scheduled start time. '
            'Electronic devices of any kind, including calculators, are not permitted '
            'unless the paper specifically states otherwise.\n\n'
            'Candidates with a documented clash should submit an application to the '
            'Examination Branch within seven working days of publication of this notice.'
        ),
    },
    {
        'title': 'Undergraduate Application Deadline Extended to 30 September',
        'category': 'Admission',
        'reference_code': 'JU/ADM/2026/012',
        'published_date': datetime.date(2026, 9, 5),
        'has_pdf': True,
        'description': (
            'Following requests from candidates, the deadline for submitting '
            'applications to undergraduate programmes for Spring 2027 has been '
            'extended to 30 September 2026.\n\n'
            'This extension applies only to the submission step. Document verification '
            'and the entrance test schedule are unchanged. Applicants are advised to '
            'submit well before the deadline, as the portal may be slow in the final '
            'days.\n\n'
            'Merit scholarships are awarded on a rolling basis and are not reserved '
            'until the admission list is formally published.'
        ),
    },
    {
        'title': 'Library Week 2026: Schedule and Registration',
        'category': 'Campus',
        'reference_code': 'JU/LIB/2026/007',
        'published_date': datetime.date(2026, 8, 28),
        'has_pdf': False,
        'description': (
            'Library Week runs from 12 to 16 October 2026 in the Central Library. '
            'Sessions are free and open to all registered students, staff and alumni.\n\n'
            'The week opens with an exhibition of rare holdings from the eastern '
            'collection, followed by workshops on searching the digital catalogue, '
            'citation practice and research data management.\n\n'
            'Seats for the hands-on workshops are limited to twenty per session and '
            'require registration at the circulation desk.'
        ),
    },
    {
        'title': 'Faculty Workshop: Writing Competitive Research Proposals',
        'category': 'Research',
        'reference_code': 'JU/RES/2026/019',
        'published_date': datetime.date(2026, 8, 21),
        'has_pdf': True,
        'description': (
            'A two-day workshop on writing competitive research proposals will be held '
            'for faculty and research staff, led by external reviewers from the '
            'national research council.\n\n'
            'The workshop covers problem framing, budget narratives, reviewer '
            'expectations and responses to rejection. Participants are asked to bring '
            'a draft proposal for structured feedback.\n\n'
            'Forty seats are available. Registration closes one week before the session '
            'and is subject to approval by the relevant dean.'
        ),
    },
    {
        'title': 'Inter-Faculty Sports Meet: Team Registration Open',
        'category': 'Campus',
        'reference_code': 'JU/STU/2026/003',
        'published_date': datetime.date(2026, 8, 15),
        'has_pdf': False,
        'description': (
            'Registration is now open for the annual inter-faculty sports meet in '
            'cricket, football, volleyball, basketball and badminton.\n\n'
            'Each faculty may enter one team per event. A nominated team manager must '
            'submit the player list with dates of birth verified, as eligibility is '
            'checked against the enrolment record.\n\n'
            'Nominations close on 25 September 2026. A briefing for team managers will '
            'be held in the Sports Complex immediately afterwards.'
        ),
    },
    {
        'title': 'Revised Library Opening Hours During Examination Period',
        'category': 'General',
        'reference_code': 'JU/GEN/2026/028',
        'published_date': datetime.date(2026, 8, 9),
        'has_pdf': False,
        'description': (
            'For the duration of the examination period the Central Library will open '
            'from 7:00 AM to 11:00 PM, seven days a week.\n\n'
            'Group study rooms may be booked for a maximum of three hours at a time and '
            'are released if unoccupied after fifteen minutes. The reading hall on the '
            'second floor remains open overnight during this period.'
        ),
    },
    {
        'title': 'PhD Admission: Spring 2027 Call for Applications',
        'category': 'Admission',
        'reference_code': 'JU/RGP/2026/004',
        'published_date': datetime.date(2026, 7, 30),
        'has_pdf': True,
        'description': (
            'Applications are invited for doctoral programmes across all faculties for '
            'the Spring 2027 intake.\n\n'
            'Applicants require a master degree in a relevant discipline and a research '
            'proposal of no more than three pages. Shortlisted candidates will be '
            'invited for an interview and a presentation of the proposal.\n\n'
            'Applications close on 30 November 2026. Incomplete applications will not '
            'be considered.'
        ),
    },
    {
        'title': 'Research Ethics Approval Required for Human Subject Studies',
        'category': 'Research',
        'reference_code': 'JU/RES/2026/011',
        'published_date': datetime.date(2026, 7, 22),
        'has_pdf': True,
        'description': (
            'All research involving human participants must receive approval from the '
            'University Research Ethics Committee before data collection begins.\n\n'
            'The committee meets monthly and considers submissions received at least '
            'three weeks in advance. Approval is granted for a maximum of twelve '
            'months and must be renewed if the study continues.\n\n'
            'Retrospective approval is not granted. Studies that have already begun '
            'data collection should contact the committee immediately.'
        ),
    },
    {
        'title': 'Make-Up Examination for August 2026 Sitting',
        'category': 'Examination',
        'reference_code': 'JU/REG/2026/036',
        'published_date': datetime.date(2026, 7, 18),
        'has_pdf': False,
        'description': (
            'A make-up examination will be held for candidates who could not sit the '
            'August 2026 examinations through documented illness or bereavement.\n\n'
            'Applications must be submitted to the Examination Branch within fourteen '
            'days of the missed paper, supported by the original documentary evidence. '
            'Applications received after this period will not be accepted.\n\n'
            'The make-up will run in the week of 5 October 2026 alongside the regular '
            'mid-term schedule.'
        ),
    },
    {
        'title': 'Student Union Election: Nominations and Voting Schedule',
        'category': 'General',
        'reference_code': 'JU/STU/2026/005',
        'published_date': datetime.date(2026, 7, 11),
        'has_pdf': False,
        'description': (
            'Nominations are invited for the positions of President, General Secretary, '
            'Treasurer and the four faculty representatives.\n\n'
            'Each candidate must be nominated by at least twenty current students and '
            'must submit a written declaration of any positions held in a student '
            'organisation. Campaigning is permitted from 20 to 26 September 2026.\n\n'
            'Voting takes place over three days by electronic ballot. Results will be '
            'announced at the following general meeting.'
        ),
    },
    {
        'title': 'Campus Maintenance: Water Supply Interruption',
        'category': 'Campus',
        'reference_code': 'JU/EST/2026/002',
        'published_date': datetime.date(2026, 7, 4),
        'has_pdf': False,
        'description': (
            'Water supply to the main campus will be interrupted on 26 July 2026 '
            'between 8:00 AM and 6:00 PM while reservoir tanks are cleaned and '
            'replaced.\n\n'
            'The main library block is unaffected as it has independent supply. '
            'Residence halls will provide temporary tankered water. Students should '
            'store drinking water in advance.\n\n'
            'The work is weather dependent and may be rescheduled.'
        ),
    },
    {
        'title': 'Draft Unpublished: Notice Board Maintenance Window',
        'category': 'General',
        'reference_code': None,
        'published_date': datetime.date(2026, 7, 1),
        'has_pdf': False,
        'is_published': False,
        'description': (
            'This notice is saved as a draft so the filtering behaviour can be '
            'checked. It must not appear on the public notice board until published.'
        ),
    },
]


class Command(BaseCommand):
    help = 'Create demo categories and notices for local development.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete all existing notices before seeding.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['flush']:
            deleted, _ = Notice.objects.all().delete()
            self.stdout.write('Deleted {} existing notice(s).'.format(deleted))

        categories = {}
        for name, order in CATEGORIES:
            category, _ = NoticeCategory.objects.update_or_create(
                name=name,
                defaults={'order': order, 'is_active': True},
            )
            categories[name] = category

        self.stdout.write('Categories: {}'.format(len(categories)))

        created = updated = 0

        for item in NOTICES:
            payload = dict(item)
            category_name = payload.pop('category')
            payload.pop('has_pdf', None)
            payload.setdefault('is_published', True)
            payload.setdefault('is_pinned', False)
            payload['slug'] = slugify(payload['title'])[:220]
            payload['category'] = categories[category_name]

            _, was_created = Notice.objects.update_or_create(
                title=payload['title'], defaults=payload
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Notices seeded — {} created, {} updated, {} total.'.format(
                    created, updated, Notice.objects.count()
                )
            )
        )
        self.stdout.write(
            'Attachments are not seeded. Upload a PDF to any notice in the admin '
            'to test download.'
        )
