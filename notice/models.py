"""
Models for the notice board.

Two models only. NoticeCategory exists so categories can be renamed or hidden
from the admin without touching every notice.
"""

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

MAX_ATTACHMENT_MB = 10


class NoticeCategory(models.Model):
    """A grouping such as Examination, Admission, Research or Campus."""

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(
        default=True,
        help_text='Uncheck to hide this category from the public filter list without deleting its notices.',
    )
    order = models.PositiveSmallIntegerField(
        default=0, help_text='Lower numbers appear first in the filter dropdown.'
    )

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Notice categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class NoticeQuerySet(models.QuerySet):
    def published(self):
        """Notices visible to the public. Drafts never reach a visitor."""
        return self.filter(is_published=True)

    def board_order(self):
        """Pinned notices first, then newest."""
        return self.order_by('-is_pinned', '-published_date', '-id')


class Notice(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        NoticeCategory,
        on_delete=models.PROTECT,
        related_name='notices',
        help_text='Cannot be deleted while notices still use it.',
    )
    description = models.TextField(help_text='Full text shown on the notice page.')

    reference_code = models.CharField(
        max_length=40,
        unique=True,
        blank=True,
        null=True,
        help_text='Optional official code, for example JU/REG/2026/041.',
    )

    published_date = models.DateField(help_text='The date printed on the notice.')

    attachment = models.FileField(
        upload_to='notices/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf'])],
        help_text='Optional PDF. Maximum {} MB.'.format(MAX_ATTACHMENT_MB),
    )

    is_published = models.BooleanField(
        default=True, help_text='Uncheck to hide from the public notice board.'
    )
    is_pinned = models.BooleanField(
        default=False, help_text='Pinned notices stay at the top of the list.'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NoticeQuerySet.as_manager()

    class Meta:
        ordering = ['-is_pinned', '-published_date', '-id']
        verbose_name = 'notice'
        verbose_name_plural = 'notices'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.attachment:
            size_mb = self.attachment.size / (1024 * 1024)
            if size_mb > MAX_ATTACHMENT_MB:
                raise ValidationError(
                    {'attachment': 'File is {:.1f} MB. Maximum is {} MB.'.format(
                        size_mb, MAX_ATTACHMENT_MB
                    )}
                )

    def get_absolute_url(self):
        return reverse('notice:notice_detail', kwargs={'slug': self.slug})

    @property
    def has_attachment(self):
        return bool(self.attachment)
