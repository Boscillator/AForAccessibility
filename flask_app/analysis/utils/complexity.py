import string
import json
import re

def dale_chall_score(words, sentences, characters):
    return round(4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43)

def check_punc(word):
    for i in word:
        if i in ".?!":
            return True
    return False

def tot_complexity(data):
    transcript = ""
    for row in data:
        if len(row["transcript"]) > 0:
            transcript = transcript + " " + row["transcript"]

    sentences, time_range = format_times(data)

    words = transcript.split(" ")

    sent_count = len(sentences)
    word_count = len(words)

    filtered_text = re.sub(r'[^\w\s]', '', transcript)
    filtered_text = filtered_text.replace(" ", "").lower()
    character_count = len(filtered_text)

    return dale_chall_score(word_count, sent_count, character_count)

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
        sentences.append(sentence)
        times.append(time[-1] - time[0])

    return sentences, times

def complexity(data, window=30):
    transcript = ""
    for row in data:
        if len(row["transcript"]) > 0:
            transcript = transcript + " " + row["transcript"]

    sentences, time_range = format_times(data)
    t = 0
    t_temp = 0
    comp = []
    t_w_count = 0
    t_s_count = 0
    t_transcript = ""
    for i in range(len(time_range)):
        t += time_range[i]
        t_temp += time_range[i]
        t_s_count += 1
        t_w_count += len(sentences[i].split(" "))
        t_transcript += " " + sentences[i]
        if t_temp >= window:
            filtered_text = re.sub(r'[^\w\s]', '', t_transcript)
            filtered_text = filtered_text.replace(" ", "").lower()
            character_count = len(filtered_text)

            comp.append([t, dale_chall_score(t_w_count, 
                                                   t_s_count, character_count)])
            
            t_w_count = 0
            t_s_count = 0
            t_temp = 0
            t_transcript = ""

    return comp, tot_complexity(data)