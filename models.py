from sqlalchemy import Column, Date, Integer, String, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
import enum

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


class PersonRole(enum.IntEnum):
    our_client = 1
    their_client = 2
    our_lawyer = 3
    their_lawyer = 4
    judge = 5
    witness = 6
    expert = 7
    other = 8


class IntEnumType(TypeDecorator):
    """
    Allows storing Python's IntEnum as an Integer in the database.
    """

    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnumType, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value
        elif isinstance(value, self._enumtype):
            return value.value
        else:
            raise ValueError("Invalid value for enum {}".format(self._enumtype))

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=True)
    role = Column(IntEnumType(PersonRole), nullable=False, default=PersonRole.other)
    # TODO: add contact information and address

    def __repr__(self):
        return "<Person(name='{}', surname='{}', birthdate='{}', role='{}')>".format(
            self.name, self.surname, self.birthdate, self.role
        )

    def __str__(self):
        return "{} {}".format(self.name, self.surname)

    def __init__(
        self,
        name: str,
        surname: str,
        birthdate: Date = None,
        role: PersonRole = PersonRole.other,
    ):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.role = role

    def is_lawyer(self):
        return (
            self.role == PersonRole.our_lawyer or self.role == PersonRole.their_lawyer
        )

    def is_judge(self):
        return self.role == PersonRole.judge

    def is_client(self):
        return (
            self.role == PersonRole.our_client or self.role == PersonRole.their_client
        )

    def is_witness(self):
        return self.role == PersonRole.witness

    def is_expert(self):
        return self.role == PersonRole.expert

    def is_other(self):
        return self.role == PersonRole.other
