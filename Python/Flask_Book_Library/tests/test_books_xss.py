import unittest

from project import app, db
from project.books.models import Book


class AddBookXssTest(unittest.TestCase):
    def setUp(self):
        self.marker = f"<script>/* xss */</script>"
        self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            Book.query.filter_by(name=self.marker).delete()
            db.session.commit()

    def test_added_book_name_is_rendered_escaped(self):
        response = self.client.post(
            "/books/create",
            json={
                "name": self.marker,
                "author": "Test Author",
                "year_published": 2024,
                "book_type": "2days",
            },
        )

        self.assertEqual(response.status_code, 302)

        page = self.client.get("/books/")

        self.assertEqual(page.status_code, 200)
        self.assertNotIn(self.marker.encode(), page.data)


if __name__ == "__main__":
    unittest.main()