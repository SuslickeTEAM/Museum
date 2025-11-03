"""
Museum application views.

This module contains view functions for displaying museum content.
"""

import logging
from typing import Any

from django.db.models import Prefetch, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Event, Exhibit

logger = logging.getLogger(__name__)


def main(request: HttpRequest) -> HttpResponse:
    """
    Render the main homepage with categories and events.

    Displays:
    - All exhibition categories with their associated exhibits (prefetched)
    - Active events/news items

    Args:
        request: HTTP request object

    Returns:
        Rendered homepage template
    """
    try:
        # Prefetch related exhibits for each category to minimize DB queries
        categories: QuerySet[Category] = Category.objects.prefetch_related(
            Prefetch(
                "exhibits",
                queryset=Exhibit.objects.select_related("category").order_by("-created_at"),
            )
        ).all()

        # Only show active events, ordered by creation date
        events: QuerySet[Event] = Event.objects.filter(is_active=True).order_by("-created_at")

        context: dict[str, Any] = {
            "categories": categories,
            "events": events,
        }

        logger.debug(
            f"Main page loaded with {categories.count()} categories and {events.count()} events"
        )

        return render(request, "main.html", context)

    except Exception as e:
        logger.error(f"Error loading main page: {e}", exc_info=True)
        # Re-raise to let Django's error handling take over
        raise


def exhibits(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Render exhibits page for a specific category.

    Displays all exhibits belonging to the specified category.

    Args:
        request: HTTP request object
        pk: Primary key of the category

    Returns:
        Rendered exhibits template

    Raises:
        Http404: If category with given pk does not exist
    """
    try:
        # Get category or return 404 if not found
        category: Category = get_object_or_404(Category, pk=pk)

        # Get all exhibits for this category with optimized query
        exhibits_list: QuerySet[Exhibit] = (
            Exhibit.objects.filter(category=pk).select_related("category").order_by("-created_at")
        )

        # Count exhibits with audio
        exhibits_with_audio = exhibits_list.exclude(audio="").count()

        context: dict[str, Any] = {
            "exhibits": exhibits_list,
            "category": category,
            "exhibits_with_audio": exhibits_with_audio,
        }

        logger.debug(
            f"Exhibits page loaded for category '{category.title}' with {exhibits_list.count()} exhibits"
        )

        return render(request, "exhibitions.html", context)

    except Category.DoesNotExist:
        logger.warning(f"Category with pk={pk} not found")
        raise

    except Exception as e:
        logger.error(f"Error loading exhibits page for category {pk}: {e}", exc_info=True)
        raise
