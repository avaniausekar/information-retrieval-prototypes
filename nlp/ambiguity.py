import nltk 
from nltk.corpus import wordnet as wn 
 
def lesk(context_sentence, ambiguous_word): 
    best_sense = None 
    max_overlap = 0 
    context = set(context_sentence) 
     
    for sense in wn.synsets(ambiguous_word): 
        signature = set(wn.synset(sense.name()).definition().split())  # Using synset definition as signature 
         
        # Adding example sentences to the signature 
        for example in wn.synset(sense.name()).examples(): 
            signature.update(example.split()) 
         
        overlap = len(context.intersection(signature)) 
        if overlap > max_overlap: 
            max_overlap = overlap 
            best_sense = sense 
     
    return best_sense 
 
print("Various definitions of bank: ") 
for ss in wn.synsets('bank'): 
    print(ss, ss.definition()) 
 
print()  
sentence = "He went to the bank to deposit his money." 
print(sentence) 
# Tokenize the sentence 
tokens = nltk.word_tokenize(sentence) 
# TODO inside lesk
# Apply the Lesk algorithm to disambiguate the word 'bank' in the given  context
wsd_synset = lesk(tokens, 'bank') 