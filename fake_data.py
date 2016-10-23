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
User1 = User(name="Miss Chiquita", email="miss@chiquita.com",
             picture='https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Chiquita_logo.svg/150px-Chiquita_logo.svg.png')
session.add(User1)
session.commit()

# Menu for UrbanBurger
company1 = Company(user_id=1, name="WorldCom")

session.add(company1)
session.commit()

job1 = Job(user_id=1, title="M&A analyst", description="Previous experience ignoring U.S. antitrust law required.", company=company1)

session.add(job1)
session.commit()


job2 = Job(user_id=1, title="Accounting Analyst", description="Create fake orders to inflate revenue. Excel skills desired, but not really required. Bonus: previous experience \"accidentally\" getting expenses and capital expenditure confused.", company=company1)

session.add(job2)
session.commit()

job3 = Job(user_id=1, title="CFO", description="Keep company from running out of money, at least on paper. Cook books so investors think everything is hunky dory.", company=company1)

session.add(job3)
session.commit()

company2 = Company(user_id=1, name="Lehman Brothers")

session.add(company2)
session.commit()

job4 = Job(user_id=1, title="Investment Banker",
                     description="Convince rich people to give you money so you can be rich too.", company=company2)

session.add(job4)
session.commit()

job_lb = Job(user_id=1, title="Quantitative Analyst",
                     description="Build mathematical models that simultaneously legitamize and obfuscate foolhardy charades like  \"credit default swaps.\"", company=company2)

session.add(job_lb)
session.commit()


job5 = Job(user_id=1, title="Vice President", description="Convince investors and shareholders that you've never been more confident about your firm's success in spite of the sky falling in plain view.", company=company2)

session.add(job1)
session.commit()


# Menu for Cocina Y Amor
company3 = Company(user_id=1, name="Monsanto")

session.add(company3)
session.commit()


job6 = Job(user_id=1, title="Staff Biologist",
                     description="Position requires advanced degree in biology from a top institution. Responsibilities include developing pesticides that kill literally everything.", company=company3)

session.add(job6)
session.commit()

job_mon = Job(user_id=1, title="Senior Geneticist",
                     description="Develop invincible zombie crops.", company=company3)

session.add(job_mon)
session.commit()

job_mon2 = Job(user_id=1, title="Logistics Analyst",
                     description="As a Logisitics Analyst, your primary responsibilty is to develop and improve business processes related to the transport of Monsanto products to public bodies of water for illegal dumping.", company=company3)

session.add(job_mon2)
session.commit()



company4 = Company(user_id=1, name="Enron")
session.add(company4)
session.commit()

job8 = Job(user_id=1, title="Executive", description="Job responsibilities include hiding losses to inflate stock price and subsequently going to prison.", company=company4)

session.add(job8)
session.commit

job9 = Job(user_id=1, title="Senior Interpretive Accountant",
                     description="We are seeking a top-notch Interpretative Accountant for our industry-reknowned Interpretative Accounting team. Prior experience in the creative interpretion of tax law required, including using modern tools like mark-to-market and shell corporations to hide losses", company=company4)

session.add(job9)
session.commit()

job10 = Job(user_id=1, title="Administrative Clerk",
                     description="Enron is seeking a new Administrative Clerk. You will provide support to the Interpretative Accounting team, including data entry, assisting with correspondence, and incinerating financial documents.", company=company4)

session.add(job10)
session.commit()


print "added companies and jobs!"
