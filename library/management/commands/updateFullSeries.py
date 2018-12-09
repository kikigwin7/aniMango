import library.models

def updateValues():
    series_objects  = library.Series.objects.filter()
    for series_object in series_objects:
        print(series_object.api_id)
