-- Sequences
CREATE SEQUENCE public.specialisation_id_seq;
CREATE SEQUENCE public.type_utilisateur_id_seq;
CREATE SEQUENCE public.type_id_seq;
CREATE SEQUENCE public.ecole_id_seq;
CREATE SEQUENCE public.ville_id_seq;
CREATE SEQUENCE public.adresse_id_seq;

-- Tables
CREATE TABLE public.specialisation (
    id_specialisation INTEGER NOT NULL DEFAULT nextval('public.specialisation_id_seq'),
    nom_specialisation VARCHAR(128) NOT NULL UNIQUE,
    CONSTRAINT specialisation_pk PRIMARY KEY (id_specialisation)
);

CREATE TABLE public.type_utilisateur (
    id_type_utilisateur INTEGER NOT NULL DEFAULT nextval('public.type_utilisateur_id_seq'),
    nom_type_utilisateur VARCHAR(64) NOT NULL UNIQUE,
    CONSTRAINT type_utilisateur_pk PRIMARY KEY (id_type_utilisateur)
);

CREATE TABLE public.type (
    id_type INTEGER NOT NULL DEFAULT nextval('public.type_id_seq'),
    nom_type VARCHAR(128) NOT NULL UNIQUE,
    CONSTRAINT type_pk PRIMARY KEY (id_type)
);

CREATE TABLE public.mail (
    adresse_mail VARCHAR(128) NOT NULL,
    id_type INTEGER NOT NULL,
    CONSTRAINT mail_pk PRIMARY KEY (adresse_mail),
    CONSTRAINT type_mail_fk FOREIGN KEY (id_type) REFERENCES public.type (id_type)
);

CREATE TABLE public.pays (
    acronyme_pays VARCHAR(128) NOT NULL,
    nom_pays VARCHAR(128) NOT NULL,
    CONSTRAINT pays_pk PRIMARY KEY (acronyme_pays)
);

CREATE TABLE public.ecole (
    id_ecole INTEGER NOT NULL DEFAULT nextval('public.ecole_id_seq'),
    nom_ecole VARCHAR(128) NOT NULL,
    acronyme_pays VARCHAR(128),
    CONSTRAINT ecole_pk PRIMARY KEY (id_ecole),
    CONSTRAINT pays_ecole_fk FOREIGN KEY (acronyme_pays) REFERENCES public.pays (acronyme_pays)
);

CREATE TABLE public.diplome (
    id_diplome INTEGER NOT NULL,
    ref_diploma VARCHAR(128) NOT NULL,
    id_specialisation INTEGER,
    id_ecole INTEGER NOT NULL,
    nom_diplome VARCHAR(256) NOT NULL,
    parcours VARCHAR(128) NOT NULL,
    CONSTRAINT diplome_pk PRIMARY KEY (id_diplome),
    CONSTRAINT specialisation_diplome_fk FOREIGN KEY (id_specialisation) REFERENCES public.specialisation (id_specialisation),
    CONSTRAINT ecole_diplome_fk FOREIGN KEY (id_ecole) REFERENCES public.ecole (id_ecole)
);

CREATE TABLE public.ville (
    id_ville INTEGER NOT NULL DEFAULT nextval('public.ville_id_seq'),
    nom_ville VARCHAR(128) NOT NULL,
    acronyme_pays VARCHAR(128) NOT NULL,
    CONSTRAINT ville_pk PRIMARY KEY (id_ville),
    CONSTRAINT pays_ville_fk FOREIGN KEY (acronyme_pays) REFERENCES public.pays (acronyme_pays)
);

CREATE TABLE public.personne (
    id_personne INTEGER NOT NULL,
    prenom VARCHAR NOT NULL,
    nom VARCHAR NOT NULL,
    nom_usage VARCHAR(128),
    date_naissance DATE,
    ref_school VARCHAR(128),
    civilite VARCHAR(64),
    id_ville INTEGER,
    adresse_mail VARCHAR(128),
    genre VARCHAR(128) NOT NULL,
    id_type_utilisateur INTEGER NOT NULL,
    acronyme_pays VARCHAR(128),
    CONSTRAINT personne_pk PRIMARY KEY (id_personne),
    CONSTRAINT ville_personne_fk FOREIGN KEY (id_ville_naissance) REFERENCES public.ville (id_ville),
    CONSTRAINT mail_personne_fk FOREIGN KEY (adresse_mail) REFERENCES public.mail (adresse_mail),
    CONSTRAINT type_utilisateur_personne_fk FOREIGN KEY (id_type_utilisateur) REFERENCES public.type_utilisateur (id_type_utilisateur),
    CONSTRAINT pays_personne_fk FOREIGN KEY (acronyme_pays) REFERENCES public.pays (acronyme_pays)
);

