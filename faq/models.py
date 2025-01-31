from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from .redis_handler import RedisHandler

translator = Translator()

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    
    def save(self, *args, **kwargs):
       
        super().save(*args, **kwargs)

    def get_translated_question(self, lang='en'):
        
    
        cache_key = f'faq_{self.id}_{lang}'
        cached_question = RedisHandler().get_cache(cache_key)
        
        if cached_question:
            return cached_question

    
        try:
            if lang != 'en':  
                translated_question = translator.translate(self.question, src='en', dest=lang).text
            else:
                translated_question = self.question 
            

            RedisHandler().set_cache(cache_key, translated_question)
            
            return translated_question

        except Exception as e:

            return self.question 

    def __str__(self):
        return self.question
