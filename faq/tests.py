from django.test import TestCase
from .models import FAQ
from googletrans import Translator
from rest_framework import status
from rest_framework.test import APIClient

translator = Translator()

class FAQTestCase(TestCase):
    def setUp(self):
        # Set up some test data for different languages
        self.faq_english = FAQ.objects.create(
            question="Can I get an interview chance in BharatFD?", 
            answer="Hopefully yes"
        )
        self.client = APIClient()

    def test_dynamic_translation(self):
        faq = FAQ.objects.get(question="Can I get an interview chance in BharatFD?")
        
        translated_hi = faq.get_translated_question('hi')
        self.assertEqual(translated_hi, translator.translate("Can I get an interview chance in BharatFD?", src='en', dest='hi').text)
        translated_sw = faq.get_translated_question('sw')
        self.assertEqual(translated_sw, "Can I get an interview chance in BharatFD?")

    def test_cache_and_fallback(self):
        faq = FAQ.objects.get(question="Can I get an interview chance in BharatFD?")

        translated_hi = faq.get_translated_question('hi')
        self.assertIsNotNone(translated_hi)
        
        translated_hi_cached = faq.get_translated_question('hi')
        self.assertEqual(translated_hi, translated_hi_cached)

        translated_invalid = faq.get_translated_question('zz')
        self.assertEqual(translated_invalid, "Can I get an interview chance in BharatFD?")

    def test_pagination(self):
        for i in range(30):
            FAQ.objects.create(
                question=f"Question {i}", 
                answer="Answer to question"
            )
        
        response = self.client.get('/api/v1/faqs/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)  # Default page size is 20
        self.assertIn('next', response.data)  # Check if pagination includes 'next'

    def test_invalid_language(self):
        response = self.client.get('/api/v1/faqs/?lang=invalidlang')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_invalid_faq_request(self):
        response = self.client.get('/api/v1/faqs/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
