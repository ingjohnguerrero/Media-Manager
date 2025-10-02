import sqlite3
import pathlib

DB = pathlib.Path(__file__).parents[1] / "mediamanager.db"
print("DB path:", DB)
if not DB.exists():
    print("No DB file to migrate. Exiting.")
    raise SystemExit(0)

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Check if media table exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='media';")
if not cur.fetchall():
    print("No media table found. Exiting.")
    conn.close()
    raise SystemExit(0)

# Check if media_type column exists
cur.execute("PRAGMA table_info(media);")
cols = [r[1] for r in cur.fetchall()]
print("Existing media columns:", cols)
if 'media_type' in cols:
    print("Column 'media_type' already exists. Nothing to do.")
    conn.close()
    raise SystemExit(0)

# Add the column with a default so existing rows get a value
print("Adding 'media_type' column to media table...")
cur.execute("ALTER TABLE media ADD COLUMN media_type TEXT DEFAULT 'media';")
conn.commit()
print("Column added.")

# Ensure no NULLs: set default 'media' where NULL
cur.execute("UPDATE media SET media_type = 'media' WHERE media_type IS NULL;")
conn.commit()
print("Updated existing rows where necessary.")

# Show final schema
cur.execute("PRAGMA table_info(media);")
for row in cur.fetchall():
    print(row)

conn.close()
print("Migration complete.")

