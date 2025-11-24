import mysql.connector
from dotenv import load_dotenv
import os
import argparse

def removeDuplicates():
    with conn.cursor() as cursor:
        cursor.execute("""
        WITH cte AS (
            SELECT *,
                   ROW_NUMBER() OVER(PARTITION BY username, passwd, hash, descript ORDER BY id) AS rn
            FROM users
        )
        DELETE FROM users
        WHERE id IN (
            SELECT id FROM cte WHERE rn > 1
        );
        """)
        conn.commit()
    print("[+] deleted duplicates")

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Input file")
parser.add_argument("-u", "--user", help="User")
parser.add_argument("-H", "--hash", action="store_true", help="Flag for adding hash into database")


args = parser.parse_args()

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database="kraken_db"
)

cursor = conn.cursor()

# flags
file_name = args.file.split("/")[-1]
print(file_name)

if args.user == None:
    user_for_db = "<BLANK>"
else:
    user_for_db = args.user

print(user_for_db)

batch_size = 10000
batch = []

with open(args.file, "r") as f:
    for i, line in enumerate(f, start=1):
        passwd = line.strip()
        if not passwd:
            continue

        if args.hash:
            batch.append((user_for_db, "", passwd, file_name))
        else:
            batch.append((user_for_db, passwd, "", file_name))
        

        if i % batch_size == 0:
            cursor.executemany(
                "INSERT IGNORE INTO users (username, passwd, hash, descript) VALUES (%s, %s, %s, %s)",
                batch
            )
            conn.commit()
            batch = []
            print(f"[i] {i} lines added ")

# insert rest
if batch:
    cursor.executemany(
        "INSERT IGNORE INTO users (username, passwd, hash, descript) VALUES (%s, %s, %s, %s)",
        batch
    )
    conn.commit()
    print(f"[+] {i} total lines inserted.")

'''
cursor.execute("SELECT * from users")

for fila in cursor.fetchall():
    print(fila)
'''

removeDuplicates()

conn.close()
