import csv
import sys
from itertools import groupby


EVENTS_WEIGHTS = {
    'web': 1.0,
    'email': 1.2,
    'social': 1.5,
    'webinar': 2.0
}


LABELS_CONDITIONS = [
    (lambda s: 75 <= s, 'platinum'),
    (lambda s: 50 <= s < 75, 'gold'),
    (lambda s: 25 <= s < 50, 'silver'),
    (lambda s: s < 25, 'bronze'),
]


def weight_score(event, score):
    return score * EVENTS_WEIGHTS[event]


def get_data(csvpath):
    """
    Returns list of tuples sorted by contact_id and event.

    Example output:

    [('1', 'web', 34.33), ('1', 'email', 3.4)]

    `csvpath` is a path to CSV file.

    Example CSV file:

    1, web, 34.33
    1, email, 3.4
    1, social, 4
    2, webinar, 55.4
    2, social, 15
    """
    with open(csvpath, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, skipinitialspace=True)
        return sorted(csvreader, key=lambda x: (x[0], x[1]))


def get_contact_scores(data):
    """
    Returns summirized and weighted scores for the contacts.

    Example output:

    [('1', 55.4), ('2', 10)]

    `data` is a list of tuples sorted by contact_id and event returned from
    `get_data` method.
    """
    contact_scores = []
    for contact_id, rows in groupby(data, lambda x: x[0]):
        rows = list(rows)
        contact_score = 0
        for event, rows in groupby(rows, lambda x: x[1]):
            score = sum([float(row[2]) for row in rows])
            weighted_score = weight_score(event, score)
            contact_score += weighted_score
        contact_scores.append((contact_id, contact_score))
    return sorted(contact_scores, key=lambda x: x[1])


def get_normalized_scores(contact_scores):
    """
    Returns normalized scores for the contacts.
    """
    normalized_contact_scores = [(contact_scores[0][0], 0)]
    if len(contact_scores) == 1:
        return normalized_contact_scores
    normalization_rate = (contact_scores[-1][1] - contact_scores[0][1]) / 100.0

    for contact, score in contact_scores[1:-1]:
        normalized_score = (score - contact_scores[0][1]) / normalization_rate
        normalized_score = int(round(normalized_score))
        normalized_contact_scores.append((contact, normalized_score))

    normalized_contact_scores.append((contact_scores[-1][0], 100))

    return normalized_contact_scores


def label(score):
    for condition, label in LABELS_CONDITIONS:
        if condition(score):
            return label


def get_labeled_scores(scores):
    lscores = []
    for contact_id, score in scores:
        lscores.append((contact_id, label(score), score))
    return lscores


def print_scores(scores):
    for contact_id, label, score in scores:
        print "%s, %s, %s" % (contact_id, label, score)


def main():
    if len(sys.argv) < 2:
        print 'usage: leadsheets csvfile'
        return
    else:
        csvpath = sys.argv[1]
        data = get_data(csvpath)
        contact_scores = get_contact_scores(data)
        normalized_scores = get_normalized_scores(contact_scores)
        labeled_scores = get_labeled_scores(normalized_scores)
        print_scores(labeled_scores)
