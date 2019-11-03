from utils.sentence_by_speaker import sentence_by_speaker
from utils.complexity import complexity
from utils.words_per_minute import words_per_minute
from utils.get_line_chart_json import get_line_chart_json
from utils.topic_cohesion import topic_cohesion
from utils.entity_extraction import entity_extraction
import json

def reformat_theme(data, type_id, title):
    return {"type": type_id, "wide": "true", "title": title, "options": data}

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
    comp = get_line_chart_json(complexity(data), title='Complexity over time', 
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

    return [reformat_theme(sbs, "transcript", "Sentence by Speaker"), reformat_theme(wpm, "highchart", "Words per Minute"), reformat_theme(comp, "highchart", "Complexity"), reformat_theme(tc, "highchart", "Topic Focus"), reformat_theme(ee, "highchart", "Entity Wordcloud")]