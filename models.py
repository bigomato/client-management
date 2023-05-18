from sqlalchemy import Column, Date, Integer, String, Table, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()

# All models inherit from Base
# Classes which still have to be created:
# - Person (needs to be extended with contact information and address)
# - Address
# - Contact
# - Case
# - Trial
# - Plaintiff
# - Defendant
# - DefendantLawyer
# - PlaintiffLawyer
# - Judgement
# - Document
# - Enum for the Judgement.type field (see https://michaelcho.me/article/using-python-enums-in-sqlalchemy-models)
# - Enum for the Person.role field


# Keine Klasse weil es eine einfache m zu n Besziehung ist
attends = Table(
    "attends",
    Base.metadata,
    Column("trial_id", Integer, ForeignKey("trial.id")),
    Column("person_id", Integer, ForeignKey("involved.id")),
)


representing = Table(
    "representing",
    Base.metadata,
    Column("client_id", Integer, ForeignKey("involved.id")),
    Column("lawyer_id", Integer, ForeignKey("involved.id")),
)


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=True)
    adress_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    contactinfos = relationship("ContactInfo", backref="person")
    # TODO: add contact information and address

    def __repr__(self):
        return "<Person(name='{}', surname='{}', birthdate='{}', role='{}')>".format(
            self.name, self.surname, self.birthdate, self.role
        )

    def __str__(self):
        return "{} {}".format(self.name, self.surname)


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    zip_code = Column(String(50), nullable=False)
    street = Column(String(50), nullable=True)
    house_number = Column(String(50), nullable=True)
    persons = relationship("Person", backref="address")

    def __repr__(self):
        return "<Address(country='{}', city='{}', zip_code='{}', street='{}', house_number='{}')>".format(
            self.country, self.city, self.zip_code, self.street, self.house_number
        )

    def __str__(self):
        return "{}, {} {}".format(self.country, self.city, self.zip_code)


class ContactInfo(Base):
    __tablename__ = "contact_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    person_id = Column(Integer, ForeignKey("person.id"), nullable=False)

    def __repr__(self):
        return "<ContactInfo(phone_number='{}', email='{}')>".format(
            self.phone_number, self.email
        )

    def __str__(self):
        return "{}, {}".format(self.email, self.phone_number)


class Case(Base):
    __tablename__ = "case"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String, nullable=False)

    involved = relationship("Involved", backref="case")
    documents = relationship("Document", backref="case")
    trials = relationship("Trial", backref="case")

    def __repr__(self):
        return "<Case(name='{}', description='{}')>".format(self.name, self.description)

    def __str__(self):
        return self.name


class Involved(Base):
    __tablename__ = "involved"
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("case.id"), nullable=False)
    role = Column(String(50), nullable=False)
    # TODO:Enum for the Involved.role field
    attendees = relationship("Trial", secondary=attends, back_populates="attendees")
    clients = relationship(
        "Involved",
        secondary=representing,
        primaryjoin=id == representing.c.lawyer_id,
        secondaryjoin=id == representing.c.client_id,
        backref="lawyers",
    )

    def __repr__(self):
        return "<Involved(person='{}', case='{}', role='{}')>".format(
            self.person_id, self.case_id, self.role
        )

    def __str__(self):
        return "{}, {}".format(self.person, self.case)


class Trial(Base):
    __tablename__ = "trial"
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("case.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    attendees = relationship("Involved", secondary=attends, back_populates="attendees")
    judgement = relationship("Judgement", backref="trial", uselist=False)

    def __repr__(self):
        return "<Trial(name='{}', description='{}')>".format(
            self.name, self.description
        )

    def __str__(self):
        return self.name


class Document(Base):
    __tablename__ = "document"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    case_id = Column(Integer, ForeignKey("case.id"), nullable=False)
    path = Column(String, nullable=False)  # Dateipfad

    def __repr__(self):
        return "<Document(name='{}', description='{}')>".format(
            self.name, self.description
        )

    def __str__(self):
        return self.name


class Judgement(Base):
    __tablename__ = "judgement"
    id = Column(Integer, primary_key=True, autoincrement=True)
    decision = Column(String(50), nullable=False)
    # TODO: Enum for the Judgement.type fiel
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    document_id = Column(Integer, ForeignKey("document.id"), nullable=True)
    trial_id = Column(Integer, ForeignKey("trial.id"), nullable=False)

    def __repr__(self):
        return "<Judgement(type='{}', date='{}')>".format(self.type, self.date)

    def __str__(self):
        return self.type
