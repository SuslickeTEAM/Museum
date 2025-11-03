"""
Tests for Museum views.
"""

from django.test import Client, TestCase
from django.urls import reverse

from Museum.models import Category, Event, Exhibit
from Museum.tests.test_models import create_test_image


class MainViewTest(TestCase):
    """Test cases for main view."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            image=create_test_image(),
        )
        self.event = Event.objects.create(
            title="Test Event",
            image=create_test_image(),
            is_active=True,
        )

    def test_main_view_status(self) -> None:
        """Test that main view returns 200 status code."""
        response = self.client.get(reverse("museum:main"))
        self.assertEqual(response.status_code, 200)

    def test_main_view_template(self) -> None:
        """Test that main view uses correct template."""
        response = self.client.get(reverse("museum:main"))
        self.assertTemplateUsed(response, "main.html")

    def test_main_view_context(self) -> None:
        """Test that main view context contains required data."""
        response = self.client.get(reverse("museum:main"))
        self.assertIn("categories", response.context)
        self.assertIn("events", response.context)

    def test_main_view_shows_active_events(self) -> None:
        """Test that only active events are shown."""
        # Create inactive event
        Event.objects.create(
            title="Inactive Event",
            image=create_test_image(),
            is_active=False,
        )

        response = self.client.get(reverse("museum:main"))
        events = response.context["events"]

        self.assertEqual(len(events), 1)
        self.assertTrue(all(event.is_active for event in events))


class ExhibitsViewTest(TestCase):
    """Test cases for exhibits view."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            image=create_test_image(),
        )
        self.exhibit = Exhibit.objects.create(
            title="Test Exhibit",
            image=create_test_image(),
            description="Test description",
            category=self.category,
        )

    def test_exhibits_view_status(self) -> None:
        """Test that exhibits view returns 200 status code."""
        response = self.client.get(reverse("museum:exhibits", kwargs={"pk": self.category.pk}))
        self.assertEqual(response.status_code, 200)

    def test_exhibits_view_template(self) -> None:
        """Test that exhibits view uses correct template."""
        response = self.client.get(reverse("museum:exhibits", kwargs={"pk": self.category.pk}))
        self.assertTemplateUsed(response, "exhibitions.html")

    def test_exhibits_view_context(self) -> None:
        """Test that exhibits view context contains required data."""
        response = self.client.get(reverse("museum:exhibits", kwargs={"pk": self.category.pk}))
        self.assertIn("exhibits", response.context)
        self.assertIn("category", response.context)

    def test_exhibits_view_shows_correct_exhibits(self) -> None:
        """Test that only exhibits from the correct category are shown."""
        # Create another category with exhibit
        other_category = Category.objects.create(
            title="Other Category",
            slug="other-category",
            image=create_test_image(),
        )
        Exhibit.objects.create(
            title="Other Exhibit",
            image=create_test_image(),
            description="Other description",
            category=other_category,
        )

        response = self.client.get(reverse("museum:exhibits", kwargs={"pk": self.category.pk}))
        exhibits = response.context["exhibits"]

        self.assertEqual(len(exhibits), 1)
        self.assertEqual(exhibits[0].category, self.category)

    def test_exhibits_view_404_for_nonexistent_category(self) -> None:
        """Test that exhibits view returns 404 for nonexistent category."""
        response = self.client.get(reverse("museum:exhibits", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)
