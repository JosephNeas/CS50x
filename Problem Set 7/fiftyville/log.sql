-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Look for all crimes that took place on July 28, 2021 and get the ID, notice a description of the CS50 duck being taken from a BAKERY in the crime report IDed at 10:15
-- Crime ID: 295
SELECT description, id FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28;

-- Look at the interviews from July 28, 2021 notice there is one mentioning a bakery with the ID 161
-- ID 161, NAME = RUTH (interviewee), look at left of the parking lot for the bakery
-- ID 162, NAME = Eugene (interviewee), ATM Leggett Street criminal took money out in the morning
-- ID 163, NAME = Raymond, saw the criminal talk to someone right after the crime for less than a minute and was planning to take a flight to Fiftyville and asked
-- the other person on the phone to buy them a ticket
SELECT name, transcript, id FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;

-- find any info from the atm transaction
-- Get the names of Kenny, Iman, Taylor, Brooke, Luca, Diana, Bruce whose license plates where all on the bakery's secutriy camera the day of the crime
-- looking at license plates that arrive close to the robbery is and leaves quick after is plate: 4328GD8 who also happened to use the atm that day
-- five people leave at 10, Luca, Taylor, Bruce, Iman, and Diana
-- Bruce leaves within minutes of the robbery being commited
SELECT DISTINCT(name), activity, hour, minute FROM people, bakery_security_logs, atm_transactions, bank_accounts WHERE atm_transactions.account_number = bank_accounts.account_number
AND bank_accounts.person_id = people.id AND bakery_security_logs.license_plate = people.license_plate AND atm_transactions.year = 2021 AND atm_transactions.month = 7
AND atm_transactions.day = 28 AND bakery_security_logs.hour < 11 AND atm_transactions.atm_location = "Leggett Street" ORDER BY hour;

-- look at bruce's number to see if he called somone for less than a minute on the day of the crime
-- See that there is a call where Bruce is on the phone for less than a minute calling the number "(375) 555-8161"
SELECT duration, caller, receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND caller IN (SELECT phone_number FROM people WHERE name = "Bruce");

-- look at who is that number Bruce called, get the name robin
SELECT name, passport_number FROM people WHERE phone_number = "(375) 555-8161";

-- check if Bruce took any flights from Fiftyville to somewhere else on July 29th, 2021
SELECT DISTINCT(origin_airport_id) from flights WHERE origin_airport_id IN (SELECT id FROM airports WHERE city = "Fiftyville");

-- he went to new york city
SELECT city FROM flights, airports, passengers, people WHERE flights.destination_airport_id = airports.id
AND passengers.flight_id = flights.id AND passengers.passport_number = people.passport_number
AND people.name = "Bruce" AND flights.origin_airport_id = 8 AND flights.year = 2021 AND flights.month = 7 and flights.day = 29;