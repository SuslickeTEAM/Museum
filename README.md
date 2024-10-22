```markdown
# Museum Website

Welcome to the **Museum Website** project! This web application is dedicated to showcasing exhibits from the museum named after Oleg Pozdnyakov. It allows users to explore categories, view exhibits, listen to audio tours, and get the latest updates about the museum.

## Features

- **Dynamic Exhibit Pages**: Displays various museum exhibits with images, descriptions, and audio tours.
- **Category Browsing**: Allows users to browse through different exhibit categories.
- **Responsive Design**: Fully responsive and mobile-friendly, ensuring a seamless experience across devices.
- **Audio Support**: Integrated audio guides for exhibits.
- **Carousel for Updates**: A dynamic carousel displaying the latest updates about museum events and exhibitions.

## Tech Stack

- **Backend**: [Django](https://www.djangoproject.com/) (Python)
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Database**: SQLite (default for development)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SuslickeTEAM/Museum
   cd Museum
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your browser and go to `http://127.0.0.1:8000/`.

## Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add some new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## Contact

For inquiries or support, reach out to:
- [SuslickeTEAM GitHub](https://github.com/SuslickeTEAM/Museum)
- [Lagbag GitHub](https://github.com/Lagbag)
