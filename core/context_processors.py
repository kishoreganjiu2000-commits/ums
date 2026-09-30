"""
Context processors for the core app.

Registered in config/settings.py under TEMPLATES['OPTIONS']['context_processors'],
so anything returned here is available in every template without each view
having to pass it through.
"""

from django.urls import reverse

# ---------------------------------------------------------------------------
# Navigation
#
# One entry per page. The header is rendered from this list instead of
# hardcoded markup, so adding a page means adding a dict here.
#
# Keys:
#   label     text shown in the bar
#   url_name  name from urls.py, resolved to a path here
#   children  optional dropdown items; omit for a plain link
#
# Only "News & Events" gets a dropdown, because it covers two pages. Every
# other item is a single page, so a submenu would only repeat its own link.
# ---------------------------------------------------------------------------
NAV_ITEMS = [
    {'label': 'Home', 'url_name': 'core:home'},
    {'label': 'About', 'url_name': 'core:about'},
    {'label': 'Academics', 'url_name': 'core:academics'},
    {'label': 'Admission', 'url_name': 'core:admission'},
    {'label': 'Research', 'url_name': 'core:research'},
    {'label': 'Students', 'url_name': 'core:students'},
    {'label': 'News & Events', 'url_name': 'core:news_events'},
    {'label': 'Notice', 'url_name': 'notice:notice_list'},
    {'label': 'Contact', 'url_name': 'core:contact'},
]


def _build_nav():
    """Resolve URL names to paths and attach ids for dropdown triggers.

    Runs once at import rather than per request - the result is constant.
    """
    items = []

    for entry in NAV_ITEMS:
        item = {'label': entry['label']}

        # A dropdown parent has no url of its own
        if 'url_name' in entry:
            item['url'] = reverse(entry['url_name'])
            # Bare name, for comparing against request.resolver_match.url_name,
            # which strips the namespace
            item['name'] = entry['url_name'].split(':')[-1]

        if 'children' in entry:
            item['id'] = 'subnav-{}'.format(entry['label'].lower().replace(' ', '-').replace('&', 'and'))
            item['children'] = [
                {
                    'label': child['label'],
                    'url': reverse(child['url_name']),
                    'name': child['url_name'].split(':')[-1],
                }
                for child in entry['children']
            ]

        items.append(item)

    return items


SITE_NAV = _build_nav()


def site_info(request):
    """University name, tagline, contact details and the navigation tree."""
    return {
        'SITE_NAME': 'Jholo University',
        'SITE_SHORT_NAME': 'JU',
        'SITE_TAGLINE': 'Knowledge in Motion',
        'SITE_PHONE': '+880 1700 000000',
        'SITE_EMAIL': 'info@jholouniversity.edu',
        'SITE_ADDRESS': 'Jholo University, University Road, Jholo City',
        'SITE_NAV': SITE_NAV,
    }
