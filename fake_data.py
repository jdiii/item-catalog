from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Company, Base, Job, User

engine = create_engine('sqlite:///jobboard.db')
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


# Create dummy user
User1 = User(name="Ferdinand Porsche", email="ferdinand@porsche.com",
             picture='https://s-media-cache-ak0.pinimg.com/564x/0e/1b/b3/0e1bb3db11cd615501e43e09d048893a.jpg')
session.add(User1)
session.commit()

# Menu for UrbanBurger
company1 = Company(user_id=1, name="WorldCom")

session.add(company1)
session.commit()

job1 = Job(user_id=1, title="Sales Manager", description="Sell telecom stuff to people. Requires people skills and, because we like to hire people who are extremely boring, 15 years of sales experience.", company=company1)

session.add(job1)
session.commit()


job2 = Job(user_id=1, title="Network Engineer", description="As a network engineer, you will connect some cables to some other cables.", company=company1)

session.add(job2)
session.commit()

job3 = Job(user_id=1, title="CFO", description="Keep company from running out of money. Cook books so investors think everything is hunky dory.", company=company1)

session.add(job3)
session.commit()

company2 = Company(user_id=1, name="Lehman Brothers")

session.add(company2)
session.commit()

job4 = Job(user_id=1, title="Investment Banker",
                     description="Convince rich people to give you money so you can be rich too", company=company2)

session.add(job4)
session.commit()


job5 = Job(user_id=1, title="Partner", description="Convince investors and shareholders that you've never been more confident about your firm's success.", company=company2)

session.add(job1)
session.commit()


# Menu for Cocina Y Amor
company3 = Company(user_id=1, name="Kmart")

session.add(company3)
session.commit()


job6 = Job(user_id=1, title="Retail Cashier",
                     description="Stand idly by cash register in empty retail store, awaiting layoffs.", company=company3)

session.add(job6)
session.commit()

job7 = Job(user_id=1, title="CEO", description="Job responsibilities include failing to respond to changing market conditions, declaring bankrupcy, taking home large paycheck.", company=company3)

session.add(job7)
session.commit()


company4 = Company(user_id=1, name="Enron")
session.add(company4)
session.commit()

job8 = Job(user_id=1, title="Executive", description="Job responsibilities include hiding losses to inflate stock price, going to prison.", company=company4)

session.add(job8)
session.commit

job9 = Job(user_id=1, title="Accountant",
                     description="Your role will be in interpretative accouting. Skills required include willfully misinterpreting tax law and  \"accidentally\" leaving out negative signs on financial disclosures.", company=company4)

session.add(job9)
session.commit()


print "added companies and jobs!"
