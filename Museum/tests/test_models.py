"""
Tests for Museum models.
"""

from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from Museum.models import Category, Event, Exhibit


def create_test_image(width: int = 100, height: int = 100) -> SimpleUploadedFile:
    """
    Create a test image file.

    Args:
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        SimpleUploadedFile with image data
    """
    file = BytesIO()
    image = Image.new("RGB", (width, height), color="red")
    image.save(file, "jpeg")
    file.seek(0)
    return SimpleUploadedFile("test.jpg", file.getvalue(), content_type="image/jpeg")


class EventModelTest(TestCase):
    """Test cases for Event model."""

    def setUp(self) -> None:
        """Set up test data."""
        self.event = Event.objects.create(
            title="Test Event",
            description="Test event description",
            image=create_test_image(),
        )

    def test_event_creation(self) -> None:
        """Test that event is created correctly."""
        self.assertEqual(self.event.title, "Test Event")
        self.assertEqual(self.event.description, "Test event description")
        self.assertTrue(self.event.is_active)
        self.assertIsNotNone(self.event.created_at)

    def test_event_str(self) -> None:
        """Test event string representation."""
        self.assertEqual(str(self.event), "Test Event")

    def test_event_repr(self) -> None:
        """Test event repr representation."""
        repr_str = repr(self.event)
        self.assertIn("Event", repr_str)
        self.assertIn("Test Event", repr_str)


class CategoryModelTest(TestCase):
    """Test cases for Category model."""

    def setUp(self) -> None:
        """Set up test data."""
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            description="Test category description",
            image=create_test_image(),
            order=1,
        )

    def test_category_creation(self) -> None:
        """Test that category is created correctly."""
        self.assertEqual(self.category.title, "Test Category")
        self.assertEqual(self.category.slug, "test-category")
        self.assertEqual(self.category.description, "Test category description")
        self.assertEqual(self.category.order, 1)

    def test_category_str(self) -> None:
        """Test category string representation."""
        self.assertEqual(str(self.category), "Test Category")

    def test_category_repr(self) -> None:
        """Test category repr representation."""
        repr_str = repr(self.category)
        self.assertIn("Category", repr_str)
        self.assertIn("test-category", repr_str)

    def test_get_exhibits_count(self) -> None:
        """Test getting exhibit count for category."""
        self.assertEqual(self.category.get_exhibits_count(), 0)

        # Add an exhibit
        Exhibit.objects.create(
            title="Test Exhibit",
            image=create_test_image(),
            description="Test description",
            category=self.category,
        )

        self.assertEqual(self.category.get_exhibits_count(), 1)


class ExhibitModelTest(TestCase):
    """Test cases for Exhibit model."""

    def setUp(self) -> None:
        """Set up test data."""
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            image=create_test_image(),
        )

        self.exhibit = Exhibit.objects.create(
            title="Test Exhibit",
            image=create_test_image(),
            description="Test exhibit description",
            category=self.category,
        )

    def test_exhibit_creation(self) -> None:
        """Test that exhibit is created correctly."""
        self.assertEqual(self.exhibit.title, "Test Exhibit")
        self.assertEqual(self.exhibit.description, "Test exhibit description")
        self.assertEqual(self.exhibit.category, self.category)
        self.assertFalse(self.exhibit.is_featured)
        self.assertEqual(self.exhibit.view_count, 0)

    def test_exhibit_str(self) -> None:
        """Test exhibit string representation."""
        self.assertEqual(str(self.exhibit), "Test Exhibit")

    def test_exhibit_repr(self) -> None:
        """Test exhibit repr representation."""
        repr_str = repr(self.exhibit)
        self.assertIn("Exhibit", repr_str)
        self.assertIn("Test Exhibit", repr_str)

    def test_exhibit_with_audio(self) -> None:
        """Test exhibit with audio file."""
        audio_file = SimpleUploadedFile("test.mp3", b"audio content", content_type="audio/mpeg")

        exhibit_with_audio = Exhibit.objects.create(
            title="Exhibit with Audio",
            image=create_test_image(),
            description="Description",
            audio=audio_file,
            category=self.category,
        )

        self.assertTrue(bool(exhibit_with_audio.audio))

    def test_related_name(self) -> None:
        """Test that related name works correctly."""
        exhibits = self.category.exhibits.all()
        self.assertEqual(exhibits.count(), 1)
        self.assertEqual(exhibits.first(), self.exhibit)
