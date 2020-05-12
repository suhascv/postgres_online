import psycopg2
import io
import sys
import pandas as pd


#takes input through command line.
#should contain football.csv in the same directory.
#first argument is database.
#second argument is password of your postgres localserver.

conn = psycopg2.connect(database=sys.argv[1],user='postgres',password=sys.argv[2],host='localhost',port=5432)
cur=conn.cursor()

print('database connected')

#schema
createFootball='''CREATE SCHEMA fb'''
cur.execute(createFootball)

print('schema fb created')

fields=['Name','Age','Nationality','Overall','Club','Value','Wage','Preferred Foot','Position']
temp=pd.read_csv('football.csv',usecols=fields)
df=temp.head(100)
countires = df.Nationality.unique()
clubs=df.Club.unique()

print('fb.country created')
#print(countires)
createCountry='''CREATE TABLE fb.Country(country_id SERIAL PRIMARY KEY,name VARCHAR(100) UNIQUE);'''
cur.execute(createCountry)

for country in countires:
    query='''INSERT INTO fb.country(name) VALUES ('{}');'''.format(country)
    cur.execute(query)

print('fb.country updated with data')

cur.execute('''INSERT INTO fb.country(name) VALUES ('Japan'),('China') ;''')
#print(clubs)update fb.players set wage=wage*1000;

Spain=['FC Barcelona','Real Madrid','Atlético Madrid','Valencia CF']
Italy=['Juventus','Milan','Inter','Lazio','Napoli','Roma']
England=['Manchester United','Manchester City','Chelsea','Tottenham Hotspur','Liverpool','Arsenal']
France=['Paris Saint-Germain','Olympique Lyonnais']
Germany=['FC Bayern München','Borussia Dortmund']
Portugal=['FC Porto']
Japan=['Vissel Kobe']
China=['Guangzhou Evergrande Taobao FC']

CreateClub='''CREATE TABLE fb.club(club_id SERIAL PRIMARY KEY,name VARCHAR(100) UNIQUE,country INTEGER REFERENCES fb.country(country_id));'''
cur.execute(CreateClub)
print('fb.club created')

for club in clubs:
    country=''
    if club in Spain:
        country='Spain'
    elif club in Italy:
        country='Italy'
    elif club in England:
        country='England'
    elif club in France:
        country='France'
    elif club in Germany:
        country='Germany'
    elif club in Portugal:
        country='Portugal'
    elif club in Japan:
        country='Japan'
    elif club in China:
        country='China'
    query='''SELECT  * from fb.country where name='{}' ;'''.format(country)
    cur.execute(query)
    c=cur.fetchall()
    #print(c,club)
    cid=c[0][0]
    
    query='''INSERT INTO fb.club(name,country) VALUES ('{}',{});'''.format(club,cid)
    cur.execute(query)


print('fb.club updated with data')

createPlayers='''CREATE TABLE fb.player(player_id SERIAL PRIMARY KEY,
              name VARCHAR(100),age INTEGER,nationality INTEGER REFERENCES fb.country(country_id),
              overall_rating NUMERIC,club INTEGER REFERENCES fb.club(club_id),value NUMERIC,Wage NUMERIC,
              preferred_foot VARCHAR(30),position VARCHAR(30));'''


print('fb.player created')
cur.execute(createPlayers)

query='''SELECT * from fb.club;'''
cur.execute(query)

clubs={}
for d in cur.fetchall():
    clubs[d[1]]=d[0]

countries={}

query='''SELECT * from fb.country;'''
cur.execute(query) 

for d in cur.fetchall():
    countries[d[1]]=d[0]

try:
    df['Nationality'].replace(countries,inplace=True)
    df['Club'].replace(clubs,inplace=True)
    df['Value']=df['Value'].str[1:-1]
    df['Wage']=df['Wage'].str[1:-1]
    df['Value']=pd.to_numeric(pd.Series(df.Value))
    df['Wage']=pd.to_numeric(pd.Series(df.Wage))

except:
    pass

buf=io.StringIO()
df.to_csv(buf,sep='\t',header=False,index=False)
buf.seek(0)
cur.copy_from(buf,'fb.player',columns=['name','age','nationality','overall_rating','club','value','wage','preferred_foot','position'])

cur.execute("update fb.player set value=value*1000000;")
cur.execute("update fb.player set wage=wage*1000;")

print('fb.country updated with data')

conn.commit()