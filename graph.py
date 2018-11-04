import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly
import plotly.plotly as py
from plotly import tools
import plotly.graph_objs as go
import json

plotly.tools.set_credentials_file(username='trevorwise16', api_key='EhhKIRbvdFkt3pfcIBP4')

def graph(arrived, left, total):
    age = [json.load(j)['faceAttributes']['age'] for j in arrived.values]
    fig = tools.make_subplots(rows=2, cols=2)

    #age histogram
    g1 = go.Histogram(age)


    labels = ['Male', 'Female']
    colors = ['#5064ff', '#E1396C']

    men = 0
    women = 0
    for face in arrived.values():
        if face['faceAttributes']['gender'] == 'male':
            men += 1
        else:
            women += 1
    values = [men, women]
    g2 = go.Pie(labels=labels, values=values,
                   hoverinfo='label+percent', textinfo='value',
                   textfont=dict(size=20),
                   marker=dict(colors=colors,
                   line=dict(color='#000000', width=2)))

    timeInClub = [faceLeft["time"] - total[faceLeft['faceId']]['time'] for faceLeft in left.values()]


    g3 = go.Histogram(timeInClub)

    fig.append_trace(g1, 1, 1)
    fig.append_trace(g2, 1, 2)
    fig.append_trace(g3, 2, 1)

    py.plot(fig, filename='basic-line', auto_open=True)


'''  
    sentimentDifference = []

    for faceLeft in left:
        first = arrived[faceLeft['faceId']]['emotion']
        for i in range(len(faceLeft['emotion'].keys())):
            dif = faceLeft['emotion'].values()[i] - first[i]

'''



