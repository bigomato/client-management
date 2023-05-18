
CREATE TABLE address (
	id INTEGER NOT NULL, 
	country VARCHAR(50) NOT NULL, 
	city VARCHAR(50) NOT NULL, 
	zip_code VARCHAR(50) NOT NULL, 
	street VARCHAR(50), 
	house_number VARCHAR(50), 
	PRIMARY KEY (id)
)




CREATE TABLE "case" (
	id INTEGER NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	description VARCHAR NOT NULL, 
	PRIMARY KEY (id)
)




CREATE TABLE document (
	id INTEGER NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	description VARCHAR, 
	date DATE NOT NULL, 
	case_id INTEGER NOT NULL, 
	path VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(case_id) REFERENCES "case" (id)
)




CREATE TABLE person (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	surname VARCHAR(50) NOT NULL, 
	birthdate DATE, 
	adress_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(adress_id) REFERENCES address (id)
)




CREATE TABLE trial (
	id INTEGER NOT NULL, 
	case_id INTEGER NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	description VARCHAR NOT NULL, 
	date DATE NOT NULL, 
	address_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(case_id) REFERENCES "case" (id), 
	FOREIGN KEY(address_id) REFERENCES address (id)
)




CREATE TABLE contact_info (
	id INTEGER NOT NULL, 
	phone_number VARCHAR(50) NOT NULL, 
	email VARCHAR(50) NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES person (id)
)




CREATE TABLE involved (
	id INTEGER NOT NULL, 
	person_id INTEGER, 
	case_id INTEGER NOT NULL, 
	role VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES person (id), 
	FOREIGN KEY(case_id) REFERENCES "case" (id)
)




CREATE TABLE judgement (
	id INTEGER NOT NULL, 
	date DATE NOT NULL, 
	description VARCHAR NOT NULL, 
	document_id INTEGER, 
	trial_id INTEGER NOT NULL, 
	decision VARCHAR(50), 
	PRIMARY KEY (id), 
	FOREIGN KEY(document_id) REFERENCES document (id), 
	FOREIGN KEY(trial_id) REFERENCES trial (id)
)




CREATE TABLE attends (
	trial_id INTEGER, 
	person_id INTEGER, 
	FOREIGN KEY(trial_id) REFERENCES trial (id), 
	FOREIGN KEY(person_id) REFERENCES involved (id)
)




CREATE TABLE representing (
	client_id INTEGER, 
	lawyer_id INTEGER, 
	FOREIGN KEY(client_id) REFERENCES involved (id), 
	FOREIGN KEY(lawyer_id) REFERENCES involved (id)
)



