from django.db import transaction
import datetime

from .models import TrainingBlueprintModel, LastMinuteSeatScrapeModel, LastMinuteSeatsModel, \
    HistoricLastMinuteSeatsModel

# Return codes
OK = "OK"
ERROR = "ERROR"

SUCCESS_CODES = {OK}


# ToDo: Avoid race conditions
def upsert_blueprints_from_dict(json_data):
    for dic in json_data:
        if "short_name" not in dic:
            return ERROR
        query_set = TrainingBlueprintModel.objects.filter(short_name=dic["short_name"])
        if query_set:
            record = query_set.first()
            try:
                record.update_by_dict(dic)
                record.save()
            except Exception:
                return ERROR
        else:
            try:
                record = TrainingBlueprintModel.from_dict(dic)
                record.save()
            except Exception:
                return ERROR


def add_new_last_minute_seat_scrape_from_dic(dic):
    try:
        with transaction.atomic():
            # First, archive all last minute seat records that refer to expired trainings
            # This keeps our table small.
            LastMinuteSeatsModel.archive_seats_of_expired_trainings()

            # Next, create a new scrape
            scrape = LastMinuteSeatScrapeModel.from_dict(dic)
            scrape.save()

            # Use the scrape data to update existing records of last minute seats
            # We start by fetching all last minute seats currently in the database
            last_minute_seat_training_name_to_record = {}
            for existing_last_minute_seat_record in LastMinuteSeatsModel.objects.all():
                last_minute_seat_training_name_to_record[existing_last_minute_seat_record.training.pk] = \
                    last_minute_seat_training_name_to_record

            # Iterate through all last minute seats fetched in the current scrape
            # and create records for them if they are different from the existing records (or no previous record exists)
            for last_minute_seat in dic["last_minute"]:
                new_record = LastMinuteSeatsModel.from_dict(last_minute_seat)

                # If we currently have a record for the same training in the database, we update it if necessary.
                # That is, we move it to the historical records and save the new one instead.
                if new_record.training.pk in last_minute_seat_training_name_to_record:
                    old_record = last_minute_seat_training_name_to_record.pop(new_record.training.pk)
                    if old_record.num_seats != new_record.num_seats:
                        historic_record = HistoricLastMinuteSeatsModel.from_last_minute_seat(old_record)
                        historic_record.save()
                        old_record.delete()
                        new_record.save()
                else:
                    # otherwise, we do not currently have an entry for last minute seats for this training, so we
                    # just save
                    new_record.save()

            # Finally, check the remaining records in the database. If a record is present in the database
            # but missing in the new scrape data, no seats are available. So we should update the data by adding a new
            # record with a value of 0.
            # The dictionary only contains records that were missing previously, so we can just add them to the
            # database
            for existing_last_minute_seat in last_minute_seat_training_name_to_record.values():
                historic_record = HistoricLastMinuteSeatsModel.from_last_minute_seat(existing_last_minute_seat)
                historic_record.save()
                existing_last_minute_seat.scrape_id = scrape
                existing_last_minute_seat.num_seats = 0
                existing_last_minute_seat.save()
    except Exception as err:
        raise err
        # ToDo: Cleanup
        return ERROR
    return OK
