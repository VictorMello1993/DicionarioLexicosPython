# -*- coding: utf-8 -*-
"""Dicionário de léxicos - SentilexPt.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MpccRX4nJko3BUIQnny6OugyWP9qVtwN

# Dicionários léxicos
São dicionários de palavras, criados manualmente ou de forma automatizada, com suas respectivas polaridades de um sentimento, onde:

* -1 - negativo
* 0  - neutro
* 1  - positivo

## Vantagem

* Não é preciso rotular dados para treinamento

## Desvantagem
* Depende muito do idioma e do tamanho da base de dados

Existem vários dicionários de léxicos existentes para se trabalhar com a polaridade das palavras de uma frase. Um deles é o SentilexPT, que contém 6531 adjetivos com informações de polaridade, alvo do sentimento e método de atribuição de polaridade

Referências: 

* https://minerandodados.com.br/analise-de-sentimentos-de-uma-forma-diferente/

* https://github.com/caiomsouza/u-tad-eds-proyecto-final/tree/master/lexicon

## SentiLex
"""

sentilexpt = open('/content/SentiLex-lem-PT01.txt', 'r')

dic_palavra_polaridade = {}
for i in sentilexpt.readlines():
  pos_ponto = i.find('.')
  palavra = (i[:pos_ponto])
  pol_pos = i.find('POL')
  polaridade = (i[pol_pos+4:pol_pos+6]).replace(';','')
  dic_palavra_polaridade[palavra] = polaridade

print(dic_palavra_polaridade)

print(dic_palavra_polaridade.get('')) #Obtendo a polaridade de uma palavra

"""##Vader

Vader é um dicionário de léxicos que mostra o grau de intensidade de polaridade de um sentimento de uma determinada palavra ou frase

Repositório: https://github.com/cjhutto/vaderSentiment
"""

# !pip3 install vaderSentiment
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analysis = TextBlob('This guy is very cool!')
# print(dir(analysis))

#Efetuando tradução para outro idioma
print(analysis.translate(to='pt'))

import nltk
nltk.download('averaged_perceptron_tagger')

print(analysis.tags)

print(analysis.sentiment)

#Obtendo o grau de polaridade de sentimento em cada frase (linha do arquivo)

pos_counts = 0
pos_correct = 0
neg_counts = 0
neg_correct = 0


with open("/content/positive.txt","r", encoding='utf-8') as f:
  for line in f.read().split('\n'):
    analysis = TextBlob(line)
    if analysis.sentiment.polarity > 0:
      pos_correct += 1
    pos_counts +=1

with open('/content/negative.txt', 'r', encoding='utf-8') as f:
  for line in f.read().split('\n'):
    analysis = TextBlob(line)
    if analysis.sentiment.polarity <= 0:
      neg_correct += 1
    neg_counts +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_counts*100.0, pos_counts))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_counts*100.0, neg_counts))

#Obtendo um score de sentimentos de uma frase
analyzer = SentimentIntensityAnalyzer()
vs = analyzer.polarity_scores('This house is amazing!')
print(vs)

#Mais exemplos de score de sentimentos
sentences = ["VADER is smart, handsome, and funny.",  # positive sentence example
             "VADER is smart, handsome, and funny!",  # punctuation emphasis handled correctly (sentiment intensity adjusted)
             "VADER is very smart, handsome, and funny.", # booster words handled correctly (sentiment intensity adjusted)
             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
             "VADER is VERY SMART, handsome, and FUNNY!!!", # combination of signals - VADER appropriately adjusts intensity
             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!", # booster words & punctuation make this close to ceiling for score
             "VADER is not smart, handsome, nor funny.",  # negation sentence example
             "The book was good.",  # positive sentence
             "At least it isn't a horrible book.",  # negated negative sentence with contraction
             "The book was only kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
             "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
             "Today SUX!",  # negative slang with capitalization emphasis
             "Today only kinda sux! But I'll get by, lol", # mixed sentiment example with slang and constrastive conjunction "but"
             "Make sure you :) or :D today!",  # emoticons handled
             "Catch utf-8 emoji such as such as 💘 and 💋 and 😁",  # emojis handled
             "Not bad at all"  # Capitalized negation
             ]

analyzer = SentimentIntensityAnalyzer()
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence)
    print("{:-<65} {}".format(sentence, str(vs)))

print('\n')

pos_counts = 0
pos_correct = 0
neg_counts  = 0
neg_correct = 0


with open("positive.txt","r") as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if vs['compound'] > 0:
            pos_correct += 1
        pos_counts +=1


with open("negative.txt","r") as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if vs['compound'] <= 0:
            neg_correct += 1
        neg_counts +=1


print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_counts*100.0, pos_counts))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_counts*100.0, neg_counts ))