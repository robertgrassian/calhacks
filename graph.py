import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly
import plotly.plotly as py
from plotly import tools
import plotly.graph_objs as go
import json

plotly.tools.set_credentials_file(username='trevorwise16', api_key='EhhKIRbvdFkt3pfcIBP4')

def graph(current, exited, total):
    fig = tools.make_subplots(rows=1, cols=2)

    g1 = graph1(total)
    g2 = graph2(total)
    g3 = graph3(total)

    fig.append_trace(g1, 1, 1)
    # fig.append_trace(g2, 1, 2)
    fig.append_trace(g3, 1, 2)

    py.plot(fig, filename='basic-line', auto_open=True)
    fig.append_trace(g1, 1, 1)
    #fig.append_trace(g2, 1, 2)
    plt.show()

'''  
    sentimentDifference = []

    for faceLeft in left:
        first = arrived[faceLeft['faceId']]['emotion']
        for i in range(len(faceLeft['emotion'].keys())):
            dif = faceLeft['emotion'].values()[i] - first[i]

'''
def graph1(total):
    age = [j['faceAttributes']['age'] for j in total.values()]
    # age histogram
    return go.Histogram(x=age)

def graph2(total):
    labels = ['Male', 'Female']
    colors = ['#5064ff', '#E1396C']

    men = 0
    women = 0
    # TODO: MAybe change just to people in the room
    for face in total.values():
        if face['faceAttributes']['gender'] == 'male':
            men += 1
        else:
            women += 1
    values = [men, women]
    return go.Pie(labels=labels, values=values,
                hoverinfo='label+percent', textinfo='value',
                textfont=dict(size=20),
                marker=dict(colors=colors,
                            line=dict(color='#000000', width=2)),
                domain={'x': [0.0, 0.5], 'y': [0.0, 0.5]})

def graph3(total, exited):
    timeInClub = [(faceLeft["time"] - total[faceLeft['faceId']]['time']).seconds // 60 for faceLeft in exited.values()]
    return go.Histogram(x=timeInClub)

def pyramidGraph(total):
    menAge = []
    womenAge = []
    max = 0
    for j in total.values():
        if j['faceAttributes']['gender'] == 'male':
            menAge.append(j['faceAttributes']['age'])
        else:
            womenAge.append(j['faceAttributes']['age'])

    women_bins = np.array([-600, -623, -653, -650, -670, -578, -541, -411, -322, -230])
    men_bins = np.array([600, 623, 653, 650, 670, 578, 541, 360, 312, 170])
    layout = go.Layout(yaxis=go.layout.YAxis(title='Age'),
                       xaxis=go.layout.XAxis(
                           range=[-1200, 1200],
                           tickvals=[-1000, -700, -300, 0, 300, 700, 1000],
                           ticktext=[1000, 700, 300, 0, 300, 700, 1000],
                           title='Number'),
                       barmode='overlay',
                       bargap=0.1)

    data = [go.Bar(y=total,
                   x=men_bins,
                   orientation='h',
                   name='Men',
                   hoverinfo='x',
                   marker=dict(color='powderblue')
                   ),
            go.Bar(y=total,
                   x=women_bins,
                   orientation='h',
                   name='Women',
                   text=-1 * women_bins.astype('int'),
                   hoverinfo='text',
                   marker=dict(color='seagreen')
                   )]

