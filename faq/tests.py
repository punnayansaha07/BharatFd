from django.test import TestCase
from .models import FAQ
from googletrans import Translator

translator = Translator()

class FAQTestCase(TestCase):
    def setUp(self):
        self.faq_english = FAQ.objects.create(
            question="Can I get an interview chance in BharatFD?", 
            answer="Hopefully yes."
        )

    def test_dynamic_translation(self):
        faq = FAQ.objects.get(question="Can I get an interview chance in BharatFD?")

        translated_hi = faq.get_translated_question('hi')
        self.assertEqual(translated_hi, translator.translate("Can I get an interview chance in BharatFD?", src='en', dest='hi').text)

        translated_bn = faq.get_translated_question('bn')
        self.assertEqual(translated_bn, translator.translate("Can I get an interview chance in BharatFD?", src='en', dest='bn').text)

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
