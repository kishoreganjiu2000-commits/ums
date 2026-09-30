"""
Search and filter form for the notice board.

Keeping this in a form rather than reading request.GET directly in the view
means the field types, the category choices and the year list are all defined
in one place, and the same object renders the filter controls.
"""

from django import forms

from .models import Notice, NoticeCategory


class NoticeSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search title, description or reference…',
                'type': 'search',
            }
        ),
    )

    category = forms.ModelChoiceField(
        required=False,
        label='Category',
        queryset=NoticeCategory.objects.none(),
        empty_label='All categories',
        # Match on slug so the filter URL stays readable (?category=examination)
        # instead of exposing database ids.
        to_field_name='slug',
    )

    year = forms.ChoiceField(
        required=False,
        label='Year',
        choices=[('', 'All years')],
        widget=forms.Select(attrs={'aria-label': 'Filter by year'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = NoticeCategory.objects.filter(is_active=True)

        # Built from published notices so the dropdown never offers a year
        # with no results.
        years = (
            Notice.objects.published()
            .values_list('published_date__year', flat=True)
            .distinct()
            .order_by('-published_date__year')
        )
        self.fields['year'].choices = [('', 'All years')] + [
            (str(y), str(y)) for y in years
        ]

    def get_filtered_notices(self, queryset):
        """Apply search and filters to a queryset."""
        if not self.is_valid():
            # Bad input in the URL (an unknown category or year) must not
            # quietly fall back to "show everything" - that looks like the
            # filter was ignored. Show nothing and let the form report why.
            return queryset.none()

        data = self.cleaned_data

        keyword = data.get('q')
        if keyword:
            queryset = queryset.filter(
                models_q(keyword)
            )

        category = data.get('category')
        if category:
            queryset = queryset.filter(category=category)

        year = data.get('year')
        if year:
            queryset = queryset.filter(published_date__year=year)

        return queryset.board_order()

    def has_query(self):
        """True when the visitor has searched or filtered, not just loaded."""
        return any(
            self.data.get(key) for key in ('q', 'category', 'year')
        )


def models_q(keyword):
    """Case-insensitive match across the fields a visitor would expect."""
    from django.db.models import Q

    return (
        Q(title__icontains=keyword)
        | Q(description__icontains=keyword)
        | Q(reference_code__icontains=keyword)
    )
