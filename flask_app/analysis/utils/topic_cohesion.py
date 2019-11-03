import argparse
import io
import os

import string

from google.cloud import language
import numpy as np
import six

import json

from itertools import zip_longest


def jaccard_similarity(list1, list2):
	s1 = set(list1)
	s2 = set(list2)
	return len(s1.intersection(s2)) / len(s1.union(s2))

def classify(text):
    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)
    response = language_client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        result[category.name] = category.confidence

    return result

def get_chunks(transcript, times):
    for chunk_size in range(2, 10):
        text_chunk = list(grouper(transcript, chunk_size, fillvalue=""))
        time_chunk = list(grouper(times, chunk_size, fillvalue=0))

        text_chunk = [" ".join(x).strip() for x in text_chunk]
        time_chunk = [sum(x) for x in time_chunk]

        good = True
        for row in text_chunk:
            if len(row.split(" ")) < 20:
                good = False
                break
        
        if good:
            break

    return text_chunk, time_chunk

def set_base_category(data):
    for i in range(len(data)):
        category = data[i]["category"].split("/")
        category = [x for x in category if x]
        score = data[i]["score"]
        if "None" in category:
            continue
        else:
            break
    return category, score

def score_cohesion(data):
    base_category, base_score = set_base_category(data)
    base_category.append("None")

    categories = [base_category[0]]
    tot_score = [1]
    for i in range(1, len(data)):
        new_category = data[i]["category"].split("/")
        new_category = [x for x in new_category if x]
        new_score = data[i]["score"]
        
        overlap = jaccard_similarity(base_category, new_category)

        if overlap > 0:
            tot_score.append(1)
            categories.append(base_category[0])
        else:
            tot_score.append(0)
            categories.append(new_category[0])

    return tot_score, categories

def check_punc(word):
    for i in word:
        if i in ".?!":
            return True
    return False

def format_times(data):
    sentences = []
    times = []
    for section in data:
        if len(section["transcript"]) > 0:
            sentence = ""
            time = []
            for row in section["words"]:
                word = row["word"]
                if not check_punc(word):
                    sentence = sentence + " " + word
                    time.append(row["startTimeSeconds"] + (row["startTimeNanos"] / 1000000000))
                else:
                    sentence = sentence + " " + word
                    time.append(row["endTimeSeconds"] + (row["endTimeNanos"] / 1000000000))
                    sentences.append(sentence.strip())
                    times.append(time[-1] - time[0])
                    sentence = ""
                    time = []

            if len(time) > 0:
                sentences.append(sentence.strip())
                times.append(time[-1] - time[0])

    return sentences, times

def generate_pie_chart(times, categories):
    data_theme = {
            "name": 'Topics',
            "colorByPoint": "true",
            "data": []
        }

    times = np.array(times)
    times = (times / np.sum(times)) * 100

    aggregate = {}
    for i in range(len(categories)):
        if categories[i] not in aggregate:
            aggregate[categories[i]] = times[i]
        else:
            aggregate[categories[i]] += times[i]

    data = []
    for category in aggregate:
        data.append({"name": category, "y": aggregate[category]})

    data[0]["sliced"] = "true"
    data[0]["selected"] = "true"

    data_theme["data"] = data

    theme = {
            "chart": {
                "plotBackgroundColor": "#ffffff",
                "plotBorderWidth": "null",
                "plotShadow": "false",
                "type": 'pie'
            },
            "title": {
                "text": 'Topic Focus'
            },
            "tooltip": {
                "pointFormat": '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            "plotOptions": {
                "pie": {
                    "allowPointSelect": "true",
                    "cursor": 'pointer',
                    "dataLabels": {
                        "enabled": "false"
                    },
                    "showInLegend": "true"
                }
            },
            "series": [data_theme]
        }

    return theme


def topic_cohesion(data):
    transcript, time_ranges = format_times(data)

    chunks, time_chunks = get_chunks(transcript, time_ranges)

    results = []
    for chunk in chunks:
        result_dict = classify(chunk)
        result = []
        for category in result_dict:
            result.append({"category": category, "score": result_dict[category]})
        if len(result) > 0:
            results.append(result[0])
        else:
            results.append({"category": "None", "score": 0.0})

    tot_score, categories = score_cohesion(results)
    
    return generate_pie_chart(time_chunks, categories)

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
