from datetime import date

# return 0 = Monday, 1 = Tuesday ... 6 = Sunday
def get_day_of_week(datetime_slot):
    year, month, day, slot = map(int, datetime_slot.strip().split('-'))
    d = date(year, month, day)
    return d.weekday()
