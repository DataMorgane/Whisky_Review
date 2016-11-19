from django.contrib import admin
from .models import Whisky, Review

# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('whisky', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']

admin.site.register(Whisky)
admin.site.register(Review, ReviewAdmin)
