from django.contrib import admin

from .models import Notice, NoticeCategory


@admin.register(NoticeCategory)
class NoticeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'notice_count')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

    @admin.display(description='Notices')
    def notice_count(self, obj):
        return obj.notices.count()


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'reference_code',
        'category',
        'published_date',
        'has_pdf',
        'is_pinned',
        'is_published',
    )
    list_display_links = ('title',)
    list_filter = ('category', 'is_published', 'is_pinned', 'published_date')
    search_fields = ('title', 'description', 'reference_code')
    list_editable = ('is_pinned', 'is_published')
    date_hierarchy = 'published_date'
    ordering = ('-is_pinned', '-published_date')
    save_on_top = True

    fieldsets = (
        ('Notice', {'fields': ('title', 'slug', 'category', 'description')}),
        ('Official details', {'fields': ('reference_code', 'published_date')}),
        ('Attachment', {'fields': ('attachment',)}),
        ('Visibility', {'fields': ('is_published', 'is_pinned')}),
    )
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(boolean=True, description='PDF')
    def has_pdf(self, obj):
        return obj.has_attachment

    def save_model(self, request, obj, form, change):
        # The admin prepopulates the slug, but typing the title is more
        # common - fill it in when left blank.
        if not obj.slug:
            from django.utils.text import slugify

            obj.slug = slugify(obj.title)[:220]

        super().save_model(request, obj, form, change)
