import mysql.connector
from dotenv import load_dotenv
import os
import argparse

def searchBy(args):
    cursor = conn.cursor()

    finalQuery = "SELECT * FROM users"
    conditions = []
    values = []

    if args.dump is not None:
        # code for replacing the "*" with the database
        if "*" in args.dump or "%" in args.dump:
            pattern = args.dump.replace("*", "%")
            conditions.append("descript LIKE %s")
            values.append(pattern)
        else:
            conditions.append("descript = %s")
            values.append(args.dump)

    if args.user is not None:
        # code for replacing the "*" with the database
        if "*" in args.user or "%" in args.user:
            pattern = args.user.replace("*", "%")
            conditions.append("username LIKE %s")
            values.append(pattern)
        else:
            conditions.append("username = %s")
            values.append(args.user)

    if args.passwd is not None:
        # code for replacing the "*" with the database
        if "*" in args.passwd or "%" in args.passwd:
            pattern = args.passwd.replace("*", "%")
            conditions.append("passwd LIKE %s")
            values.append(pattern)
        else:
            conditions.append("passwd = %s")
            values.append(args.passwd)

    if conditions:
        finalQuery += " WHERE " + " AND ".join(conditions)

    cursor.execute(finalQuery, tuple(values))

    condition_file = False

    if args.file is not None:
        condition_file = True
        if os.path.isfile(args.file):
            print(f"The file exists. Changing the name of the file to {args.file}_dump.txt")
            file_dump = args.file + "_dump.txt"
        else:
            print(f"Creating the file {args.file}")
            file_dump = args.file


    # --- DUMP RESULTS ---
    results = cursor.fetchall()

    BATCH_SIZE = 5000  

    if condition_file == False:
        for result in results:
            print(result[2])

    else:
        with open(file_dump, "w") as out:
            buffer = []
            count = 0

            for result in results:
                buffer.append(result[2] + "\n")
                count += 1

                if count >= BATCH_SIZE:
                    out.writelines(buffer)
                    buffer = []
                    count = 0

            if buffer:
                out.writelines(buffer)


    cursor.close()

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="User search")
parser.add_argument("-p", "--passwd", help="Password search")
parser.add_argument("-d", "--dump", help="dump file in database")
parser.add_argument("-f", "--file", help="File to dump")

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

searchBy(args)
conn.close()

