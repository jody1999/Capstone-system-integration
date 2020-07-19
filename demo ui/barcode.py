import mysql.connector as mysql
import sys
from getpass import getpass

def get_db_components():
    db = mysql.connect(host='localhost', user="smart", passwd="password", database="smart_system")
    cursor = db.cursor()
    return cursor, db

def scan_barcode(cursor, db):
    while(True):
        try:
            barcode = str(getpass(prompt=""))
            cursor.execute(f"insert into blood_sample (test_id) values ({barcode});")
            db.commit()
            print("Entry added")
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit(0)

def main():
    cursor, db = get_db_components()
    scan_barcode(cursor, db)

if __name__ == "__main__":
    main()
