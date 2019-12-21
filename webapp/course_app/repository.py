from .models import TrainingBlueprintModel, TrainingDateModel

# Return codes
UPDATED = "UPDATED"
CREATED = "CREATED"
ERROR = "ERROR"

SUCCESS_CODES = {UPDATED, CREATED}


# ToDo: Avoid race conditions
def upsert_blueprint_from_dict(dic):
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
        return UPDATED
    else:
        try:
            record = TrainingBlueprintModel.from_dict(dic)
            record.save()
        except Exception:
            return ERROR
        return CREATED
