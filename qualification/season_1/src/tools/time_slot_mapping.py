def get_datetime_slot(datetime, slot_duration_in_minute):
    date, time = datetime.strip().split()
    hh, mm, ss = map(int, time.split(':'))
    cum_minutes = (hh * 60) + mm + 1
    return date + '-' + str((cum_minutes / slot_duration_in_minute) + 1)
