def mape_score(label_gaps, predicted_gaps):
    num_district = len(label_gaps)
    num_timeslot = len(label_gaps[0])
    score = 0
    for d in range(num_district):
        for t in range(num_timeslot):
            score += abs((label_gaps[d][t] - predicted_gaps[d][t]) / float(label_gaps[d][t]))
    score = score / (num_district * num_timeslot)
    return score
