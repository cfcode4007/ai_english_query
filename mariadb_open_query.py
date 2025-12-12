from mariadb_connector import MariaDBConnection
import getpass
import sys

host = "192.168.123.244"
port = int("3306")
user = "colin"
database = "nation"

def safe_get_password(prompt="MariaDB password"):
    """Only ask for password when actually needed"""
    return getpass.getpass(prompt=prompt + ": ")

def main():

    password = safe_get_password(f"Password for {user}@{host}:")

    try:

        db = MariaDBConnection(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        # Now switch to the actual database for testing
        db.config['database'] = database
        db._connect()  # Reconnect with database selected

    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
    
    while True:
        sql = input("Enter a query string: ")
        if sql == "/bye" or sql == "/exit" or sql == "/quit":
            db.close
            break
        elif sql.startswith("/askai"):
            print(f"Input starts with /askai")
            continue

        try:
            results = db.execute(sql)
            if isinstance(results, list) and len(results) > 0:
                for row in results[:5]:  # Limit output
                    print("   →", row)
                if len(results) > 5:
                    print(f"   ... and {len(results) - 5} more rows")
            else:
                print("   → No rows returned" if results == [] else "   → Query OK")
            print()
        except Exception as e:
            print(f"   ERROR: {e}\n")
        finally:
            db.close()


if __name__ == "__main__":
    main()