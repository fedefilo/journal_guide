from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Users, Disciplines, Journals

engine = create_engine('sqlite:///journals.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Add Disciplines
discipline1 = Disciplines(name="Geography")
discipline2 = Disciplines(name="Philosophy")
discipline3 = Disciplines(name="History")
discipline4 = Disciplines(name="Political Science")
session.add(discipline1)
session.add(discipline2)
session.add(discipline3)
session.add(discipline4)
session.commit()

# Add test users
user1 = Users(first_name = "Fede", last_name = "Vazquez", email = "f@f.com")
user2 = Users(first_name = "Vicky", last_name = "Baratta", email = "v@v.com")

session.add(user1)
session.add(user2)
session.commit()

# Add two journals per discipline

# Geography

journal1 = Journals(title="Economic Geography", issn ="0013-0095", publisher = "Clark University", chief_editor = "John Doe", issues_per_year = 4 ,description="Journal about economic geography", disciplines = discipline1 , users = user1)

journal2 = Journals(title="Applied Geography", issn ="0143-6228", publisher = "Elsevier BV", chief_editor = "Jane Jackson", issues_per_year = 2 ,description="Journal about applied geography", disciplines = discipline1 , users = user2)
session.add(journal1)
session.add(journal2)
session.commit()

# Philosophy

journal3 = Journals(title="Synthese", issn ="0039-7857", publisher = "Reidel", chief_editor = "Ernest Sosa", issues_per_year = 4 ,description="Journal about general philosophy", disciplines = discipline2 , users = user1)

journal4 = Journals(title="Nous", issn ="0029-4624", publisher = "Wayne State University Press", chief_editor = "Plato Sanchez", issues_per_year = 12 ,description="Journal about theory of knowledge", disciplines = discipline2 , users = user2)
session.add(journal3)
session.add(journal4)
session.commit()

# History

journal5 = Journals(title="Hispanic American Historical Review", issn ="0018-2168", publisher = "Board of Editors HAHR", chief_editor = "Bona Batata", issues_per_year = 6 ,description="Journal about Hispanic History", disciplines = discipline3 , users = user1)

journal6 = Journals(title="Economic History Review", issn ="0013-0117", publisher = "Blackwell Inc.", chief_editor = "Charlemagne Gomez", issues_per_year = 3 ,description="Journal about Economic History", disciplines = discipline3 , users = user2)
session.add(journal5)
session.add(journal6)
session.commit()

# Political Science

journal7 = Journals(title="American Political Science Review", issn ="0003-0554", publisher = "Cambridge University Press", chief_editor = "Mr. President", issues_per_year = 1 ,description="Journal about Political Science, US centered.", disciplines = discipline4 , users = user1)

journal8 = Journals(title="Canadian Journal of Political Science", issn ="0013-0117", publisher = "Blackwell Inc.", chief_editor = "Mr. Vicepresident", issues_per_year = 3 ,description="Journal about Political Science - Canadian perspectives", disciplines = discipline4 , users = user2)
session.add(journal7)
session.add(journal8)
session.commit()

print "added menu items!"