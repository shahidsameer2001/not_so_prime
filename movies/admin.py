from django.contrib import admin
from .models import Movie, NoticeBoard,Series,SeriesVideo,Questions

admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(SeriesVideo)
admin.site.register(Questions)
admin.site.register(NoticeBoard)