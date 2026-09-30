"""
Placeholder content for the homepage.

This module exists only until the Notice model lands in Phase 4. Keeping the
demo data here rather than inline in the template means the swap is one line in
core/views.py - the template never changes.

Nothing in this file is copied from any real university. It is invented content
for a fictional institution.
"""

import datetime

# --- Section 2: quick access -----------------------------------------------
QUICK_LINKS = [
    {
        'label': 'Admission',
        'text': 'Requirements, fees and deadlines',
        'url_name': 'core:admission',
        'icon': 'M4 21V9l8-6 8 6v12M9 21v-6h6v6',
    },
    {
        'label': 'Programs',
        'text': '38 undergraduate and graduate degrees',
        'url_name': 'core:academics',
        'icon': 'M12 3 2 8l10 5 10-5-10-5zM6 11v5c0 1 3 2 6 2s6-1 6-2v-5',
    },
    {
        'label': 'Notices',
        'text': 'Examinations, events and announcements',
        'url_name': 'notice:notice_list',
        'icon': 'M6 9V6h12v3M6 18H4v-7h16v7h-2M8 14h8',
    },
    {
        'label': 'Library',
        'text': 'Reading rooms and digital collections',
        'url_name': 'core:students',
        'icon': 'M4 19V5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM19 17H6',
    },
    {
        'label': 'Careers',
        'text': 'Open positions across the university',
        'url_name': 'core:career',
        'icon': 'M20 7h-4V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2H4a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V8a1 1 0 0 0-1-1z',
    },
    {
        'label': 'Contact',
        'text': 'Reach any department or office',
        'url_name': 'core:contact',
        'icon': 'M21 10c0 6-9 12-9 12S3 16 3 10a9 9 0 0 1 18 0zM12 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6z',
    },
]

# --- Section 4: academic programs ------------------------------------------
PROGRAMS = [
    {
        'code': 'BSc CSE',
        'title': 'Computer Science & Engineering',
        'faculty': 'Engineering & Technology',
        'duration': '4 years',
        'text': 'Algorithms, systems, machine learning and full-stack practice.',
    },
    {
        'code': 'BBA',
        'title': 'Business Administration',
        'faculty': 'Business & Economics',
        'duration': '4 years',
        'text': 'Accounting, finance, marketing and organisational behaviour.',
    },
    {
        'code': 'LLB',
        'title': 'Bachelor of Laws',
        'faculty': 'Law & Governance',
        'duration': '4 years',
        'text': 'Constitutional, commercial and international law with moot court work.',
    },
    {
        'code': 'MBBS',
        'title': 'Medicine & Surgery',
        'faculty': 'Health Sciences',
        'duration': '6 years',
        'text': 'Clinical training from the third year at partner teaching hospitals.',
    },
    {
        'code': 'MSc DS',
        'title': 'Data Science',
        'faculty': 'Science & Technology',
        'duration': '2 years',
        'text': 'Statistics, machine learning and large-scale data engineering.',
    },
    {
        'code': 'MA Eco',
        'title': 'Economics',
        'faculty': 'Business & Economics',
        'duration': '2 years',
        'text': 'Microeconomics, econometrics and development policy analysis.',
    },
]

# --- Section 5: notices (becomes a database query in Phase 4) --------------
NOTICES = [
    {
        'title': 'Mid-Term Examination Schedule — Spring Semester',
        'reference': 'JU/REG/2026/041',
        'category': 'Examination',
        'date': datetime.date(2026, 9, 18),
        'has_pdf': True,
        'summary': 'Seating plan and timing for all mid-term papers, grouped by faculty.',
    },
    {
        'title': 'Undergraduate Application Deadline Extended to 30 September',
        'reference': 'JU/ADM/2026/012',
        'category': 'Admission',
        'date': datetime.date(2026, 9, 5),
        'has_pdf': True,
        'summary': 'The final date for submitting Spring 2027 applications is extended.',
    },
    {
        'title': 'Library Week 2026: Schedule and Registration',
        'reference': 'JU/LIB/2026/007',
        'category': 'Campus',
        'date': datetime.date(2026, 8, 28),
        'has_pdf': False,
        'summary': 'A week of exhibitions, workshops and open-access sessions.',
    },
    {
        'title': 'Faculty Workshop: Writing Competitive Research Proposals',
        'reference': 'JU/RES/2026/019',
        'category': 'Research',
        'date': datetime.date(2026, 8, 21),
        'has_pdf': True,
        'summary': 'Two-day workshop led by external reviewers. Seats limited to 40.',
    },
    {
        'title': 'Inter-Faculty Sports Meet: Team Registration Open',
        'reference': 'JU/STU/2026/003',
        'category': 'Campus',
        'date': datetime.date(2026, 8, 15),
        'has_pdf': False,
        'summary': 'Cricket, football, volleyball and basketball. Nominations close 25 September.',
    },
]

