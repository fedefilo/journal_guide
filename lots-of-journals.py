# Udacity Full Stack Web Developer Nanodegree
# Project 3 - Item catalog
# Journal Catalog App
# by Federico Vasen
# File with database test suite
# Dec 23, 2015

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Users, Disciplines, Journals


# Database connect and session start
engine = create_engine('sqlite:///journals.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
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
user1 = Users(name="Fede", email="f@f.com")
user2 = Users(name="Vicky", email="v@v.com")

session.add(user1)
session.add(user2)
session.commit()

# Add two journals per discipline

# Geography

journal1 = Journals(
    title="Economic Geography",
    issn="0013-0095",
    publisher="Clark University",
    chief_editor="John Doe",
    issues_per_year=4,
    description="Journal about economic geography",
    disciplines=discipline1,
    users=user1,
    picture="1.jpg")

journal2 = Journals(
    title="Applied Geography",
    issn="0143-6228",
    publisher="Elsevier BV",
    chief_editor="Jane Jackson",
    issues_per_year=2,
    description="Journal about applied geography",
    disciplines=discipline1,
    users=user2,
    picture="2.gif")
session.add(journal1)
session.add(journal2)
session.commit()

# Philosophy

journal3 = Journals(
    title="Synthese",
    issn="0039-7857",
    publisher="Reidel",
    chief_editor="Ernest Sosa",
    issues_per_year=4,
    description="Journal about general philosophy",
    disciplines=discipline2,
    users=user1,
    picture="3.jpg")

journal4 = Journals(
    title="Nous",
    issn="0029-4624",
    publisher="Wayne State University Press",
    chief_editor="Plato Sanchez",
    issues_per_year=12,
    description="Journal about theory of knowledge",
    disciplines=discipline2,
    users=user2,
    picture="4.gif")
session.add(journal3)
session.add(journal4)
session.commit()

# History

journal5 = Journals(
    title="Hispanic American Historical Review",
    issn="0018-2168",
    publisher="Board of Editors HAHR",
    chief_editor="Bona Batata",
    issues_per_year=6,
    description="Journal about Hispanic History",
    disciplines=discipline3,
    users=user1)

journal6 = Journals(
    title="Economic History Review",
    issn="0013-0117",
    publisher="Blackwell Inc.",
    chief_editor="Charlemagne Gomez",
    issues_per_year=3,
    description="Journal about Economic History",
    disciplines=discipline3,
    users=user2)
session.add(journal5)
session.add(journal6)
session.commit()

# Political Science

journal7 = Journals(
    title="American Political Science Review",
    issn="0003-0554",
    publisher="Cambridge University Press",
    chief_editor="Mr. President",
    issues_per_year=1,
    description="Journal about Political Science, US centered.",
    disciplines=discipline4,
    users=user1)

journal8 = Journals(
    title="Canadian Journal of Political Science",
    issn="0013-0117", publisher="Blackwell Inc.",
    chief_editor="Mr. Vicepresident",
    issues_per_year=3,
    description="Journal about Political Science - Canadian perspectives",
    disciplines=discipline4,
    users=user2)
session.add(journal7)
session.add(journal8)
session.commit()

print "added menu items!"
