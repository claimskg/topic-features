import sys, getopt
import pickle
import nltk
import csv

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from rdflib import Graph

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(sentence)]).lower().strip()
	
def get_claims(g):
    qres = g.query(
    """
    PREFIX schema: <http://schema.org/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?claim ?text ?date ?keywords ?orgName ?ratingName WHERE {
        ?claimReview schema:itemReviewed ?claim.
        ?claimReview schema:reviewRating ?rating.
        ?claimReview schema:author ?org.
        ?org schema:name ?orgName.
        ?rating schema:author <http://data.gesis.org/claimskg/organization/claimskg>.
        ?rating schema:alternateName ?ratingName.
        ?claim a schema:CreativeWork.
        ?claim schema:keywords ?keywords.
        ?claim schema:text ?text
        OPTIONAL {?claim schema:datePublished ?date}.
    } ORDER BY DESC (?date) ASC(?claim)
    """)
    return qres

def main(argv):
	ttlfile = "Data/claimskg_v1.0.ttl"
	csvfile = "Data/data.csv"
	
	#Load Data
	g = Graph()
	g.parse(ttlfile, format="turtle")
	
	#TTL to CSV
	qres = get_claims(g)
	
	rows = list()
	header = ["uri","date","claim","keywords","organization","rating"]
	rows.append(header)

	for row in qres:
		claim = row.claim
		date = row.date
		keywords = ",".join([lemmatize_sentence(x) for x in row.keywords.split(',')])
		orgName = row.orgName.value
		ratingName = row.ratingName.value
		text = row.text.value
		
		if date == None:
			date = ''
		else:
			date = date.value.strftime("%m/%d/%Y")
			
		claim_row = [claim,date,text,keywords,orgName,ratingName]
		rows.append(claim_row)

	with open(csvfile,'w',newline='',encoding="utf-8") as writeFile:
		writer = csv.writer(writeFile,delimiter=';')
		writer.writerows(rows)
		writeFile.close()

if __name__ == "__main__":
	main(sys.argv[1:])