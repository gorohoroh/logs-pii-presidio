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
    for person in persons[:5]:  # Logging only 5 for testing purposes
        log_message = f"Person Info: Name: {person[0]} {person[1]}, Email: {person[2]}, Phone: {person[3]}, Address: {person[4]}, DOB: {person[5]}, SSN: {person[6]}"
        logger.info(log_message)

        # Logging individual fields
        logger.info(f"Logging email only: {person[2]}")
        logger.info(f"Logging phone only: {person[3]}")
        logger.info(f"Logging address only: {person[4]}")

        # Logging an object simulation
        person_obj = {
            "first_name": person[0],
            "last_name": person[1],
            "email": person[2],
            "phone": person[3],
            "address": person[4],
            "dob": person[5],
            "ssn": person[6]
        }
        logger.info(f"Logging full person object: {person_obj}")

    # Logging random PII data not from database
    logger.info(
        f"Customer Support received a call from {fake.first_name()} {fake.last_name()} at {fake.phone_number()} regarding their order.")
    logger.info(f"Suspicious login attempt detected for user {fake.email()} from IP 192.168.1.101.")
    logger.info(f"New employee onboarded: {fake.first_name()} {fake.last_name()}, SSN: {fake.ssn()}.")
    logger.info(
        f"Medical record processed for patient {fake.first_name()} {fake.last_name()}, DOB: {fake.date_of_birth()}.")
    logger.info(f"Shipping details updated for {fake.first_name()} {fake.last_name()} at {fake.address()}.")

    # Additional test cases for log filtering
    logger.info(f"DEBUG: Processing payment for 1234-5678-9876-5432, user email: {fake.email()}.")
    logger.info(
        f"User feedback: 'I, {fake.first_name()} {fake.last_name()}, had an issue with my account {fake.email()}.'")

    response_data = {"user": {"name": fake.name(), "ssn": fake.ssn(), "email": fake.email()}}
    logger.info(f"API response: {response_data}")

    logger.info(f"Multi-line log test:\nUser: {fake.name()}\nEmail: {fake.email()}\nPhone: {fake.phone_number()}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    setup_database()
    log_person_data()
    print("Logging complete. Check app.log for output.")
