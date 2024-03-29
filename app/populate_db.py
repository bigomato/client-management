from datetime import date, datetime
import random
import requests
import json

from app import db
from app.models.models import *


def generate_fake_persons(
    number_of_persons: int, db=db, seed="foobar", use_randomuser=True
):
    # https://randomuser.me/api/?results={number_of_persons}
    res = requests.get(
        "https://randomuser.me/api/",
        params={
            "results": number_of_persons,
            "inc": "name, dob, location, phone, email",
            "nat": "DE",
            "seed": seed,
        },
    )
    data = json.loads(res.text)
    entries = []
    for person in data["results"]:
        r = random.randint(0, 1)
        p = Person(
            name=person["name"]["first"],
            surname=person["name"]["last"],
            birthdate=datetime.strptime(person["dob"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            our_client=r,
            our_lawyer=not r,
        )
        adress = Address(
            street=person["location"]["street"]["name"],
            house_number=person["location"]["street"]["number"],
            zip_code=person["location"]["postcode"],
            city=person["location"]["city"],
            country=person["location"]["country"],
        )
        p.address = adress
        contact = ContactInfo(
            phone_number=person["phone"],
            email=person["email"],
            person=p,
        )
        entries.append(p)
        entries.append(adress)
        entries.append(contact)
    db.session.add_all(entries)


def generate_fake_cases(number_of_cases, db=db, seed="foobar"):
    persons = db.session.query(Person).filter(Person.our_client == True).all()
    lawyers = db.session.query(Person).filter(Person.our_lawyer == True).all()
    addresses = db.session.query(Address).all()
    for i in range(number_of_cases):
        status = random.choice([CaseStatus.ongoing, CaseStatus.won, CaseStatus.lost])
        case = Case(
            name=f"Case {i}", description=f"Description {i}", case_status=status
        )
        db.session.add(case)

        # involvements
        for j in range(2):
            person = random.choice(persons)
            lawyer = random.choice(lawyers)
            r = InvolvementRole.victim if j % 2 == 0 else InvolvementRole.suspect
            lr = (
                InvolvementRole.victim_lawyer
                if j % 2 == 0
                else InvolvementRole.suspect_lawyer
            )
            inv = Involved(
                person=person,
                case=case,
                role=r,
            )
            lawyer_inv = Involved(
                person=lawyer,
                case=case,
                role=lr,
            )
            inv.lawyers.append(lawyer_inv)
            db.session.add(inv, lawyer_inv)

        # trials
        for j in range(2):
            trial = Trial(
                name=f"Trial {j}",
                description=f"Description {j}",
                date=date.today(),
                case=case,
                address=random.choice(addresses),
            )
            db.session.add(trial)

            judgement = Judgement(
                description=f"Judgement {j} for trial {trial.id}",
                trial=trial,
                date=date.today(),
                judgement=JudgemenType.other,
            )
            db.session.add(judgement)

        # documents
        for k in range(2):
            doc = Document(
                name=f"Document {k} for case {case.name}",
                description=f"This is document {k} for case {case.name}",
                path=f"/docs/{case.name}/document_{k}.pdf",
                date=date.today(),
                case=case,
            )
            db.session.add(doc)

    db.session.commit()


session = db.session


def populate_db():
    print("Populating database...")
    generate_fake_persons(200)
    print("Generated fake persons")
    generate_fake_cases(100)
    print("Generated fake cases")
    # get all cases
    person1 = Person(
        name="John", surname="Doe", birthdate=date(1990, 1, 1), our_client=True
    )
    person2 = Person(name="Jane", surname="Doe", birthdate=date(1991, 1, 1))
    person3 = Person(
        name="Max", surname="Mustermann", birthdate=date(1992, 1, 1), our_lawyer=True
    )
    person4 = Person(name="Erika", surname="Mustermann", birthdate=date(1993, 1, 1))

    session.add_all([person1, person2, person3, person4])
    session.commit()

    address1 = Address(
        street="Main Street",
        house_number="1",
        zip_code="12345",
        city="New York",
        country="USA",
    )
    address2 = Address(
        street="Second Street",
        house_number="2",
        zip_code="23456",
        city="Los Angeles",
        country="USA",
    )

    session.add_all([address1, address2])
    session.commit()

    # make john doe live in new york
    john_doe = session.query(Person).filter(Person.name == "John").first()
    adddress_new_york = (
        session.query(Address).filter(Address.city == "New York").first()
    )
    john_doe.address = adddress_new_york
    session.commit()

    case1 = Case(name="Case 1", description="Description 1")
    inv1 = Involved(person=john_doe, case=case1, role=InvolvementRole.victim)
    inv2 = Involved(person=person2, case=case1, role=InvolvementRole.suspect)
    inv3 = Involved(person=person3, case=case1, role=InvolvementRole.victim_lawyer)
    inv4 = Involved(person=person4, case=case1, role=InvolvementRole.suspect_lawyer)

    session.add_all([case1, inv1, inv2, inv3, inv4])
    session.commit()

    doc1 = Document(
        name="Document 1", path="path/to/document1", case=case1, date=date(2020, 1, 1)
    )
    doc2 = Document(
        name="Document 2", path="path/to/document2", case=case1, date=date(2020, 1, 2)
    )
    doc3 = Document(
        name="Document 3", path="path/to/document3", case=case1, date=date(2020, 1, 3)
    )

    session.add_all([doc1, doc2, doc3])
    session.commit()

    trial1 = Trial(
        name="Trial 1",
        description="Description 1",
        date=date(2020, 1, 1),
        case=case1,
        address=adddress_new_york,
    )

    trial2 = Trial(
        date=date(2020, 1, 2),
        description="Description 2",
        case=case1,
        address=address2,
        name="Trial 2",
    )
    trial3 = Trial(
        date=date(2020, 1, 3),
        description="Description 3",
        case=case1,
        address=address1,
        name="Trial 3",
    )

    session.add_all([trial1, trial2, trial3])
    session.commit()

    vicitim = (
        session.query(Involved)
        .filter(Involved.case == case1)
        .filter(Involved.role == InvolvementRole.victim)
        .first()
    )

    suspect = (
        session.query(Involved)
        .filter(Involved.case == case1)
        .filter(Involved.role == InvolvementRole.suspect)
        .first()
    )

    suspect_lawyer = (
        session.query(Involved)
        .filter(Involved.case == case1)
        .filter(Involved.role == InvolvementRole.suspect_lawyer)
        .first()
    )

    victim_lawyer = (
        session.query(Involved)
        .filter(Involved.case == case1)
        .filter(Involved.role == InvolvementRole.victim_lawyer)
        .first()
    )

    vicitim.lawyers.append(victim_lawyer)
    suspect.lawyers.append(suspect_lawyer)

    session.commit()

    trial = (
        session.query(Trial)
        .join(Case)
        .filter(Case.name == "Case 1")
        .order_by(Trial.date)
        .all()
    )

    # get case with first hearing
    case = session.query(Case).join(Trial).filter(Trial.id == trial[0].id).first()

    for inv in case.involved:
        inv.attend(trial[0])

    case.involved[0].attend(trial[1])
    case.involved[1].attend(trial[1])
    case.involved[0].attend(trial[2])
    case.involved[1].attend(trial[2])
    case.involved[3].attend(trial[2])

    contact_joe = ContactInfo(
        email="john@gamil.com", phone_number="123456789", person=john_doe
    )

    session.add(contact_joe)
    session.commit()

    # print(john_doe)

    judgement1 = Judgement(
        description="Description 1",
        trial_id=trial[0].id,
        date=date(2020, 1, 1),
        judgement=JudgemenType.condemnation,
    )

    session.add(judgement1)
    session.commit()
