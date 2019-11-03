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
    tc = topic_cohesion(data)
    ee = entity_extraction(data)

    sbs = sentence_by_speaker(data)
    wpm = words_per_minute(data)
    comp = get_complexity_line_chart(complexity(data), title='Complexity over time', 
            y_label='Complexity', x_label='Time (s)')
    
    line_chart_data = []
    for speaker in wpm:
        temp_list = []
        for segment in wpm[speaker]:
            temp_list += [list(i) for i in zip(
                    [x / (60*10**9) for x in segment['steps']], segment['i_wpm'])]
        line_chart_data.append(temp_list)
        
    wpm = get_line_chart_json(line_chart_data, title='Words per minute', 
            y_label='Words per minute', x_label='Time (min)')
    
    ret = []
    try:
        ret.append(reformat_transcript(sbs, "transcript", "Sentence by Speaker"))
    except:
        traceback.print_exc()
    try:
        ret.append(reformat_theme(wpm, "highchart", "Words per Minute"))
    except:
        traceback.print_exc()
    try:
        ret.append(reformat_theme(comp, "highchart", "Complexity"))
    except:
        traceback.print_exc()
    try:
        ret.append(reformat_theme(tc, "highchart", "Topic Focus"))
    except:
        traceback.print_exc()
    #try:
    #    ret.append(reformat_theme(ee, "highchart", "Entity Wordcloud"))
    #except:
    #    traceback.print_exc()

    return ret