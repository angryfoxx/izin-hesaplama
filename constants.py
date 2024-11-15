from datetime import date

from convertdate import islamic

TODAY = date.today()
CURRENT_YEAR = TODAY.year
NEXT_YEAR = CURRENT_YEAR + 1
CURR_ISLAMIC_YEAR, CURR_ISLAMIC_MONTH, _ = islamic.from_gregorian(
    TODAY.year, TODAY.month, TODAY.day
)
