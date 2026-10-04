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
    {'label': 'About', 'url_name': 'core:about'},
    {'label': 'Administration', 'url_name': 'core:administration', 'children': [
        {'label': 'Vice-Chancellor', 'url_name': 'core:vice_chancellor'},
        {'label': 'Pro Vice-Chancellor', 'url_name': 'core:about'},
        {'label': 'Registrar', 'url_name': 'core:about'},
        {'label': 'Director (Finance and Accounts)', 'url_name': 'core:about'},
        {'label': 'Director (Planning and Development)', 'url_name': 'core:research'},
        {'label': 'Other Offices', 'url_name': 'core:contact'},
    ]},
    {'label': 'Academics', 'url_name': 'core:academics'},
    {'label': 'Admission', 'url_name': 'core:admission'},
    {'label': 'Research', 'url_name': 'core:research'},
    {'label': 'Students', 'url_name': 'core:students'},
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
            item['children'] = []
            for child in entry['children']:
                child_item = {'label': child['label']}
                if 'url_name' in child:
                    child_item['url'] = reverse(child['url_name'])
                    child_item['name'] = child['url_name'].split(':')[-1]
                elif 'url' in child:
                    child_item['url'] = child['url']
                    child_item['name'] = child['label'].lower().replace(' ', '-')
                item['children'].append(child_item)

        items.append(item)

    return items


SITE_NAV = _build_nav()


def site_info(request):
    """University name, tagline, contact details and the navigation tree."""
    return {
        'SITE_NAME': 'Lakshmipur Science and Technology',
        'SITE_SHORT_NAME': 'Lakshmipur Science and Technology',
        'SITE_TAGLINE': '',
        'SITE_PHONE': '+880 1700 000000',
        'SITE_EMAIL': 'info@jholouniversity.edu',
        'SITE_ADDRESS': 'Lakshmipur Science and Technology, University Road, Lakshmipur',
        'SITE_NAV': SITE_NAV,
    }
