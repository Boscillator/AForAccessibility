from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1 import enums
import io
import json
import traceback


def parse_stt_results(response):
    res = []
    count = 0
    for result in response.results:
        alternative = result.alternatives[0]
        row = {"id": count, "transcript": alternative.transcript, "words": []}
        for word in alternative.words:
            sub_row = {"word": word.word, "startTimeSeconds": word.start_time.seconds, "startTimeNanos": word.start_time.nanos,
                       "endTimeSeconds": word.end_time.seconds, "endTimeNanos": word.end_time.nanos, "speakerTag": word.speaker_tag}
            row["words"].append(sub_row)
        res.append(row)
        count += 1
    return res


def stt_from_uri(storage_uri, sample_rate, channels=2):
    try:
        client = speech_v1p1beta1.SpeechClient()

        language_code = "en-US"
        enable_word_time_offsets = True
        sample_rate_hertz = sample_rate
        enable_automatic_punctuation = True

        enable_speaker_diarization = True
        diarization_speaker_count = 3

        config = {
            "enable_speaker_diarization": enable_speaker_diarization,
            "diarization_speaker_count": diarization_speaker_count,
            "enable_automatic_punctuation": enable_automatic_punctuation,
            "enable_word_time_offsets": enable_word_time_offsets,
            "language_code": language_code,
            "sample_rate_hertz": sample_rate_hertz,
            "audio_channel_count": channels
        }

        audio = {"uri": storage_uri}

        operation = client.long_running_recognize(config, audio)
        response = operation.result()

        odata = parse_stt_results(response)

        return odata
    except Exception as e:
        traceback.print_exc()