# --- Section 6: news --------------------------------------------------------
NEWS = [
    {
        'title': 'Centre for Applied Intelligence Opens on Campus',
        'category': 'Research',
        'date': datetime.date(2026, 9, 12),
        'text': 'The new centre brings together computer science, statistics and '
                'engineering faculty around shared compute infrastructure.',
        'image': 'img/news-research.jpg',
        'alt': 'Students working together at a bench in a university science laboratory',
    },
    {
        'title': 'Graduates Secure Roles Within Six Months of Convocation',
        'category': 'Achievements',
        'date': datetime.date(2026, 9, 4),
        'text': 'Placement support included industry internships, mock interviews '
                'and an annual recruitment day with sixty participating employers.',
        'image': 'img/news-graduates.jpg',
        'alt': 'Three graduates in caps and gowns celebrating together outdoors',
    },
    {
        'title': 'Engineering Team Wins National Robotics Championship',
        'category': 'Student Life',
        'date': datetime.date(2026, 8, 30),
        'text': 'A final-year project on autonomous warehouse sorting took first place '
                'against entries from thirty-one teams.',
        'image': 'img/news-robotics.jpg',
        'alt': 'Engineers collaborating on a robotics project inside a workshop',
    },
    {
        'title': 'Teaching Hospital Partnership Signed for Clinical Training',
        'category': 'Partnership',
        'date': datetime.date(2026, 8, 22),
        'text': 'The agreement guarantees supervised clinical placements for medical '
                'students from their third year onward.',
        'image': 'img/news-clinical.jpg',
        'alt': 'Medical students in white coats discussing notes in a hospital hallway',
    },
]

# --- Section 7: events ------------------------------------------------------
EVENTS = [
    {
        'title': 'Annual Convocation Ceremony',
        'date': datetime.date(2026, 10, 14),
        'time': '10:00 AM',
        'venue': 'Grand Auditorium',
        'text': 'Awarding of degrees to the graduating cohorts of 2026.',
    },
    {
        'title': 'International Research Colloquium',
        'date': datetime.date(2026, 10, 22),
        'time': '9:30 AM',
        'venue': 'Seminar Block A',
        'text': 'Invited speakers from six countries across science, law and policy.',
    },
    {
        'title': 'Career Fair and Internship Drive',
        'date': datetime.date(2026, 11, 8),
        'time': '11:00 AM',
        'venue': 'Exhibition Grounds',
        'text': 'Open to final-year students and recent graduates. Registration required.',
    },
    {
        'title': 'Inter-Faculty Cultural Week',
        'date': datetime.date(2026, 11, 19),
        'time': '4:00 PM',
        'venue': 'Open Air Theatre',
        'text': 'Seven days of performances, exhibitions and the inter-faculty finale.',
    },
]

# --- Leadership messages -----------------------------------------------------
# This is a demonstration site. The people, offices and statements below are
# fictional and must not be read as the words of any real person or office.
# The Chancellor is shown as the President of Bangladesh holding the
# cancellership, which is the constitutional pattern for public universities in
# the country; the officeholder is deliberately left unnamed. The portraits are
# generic stock photography - see static/img/ATTRIBUTIONS.md.
LEADERS = [
    {
        'name': 'His Excellency the President',
        'role': 'Chancellor',
        'office': "President of the People's Republic of Bangladesh",
        'portrait': 'img/chancellor.jpg',
        'alt': 'Portrait of the Chancellor of Jholo University',
        'message': (
            'It is a privilege to serve as Chancellor of Jholo University, and the '
            'office carries a plain responsibility: that the institution remains '
            'answerable to the students who study within these walls and to the '
            'communities that surround it. A university earns its standing slowly, '
            'in classrooms, laboratories and clinics rather than in announcements. '
            'The founding conviction of Jholo has been that a student should be '
            'known by the teachers who teach them, and that a degree should mean '
            'something to those who later employ its holder. That conviction has '
            'not changed as we have grown, and it will not change in the decades '
            'ahead.'
        ),
    },
    {
        'name': 'Prof. Dr. Anwarul Kabir',
        'role': 'Vice-Chancellor',
        'office': None,
        'portrait': 'img/vice-chancellor.jpg',
        'alt': 'Portrait of the Vice-Chancellor of Jholo University',
        'message': (
            'Our task each year is unglamorous and exacting: keep lecture groups '
            'small, keep assessment honest, and keep every programme current with '
            'the work our graduates will actually do. Our teaching staff hold '
            'terminal degrees, our programmes carry real laboratory and field '
            'work, and our twelve research centres stay close to regional '
            'industry. Those are the commitments I would ask you to hold us to.'
        ),
    },
]

# --- Mission and vision ------------------------------------------------------
# Shown on the homepage directly under the About section. Fictional, like the
# rest of this file - nothing here is a statement of any real institution.
# Icons are 24x24 stroke paths, same convention as QUICK_LINKS.
MISSION_VISION = [
    {
        'label': 'Our Mission',
        'title': 'Teach honestly, research usefully',
        'icon': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM12 13a1 1 0 1 0 0-2 1 1 0 0 0 0 2z',
        'text': (
            'To teach honestly and research usefully, so that a graduate of this '
            'university is trusted to do real work in the field they trained in.'
        ),
        'points': [
            'Small lecture groups, taught by staff who hold terminal degrees',
            'Every programme carries a substantial project or clinical component',
            'Research directed at questions the region actually has open',
        ],
    },
    {
        'label': 'Our Vision',
        'title': 'Judgement as well as degrees',
        'icon': 'M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7zM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z',
        'text': (
            'A university the region looks to for judgement as much as for '
            'diplomas &mdash; known for teaching that holds up outside the '
            'classroom, and for graduates who keep learning after they leave.'
        ),
        'points': [
            'Programmes reviewed externally every five years against current practice',
            'Library, career services and counselling open to every student',
            'A graduate network that reaches far beyond the region',
        ],
    },
]

# --- Section 9: statistics --------------------------------------------------
STATS = [
    {'value': 4200, 'label': 'Students enrolled'},
    {'value': 180, 'label': 'Faculty members'},
    {'value': 38, 'label': 'Degree programmes'},
    {'value': 12, 'label': 'Research centres'},
]
