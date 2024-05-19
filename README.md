# CITS3403Project
Repository for CITS3403 Project 

## Description

**recollective** is a website based around finding media recommended by other people,
from young to old, based on what you have previously enjoyed. Through posting in the 
respective category, you can request any form of media that others may think that you
might enjoy, employing the biggest database of reccommendations, EVERYONE!
There is a search function and the ability to sort posts by format or even by likes, dislikes
or how recently it was posted! Comment under others posts to reccommend some of your 
favourites that they might enjoy because of their interest in a specific aspect!

## Team Members

| UWA ID | Name | Github User Name |
|--------|------|------------------|
| 23390554 | Jeremy Butson | MonkeInABox |
| 23135002 | Joel Willoughby | Jamlons   |
| 23690864 | Lim Kar Yee Megan | m3ganz   |
| 23360073 | Dylan Arto | Skoll-8 |

## Deployment

To deploy this project:

In: `/CITS3403` folder  
Enter: `python3 -m venv venv`  
Enter: `source venv/bin/activate (on linux)`  
Enter: `pip install -r /requirements.txt` 
Enter: `flask run`  

You will now see the CMD window for the web server up and running!  
Most likely it will be hosted on 127.0.0.1:5000 

**If app.db is missing**  
Enter: `flask db init`  
Enter: `flask db migrate`  
Enter: `flask db upgrade` 

## Testing

To test this project:

In: `/CITS3403` folder, ensure the website is running
Enter: `python -m unittest test.py`

*Issues* may arise if the `chromedriver.exe` file is not the same version as your chromium
tester executable that is where it is expected to be.



## FAQ

#### If you make changes to models.py  
Enter: `flask db migrate`  
Enter: `flask db upgrade`

#### If you want to reset the database  
delete migrations and app.db   
Enter: `flask db init`   
Enter: `flask db migrate`  
Enter: `flask db upgrade base`
