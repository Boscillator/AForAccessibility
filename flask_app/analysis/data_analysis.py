from analysis.utils.sentence_by_speaker import sentence_by_speaker
from analysis.utils.complexity import complexity
from analysis.utils.words_per_minute import words_per_minute
from analysis.utils.get_line_chart_json import get_line_chart_json, get_complexity_line_chart
from analysis.utils.topic_cohesion import topic_cohesion
from analysis.utils.entity_extraction import entity_extraction
import json
import traceback


def reformat_theme(data, type_id, title):
    return {"type": type_id, "wide": "true", "title": title, "options": data}


def reformat_transcript(data, type_id, title):
    return {"type": type_id, "wide": "true", "title": title, "body": data}


def data_analysis(data):
    """
    Run the various metrics on the transcript.

    Args:
        data: A dictionary containing raw speech to text data.

    """

    ret = []
    try:
        sbs = sentence_by_speaker(data)
        ret.append(reformat_transcript(
            sbs, "transcript", "Sentence by Speaker"))
    except:
        traceback.print_exc()

    try:
        wpm = get_line_chart_json(words_per_minute(data), title='Words per minute',
                                  y_label='Words per minute', x_label='Time (min)')
        ret.append(reformat_theme(wpm, "highchart", "Words per Minute"))
    except:
        traceback.print_exc()

    try:
        comp = get_complexity_line_chart(complexity(data), title='Complexity over time',
                                         y_label='Complexity', x_label='Time (s)')
        ret.append(reformat_theme(comp, "highchart", "Complexity"))
    except:
        traceback.print_exc()

    try:
        tc = topic_cohesion(data)
        ret.append(reformat_theme(tc, "highchart", "Topic Focus"))
    except:
        traceback.print_exc()

    # try:
    #    ee = entity_extraction(data)
    #    ret.append(reformat_theme(ee, "highchart", "Entity Wordcloud"))
    # except:
    #    traceback.print_exc()

    return ret
