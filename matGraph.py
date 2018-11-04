import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

def graph_all(inFrame, outFrame):
    plt.ion()
    fig = plt.figure(1)
    plt.subplot(221)
    create_age_hist(inFrame)
    plt.subplot(222)
    create_gender_bar(inFrame)
    if outFrame is not None:
        plt.subplot(223)
        out_graph_test(outFrame)
    plt.subplot(224)
    create_sentiments_hist(inFrame)
    plt.pause(1)
    plt.clf()

def create_age_hist(dataframe):
    if dataframe.size > 3:
        agesMale = dataframe[dataframe['faceAttributes.gender']=='male']['faceAttributes.age']
        agesFemale = dataframe[dataframe['faceAttributes.gender']=='female']['faceAttributes.age']
        # plt.hist(agesMale, alpha=0.5)
        # plt.hist(agesFemale, alpha=0.5)
        if agesFemale.size > 2 and agesMale.size > 2:
            sns.distplot(agesFemale, label="Female", hist_kws={'color':'r'}, kde_kws={'color':'r'})
            sns.distplot(agesMale, label="Male",hist_kws={'color':'b'}, kde_kws={'color':'b'})
        else:
            sns.distplot(agesFemale, kde=False, label="Female", hist_kws={'color':'r'})
            sns.distplot(agesMale, kde=False, label="Male", hist_kws={'color':'b'})
        plt.legend()
        plt.xlabel("Age Density based on Sex")
        plt.show()


def create_gender_bar(dataframe):
    gender_info = dataframe.groupby('faceAttributes.gender').count()[['faceId']].reset_index()
    print(gender_info)
    g = sns.barplot(data=gender_info, x='faceAttributes.gender', y='faceId', hue='faceAttributes.gender', palette=['r','b'])
    plt.xlabel('Number of Men vs Women')
    plt.show()

def out_graph_test(dataframe):
    out = dataframe['faceAttributes.age']

    plt.hist(out)

def create_sentiments_hist(dataframe):
   emotions = dataframe[['faceAttributes.emotion.happiness','faceAttributes.emotion.sadness','faceAttributes.emotion.anger','faceAttributes.emotion.disgust']]
   x = np.array(['Happiness','Sadness','Anger','Disgust'])
   y = np.array([emotions['faceAttributes.emotion.happiness'].mean(),emotions['faceAttributes.emotion.sadness'].mean(),emotions['faceAttributes.emotion.anger'].mean(),emotions['faceAttributes.emotion.disgust'].mean()])
   sns.barplot(x,y)
   plt.legend()
   plt.xlabel('Emotions')
   plt.show()
