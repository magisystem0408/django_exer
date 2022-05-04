from django.contrib import admin
from .models import Question,Choice

# データベースを登録
admin.site.register(Question)
admin.site.register(Choice)
