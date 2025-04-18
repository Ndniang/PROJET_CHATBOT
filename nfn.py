import nltk 

# Télechargement des ressources nécessaires 

nltk.download('punkt_tab')  #Nécessaire pour découper un texte en phrase et en mots (tokenisation)
nltk.download('averaged_perceptron_tagger') #C'est nécessaire pour reconnaitre la nature des mots(nom, verbe, adjectif)=étiquetage grammatical
nltk.download('stopwords') #liste des mots courants inutiles pour l'analyse(exemple: le, la, les,...), à suprimer du texte
nltk.download('wordnet')  #dictionnaire lexical pour faire de la lemmatisation(trouver la forme de base des mots)
nltk.download('omw-1.4')  #nécessaire pour que WordNet puisse fonctioné correctement

import streamlit as st
import string   #bibliothéque utilisé pour les opérations(sur les chaînes)
from nltk.tokenize import word_tokenize, sent_tokenize #word_tokenize(permet de découpouper les phrases en mots),sent_tokenize(pour découper en phrase)
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer # WordNetLemmatizer permet de faire de la lemmatisation de mot àà sa forme de base

#Chargemment du texte (le texte est en français)
with open('pub_entreprise.txt' ,'r', encoding = 'utf-8') as f:
    data = f.read().replace('\n', '')
    
# Découper (on va diviser le texte en phrases)
sentences = sent_tokenize(data)
stop_words = set(stopwords.words('french'))
#Prétraitement: tokenisation, nettoyer, leme=matisation

#Nettoyage d'une phrase en supprimant les mots inutiles et en ramenant les mots à leuurs forme de base
def preprocess(sentence):
    
    words = word_tokenize(sentence, language ='french')  #Découpe la phrase en mots en précisant que le texte est en français
    words = [word.lower() for word in words if word.lower() not in stop_words and word not in string.punctuation]
    #word.lower: transforme tous les mots en minuscules (pour éviter les doublons)
    #if word.lower() not in stop_word: on enléve les mots vides(comme les articles : le, la, est, et...)
    #and word not in string.punctuation : on enléve aussi la ponctuation(comme :,!,?, etc)

    #on crée un lemmantiseur/ ramner les mots à leur forme de base
    lemmatizer = WordNetLemmatizer()

    #On applique le lemmatiseur à chaque mot dans la liste
    words = [lemmatizer.lemmatize(word) for word in words] 

    #La fonction retourne la liste des mots final nettoyés et simplifiés.
    return words 

#Corpus prétraité : c'est une collection de textes ou de phrases, souvent utilisée en traitement de texte
corpus = [preprocess(sentence) for sentence in sentences]

#Fonction de recherche de la phrase la plus pertinente
#Cette fonction cherche la phrase la plus pertinente du texte par rapport à une question posée par l'utilisateur(appelée ici query)

def get_most_relevant_sentence(query):  #obtenir la phrase la plus pertinente
    query = preprocess(query) #query est le paramétre de la fonction. Il représente la question ou la requête de l'utulisateur
    #On utilise la fonction preprocess pour traiter la requête de l'utilisateur

    #on initialise une variable max_similarity à 0
    #Cette variable va stocker le score de similarité maximal trouvé jusqu'à présent
    #Au début, on n'a pas encore comparé à aucune phrase, donc la similarité maximale est égal à zéro
    max_similarity = -1

    #on initialise une variable most_relevant_sentence à une chaîne de caractére vide
    #cette variable va stocker la phrase du corpus qui a la plus grande similarité avec la requête
    #Au début on n'a pas triuver de phrase pertinente, donc elle est vide
    most_relevant_sentence = ""

    #C'est une boucle for qui va parcourir toutes les phrases du corpus
    #énumerate(corpus) permet d'obtenir à la fois(i) et la phrase(sentence)
    for i, sentence in enumerate(corpus):
        similarity = len(set(query).intersection(sentence))/float(len(set(query).union(sentence)))
        
        #set(query):converti la requête en un ensemble de mots uniques.
        #set(sentence):converti la phrase courante en un ensemble de mots uniques.
        #set(query).intersection(sentence):Trouve les mots qui sont à la fois dans la requête et dans la phrase.
        #len(set(query).intersection(sentence)):compte le nombre de mots communs.
        #set(query).union(sentence):trouve tous les mots qui sont soit dans la requête, soit dans la phrase.
        #len(set(query).union(sentence)):compte le nombre total de mots uniques dans la requete et dans la phrase.
        #la similarité est calculée comme le nombre de mots communs divisé par le nombre total de mots uniques. Cela donne une mesure de la proportion de mots partagés entre la requête et la phrase

        #on vérifie si la situation calculée pour la phrase courant est supérieur à la similarité maximale trouvée
        if similarity > max_similarity :
            max_similarity = similarity
            most_relevant_sentence = sentence[i]
    return most_relevant_sentence

#Interface streamlit 

st.title("Chatbot Eclat Brillant")

question = st.text_input("Posez une question sur nos produits :")

if question:
    response = get_most_relevant_sentence(question)
    st.write("Reponse : ",response)





