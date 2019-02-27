from RDRPOSTagger3.pSCRDRtagger import RDRPOSTagger
from RDRPOSTagger3.Utility.Utils import readDictionary
r = RDRPOSTagger.RDRPOSTagger()
r.constructSCRDRtreeFromRDRfile("F:\hiwi\\09september\\try_morpho_tagger\RDRPOSTagger3\Models\MORPH\German.RDR")
DICT = readDictionary("F:\hiwi\\09september\\try_morpho_tagger\RDRPOSTagger3\Models\MORPH\German.DICT")
result=r.tagRawSentence(DICT, "In dieser Funktion leitet die 60-Jährige die Renovierung des UN-Hauptquartiers in New York, die bis 2013 dauern soll.")
print(type(result))
print(result)