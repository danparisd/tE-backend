from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from models import Take, Language, Book, User, Comment

view_set_url = 'http://127.0.0.1:8000/api/exclude_files/'
my_file = 'en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class ExcludedFileViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.take_object = Take(location=my_file, chapter=5, is_export=True, is_source=False, id=1, language_id=1,
                                book_id=1, user_id=1)
        self.language_object = Language(slug='en-x-demo', name='english', id=1)
        self.book_object = Book(name='english', booknum=5, id=1)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment(location='/test-location/', id=1)

    def test_post_method_for_excluded_file_view_set(self):
        """Unit Testing the method for handling POST requests to the API at the Excluded File View URL"""
        # populating our temporary database
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.comment_object.save()
        self.take_object.save()
        response = self.client.post(view_set_url, {'chapter': 5}, format='json')
        result = str(response.data)  # convert data returned from post request to string so we can checkthe data inside
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)  # testing that we get the correct status response from the API
        self.assertNotEqual(0, len(response.data))  # testing that we do not get an empty response from the api
        self.assertIn(my_file, result)  # test that data returned matches location of file
        # cleaning out our temporary database
        self.language_object.delete()
        self.book_object.delete()
        self.user_object.delete()
        self.comment_object.delete()
        self.take_object.delete()
