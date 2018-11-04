# calhacks
Cal Hacks 5.0
Our project for CalHacks 2018

## Our Project

For our project, we chose to utilize Microsoft's Faces API to analyze attendee flow in events or other crowded areas.
The API itself is a powerful image recognition tool, which provides a lot of useful information that's extremely valuable
to people trying to understand the demographics of people attending their events, such as age or gender, but at the same
time we can actually see changes in emotion over the course of the event to make decisions about improving their
experience. By setting up two cameras, an entrance and an exit, we can visualize and understand these analytics
that the API provides purely based on facial recognition. Our final design is a dashboard of useful charts and analytics that can help someone managing large amounts of people make decisions to improve their experience. 

## Implementation

Our project is written in Python, as most of what we developed involves real time scripting and constant updates from a webcam, so it was easiest for us to develop and deploy quickly using this familiar language. We've also leveraged OpenCV, in order to take camera information and transform it into easily usable frames for the Faces API. Our analytics were built using Seaborn to create insightful graphs.

Our core logic revolves around an "In" and and "Out" camera, that respectively take notice when someone first enters the event, and when they exit. We can recognize people seen first in the "In" camera when they leave, so we use these two distinct endpoints to create our analytics.

## Future Plans

We have a couple things in store for our project. First off, we're looking to host our scripts using a Django web application, and connect this remotely with our viewing cameras so we can constantly crunch data in real time. 

We'll also be storing all of this event data, and the large number of data points we have access can be very useful for data science and machine learning models, so we hope to create analytics to further improve these businesses goals.
