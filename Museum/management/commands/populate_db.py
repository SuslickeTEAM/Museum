import random
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image

from Museum.models import Category, Event, Exhibit


class Command(BaseCommand):
    help = "Populates the database with demo data"

    def handle(self, *args, **kwargs):
        # Create some categories
        category_names = ["Art", "History", "Science", "Nature", "Technology"]
        categories = []
        for name in category_names:
            category = Category.objects.create(
                title=name, image=self.get_dummy_image("category", (400, 300))
            )
            categories.append(category)

        # Create some events
        for i in range(5):
            Event.objects.create(image=self.get_dummy_image("event", (600, 400)))

        # Create some exhibits
        exhibit_titles = [
            "Dinosaur Fossil",
            "Ancient Sculpture",
            "Space Shuttle Model",
            "Impressionist Painting",
            "Medieval Armor",
        ]
        for title in exhibit_titles:
            Exhibit.objects.create(
                title=title,
                image=self.get_dummy_image("exhibit", (800, 600)),
                description=f"Description for {title}",
                audio=None,  # Optional: Add audio files if needed
                category=random.choice(categories),
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated the database with demo data."))

    def get_dummy_image(self, image_type, size):
        """
        Generates a dummy image and returns it as a Django file-like object.
        """
        img = Image.new(
            "RGB",
            size,
            color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        )
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return ContentFile(buffer.getvalue(), f"{image_type}.png")
