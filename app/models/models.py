from sqlalchemy import Column, Date, Integer, String, Table, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import enum
from app import db


class InvolvementRole(enum.IntEnum):
    victim_lawyer = 1
    suspect_lawyer = 2
    victim = 3
    suspect = 4
    witness = 5
    judge = 6
    other = 7

    def __str__(self) -> str:
        return self.name

    def display(self) -> str:
        match self:
            case InvolvementRole.victim_lawyer:
                return "Anwalt des Klägers"
            case InvolvementRole.suspect_lawyer:
                return "Anwalt des Angeklagten"
            case InvolvementRole.victim:
                return "Kläger"
            case InvolvementRole.suspect:
                return "Angeklagter"
            case InvolvementRole.witness:
                return "Zeuge"
            case InvolvementRole.judge:
                return "Richter"
            case InvolvementRole.other:
                return "Sonstige"
            case _:
                return "Unbekannt"


InvolvementRoleType: Enum = Enum(
    InvolvementRole,
    name="involvement_role_type",
    create_constraint=True,
    metadata=db.metadata,
    validate_strings=True,
)


class CaseStatus(enum.IntEnum):
    won = 1
    lost = 2
    ongoing = 3

    def __str__(self) -> str:
        return self.name


CaseStatusType: Enum = Enum(
    CaseStatus,
    name="case_status_type",
    create_constraint=True,
    metadata=db.metadata,
    validate_strings=True,
)


class JudgemenType(enum.IntEnum):
    arrangement = 1  # Vergleich
    not_guilty = 2  # Freispruch
    condemnation = 3  # Verurteilung
    dismissal = 4  # Klageabweisung
    suspension = 5  # Einstellung
    revision = 6  # Revision
    delay = 7  # Verzögerung
    other = 8  # Andere

    def __str__(self) -> str:
        return self.name

    def display(self) -> str:
        match self:
            case JudgemenType.arrangement:
                return "Vergleich"
            case JudgemenType.not_guilty:
                return "Freispruch"
            case JudgemenType.condemnation:
                return "Verurteilung"
            case JudgemenType.dismissal:
                return "Klageabweisung"
            case JudgemenType.suspension:
                return "Einstellung"
            case JudgemenType.revision:
                return "Revision"
            case JudgemenType.delay:
                return "Verzögerung"
            case JudgemenType.other:
                return "Andere"
            case _:
                return "Unbekannt"


JudgementTypeType: Enum = Enum(
    JudgemenType,
    name="judgement_type_type",
    create_constraint=True,
    metadata=db.metadata,
    validate_strings=True,
)

# Keine Klasse weil es eine einfache m zu n Besziehung ist
attends = Table(
    "attends",
    db.metadata,
    Column("trial_id", Integer, ForeignKey("trial.id")),
    Column("person_id", Integer, ForeignKey("involved.id")),
)


representing = Table(
    "representing",
    db.metadata,
    Column("client_id", Integer, ForeignKey("involved.id")),
    Column("lawyer_id", Integer, ForeignKey("involved.id")),
)


class Person(db.Model):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=True)
    adress_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    our_lawyer = Column(Boolean, nullable=False, default=False)
    our_client = Column(Boolean, nullable=False, default=False)
    contactinfos = relationship("ContactInfo", backref="person")
    involvements = relationship("Involved", backref="person")

    def __repr__(self):
        return "<Person(name='{}', surname='{}', birthdate='{}', role='{}')>".format(
            self.name, self.surname, self.birthdate, self.role
        )

    def __str__(self):
        s = "{} {}".format(self.name, self.surname)
        for ci in self.contactinfos:
            s += "\n\t{}".format(str(ci))
        return s


class Address(db.Model):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    zip_code = Column(String(50), nullable=False)
    street = Column(String(50), nullable=True)
    house_number = Column(String(50), nullable=True)
    persons = relationship("Person", backref="address")
    trials = relationship("Trial", backref="address")

    def __repr__(self):
        return "<Address(country='{}', city='{}', zip_code='{}', street='{}', house_number='{}')>".format(
            self.country, self.city, self.zip_code, self.street, self.house_number
        )

    def __str__(self):
        return "{}, {} {}".format(self.country, self.city, self.zip_code)


class ContactInfo(db.Model):
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


class Case(db.Model):
    __tablename__ = "case"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String, nullable=False)
    involved = relationship("Involved", backref="case")
    documents = relationship("Document", backref="case")
    trials = relationship("Trial", backref="case")
    case_status = Column(CaseStatusType, nullable=False, default=CaseStatus.ongoing)

    def __repr__(self):
        return "<Case(name='{}', description='{}')>".format(self.name, self.description)

    def __str__(self):
        s = f"Case {self.name}: {self.description}:\n"
        for involement in self.involved:
            s += f" * {involement.person.name} {involement.person.surname}: {involement.role}\n"
            if (
                involement.role == InvolvementRole.victim_lawyer
                or involement.role == InvolvementRole.suspect_lawyer
            ) and involement.clients:
                s += f"   Clients:\n"
                for client in involement.clients:
                    s += f"    * {client.person.name} {client.person.surname} ({InvolvementRole(client.role)})\n"
        s += "Documents:\n"
        for document in self.documents:
            s += f" * {document.name}\n"
        s += "Trials:\n"
        for trial in self.trials:
            s += f" * {trial.date}: {trial.description}\n"
            if trial.address:
                s += f"   Address: {trial.address.street} {trial.address.house_number} {trial.address.zip_code} {trial.address.city} {trial.address.country}\n"
            if trial.judgement:
                s += f"   Judgement: {trial.judgement}\n"
            if trial.attendees:
                s += f"   Attendees:\n"
                for involvement in trial.attendees:
                    s += f"    * {involvement.person.name} {involvement.person.surname} ({InvolvementRole(involvement.role)})\n"
        return s


class Involved(db.Model):
    __tablename__ = "involved"
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey("person.id"))
    case_id = Column(Integer, ForeignKey("case.id"), nullable=False)
    role = Column(InvolvementRoleType, nullable=False)
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

    def attend(self, trial):
        self.attendees.append(trial)


class Trial(db.Model):
    __tablename__ = "trial"
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("case.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)

    attendees = relationship("Involved", secondary=attends, back_populates="attendees")
    judgement = relationship("Judgement", uselist=False, backref="trial")

    def __repr__(self):
        return "<Trial(name='{}', description='{}')>".format(
            self.name, self.description
        )

    def __str__(self):
        return self.name


class Document(db.Model):
    __tablename__ = "document"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    case_id = Column(Integer, ForeignKey("case.id"), nullable=False)
    path = Column(String, nullable=False)  # Dateipfad

    def __repr__(self):
        return "<Document(name='{}', description='{}')>".format(
            self.name, self.description
        )

    def __str__(self):
        return self.name


class Judgement(db.Model):
    __tablename__ = "judgement"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    document_id = Column(Integer, ForeignKey("document.id"), nullable=True)
    trial_id = Column(Integer, ForeignKey("trial.id"), nullable=False)
    judgement = Column(JudgementTypeType, nullable=True)
    # FIXME: add a proper connection between trial and judgement so you can use judgement.trial
    document = relationship("Document", uselist=False, backref="judgement")

    def __repr__(self):
        return "<Judgement(type='{}', date='{}')>".format(self.type, self.date)

    def __str__(self):
        return self.description + f" ({self.judgement})"
