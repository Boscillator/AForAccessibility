import nltk
from statistics import mode

def sentence_by_speaker(data):
    """
    Return transcript as pairs of sentences and their speakers.

    Args:
        data: A dictionary containing raw speech to text data.
      
    Returns:
        A list of dictionaries which contain the sentence and its speaker. 
    """
    
    transcript = ''
    for i in range(len(data)):
        transcript += data[i]['transcript']
    
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(transcript.strip())
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