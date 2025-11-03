"""
Django admin configuration for Museum application with Unfold theme.
"""

from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Category, Event, Exhibit


@admin.register(Event)
class EventAdmin(ModelAdmin):
    """Admin interface for Event model."""

    list_display = ("title", "is_active", "created_at", "image_preview")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "image_preview")
    list_per_page = 20

    fieldsets = (
        (None, {"fields": ("title", "description", "image", "image_preview")}),
        ("Настройки", {"fields": ("is_active",)}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def image_preview(self, obj: Event) -> str:
        """Display image preview in admin."""
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Предпросмотр"


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """Admin interface for Category model."""

    list_display = ("title", "slug", "order", "exhibits_count", "created_at", "image_preview")
    list_filter = ("created_at",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "exhibits_count", "image_preview")
    list_editable = ("order",)
    list_per_page = 20

    fieldsets = (
        (None, {"fields": ("title", "slug", "description", "image", "image_preview")}),
        ("Настройки", {"fields": ("order",)}),
        ("Статистика", {"fields": ("exhibits_count",), "classes": ("collapse",)}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def image_preview(self, obj: Category) -> str:
        """Display image preview in admin."""
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Предпросмотр"

    def exhibits_count(self, obj: Category) -> int:
        """Display number of exhibits in category."""
        return obj.get_exhibits_count()

    exhibits_count.short_description = "Количество экспонатов"

    def get_queryset(self, request):
        """Optimize queryset with annotated counts."""
        queryset = super().get_queryset(request)
        return queryset.annotate(exhibit_count=Count("exhibits"))


@admin.register(Exhibit)
class ExhibitAdmin(ModelAdmin):
    """Admin interface for Exhibit model."""

    list_display = (
        "title",
        "category",
        "is_featured",
        "view_count",
        "has_audio",
        "created_at",
        "image_preview",
    )
    list_filter = ("category", "is_featured", "created_at")
    search_fields = ("title", "description")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "view_count", "image_preview", "audio_preview")
    list_editable = ("is_featured",)
    list_per_page = 20
    autocomplete_fields = ()

    fieldsets = (
        (None, {"fields": ("title", "category", "description")}),
        ("Медиа", {"fields": ("image", "image_preview", "audio", "audio_preview")}),
        ("Настройки", {"fields": ("is_featured",)}),
        ("Статистика", {"fields": ("view_count",), "classes": ("collapse",)}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def image_preview(self, obj: Exhibit) -> str:
        """Display image preview in admin."""
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Предпросмотр"

    def audio_preview(self, obj: Exhibit) -> str:
        """Display audio player in admin."""
        if obj.audio:
            return format_html('<audio controls src="{}"></audio>', obj.audio.url)
        return "Нет аудио"

    audio_preview.short_description = "Аудиогид"

    def has_audio(self, obj: Exhibit) -> bool:
        """Check if exhibit has audio guide."""
        return bool(obj.audio)

    has_audio.short_description = "Есть аудио"
    has_audio.boolean = True


# Customize admin site headers
admin.site.site_header = "Музей Боевой Славы - Администрирование"
admin.site.site_title = "Музей Боевой Славы"
admin.site.index_title = "Управление контентом"
