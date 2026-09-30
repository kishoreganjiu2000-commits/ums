"""
Views for the notice board.

ListView handles pagination. DetailView handles a single notice. The download
view exists so templates never link straight at MEDIA_URL - when media moves to
object storage, only this file changes.
"""

from django.http import FileResponse, Http404
from django.views.generic import DetailView, ListView

from .forms import NoticeSearchForm
from .models import Notice


class NoticeListView(ListView):
    model = Notice
    template_name = 'notice/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 10

    def get_queryset(self):
        self.form = NoticeSearchForm(self.request.GET)

        queryset = Notice.objects.published().select_related('category')
        queryset = self.form.get_filtered_notices(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['result_count'] = context['paginator'].count
        return context


class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'notice/notice_detail.html'
    context_object_name = 'notice'

    def get_queryset(self):
        # Drafts stay invisible: a direct URL must not reveal an unpublished
        # notice.
        return Notice.objects.published().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        published = Notice.objects.published().select_related('category')

        newest = published.filter(
            published_date__lte=self.object.published_date
        ).exclude(pk=self.object.pk)
        oldest = published.filter(
            published_date__gt=self.object.published_date
        ).exclude(pk=self.object.pk)

        context['newer_notice'] = newest.first()
        context['older_notice'] = oldest.last()

        # Checked here (one file per detail page) so the template never shows a
        # download button for a file that is not really there.
        context['file_available'] = bool(
            self.object.attachment
            and self.object.attachment.storage.exists(self.object.attachment.name)
        )

        return context


def notice_download(request, slug):
    """Stream the PDF with a download filename."""
    notice = Notice.objects.published().filter(slug=slug).first()

    if notice is None or not notice.has_attachment:
        raise Http404('That notice has no downloadable file.')

    # The row can point at a file that was removed from the media directory
    # (manual cleanup, failed upload, moved storage). A missing file is a
    # missing notice as far as the visitor is concerned, not a server error.
    if not notice.attachment.storage.exists(notice.attachment.name):
        raise Http404('That file is no longer available.')

    return FileResponse(
        notice.attachment.open('rb'),
        as_attachment=True,
        filename=notice.attachment.name.rsplit('/', 1)[-1],
        content_type='application/pdf',
    )
