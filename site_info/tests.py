from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase, Client

from news.models import Article
from events.models import Event

# Create your tests here.
class GetHomeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Home_user_asbibvsidb', email='Home_user_asbibvsidb@mail.com', password='alsdgbil136381bvilabb')
        self.article = Article.objects.create(title="Test", content="Lorem ipsum", article_type="News", created_by=self.user)
        self.event = Event.objects.create(title="test_event", subtitle="TestSubtitle", when = timezone.now() + timedelta(days=365),
            where="Test_place", details="Test details", max_signups=20, signups_open=timezone.now() + timedelta(days=1), signups_close=timezone.now() + timedelta(days=360)
        )
        
    def test_get_home(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        
    def tearDown(self):
        self.event.delete()
        self.article.delete()
        self.user.delete()