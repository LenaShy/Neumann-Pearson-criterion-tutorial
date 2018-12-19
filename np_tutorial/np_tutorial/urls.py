from django.contrib import admin
from django.urls import path, include

from .views import home_page, button_click

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('choose_method/', button_click, name='button_click'),
    path('tutorial/', include(('tutorial.urls', 'tutorial'), namespace='tutorial')),
]
