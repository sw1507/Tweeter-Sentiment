from data.uw_ischool_sample import SAMPLE_TWEETS
from data.sentiments_nrc import SENTIMENTS, EMOTIONS
import re
import requests
from functools import reduce
    
def text_split(text):
    """The text_split function is defined to split a sentence into a list of words. Punctuations, words with only one characters, as well as special characters are ignored"""
    new_text = re.split('\W+', text)
    texts = [string.lower() for string in new_text]
    text_after_split = []
    for text in texts:
        if len(text)> 1:
            text_after_split.append(text)
    return (text_after_split)

def words_contain_emotion(text, test_emo):
    """The function words_contain_emotion takes in a text and a emotion word as arguments, the functionfilters the text and returns only those words that contain the specific emotion (test_emo).In this assignment the test_emo basically refers to emotional word contained in imported list EMOTIONS"""
    texts = text_split(text)
    default = 0
    emotion_list = []
    list_all_in_senti=[]
    list_no_emotion=[]
    for text in texts: # for each word in the split text
        if SENTIMENTS.get(text,default) != 0: # if SENTIMENTS contain the word
            emotion_dic = SENTIMENTS.get(text) # the corresponding emotion is added to the emotion_dic as a dictionary item
            list_all_in_senti.append(text)
            if emotion_dic.get(test_emo) != 1:
                list_no_emotion.append(text)
    emotion_list = list(set(list_all_in_senti)^set(list_no_emotion))
    return emotion_list # ["amazingly", "prefer", "sunshine"]

def words_fill_in_emotions(text):
    """The function words_fill_in_emotions determines which words from a list have each emotional word, it produce a dictionary with each word from the EMOTIONS followed by a list of corresponding words in the given text"""
    texts = text_split(text) # ['amazingly', 'prefer', 'rainy', 'day', 'to', 'sunshine']
    emo_list = []
    for EMOTION in EMOTIONS:
        emo_list.append(words_contain_emotion(text, EMOTION))
    return dict(zip(EMOTIONS, emo_list)) 

def most_common_words(text_list):
    """The function most_common_words calculate the number of appearance of each word in a list and return a result to display the first 3 common words in that list."""
    words_count = ()
    sorted_list = []
    sorted_list_words = []
    for word in set(text_list): 
        words_count = (word, text_list.count(word))
        sorted_list.append(words_count)   #
    tuples = sorted(sorted_list, key=lambda x:x[1], reverse=True) # generate a list, each item is a tuple, and each tuple is in the format of (word,the number of appearance of the word)
    for tuple in tuples:
        sorted_list_words.append(tuple[0])
    return sorted_list_words[0:3]
     
def analyze_tweenze(tweets,emotion):
    """The function analyze_tweeze takes a tweet, which should be a list with each tweet stored in it as dictionary, and a emotion word from the imported list EMOTIONS. The function outputs the emotion, the word represent that emotion's percentage, most common words appeared in the tweets, as well as most common hashtags for that emotion"""
    indexs = []
    list_emotional = []
    texts = []
    texts_new = []
    hashtags_list = []     
    '''calculate the percentage'''    
    for tweet in tweets:
        indexs.append(words_contain_emotion(tweet.get("text"), emotion)) # all values for key "text" in SAMPLE_TWEETS gathered in a list called lists
        texts.append(text_split(tweet.get("text")))  # get a list with all values for key "text" in SAMPLE_TWEETS, with each value splited into separate words
    indexs = [index for index in indexs if len(index)!=0] # delete those values with no words in lists  
    for index in indexs:
        for i in range (len(index)):
            list_emotional.append(index[i]) # list_emotional is a list of words with emotions filtered
    num_of_emotional_words = len(list_emotional) # count the number of emotional words appeared in tweets    
    for text in texts:
        for j in range(len(text)):
            texts_new.append(text[j])
    num_of_total_words = len(texts_new) # count the number of words appeared in tweets    
    '''calculate hashtags '''  
    for tweet in tweets:
        if len(words_fill_in_emotions(tweet.get("text"))[emotion])>0:
            if len(tweet.get("entities").get("hashtags"))!=0:
                for i in range(0,len(tweet.get("entities").get("hashtags"))):
                    hashtags_list.append("#" + tweet.get("entities").get("hashtags")[i].get("text"))
    hashtags_list = [string.lower() for string in hashtags_list]      
    '''function results'''    
    percentage_with_emotion = num_of_emotional_words/num_of_total_words       
    example_words = most_common_words(list_emotional)
    example_hashtags = most_common_words(hashtags_list)
    statistics_result = {'emotion':emotion,'percentage':percentage_with_emotion,'word':example_words,'hashtag':example_hashtags}
    return statistics_result
     
def statistics_display(data,emotion): 
    """The function statistics_display take tweets and a emotion word as arguments, output the emotion, the word represent that emotion's percentage, most common words appeared in the tweets, as well as most common hashtags for that emotion in a table format"""
    percent_result = analyze_tweenze(data,emotion)['percentage']
    word_result = analyze_tweenze(data,emotion)['word']
    hash_result = analyze_tweenze(data,emotion)['hashtag']
    str = ", "
    print("{0:14} {1:<11.2%} {2:35} {3:45}".format(emotion, percent_result, str.join(word_result), str.join(hash_result)))

def tweets_display(tweets_data):
    """To produce a list of emotional words in the sequence of number of appearance in all tweeets"""
    dics = {"positive": [],"negative": [],"anger": [],"anticipation": [],"disgust": [],"fear": [],"joy": [],"sadness": [],"surprise": [],"trust": []}
    for tweet in tweets_data:
        for emotion in EMOTIONS:
            dics[emotion].append(words_fill_in_emotions(tweet["text"])[emotion])
            dics[emotion] = [item for item in dics[emotion] if len(item) != 0]
    a = []
    list_count_total = []
    for emotion in EMOTIONS:
        words = dics[emotion]
        for word in words:
            for i in range(len(word)):
                a.append(word)
        tuple_count_total = (emotion,len(a)) 
        list_count_total.append(tuple_count_total)
        a = []
    keys = sorted(list_count_total, key=lambda x:x[1], reverse=True) # generate a list, each item is a tuple, and each tuple is in the format of (emotional word,the number of appearance of the word in all tweets)
    sorted_common_list = []
    """produce the output"""
    for key in keys:
        sorted_common_list.append(key[0]) # sorted_common_list is the list of emotional words with most common word displayed first ['positive', 'trust', 'anticipation', 'joy', 'surprise', 'negative', 'sadness', 'disgust', 'fear', 'anger']   
    print("{0:14} {1:11} {2:35} {3:45}".format("EMOTION","% OF WORDS","EXAMPLE WORDS", "HASHTAGS")) # print the table title
    for emotion in sorted_common_list:
        statistics_display(tweets_data,emotion) # print the table content

def download(username):
    '''the function download takes in a twitter username as argument and return data required'''
    screen_name = {'screen_name': username}
    r = requests.get('https://faculty.washington.edu/joelross/proxy/twitter/timeline', params=screen_name)
    return r.json()
    
username = input("Please input twitter user name:\n")
if username == "SAMPLE":
    tweets_data = SAMPLE_TWEETS
else:
    tweets_data = download(username)
tweets_display(tweets_data)