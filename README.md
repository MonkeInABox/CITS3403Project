# CITS3403Project
Repository for CITS3403 Project 

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
Enter: `flask db migrate`  
Enter: `flask db upgrade base`
