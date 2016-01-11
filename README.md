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
**Login works OK in a Chrome incognito window. Please test it there.**
Some screenshots provided in the screenshot folder.


**Installation instructions**

*See requirements.txt for needed packages*

1. Clone the current repository inside the Fullstack Nanodegree Vagrant machine
2. If not already available, install SeaSurf CSRF Flask Extension
`sudo pip install flask-seasurf`
3. Run database_setup.py to create the SQLite database
4. Run lots-of-journals.py to populate the database with some test journals (not available for editing by registered users)
5. Run project.py
6. Go to http://localhost:5000
7. Use the app
8. Ctrl+C to interrupt the app

**API endpoints**

The application provides the information of the database both in XML and JSON format through the following routes:

*List all disciplines with corresponding id*
XML: `/disciplines/XML`
JSON: `/disciplines/JSON`

*List all journals in a given discipline*
XML: `/disciplines/<discipline_id>/XML`
JSON: `/disciplines/<discipline_id>/JSON`

*Journal info page*
XML: `/journal/<int:journal_id>/XML`
JSON: `/journal/<int:journal_id>/JSON`





Hope you like it!
