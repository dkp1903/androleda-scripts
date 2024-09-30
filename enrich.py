import spacy
nlp = spacy.load('en_core_web_sm')

def enrich_content(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

rss_summary = "This is an example RSS feed summary about engineering blogs and technologies."
entities = enrich_content(rss_summary)
print(entities)  # [('RSS', 'ORG'), ('engineering blogs', 'ORG')]
