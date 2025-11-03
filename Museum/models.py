"""
Museum application models.

This module defines the database models for the Museum application:
- Event: News and announcements
- Category: Exhibit categories
- Exhibit: Museum items with images, descriptions, and audio
"""

import io
from typing import Any

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image


class TimestampedModel(models.Model):
    """Abstract base model with automatic timestamp fields."""

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата создания"), db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        abstract = True


def resize_image(image_field: Any, max_width: int, max_height: int, quality: int = 85) -> None:
    """
    Automatically resize and optimize an image.

    Args:
        image_field: Django ImageField instance
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100)
    """
    if not image_field:
        return

    try:
        img = Image.open(image_field)

        # Convert RGBA to RGB if necessary
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Calculate new dimensions maintaining aspect ratio
        if img.width > max_width or img.height > max_height:
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        # Save to memory buffer
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        # Update the image field
        image_field.save(image_field.name, ContentFile(output.read()), save=False)
    except Exception:
        # If image processing fails, keep the original
        pass


class Event(TimestampedModel):
    """
    Museum events and news announcements.

    Attributes:
        image: Event image (auto-resized to fit within max dimensions)
        title: Event title
        description: Event description
        is_active: Whether the event is currently active
    """

    image = models.ImageField(
        upload_to="media/event/",
        verbose_name=_("Изображение"),
        help_text=_("Изображение будет автоматически оптимизировано"),
    )
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    description = models.TextField(
        blank=True, default="", verbose_name=_("Описание"), help_text=_("Краткое описание события")
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_("Активно"), help_text=_("Отображать событие на сайте")
    )

    class Meta:
        verbose_name = _("Событие")
        verbose_name_plural = _("События")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"<Event(id={self.pk}, title='{self.title}', active={self.is_active})>"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save model with automatic image resizing."""
        # Resize image before saving
        if self.image:
            max_width = getattr(settings, "MAX_IMAGE_WIDTH", 1920)
            max_height = getattr(settings, "MAX_IMAGE_HEIGHT", 1920)
            quality = getattr(settings, "IMAGE_QUALITY", 85)
            resize_image(self.image, max_width, max_height, quality)

        super().save(*args, **kwargs)


class Category(TimestampedModel):
    """
    Exhibition categories for organizing exhibits.

    Attributes:
        title: Category name
        image: Category cover image (auto-resized to fit within max dimensions)
        description: Category description
        slug: URL-friendly identifier
        order: Display order (lower numbers appear first)
    """

    title = models.CharField(max_length=100, verbose_name=_("Название"), unique=True)
    image = models.ImageField(
        upload_to="media/category/",
        verbose_name=_("Изображение"),
        help_text=_("Изображение будет автоматически оптимизировано"),
    )
    description = models.TextField(
        blank=True, default="", verbose_name=_("Описание"), help_text=_("Описание категории")
    )
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("URL"))
    order = models.PositiveIntegerField(
        default=0, verbose_name=_("Порядок"), help_text=_("Порядок отображения (меньше = выше)")
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["order", "title"]
        indexes = [
            models.Index(fields=["order", "title"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"<Category(id={self.pk}, title='{self.title}', slug='{self.slug}')>"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save model with automatic image resizing."""
        # Resize image before saving
        if self.image:
            max_width = getattr(settings, "MAX_IMAGE_WIDTH", 1920)
            max_height = getattr(settings, "MAX_IMAGE_HEIGHT", 1920)
            quality = getattr(settings, "IMAGE_QUALITY", 85)
            resize_image(self.image, max_width, max_height, quality)

        super().save(*args, **kwargs)

    def get_exhibits_count(self) -> int:
        """Return the number of exhibits in this category."""
        return self.exhibits.count()


class Exhibit(TimestampedModel):
    """
    Museum exhibit items.

    Attributes:
        title: Exhibit name
        image: Exhibit image (auto-resized to fit within max dimensions)
        description: Detailed description
        audio: Optional audio guide
        category: Associated category
        is_featured: Whether to feature this exhibit on homepage
        view_count: Number of times this exhibit was viewed
    """

    title = models.CharField(max_length=100, verbose_name=_("Название"))
    image = models.ImageField(
        upload_to="media/exhibit_images/",
        verbose_name=_("Изображение"),
        help_text=_("Изображение будет автоматически оптимизировано"),
    )
    description = models.TextField(
        verbose_name=_("Описание"), help_text=_("Подробное описание экспоната")
    )
    audio = models.FileField(
        upload_to="media/exhibit_audio/",
        null=True,
        blank=True,
        verbose_name=_("Аудиогид"),
        help_text=_("Аудиозапись с описанием экспоната (необязательно)"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("Категория"),
        related_name="exhibits",
        db_index=True,
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Избранное"),
        help_text=_("Отображать на главной странице"),
    )
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("Просмотры"), editable=False)

    class Meta:
        verbose_name = _("Экспонат")
        verbose_name_plural = _("Экспонаты")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["category", "-created_at"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["-view_count"]),
        ]

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return (
            f"<Exhibit(id={self.pk}, title='{self.title}', "
            f"category='{self.category.title}', featured={self.is_featured})>"
        )

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save model with automatic image resizing."""
        # Don't resize if only updating view_count
        update_fields = kwargs.get("update_fields")
        if update_fields and "view_count" in update_fields and len(update_fields) == 1:
            super().save(*args, **kwargs)
            return

        # Resize image before saving
        if self.image:
            max_width = getattr(settings, "MAX_IMAGE_WIDTH", 1920)
            max_height = getattr(settings, "MAX_IMAGE_HEIGHT", 1920)
            quality = getattr(settings, "IMAGE_QUALITY", 85)
            resize_image(self.image, max_width, max_height, quality)

        super().save(*args, **kwargs)

    def increment_view_count(self) -> None:
        """Increment the view count for this exhibit."""
        self.view_count = models.F("view_count") + 1
        self.save(update_fields=["view_count"])
