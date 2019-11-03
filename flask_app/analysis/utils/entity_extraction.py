from google.cloud import language_v1
from google.cloud.language_v1 import enums
import json
import numpy as np

def sample_analyze_entities(text_content):
    """
    Analyzing Entities in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    type_ = enums.Document.Type.PLAIN_TEXT

    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)
    
    # ignore_tags = ["COMMON", "NUMBER", "PRICE"]

    entity_list = []
    salience_list = []
    for entity in response.entities:
        tag = ""

        entity_type = enums.Entity.Type(entity.type).name
        if entity_type == "OTHER":
            mention_type = ""
            for mention in entity.mentions:
                mention_type = enums.EntityMention.Type(mention.type).name
                break
            if mention_type != "COMMON":
                tag = entity.name
        else:
            if entity_type != "NUMBER" and entity_type != "PRICE":
                tag = entity.name

        if len(tag) > 0:
            salience_list.append(entity.salience)
            entity_list.append(tag)

    salience_list = np.array(salience_list)

    salience_list = salience_list / np.sum(salience_list)

    aggregate = {}
    for i in range(len(entity_list)):
        if entity_list[i] not in aggregate:
            aggregate[entity_list[i]] = salience_list[i]
        else:
            aggregate[entity_list[i]] += salience_list[i]

    res = []
    for name in aggregate:
        res.append({"name": name, "weight": aggregate[name]})

    return res

def entity_extraction(data):
    transcripts = ""
    for row in data:
        transcript = row["transcript"]
        if len(transcript) > 0:
            transcripts = transcripts + " " + transcript

    data = sample_analyze_entities(transcripts)

    theme = {
            "series": [{
                "type": 'wordcloud',
                "data": data,
                "name": 'Salience'
            }],
            "title": {
                "text": 'Entity Wordcloud'
            }
        }

    return theme