# Rock Paper Scissors Shoot!
# How to play
Just preass the start game button, and make sure to hold your hand in that position for 1 second after it says shoot, also please dont spam the button, as that just makes the computer win each time. It tracks the total amount of wins for all people who have played the project not just you, so lets see if we can beat our AI, overlords. Right now it is running at  https://rpss.rmardia.hackclub.app/. 
# How it works
THis is a python script that I am hosting on nest that uses mediapip to capture the location of your hands, and add classify them using a model which I trained using c.py. All the data is stored and classified in the data folder, and if you want to callect more, you can collect it by running c.py, and if you want to run it locally, you can do so py running app.py.
# Let me rant for a bit
This project took so so so long to make. At first when I frained the model I tried to convert it to a model that was compatible with javescript, so that I could make this website. But forsome reason I had problems with the converter library and I tried EVERYTHING to convert it, but it just was not working. Then, I tried coding the entire collection code to have it output a javascript compatible file, but that also did not work. Later I saw thought I could just run python on the nest project, but than it took me more than a day for me to get that running. Then I had to train the model for soooooo long. I also got some of my family and friends to do around 30 photos  for a bag of Cheetos, so that did help with getting different data. Then when I delpoyed the project for the fist time, I FORGOT TO RUN THE PROJECT ON NEST! and so the demo did not work *smacks* *forehead*. Now I have updated some code did some more training, and now hopefully it actually works.
# Credit
I did take some indpiration from this instructable https://www.instructables.com/Working-Harry-Potter-Wand-With-AI/, and the rock paper scissors game, but that so old I'm pretty sure it is open source by now. I used the mediapipe library for detecting hands.
