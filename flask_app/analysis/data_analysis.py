from analysis.utils.sentence_by_speaker import sentence_by_speaker
from analysis.utils.complexity import complexity
from analysis.utils.words_per_minute import words_per_minute
from analysis.utils.get_line_chart_json import get_line_chart_json, get_complexity_line_chart
from analysis.utils.topic_cohesion import topic_cohesion
from analysis.utils.entity_extraction import entity_extraction

import numpy as np

import json
import traceback

def get_avg_wpm(wpm):
    wpm_list = []
    for speaker in wpm:
        if len(wpm) < 2:
            continue
        data = np.array(wpm[speaker])
        wpm_list.append(np.mean(data[:,1]))
    avg_wpm = sum(wpm_list) / len(wpm_list)
    return {"type": "bigtext", "title": "Avg WPM", "body": '{}'.format(int(avg_wpm)), "wide": False, "tip": "Word comprehension begins to gradually decline above speeds of 150 wpm, and completely falls off above 250 wpm. We recommend you keep your average wpm below 150 wpm!"}

def get_tot_comp(comp):
    return {"type": "bigtext", "title": "Total Complexity", "body": '{}'.format(comp), "wide": False, "tip": "Student readability is maximized between the complexity values of 5 and 14. Anything greater than this range will result in a drop of overall understanding of your lecture!"}

def get_tot_pauses(wpm, threshold=5):
    pauses = 0
    for speaker in wpm:
        data = np.array(wpm[speaker])[:, 1]
        pauses += len(data[data <= threshold])
    return {"type": "bigtext", "title": "Total Pauses", "body": '{}'.format(pauses), "wide": False, "tip": "Pauses break up a lecture, giving students time to gather their thoughts and notes. We encourage you to take more pauses the longer your lecture is!"}

def reformat_theme(data, type_id, title):
    return {"type": type_id, "wide": "true", "title": title, "options": data}

def reformat_pie(data, type_id, title):
    return {"type": type_id, "wide": False, "title": title, "options": data}

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
        tc = topic_cohesion(data)
        ret.append(reformat_pie(tc, "highchart", "Topic Focus"))
    except:
        traceback.print_exc()

    wpm_data = None
    try:
        wpm_data = words_per_minute(data)
        wpm = get_line_chart_json(wpm_data, title='Words per minute',
                                  y_label='Words per minute', x_label='Time (s)')
        ret.append(reformat_theme(wpm, "highchart", "Words per Minute"))
        ret.append(get_avg_wpm(wpm_data))
    except:
        traceback.print_exc()

    try:
        comp_data, tot_comp = complexity(data)
        comp = get_complexity_line_chart(comp_data, title='Complexity over time',
                                         y_label='Complexity', x_label='Time (s)')
        ret.append(reformat_theme(comp, "highchart", "Complexity"))
        ret.append(get_tot_pauses(wpm_data))
        ret.append(get_tot_comp(tot_comp))
    except:
        traceback.print_exc()
        
    # try:
    #    ee = entity_extraction(data)
    #    ret.append(reformat_theme(ee, "highchart", "Entity Wordcloud"))
    # except:
    #    traceback.print_exc()

    return ret

if __name__ == "__main__":
    with open('../../../accessibility/analysis/data/Useful_Idiots_Sanders_Interview.json') as json_file:
        data = json.load(json_file)

    test = data_analysis(data)
    print(test)