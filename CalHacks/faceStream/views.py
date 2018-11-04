from django.http import HttpResponse
from django.template import loader
# Create your views here.

from numpy import pi
from django.shortcuts import render, render_to_response

from bokeh.plotting import figure
from bokeh.embed import components

def graph(request):
    template = loader.get_template('faceStream/index.html')
    return HttpResponse(template.render({}, request))



def bokeh(request):
    MalePercent = .6

    # define starts/ends for wedges from percentages of a circle
    percents = [0,MalePercent,1]
    starts = [p*2*pi for p in percents[:-1]]
    ends = [p*2*pi for p in percents[1:]]

    # a color for each pie piece
    colors = ["blue", "pink"]

    p = figure(x_range=(-1,1), y_range=(-1,1))

    p.wedge(x=0, y=0, radius=1, start_angle=starts, end_angle=ends, color=colors)

    script, div = components(p)

    #Feed them to the Django template.
    return render(request, 'faceStream/bokeh.html', {'script' : script , 'div' : div})
