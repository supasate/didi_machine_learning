def get_time_slot(datetime):
    date, time = datetime.split()
    hh, mm, ss = map(int, time.split(':'))
    cum_minutes = (hh * 60) + mm + 1
    return date + '-' + str(cum_minutes / 10)
