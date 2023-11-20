# cs347final

Dominion Game
By: Brendan, Bryce, Will, and Peter

This is an implementation in Docker of the Dominion board game for two players. Players can play against an AI or against another player on the local machine. This game follows all of the rules of the physical game and implents all cards and features.



How to play Dominion:
    1. Pull our repo from github
    2. In a terminal where the current directory is cs347-final run "docker-compose up --build"
    3. Go to localhost:7555/ to start game

Code Structure
api
    - In api we have our main backend.py file that runs all our backend. This imports the other python files in the directory. These files import card_scripting which scipts how cards function.
db
    - In db all we do is create the datase docker container.
web
    - In web he have our main frontend.py file that runs all our frontend. We also have tutorial_executer.py which executes the tutorial. Then we have our static resources such as images and css in the static directory. Finally, we have our html templates in the templates directory.

Code from other Team
- The code from the other Team is in web/frontend.py and is indicated in the comments.