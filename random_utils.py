import csv
import random


def get_random_terms(k):
    """Will retrieve k random terms"""
    with open('dic.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        wordlist = [row["Word"].lower() for row in reader]
    return random.choices(wordlist, k=k)