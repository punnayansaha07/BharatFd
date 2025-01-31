from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from .redis_handler import RedisHandler

translator = Translator()

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.question_hi:
            self.question_hi = translator.translate(self.question, src='en', dest='hi').text
        if not self.question_bn:
            self.question_bn = translator.translate(self.question, src='en', dest='bn').text
        super().save(*args, **kwargs)

    def get_translated_question(self, lang):

        cache_key = f'faq_{self.id}_{lang}'
        cached_question = RedisHandler().get_cache(cache_key)
        
        if cached_question:
            return cached_question
        else:
        
            translated_question = getattr(self, f'question_{lang}', self.question)
            RedisHandler().set_cache(cache_key, translated_question)
            return translated_question

    def __str__(self):
        return self.question
