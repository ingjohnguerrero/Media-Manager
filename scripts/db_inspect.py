import sqlite3
import pathlib

db_path = pathlib.Path(__file__).parents[1] / "mediamanager.db"
print("DB path:", db_path)
if not db_path.exists():
    print("Database file does not exist.")
    raise SystemExit(0)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# list tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cur.fetchall()]
print("Tables:", tables)

# print schema for media table if exists
if 'media' in tables:
    print('\nSchema for media:')
    cur.execute("PRAGMA table_info(media);")
    for row in cur.fetchall():
        print(row)
    print('\nRows in media:')
    cur.execute("SELECT id, alt_text, extension, url, media_type FROM media;")
    rows = cur.fetchall()
    for r in rows:
        print(r)
else:
    print('No media table found.')

conn.close()

