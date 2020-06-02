import json
import sqlite3

conn = sqlite3.connect('mytracks.sqlite')
cur = conn.cursor()

cur.executescript('''
    DROP TABLE IF EXISTS ARTIST;
    DROP TABLE IF EXISTS ALBUM;
    DROP TABLE IF EXISTS TRACKS;

    CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);
CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER
);
''')

with open('YourLibrary.json') as fh:
    data = json.load(fh)


for item in data['tracks']:
    artist = item['artist']
    album = item['album']
    track = item['track']

    print(track, album, artist)

    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', (artist, ))
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id) 
        VALUES ( ?, ?)''',
                (track, album_id))

    conn.commit()
