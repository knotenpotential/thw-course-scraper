from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('api/add_blueprint/', views.add_blueprint, name='add_blueprint'),
]