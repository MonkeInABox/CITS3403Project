# CITS3403Project
Repository for CITS3403 Project 

| UWA ID | Name | Github User Name |
|--------|------|------------------|
| 23390554 | Jeremy Butson | MonkeInABox |
| 23135002 | Joel Willoughby | Jamlons   |
| 23690864 | Lim Kar Yee Megan | m3ganz   |
| 23360073 | Dylan Arto | Skoll-8 |

Enter: `flask run`  

You will now see the CMD window for the web server up and running!  
Most likely it will be hosted on 127.0.0.1:5000

## Deployment

To deploy this project:

Enter: `/CITS3403` folder  
Enter: `python3 -m venv venv`  
Enter: `source venv/bin/activate (on linux)`  
Enter: `pip install -r /requirements.txt`  

**If app.db is missing**  
Enter: `flask db init`  
Enter: `flask db migrate`  
Enter: `flask db upgrade` 



## FAQ

#### If you make changes to models.py  
Enter: `flask db migrate`  
Enter: `flask db upgrade`

#### If you want to reset the database  
delete migrations and app.db   
Enter: `flask db init`   
Enter: `flask db migrate`  
Enter: `flask db upgrade base`
