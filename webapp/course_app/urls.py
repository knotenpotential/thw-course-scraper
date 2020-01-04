from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('api/add_blueprints/', views.add_blueprints, name='add_blueprints'),
    path('api/add_trainings/', views.add_training_dates, name='add_trainings'),
    path('api/add_scrape/', views.add_scrape, name='add_scrape')
]
