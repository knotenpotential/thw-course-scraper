from django.db import models


# Mixin to add automatic creation and edit date fields to our model.
# Source: https://stackoverflow.com/questions/3429878/automatic-creation-date-for-django-model-form-objects
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Class for storing training blueprints such as
# https://www.thw-ausbildungszentrum.de/SharedDocs/Lehrgaenge/THW-BuS/DE/LG_1_663.html?nn=6228646
class TrainingBlueprint(models.Model):
    short_name = models.CharField(max_length=20, db_index=True)
    long_name = models.CharField(max_length=255)
    participants = models.TextField()
    prerequisites = models.TextField()
    goal = models.TextField()
    content = models.TextField()
    last_edit_at = models.DateTimeField(auto_now=True)


# Class for storing concrete training instances that are derived from the blueprint
class TrainingDate(models.Model):
    training = models.ForeignKey(TrainingBlueprint, on_delete=models.DO_NOTHING)  # When a blueprint is deleted (e.g.
    #  because the training is no longer offered), the historic trainigs should not be deleted
    training_id = models.CharField(max_length=20, db_index=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    deadline = models.DateField()
    last_edit_at = models.DateTimeField(auto_now=True)
