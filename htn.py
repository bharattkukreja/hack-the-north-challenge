import sqlite3
import json
import urllib2

# getting the json from the url
url = 'https://htn-interviews.firebaseio.com/users.json'
json_data = json.load(urllib2.urlopen(url))

db = sqlite3.connect('htn.db')
c = db.cursor()
print "Opened database successfully";

# users table
c.execute('''CREATE TABLE IF NOT EXISTS HTN
    (ID          INT PRIMARY KEY   NOT NULL,
     NAME        TEXT              NOT NULL,
     COMPANY     TEXT              NOT NULL,
     EMAIL       TEXT              NOT NULL,
     PHONE       TEXT              NOT NULL,
     PICTURE     TEXT              NOT NULL,
     LATITUDE    REAL              NOT NULL,
     LONGITUDE   REAL              NOT NULL);''')
db.commit();

# skills table
# ID is to ensure every tuple has a unique VALUES
# ID_HTN matches the user in htn table
c.execute('''CREATE TABLE IF NOT EXISTS SKILLS
    (ID      INT    PRIMARY KEY   NOT NULL,
     ID_HTN  TEXT                 NOT NULL,
     NAME    TEXT                 NOT NULL,
     RATING  REAL                 NOT NULL);''')
db.commit();
print "Tables created successfully";

# insert or ignore will ignore any duplicate id's
# would be used when the the program is executed more than once since table would
#   already exist in the database
query_applicants = "INSERT OR IGNORE INTO HTN VALUES (?,?,?,?,?,?,?,?)"
query_skills = "INSERT OR IGNORE INTO SKILLS VALUES (?,?,?,?)"
columns_applicants = ['name', 'company', 'email', 'phone', 'picture', 'latitude', 'longitude']
columns_skills = ['id_htn', 'id', 'name', 'rating']
count_htn = 1
count_skills = 1

for data in json_data:
    try:
        keys_applicants = (count_htn,) + tuple(data[c] for c in columns_applicants)
        c.execute(query_applicants, keys_applicants)
        db.commit();

        for skill in data['skills']:
            try:
                keys_skills = (count_skills, count_htn, skill['name'], skill['rating'])
                c.execute(query_skills, keys_skills)
                db.commit();
            except Exception as error:
                print error
            count_skills += 1
        count_htn += 1

    except Exception as error:
        print error

c.close()
