def targetFeatureSplit(data):
    target = []
    features = []
    for item in date:
        target.append(item[len(item) - 1])
        features.append(item[: -1])

    return target, features
