"""
Views for the core app.

Most sections are static pages and need no view beyond the TemplateView
declared inline in urls.py. Only the homepage has real work to do, because it
assembles content from several places.

The homepage currently reads from core/demo_data.py. In Phase 4 the Notice
query replaces the notices lookup - one line changes, the template does not.
"""

from django.views.generic import TemplateView

from notice.models import Notice

from . import demo_data

# Sections that exist as a URL but have no page built yet. Every one of them
# answers with the same "under development" page instead of a 500, so a visitor
# who follows any button in the header, footer or homepage gets a real page.
PENDING_SECTIONS = {
    'about': (
        'About',
        'Our history, leadership, governance and the people who make Jholo '
        'University what it is.',
    ),
    'academics': (
        'Academics',
        'All 38 degree programmes across six faculties, with curriculum, '
        'duration and credit details.',
    ),
    'admission': (
        'Admission',
        'Application deadlines, eligibility, tuition and the full scholarship '
        'table.',
    ),
    'research': (
        'Research',
        'Our twelve research centres, funding, publications and industry '
        'partnerships.',
    ),
    'students': (
        'Students',
        'Library, accommodation, career services, counselling and the student '
        'portal.',
    ),
    'news_events': (
        'News &amp; Events',
        'The university newsroom, press releases and the full events calendar.',
    ),
    'career': (
        'Careers',
        'Open positions across faculty and administration, and how to apply.',
    ),
    'contact': (
        'Contact',
        'Campus address, department directory, admissions helpline and the '
        'contact form.',
    ),
}


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'quick_links': demo_data.QUICK_LINKS,
            'programs': demo_data.PROGRAMS,
            # Real query. Pins first, then newest.
            'notices': Notice.objects.published().select_related('category').board_order()[:3],
            'news': demo_data.NEWS[:3],
            'events': demo_data.EVENTS[:3],
            'leaders': demo_data.LEADERS,
            'places': demo_data.PLACES,
            'mission_vision': demo_data.MISSION_VISION,
            'stats': demo_data.STATS,
        })

        return context


class ComingSoonView(TemplateView):
    """
    Placeholder for a section whose page has not been written yet.

    Serving this instead of a missing template means no link in the site can
    produce a server error, and the visitor always lands on something that
    looks deliberate. When the real page is ready, point the URL at it and
    delete the entry from PENDING_SECTIONS.
    """

    template_name = 'core/coming_soon.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title, summary = PENDING_SECTIONS.get(
            kwargs.get('section'),
            ('This page', 'Content is on the way.'),
        )

        context['page_title'] = title
        context['page_summary'] = summary

        return context


class ViceChancellorView(TemplateView):
    """
    The Vice-Chancellor's own page, linked from Administration in the header.

    Reads the same VICE_CHANCELLOR dict the homepage carousel does, so the short
    quote there and the full speech here are one text rather than two.
    """

    template_name = 'core/vice_chancellor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vc'] = demo_data.VICE_CHANCELLOR
        context['vc_recent_notices'] = Notice.objects.published().board_order()[:3]

        return context
