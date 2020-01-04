import arrow
from django.db import models
from .datetime_util import iso_ts_to_naive_utc


# Mixin to add automatic creation and edit date fields to our model.
# Source: https://stackoverflow.com/questions/3429878/automatic-creation-date-for-django-model-form-objects


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scraped_at = models.DateTimeField()

    class Meta:
        abstract = True


# Class for storing training blueprints such as
# https://www.thw-ausbildungszentrum.de/SharedDocs/Lehrgaenge/THW-BuS/DE/LG_1_663.html?nn=6228646
class TrainingBlueprintModel(TimeStampMixin):
    short_name = models.CharField(max_length=20, primary_key=True)
    long_name = models.CharField(max_length=255)
    complete_name = models.CharField(max_length=255)
    content = models.TextField()

    @staticmethod
    def from_dict(dic):
        scraped_at = iso_ts_to_naive_utc(dic["scraped_at"])
        record = TrainingBlueprintModel(short_name=dic["short_name"],
                                        long_name=dic["long_name"],
                                        complete_name=dic["complete_name"],
                                        content=dic["content"],
                                        scraped_at=scraped_at)
        return record

    def update_by_dict(self, dic):
        self.short_name = dic["short_name"]
        self.long_name = dic["long_name"]
        self.complete_name = dic["complete_name"]
        self.content = dic["content"]

    @staticmethod
    def get_by_short_name(short_name):
        return TrainingBlueprintModel.objects.get(short_name=short_name)

    # ToDo: add validator for dict


# Class for storing concrete training instances that are derived from the blueprint
class TrainingDateModel(TimeStampMixin):
    training_short_name = models.CharField(max_length=20, db_index=True, primary_key=True)  # Like N 047/20
    blueprint = models.ForeignKey(TrainingBlueprintModel, on_delete=models.DO_NOTHING)  # When a blueprint is deleted
    # (e.g. because the training is no longer offered), the historic trainings should not be deleted
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    deadline = models.DateField()

    def is_expired(self):
        return self.start_time < arrow.utcnow()

    @staticmethod
    def from_dict(dic):
        scraped_at = iso_ts_to_naive_utc(dic["scraped_at"])
        blueprint = TrainingBlueprintModel.get_by_short_name(dic["blueprint"])
        record = TrainingDateModel(training_short_name=dic["training_short_name"],
                                   blueprint=blueprint,
                                   start_time=iso_ts_to_naive_utc(dic["start_time"]),
                                   end_time=iso_ts_to_naive_utc(dic["end_time"]),
                                   deadline=dic["deadline"],
                                   scraped_at=scraped_at)
        return record

    @staticmethod
    def get_by_short_name(short_name):
        return TrainingDateModel.objects.get(training_short_name=short_name)


class LastMinuteSeatScrapeModel(TimeStampMixin):

    @staticmethod
    def from_dict(dic):
        scraped_at = iso_ts_to_naive_utc(dic["scraped_at"])
        record = LastMinuteSeatScrapeModel(scraped_at=scraped_at)
        return record


class LastMinuteSeatsModel(TimeStampMixin):
    class Meta:
        unique_together = (('training', 'scrape_id'),)
        indexes = [
            models.Index(fields=['training', 'scrape_id']),
        ]

    training = models.ForeignKey(TrainingDateModel, on_delete=models.DO_NOTHING)
    scrape_id = models.ForeignKey(LastMinuteSeatScrapeModel, on_delete=models.DO_NOTHING)
    num_seats = models.IntegerField()
    hyperlink = models.TextField()

    @staticmethod
    def archive_seats_of_expired_trainings():
        prev_scrape = LastMinuteSeatsModel.objects.all()
        for last_minute_seat in prev_scrape:
            training = last_minute_seat.training
            if training.is_expired():
                historic_record = HistoricLastMinuteSeatsModel(training=training,
                                                               scrape_id=last_minute_seat.scrape_id,
                                                               num_seats=last_minute_seat.num_seats)
                historic_record.save()
                last_minute_seat.delete()

    @staticmethod
    def from_dict(dic):
        training = TrainingDateModel.get_by_short_name(dic["short_name"])
        scraped_at = iso_ts_to_naive_utc(dic["scraped_at"])
        scrape_id = dic["scrape_id"]
        num_seats = dic["num_seats"]
        hyperlink = dic["hyperlink"]
        record = LastMinuteSeatsModel(training=training, scrape_id=scrape_id, num_seats=num_seats,
                                      scraped_at=scraped_at, hyperlink=hyperlink)
        return record


class HistoricLastMinuteSeatsModel(TimeStampMixin):
    class Meta:
        unique_together = (('training', 'scrape_id'),)
        indexes = [
            models.Index(fields=['training', 'scrape_id']),
        ]

    training = models.ForeignKey(TrainingDateModel, on_delete=models.DO_NOTHING)
    scrape_id = models.ForeignKey(LastMinuteSeatScrapeModel, on_delete=models.DO_NOTHING)
    num_seats = models.IntegerField()

    @staticmethod
    def from_last_minute_seat(last_minute_seat):
        return HistoricLastMinuteSeatsModel(training=last_minute_seat.training, scrape_id=last_minute_seat.scrape_id,
                                            num_seats=last_minute_seat.num_seats, scraped_at=last_minute_seat.scraped_at)
