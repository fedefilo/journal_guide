*FSND Project 3 / Journal Item Catalog*

*This is Udacity's FSND 3rd Project*

*by Federico Vasen*

**About the application**

It is a catalog of scholarly journals.
Visitors can navigate categories and item pages and access information in JSON and XML.
Logged users can add journals and disciplines. 
Disciplines can be added and deleted by all users/
Journals can only be edited or deleted by the user that created the entry.
Login and registration only possible with a Facebook account.
Some screenshots provided in the screenshot folder.

**Installation instructions**

1. Clone the current repository inside the Fullstack Nanodegree Vagrant machine
2. If not already available, install SeaSurf CSRF Flask Extension
   sudo pip install flask-seasurf
3. Run database_setup.py to create the SQLite database
4. Run lots-of-journals.py to populate the database with some test journals (not available for editing by registered users)
5. Run project.py
6. Go to http://localhost:5000
7. Use the app
8. Ctrl+C to interrupt the app

Hope you like it!
