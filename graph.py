import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='trevorwise16', api_key='EhhKIRbvdFkt3pfcIBP4')




data = [trace0, trace1]

py.iplot(data, filename='basic-line')
