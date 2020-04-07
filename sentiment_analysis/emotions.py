# Authon Elena Stamatelou

import spacy
import pandas as pd
import scrapper
news = scrapper.news_scrapper()
indexes = {}
df = pd.read_csv('greek_sentiment_lexicon.tsv',sep='\t')
df = df.fillna('N/A')
for index, row in df.iterrows():
    df.at[index, "Term"] = row["Term"].split(' ')[0]
    indexes[df.at[index, "Term"]] = index

indexes_pos = {}    
positive = pd.read_csv('positive_words_el.txt' , sep=',' )
for index, row in positive.iterrows():
    positive.at[index, "words"] = row["words"].split(' ')[0]
    indexes_pos[positive.at[index, "words"]] = index

indexes_neg = {}    
negative = pd.read_csv('negative_words_el.txt' , sep=',' )
for index, row in negative.iterrows():
    negative.at[index, "words"] = row["words"].split(' ')[0]
    indexes_neg[negative.at[index, "words"]] = index
column_names = ['subjectivity', 'anger', 'disgust', 
                            'fear', 'happiness', 'sadness',
                             'surprise', 'polarity']
scores=pd.DataFrame(columns = column_names)
for i in range(len(news)):
 text = news['title'][i]

#text = '''Έχω μείνει συνέχεια έκπληκτος! Πώς γίνεται αυτό; Η σοφία είναι τόσο μεγάλη! Α, τώρα εξηγούνται όλα.'''
#text = '''Τσιόδρας: «Δύσκολο θέμα» τα κλιματιστικά -Τι συμβουλεύει ο λοιμωξιολόγος'''
#text = '''Κορονοϊός Ελλάδα: Αυτά είναι τα 10 νέα μέτρα που θα ανακοινώσει η κυβέρνηση'''
#text = '''Κορονοϊός: Νέο πειραματικό φάρμακο δίνει ελπίδες - Η δήλωση Τσιόδρα -'''
 subj_scores = {
    'OBJ': 0,
    'SUBJ-': 0.5,
    'SUBJ+': 1,
 }

 emotion_scores = {
    'N/A': 0,
    '1.0': 0.2,
    '2.0': 0.4,
    '3.0': 0.6,
    '4.0': 0.8,
    '5.0': 1,
 }
 polarity_scores = 0 
#polarity_scores = {
#    'N/A': 0,
#    'BOTH': 0,
#    'NEG': -1,
#    'POS': 1
#}
 
 nlp = spacy.load('el_core_news_sm')
 doc = nlp(text)
 subjectivity_score = 0
 anger_score = 0
 disgust_score = 0
 fear_score =  0
 happiness_score = 0
 sadness_score = 0
 surprise_score = 0
 matched_tokens = 0
 for token in doc:
    lemmatized_token = token.lemma_
    print(lemmatized_token)
    if (lemmatized_token in indexes) :
        indx = indexes[lemmatized_token]
#        print(indx)
        pos_flag = False
        for col in ["POS1", "POS2", "POS3", "POS4"]:
            if (token.pos_ == df.at[indx,col]):
                pos_flag = True
                break
        if (pos_flag == True):
            print(pos_flag, lemmatized_token)
            match_col_index = [int(s) for s in col if s.isdigit()][0]
            subjectivity_score += subj_scores[df.at[indx,'Subjectivity'+str(match_col_index)]]
            anger_score += emotion_scores[str(df.at[indx, 'Anger'+str(match_col_index)])]
            disgust_score += emotion_scores[str(df.at[indx, 'Disgust'+str(match_col_index)])]
            fear_score += emotion_scores[str(df.at[indx, 'Fear'+str(match_col_index)])]
            happiness_score += emotion_scores[str(df.at[indx, 'Happiness'+str(match_col_index)])]
            sadness_score += emotion_scores[str(df.at[indx,'Sadness'+str(match_col_index)])]
            surprise_score += emotion_scores[str(df.at[indx, 'Surprise'+str(match_col_index)])]
            matched_tokens+=1
#            print(lemmatized_token)
#            for child in token.children:
#                print(child, child.dep_)
    if (lemmatized_token in indexes_pos) :
        polarity_scores = polarity_scores + 1
        print('positive', lemmatized_token)
    if (lemmatized_token in indexes_neg) :
        polarity_scores = polarity_scores - 1
        print('negative',lemmatized_token)


 current_scores = pd.DataFrame(pd.Series([subjectivity_score,  anger_score,  disgust_score, 
                            fear_score,  happiness_score, sadness_score,surprise_score,  polarity_scores])).T

 current_scores.columns = column_names
  
 scores = pd.concat([scores,current_scores], ignore_index=True)

 print(text, scores)
#print('Polarity' , polarity_scores)
#try:
#    print('Subjectivity: ' + str(subjectivity_score/matched_tokens * 100)+'%')
#    
#    emotions = {'anger': anger_score, 'disgust': disgust_score, 'fear':fear_score, 'happiness':happiness_score, 'sadness': sadness_score, 'surprise': surprise_score}
#    emotion = max(emotions.items(), key=operator.itemgetter(1))[0]
#    if (emotions[emotion] == 0):
##        print('Unable to detect emotion')
#    else:
##        print('Main emotion: ' + emotion + '. Emotion score: ' + str(emotions[emotion]*100/matched_tokens) + '%')
#except:
##    print('Subjectivity: 0 ')
##    print('No matched tokens')
 

news = pd.concat([news,scores], ignore_index= True, axis = 1) 
column_names = ['title', 'content','subjectivity', 'anger', 'disgust', 
                            'fear', 'happiness', 'sadness',
                             'surprise', 'polarity']
news.columns=column_names
news = news.drop_duplicates()
news.to_json(r'news_sentiment.json',lines = False)
with open('news_sentiment.json', 'w', encoding='utf-8') as file:
    news.to_json(file, force_ascii=False, lines = False, orient = "records")

# df.to_json(file, 