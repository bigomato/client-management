from datetime import datetime
from databse import session
from models import Person, PersonRole
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
    generate_fake_persons(10)
    session.commit()

    for person in session.query(Person).all():
        print(str(person) + " is a " + str(PersonRole(person.role).name))
