from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('api/add-blueprints/', views.add_blueprints, name='add_blueprints'),
    path('api/add-trainings/', views.add_training_dates, name='add_trainings'),
    path('api/add-scrape/', views.add_scrape, name='add_scrape'),
    path('api/get-blueprints/', views.get_training_blueprints, name='get_training_blueprints')
]
