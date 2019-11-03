from statistics import mode

def check_punc(word):
    for i in word:
        if i in ".?!":
            return True
    return False

def sec_from_word(word):
    return word["startTimeSeconds"] + (word["startTimeNanos"] / 10**9)

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
                    time.append(sec_from_word(row))
                else:
                    sentence = sentence + " " + word
                    time.append(sec_from_word(row))
                    sentences.append(sentence.strip())
                    times.append(time[-1] - time[0])
                    sentence = ""
                    time = []

            if len(time) > 0:
                sentences.append(sentence.strip())
                times.append(time[-1] - time[0])

    return sentences, times

def sentence_by_speaker(data):
    """
    Return transcript as pairs of sentences and their speakers.

    Args:
        data: A dictionary containing raw speech to text data.
      
    Returns:
        A list of dictionaries which contain the sentence and its speaker. 
    """
    
    sentences, times = format_times(data)

    sentence_by_speaker = [0]*len(sentences) 
    
    s = 0
    speakers = []   
    for word in data[-1]['words']:
        if s < len(sentences):
            if word['word'] in sentences[s]:
                speakers.append(word['speakerTag'])
            else:
                if speakers == []:
                    sentence_by_speaker[s] = 1
                else:
                    sentence_by_speaker[s] = mode(speakers)
                speakers = []
                s += 1
    return [dict(zip(['sentence', 'key'], i)) for i in list(zip(sentences, 
            sentence_by_speaker))]