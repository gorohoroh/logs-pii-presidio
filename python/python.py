import logging
import psycopg2
from faker import Faker
from pii_logger import logger  # Import global logger

# Database connection settings
DB_CONFIG = {
    "dbname": "pii_database",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

fake = Faker()


# Database setup & seeding
def setup_database():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id SERIAL PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            dob DATE,
            ssn TEXT
        );
    """)

    cur.execute("SELECT COUNT(*) FROM persons;")
    count = cur.fetchone()[0]

    if count == 0:
        persons = [
            (fake.first_name(), fake.last_name(), fake.email(), fake.phone_number(), fake.address(),
             fake.date_of_birth(), fake.ssn())
            for _ in range(500)
        ]

        cur.executemany("""
            INSERT INTO persons (first_name, last_name, email, phone, address, dob, ssn) 
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, persons)
        conn.commit()

    cur.close()
    conn.close()


# Fetch and log person data
def log_person_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT first_name, last_name, email, phone, address, dob, ssn FROM persons;")
    persons = cur.fetchall()
    for person in persons:
        log_message = f"Person Info: Name: {person[0]} {person[1]}, Email: {person[2]}, Phone: {person[3]}, Address: {person[4]}, DOB: {person[5]}, SSN: {person[6]}"
        logger.info(log_message)
    cur.close()
    conn.close()


if __name__ == "__main__":
    setup_database()
    log_person_data()
    print("Logging complete. Check app.log for output.")
