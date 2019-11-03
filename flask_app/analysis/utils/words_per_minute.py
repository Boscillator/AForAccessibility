

def sec_from_word(word):
    return word["startTimeSeconds"] + (word["startTimeNanos"] / 10**9)


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

    pause_thresh = pause_thresh / 10**9
    window = window / 10**9
    # windows per minute
    win_per_min = 60 / window

    #print(data)

    all_words = data[-1]["words"]
    #for item in data:
    #    all_words += item["words"]

    all_speakers = set([w["speakerTag"] for w in all_words])
    out = {}
    for s in all_speakers:
        words = sorted([w for w in all_words if w["speakerTag"] == s],
                       key=lambda x: x["startTimeSeconds"] + x["startTimeNanos"] / 10**9)
        out[s] = []
        queue = [words[0]]
        for i in range(1, len(words)):
            next_word = words[i]
            word_time = sec_from_word(next_word)
            time_diff = word_time - sec_from_word(queue[0])
            while time_diff > window and len(queue) != 0:
                queue = queue[1:]
                if len(queue) == 0:
                    break
                time_diff = word_time - sec_from_word(queue[0])
            queue.append(next_word)
            out[s].append([word_time, len(queue) * win_per_min])

    return out
