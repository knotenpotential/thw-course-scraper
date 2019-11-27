from django.db import models


# Class for storing training blueprints such as
# https://www.thw-ausbildungszentrum.de/SharedDocs/Lehrgaenge/THW-BuS/DE/LG_1_663.html?nn=6228646
class TrainingBlueprint(models.Model):
    short_name = models.CharField(max_length=20, db_index=True)
    long_name = models.CharField(max_length=255)
    participants = models.TextField()
    prerequisites = models.TextField()
    goal = models.TextField()
    content = models.TextField()


# Class for storing concrete training instances that are derived from the blueprint
class TrainingDate(models.Model):
    training = models.ForeignKey(TrainingBlueprint, on_delete=models.CASCADE)  # Should we cascade here?
    training_id = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    deadline = models.DateField()
