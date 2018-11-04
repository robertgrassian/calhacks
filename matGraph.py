import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

def create_age_hist(dataframe):
    ages = dataframe['faceAttributes.age']
    plt.ion()
    plt.hist(ages)
    plt.show()
    plt.pause(1)

def create_gender_bar(dataframe):
    gender_info = dataframe['faceAttributes.gender']
    print(gender_info)