CREATE TABLE public.adresse (
    adresse_id INTEGER NOT NULL DEFAULT nextval('public.adresse_id_seq'),
    adresse_1 VARCHAR(128) NOT NULL,
    adresse_2 VARCHAR(128),
    adresse_3 VARCHAR(128),
    adresse_4 VARCHAR(128),
    id_ville INTEGER NOT NULL,
    id_personne INTEGER NOT NULL,
    npai BOOLEAN DEFAULT false NOT NULL,
    code_postal INTEGER NOT NULL,
    type_adresse VARCHAR(128) NOT NULL,
    id_type INTEGER NOT NULL,
    CONSTRAINT adresse_pk PRIMARY KEY (adresse_id),
    CONSTRAINT ville_adresse_fk FOREIGN KEY (id_ville) REFERENCES public.ville (id_ville),
    CONSTRAINT type_adresse_fk FOREIGN KEY (id_type) REFERENCES public.type (id_type),
    CONSTRAINT personne_adresse_fk FOREIGN KEY (id_personne) REFERENCES public.personne (id_personne)
);

CREATE TABLE public.a_un_diplome (
    id_diplome INTEGER NOT NULL,
    id_personne INTEGER NOT NULL,
    date_diplomation DATE NOT NULL,
    date_integration DATE NOT NULL,
    est_diplome BOOLEAN NOT NULL,
    CONSTRAINT a_un_diplome_pk PRIMARY KEY (id_diplome, id_personne),
    CONSTRAINT diplome_a_un_diplome_fk FOREIGN KEY (id_diplome) REFERENCES public.diplome (id_diplome),
    CONSTRAINT personne_a_un_diplome_fk FOREIGN KEY (id_personne) REFERENCES public.personne (id_personne)
);

-- Linking sequences to columns
ALTER SEQUENCE public.specialisation_id_seq OWNED BY public.specialisation.id_specialisation;
ALTER SEQUENCE public.type_utilisateur_id_seq OWNED BY public.type_utilisateur.id_type_utilisateur;
ALTER SEQUENCE public.type_id_seq OWNED BY public.type.id_type;
ALTER SEQUENCE public.ecole_id_seq OWNED BY public.ecole.id_ecole;
ALTER SEQUENCE public.ville_id_seq OWNED BY public.ville.id_ville;
ALTER SEQUENCE public.adresse_id_seq OWNED BY public.adresse.adresse_id;

