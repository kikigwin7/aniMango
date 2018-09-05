import time
import gspread

from django.core.management.base import BaseCommand, CommandError
from oauth2client.service_account import ServiceAccountCredentials
from anilist_api.anilist import get_series_by_name
from library.models import Series, Item
from django.db import IntegrityError


def getSpreadsheetData():
    # Load in the scope and the details of API credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('library/management/commands/authdetails.json', scope)
    client = gspread.authorize(creds)

    # Select the right spreadsheet and the sheet that the data is on
    sheet = client.open("Library list Current").sheet1

    # Return the values that we need for later
    # [0] = Name of series, [1] = Type of series, [2] = If we can find this series or not, [3] = Volume number
    listOfTitles = [sheet.col_values(1), sheet.col_values(2), sheet.col_values(3), sheet.col_values(4)]
    return listOfTitles


# Updates the spreadsheet at the specified position
def updateSheet(x, y, value):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('library/management/commands/authdetails.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Library list Current").sheet1
    print(value)
    sheet.update_cell(y, x, value)


class Command(BaseCommand):
    help = 'Adds the library spreadsheet to the site'

    def handle(self, *args, **options):
        listOfTitles = getSpreadsheetData()

        # This should loop through the spreadsheet and add the value into the library after getting details from anilist
        for x in range(0, 107):
            title = listOfTitles[0][x]
            type = listOfTitles[1][x].lower()
            # Sleep for a short period of time to ensure we do not get rate limited... Running time for this command
            # is fairly slow as a result of this.
            time.sleep(.25)

            # Check if we have already added the series into the site:

            try:
                # Creates a series object and gets the ID of the series from the anilist API (data entry done by same
                #  as autofill)
                series = Series()
                series.auto_populate_data = True
                series.ani_link = "https://anilist.co/{0!s}/{1!s}".format(type,
                                                                          get_series_by_name(type, title)[0]['id'])

                try:
                    series.save()
                    print("Added " + series.ani_link)
                    # Create an item and add this item into the site
                    itemToAdd = Item()
                    itemToAdd.parent_series = series
                    itemToAdd.name = "Vol " + listOfTitles[3][x];
                    if type == "anime":
                        itemToAdd.media_type = "DVD"
                    else:
                        itemToAdd.media_type = "Manga"
                    itemToAdd.save()


                except IntegrityError as e:
                    # If the series already exists, we will search for it and set series to be the value of it
                    # ensuring we have a valid entry for the parent_series value
                    print("Failed to add " + series.ani_link + "! Duplicate entry!")
            except RuntimeError as e:
                # Update the sheet stating that the series could not be found on anilist and manual entry is required
                updateSheet(3, x + 1, "Could not find series - Manual Entry required!")
            except KeyError as e:
                updateSheet(3, x + 1, "Could not find series - Manual Entry required!")
