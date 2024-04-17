import unittest
from app import app, db, Note

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_page_post(self):
        response = self.app.post('/', data={'title': 'Test Note', 'content': 'This is a test note.'}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_view_note(self):
        with app.app_context():
            note = Note(title='Test Title', content='Test Content')
            db.session.add(note)
            db.session.commit()
            note_id = note.id

        response = self.app.get(f'/view/{note_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Title', response.data)
        self.assertIn(b'Test Content', response.data)

    def test_update_note(self):
        with app.app_context():
            note = Note(title='Initial Title', content='Initial Content')
            db.session.add(note)
            db.session.commit()
            note_id = note.id

        response = self.app.post(f'/update/{note_id}', data={'title': 'Updated Title', 'content': 'Updated Content'}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_delete_note(self):
        with app.app_context():
            note = Note(title='Test Title', content='Test Content')
            db.session.add(note)
            db.session.commit()
            note_id = note.id

        response = self.app.get(f'/delete/{note_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test Title', response.data)

if __name__ == '__main__':
    unittest.main()