-- Populating country table
INSERT INTO pays (acronyme_pays, nom_pays) VALUES 
('AF', 'Afghanistan'),
('AL', 'Albanie'),
('DZ', 'Algérie'),
('AD', 'Andorre'),
('AO', 'Angola'),
('AR', 'Argentine'),
('AM', 'Arménie'),
('AU', 'Australie'),
('AT', 'Autriche'),
('AZ', 'Azerbaïdjan'),
('BS', 'Bahamas'),
('BH', 'Bahreïn'),
('BD', 'Bangladesh'),
('BB', 'Barbade'),
('BY', 'Bélarus'),
('BE', 'Belgique'),
('BZ', 'Belize'),
('BJ', 'Bénin'),
('BT', 'Bhoutan'),
('BO', 'Bolivie'),
('BA', 'Bosnie-Herzégovine'),
('BW', 'Botswana'),
('BR', 'Brésil'),
('BN', 'Brunei'),
('BG', 'Bulgarie'),
('BF', 'Burkina Faso'),
('BI', 'Burundi'),
('CV', 'Cap-Vert'),
('KH', 'Cambodge'),
('CM', 'Cameroun'),
('CA', 'Canada'),
('KY', 'Cayman Islands'),
('CF', 'République Centrafricaine'),
('TD', 'Tchad'),
('CL', 'Chili'),
('CN', 'Chine'),
('CO', 'Colombie'),
('KM', 'Comores'),
('CG', 'Congo'),
('CD', 'République Démocratique du Congo'),
('CR', 'Costa Rica'),
('CI', 'Côte d''Ivoire'),
('HR', 'Croatie'),
('CU', 'Cuba'),
('CY', 'Chypre'),
('CZ', 'République Tchèque'),
('DK', 'Danemark'),
('DJ', 'Djibouti'),
('DM', 'Dominique'),
('DO', 'République Dominicaine'),
('EC', 'Équateur'),
('EG', 'Égypte'),
('SV', 'Salvador'),
('GQ', 'Guinée équatoriale'),
('ER', 'Érythrée'),
('EE', 'Estonie'),
('SZ', 'Eswatini'),
('ET', 'Éthiopie'),
('FJ', 'Fidji'),
('FI', 'Finlande'),
('FR', 'France'),
('GA', 'Gabon'),
('GM', 'Gambie'),
('GE', 'Géorgie'),
('DE', 'Allemagne'),
('GH', 'Ghana'),
('GR', 'Grèce'),
('GD', 'Grenade'),
('GT', 'Guatemala'),
('GN', 'Guinée'),
('GW', 'Guinée-Bissao'),
('GY', 'Guyana'),
('HT', 'Haïti'),
('HN', 'Honduras'),
('HK', 'Hong Kong'),
('HU', 'Hongrie'),
('IS', 'Islande'),
('IN', 'Inde'),
('ID', 'Indonésie'),
('IR', 'Iran'),
('IQ', 'Irak'),
('IE', 'Irlande'),
('IL', 'Israël'),
('IT', 'Italie'),
('JM', 'Jamaïque'),
('JP', 'Japon'),
('JO', 'Jordanie'),
('KZ', 'Kazakhstan'),
('KE', 'Kenya'),
('KI', 'Kiribati'),
('KP', 'Corée du Nord'),
('KR', 'Corée du Sud'),
('KW', 'Koweït'),
('KG', 'Kirghizistan'),
('LA', 'Laos'),
('LV', 'Lettonie'),
('LB', 'Liban'),
('LS', 'Lesotho'),
('LR', 'Libéria'),
('LY', 'Libye'),
('LI', 'Liechtenstein'),
('LT', 'Lituanie'),
('LU', 'Luxembourg'),
('MO', 'Macao'),
('MK', 'Macédoine'),
('MG', 'Madagascar'),
('MW', 'Malawi'),
('MY', 'Malaisie'),
('MV', 'Maldives'),
('ML', 'Mali'),
('MT', 'Malte'),
('MH', 'Îles Marshall'),
('MQ', 'Martinique'),
('MR', 'Mauritanie'),
('MU', 'Maurice'),
('MX', 'Mexique'),
('FM', 'Micronésie'),
('MD', 'Moldavie'),
('MC', 'Monaco'),
('MN', 'Mongolie'),
('ME', 'Monténégro'),
('MA', 'Maroc'),
('MZ', 'Mozambique'),
('MM', 'Myanmar'),
('NA', 'Namibie'),
('NR', 'Nauru'),
('NP', 'Népal'),
('NL', 'Pays-Bas'),
('NC', 'Nouvelle-Calédonie'),
('NZ', 'Nouvelle-Zélande'),
('NI', 'Nicaragua'),
('NE', 'Niger'),
('NG', 'Nigeria'),
('NO', 'Norvège'),
('OM', 'Oman'),
('PK', 'Pakistan'),
('PW', 'Palaos'),
('PA', 'Panama'),
('PG', 'Papouasie-Nouvelle-Guinée'),
('PY', 'Paraguay'),
('PE', 'Pérou'),
('PH', 'Philippines'),
('PL', 'Pologne'),
('PT', 'Portugal'),
('QA', 'Qatar'),
('RO', 'Roumanie'),
('RU', 'Russie'),
('RW', 'Rwanda'),
('KN', 'Saint-Christophe-et-Niévès'),
('LC', 'Sainte-Lucie'),
('VC', 'Saint-Vincent-et-les Grenadines'),
('WS', 'Samoa'),
('SM', 'Saint-Marin'),
('ST', 'São Tomé-et-Principe'),
('SA', 'Arabie Saoudite'),
('SN', 'Sénégal'),
('RS', 'Serbie'),
('SC', 'Seychelles'),
('SL', 'Sierra Leone'),
('SG', 'Singapour'),
('SK', 'Slovaquie'),
('SI', 'Slovénie'),
('SB', 'Îles Salomon'),
('SO', 'Somalie'),
('ZA', 'Afrique du Sud'),
('SS', 'Soudan du Sud'),
('ES', 'Espagne'),
('LK', 'Sri Lanka'),
('SD', 'Soudan'),
('SR', 'Suriname'),
('SE', 'Suède'),
('CH', 'Suisse'),
('SY', 'Syrie'),
('TW', 'Taïwan'),
('TJ', 'Tadjikistan'),
('TZ', 'Tanzanie'),
('TH', 'Thaïlande'),
('TG', 'Togo'),
('TO', 'Tonga'),
('TT', 'Trinité-et-Tobago'),
('TN', 'Tunisie'),
('TR', 'Turquie'),
('TM', 'Turkménistan'),
('TV', 'Tuvalu'),
('UG', 'Ouganda'),
('UA', 'Ukraine'),
('AE', 'Émirats Arabes Unis'),
('GB', 'Royaume-Uni'),
('US', 'États-Unis'),
('UY', 'Uruguay'),
('UZ', 'Ouzbékistan'),
('VU', 'Vanuatu'),
('VE', 'Venezuela'),
('VN', 'Vietnam'),
('YE', 'Yémen'),
('ZM', 'Zambie'),
('ZW', 'Zimbabwe');
