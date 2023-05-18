from datetime import date, datetime
from databse import session
from models import *
import requests
import json


def generate_fake_persons(number_of_persons: int, session=session, seed="foobar"):
    # https://randomuser.me/api/?results={number_of_persons}
    res = requests.get(
        "https://randomuser.me/api/",
        params={
            "results": number_of_persons,
            "inc": "name, dob",
            "nat": "de",
            "seed": seed,
        },
    )
    data = json.loads(res.text)
    persons = []
    for person in data["results"]:
        persons.append(
            Person(
                name=person["name"]["first"],
                surname=person["name"]["last"],
                birthdate=datetime.strptime(
                    person["dob"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            )
        )
    session.add_all(persons)


if __name__ == "__main__":
    person1 = Person(name="John", surname="Doe", birthdate=date(1990, 1, 1))
    person2 = Person(name="Jane", surname="Doe", birthdate=date(1991, 1, 1))
    person3 = Person(name="Max", surname="Mustermann", birthdate=date(1992, 1, 1))
    person4 = Person(name="Erika", surname="Mustermann", birthdate=date(1993, 1, 1))

    session.add_all([person1, person2, person3, person4])
    session.commit()
