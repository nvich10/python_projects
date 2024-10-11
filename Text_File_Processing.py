#Noah Vich

import re
import string
import readability
import sys


#title
print('\tState of the Union Speeches Breakdown\n')


#readability function
def readabilityScore (openFile) :
  results = readability.getmeasures(openFile, lang='en') #get readability score
  score = results['readability grades']['FleschReadingEase']
  print(f'readability score: {score:.5f}')

  if score > 89 and score < 101 :
    print('Easy to read')
  if score > 79 and score < 90 :
    print('Easy to read.')
  if score > 69 and score < 80 :
    print('Fairly easy to read.')
  if score > 59 and score < 70 :
    print('Plain english.')
  if score > 49 and score < 60 :
    print('Fairly difficult to read.')
  if score > 29 and score < 50 :
    print('Difficult to read.')
  if score > -1 and score < 30 :
    print('Very hard to read.')



#Wordcloud Function
def wordCloud (openFile) :
  from os import path
  from PIL import Image
  import numpy as np
  import matplotlib.pyplot as plt
  from wordcloud import WordCloud, STOPWORDS

  #create mask - ADDITIONAL ENHANCEMENT
  USA_image = "USA-mask.jpg" #check direcgtory for this file
  image_mask = np.array(Image.open(USA_image))

  word_tup = tenWordsFunction(openFile, False)
  word_dict = dict(word_tup) #get dictionary of popular words

  wordCloud = WordCloud(background_color="white", mask=image_mask)
  wordCloud.generate_from_frequencies(word_dict) #build word cloud

  plt.figure(figsize=(4,3), dpi=120)
  plt.imshow(wordCloud, interpolation='bilinear')
  plt.axis("off")
  plt.show()


#find 10 most common words
def tenWordsFunction (openFile, printed) :
  masterDict = dict() #holds final 10 most popular
  tempList = list() #holds word for only a set amount of processing

  for line in openFile :
    line = line.translate(str.maketrans('','',string.punctuation)) #remove punctuation
    tempList = re.findall(r'\b\w+\b', line)
    for word in tempList :
      if len(word) < 5 : #I find that words with over 5 length are much more interesting and applicable
        del word
        continue
      word = word.lower()
      if word in masterDict :
        masterDict[word] += 1
      else :
        masterDict[word] = 1


  #sort dictionary
  sorted_dict = sorted(masterDict.items(), key=lambda x: x[1], reverse=True)

  if printed == True :
    count = 0
    while count < 10 :
      key,value = sorted_dict[count]
      print(key, ': ', value, sep='')
      count += 1

  return sorted_dict



#find average amount of words in scentences
def averageWordsFunction (openFile) :
  honorifics = ("Mrs.", "Mr.", "Sr.", "Dr.", "Prof.", "Capt.", "Gen.", "Sen.", "Rev.", "Hon.", "St.") #remove these

  totalWords, _ = wordCountFunction(openFile, False) #get total word count

  tempList = list()
  openFile.seek(0)
  totalSentences = 0

  for line in openFile :
    line = line.strip()
    tempList = line.split(' ')
    count = -1
    for word in tempList :
      count += 1
      if word in honorifics or word == '' :
        del tempList[count]
    for word in tempList :
      if '.' in word or '?' in word or '!' in word :  #if word has punctuation, add one to toal sentences
        totalSentences += 1

  #calculate average words per sentence
  averageWords_per_line = totalWords / totalSentences
  print(f'Average words per line: {averageWords_per_line:.5f} words')



#finds average amount of letters per word
def averageLettersFunction(openFile) :
  totalWords, masterList = wordCountFunction(openFile, False) #get total words and list of words
  totalChars = 0 #total amount of chars in entire file

  for word in masterList :
    totalChars += len(word)
  #calculate average letter per word
  averageChars = totalChars / totalWords

  print(f'Average letters per word: {averageChars:.5f} letters')



#finds number of words in a speech
def wordCountFunction(openFile, printed) :
  totalWords = 0
  masterList = list()
  for line in openFile :
    line = line.translate(str.maketrans('','',string.punctuation)) #remove punctuation
    split = re.findall(r'\b\w+\b', line) #find words using reg ex
    for word in split :
      totalWords += 1
      masterList.append(word)

  if printed == True :
    print('Total words in the speech:', totalWords, 'words')

  return totalWords, masterList



#make sure file opens -> call menu function
def fileNameFunction () :
  try_file_open = False
  while try_file_open == False:
    try :
      fileName = input('Enter file name: ')
      with open(fileName, 'r') as openFile :
       #call functions here
       menuSelection(openFile)
       try_file_open = True

    except :
      print('Error! Check your directory & enter correct file name.')



#calls functions to operate on files
def menuSelection(openFile) :
  repeater = True
  while repeater == True :
    openFile.seek(0)
    print('\nWhat would you like to know about this speech?\n'
            '1) Word Count\n'
            '2) Average word length\n'
            '3) Average words per scentence\n'
            '4) 10 most common words\n'
            '5) Generate Word Cloud\n'
            '6) Readability Score\n'
            '0) Enter new file\n\n'
            "   To exit enter 'x'\n")

    userChoice = input('Menu choice: ')


    if userChoice in ['0','1','2','3','4','5','6','x']:
        if userChoice == 'x' :
          repeater = False
          break
        if userChoice == '1' :
            wordCountFunction(openFile, True)
        elif userChoice == '2' :
            averageLettersFunction(openFile)
        elif userChoice == '3' :
            averageWordsFunction(openFile)
        elif userChoice == '4' :
            tenWordsFunction(openFile, True)
        elif userChoice == '5' :
              wordCloud(openFile)
              break
        elif userChoice == '6' :
            readabilityScore(openFile)
        elif userChoice == '0' :
            fileNameFunction()
            break
    else:
      print("Seems to be an error. Try again")



fileNameFunction()