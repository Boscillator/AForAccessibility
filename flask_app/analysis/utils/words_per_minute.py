def words_per_minute(data, pause_thresh=10**10, window=10**10):
    """
    Calculate the words per minute for a given text.

    Args:
        data: A dictionary containing speech to text data.
        pause_thresh: The minimum time to wait before recognizing the gap as a 
            pause.
        window: the time resolution at which the instantaneous words per minute
            is calculated.
      
    Returns:
        out: A dictionary where the key is the speaker id. The value of each
            dictionary contains a list of dictionaries where each dictionary
            represents a segment where the speaker was speaking without 
            pausing. Each dictionary contains various metrics for that segment. 
    """
    out = {}  
    for word in data[-1]['words']:
        if word['speakerTag'] not in out:
            out[word['speakerTag']] = [{'first':-1, 'last':0, 'words':0, 
               'wpm':0, 'i_wpm':[0], 'steps':[0]}]
        if ((word['startTimeSeconds']*10**9 + word['startTimeNanos'] 
        - out[word['speakerTag']][-1]['last']) > pause_thresh) and (out[word['speakerTag']][-1]['first'] != -1):
            out[word['speakerTag']].append({'first':-1, 'last':0, 'words':0, 
               'wpm':0, 'i_wpm':[0], 'steps':[0]})
        if out[word['speakerTag']][-1]['first'] == -1:
            out[word['speakerTag']][-1]['first'] = word['startTimeSeconds']*10**9 + word['startTimeNanos']
        out[word['speakerTag']][-1]['last'] = word['endTimeSeconds']*10**9 + word['endTimeNanos']
        out[word['speakerTag']][-1]['words'] += 1
        
        out[word['speakerTag']][-1]['steps'][-1] += ((word['endTimeSeconds']*10**9 + word['endTimeNanos']) - 
           (word['startTimeSeconds']*10**9 + word['startTimeNanos']))
        out[word['speakerTag']][-1]['i_wpm'][-1] += 1
        if out[word['speakerTag']][-1]['steps'][-1] > window:
            out[word['speakerTag']][-1]['i_wpm'][-1] = (out[word['speakerTag']][-1]['i_wpm'][-1]/
               (out[word['speakerTag']][-1]['steps'][-1]/(60*10**9)))
            out[word['speakerTag']][-1]['steps'][-1] = word['endTimeSeconds']*10**9 + word['endTimeNanos']
            out[word['speakerTag']][-1]['steps'].append(0)
            out[word['speakerTag']][-1]['i_wpm'].append(0)
    for speaker in out:
        for temp in out[speaker]:
            temp['wpm'] = temp['words']/((temp['last'] - temp['first'])/(60*10**9))
            temp['steps'].pop()
            temp['i_wpm'].pop()
            
    return out