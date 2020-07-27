
def scan_barcode():
    try:
        barcode = str(getpass(prompt=""))
        print(barcode)
#            cursor.execute(f"insert into blood_sample (test_id) values ({barcode});")
#            db.commit()
#            print("Entry added")
    except KeyboardInterrupt:
        print("Bye!")
        sys.exit(0)

def main():
#    cursor, db = get_db_components()
    scan_barcode()

if __name__ == "__main__":
    main()
