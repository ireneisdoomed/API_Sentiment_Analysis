import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from src.mongo import *
import numpy as np
from wordcloud import wordcloud

def polarityScore(message):
    '''
    Calculates Polarity Score using the NLTK library
    Returns a dictionary with the degree of negativity, positivity, neutrality 
    and the compound of all in a range of -1 to 1
    '''
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(message)
#   return {"score" : sia.polarity_scores(message)}

def chatScore(chatName):
    '''
    Returns a dictionary with the result of the Polarity Score "compound" added to
    the message data for a given chat
    '''
    content = getMessages(chatName)
    for e in content:
        value = polarityScore(e["message"])["compound"]
        e["compound"] = value
    return content

def calculateScore(chatName):
    '''
    Returns the average of the compounds component of all messages for a given chat
    '''
    content = chatScore(chatName)
    compounds = [e["value"] for e in content]
    return np.mean(compounds)

def userScore(chatName, username):
    '''
    Returns the average of the compounds component of all messages for a given chat and user
    '''
    content = getMessages(chatName)
    mssg = [e["message"] for e in content if e["username"] == username]
    
    userScore = [polarityScore(e) for e in mssg]

    return np.mean(userScore)

def wordCloud(chatName):
    '''
    Generates a image file with a wordcloud of the most used words for a given chat.
    '''
    messages = getMessages(chatName)
    allWords = " ".join(messages)
    wrdcld = wordcloud(width = 1000, height = 500).generate(allWords)
    plt.figure(figsize=(15,8))
    plt.imshow(wrdcld)
    plt.axis("off")
    plt.savefig("wordcloud"+".png", bbox_inches='tight')
    plt.show()
    plt.close()
#send_from_directory