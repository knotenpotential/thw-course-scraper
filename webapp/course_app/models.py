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
class TrainingBlueprintModel(TimeStampMixin):
    short_name = models.CharField(max_length=20, db_index=True)
    long_name = models.CharField(max_length=255)
    complete_name = models.CharField(max_length=255)
    participants = models.TextField()
    prerequisites = models.TextField()
    goal = models.TextField()
    content = models.TextField()

    @staticmethod
    def from_dict(dic):
        record = TrainingBlueprintModel(short_name=dic["short_name"],
                                        long_name=dic["long_name"],
                                        complete_name=dic["complete_name"],
                                        participants=dic["participants"],
                                        prerequisites=dic["prerequisites"],
                                        goal=dic["goal"],
                                        content=dic["content"])
        return record

    def update_by_dict(self, dic):
        self.short_name = dic["short_name"]
        self.long_name = dic["long_name"]
        self.complete_name = dic["complete_name"]
        self.participants = dic["participants"]
        self.prerequisites = dic["prerequisites"]
        self.goal = dic["goal"]
        self.content = dic["content"]

    # ToDo: add validator for dict


# Class for storing concrete training instances that are derived from the blueprint
class TrainingDateModel(TimeStampMixin):
    training = models.ForeignKey(TrainingBlueprintModel, on_delete=models.DO_NOTHING)  # When a blueprint is deleted
    # (e.g. because the training is no longer offered), the historic trainings should not be deleted
    training_short_name = models.CharField(max_length=20, db_index=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    deadline = models.DateField()
