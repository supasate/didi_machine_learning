def mape_score(label_gaps, predicted_gaps):
    if len(label_gaps) < 1:
        return None

    score = 0
    if label_gaps[0] is list:
        num_district = len(label_gaps)
        num_timeslot = len(label_gaps[0])
        score = 0
        for d in range(num_district):
            for t in range(num_timeslot):
                score += abs((label_gaps[d][t] - predicted_gaps[d][t]) / float(label_gaps[d][t]))
        score = score / (num_district * num_timeslot)
    else:
        for i in range(len(label_gaps)):
            score += abs((label_gaps[i] - predicted_gaps[i]) / float(label_gaps[i]))
        score = score / len(label_gaps)
    return score
