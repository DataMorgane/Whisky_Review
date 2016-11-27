import sys, os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Whisky_Review.settings")

import django

django.setup()

from reviews.models import Whisky


def save_whisky_from_row(whisky_row):
    whisky = Whisky()
    whisky.id = whisky_row[0]
    whisky.name = whisky_row[1]
    whisky.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        whiskys_df = pd.read_csv(sys.argv[1])
        print(whiskys_df)

        whiskys_df.apply(
            save_whisky_from_row,
            axis=1
        )

        print
        "There are {} whiskies".format(Whisky.objects.count())

    else:
        print
        "Please, provide whisky file path"