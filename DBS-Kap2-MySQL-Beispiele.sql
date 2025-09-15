# Vorlesung Datenbanksysteme, SS 2025
# Beispiel "Projektverwaltung" für MySQL
#
# Karlsruher Institut für Technologie
# Institut AIFB

CREATE DATABASE Projektverwaltung;
USE Projektverwaltung;

CREATE TABLE angestellte (
  ANGNR INTEGER PRIMARY KEY,
  NAME VARCHAR(30),
  WOHNORT VARCHAR(30),
  ABTNR INTEGER);

CREATE TABLE projekt (
  PNAME VARCHAR(15),
  PNR INTEGER PRIMARY KEY,
  PFILIALE VARCHAR(30),
  PLEITER INTEGER REFERENCES angestellte(ANGNR));

CREATE TABLE angpro (
  PNR INTEGER REFERENCES projekt(PNR),
  ANGNR INTEGER REFERENCES angestellte(ANGNR),
  PROZARBZEIT REAL,
  PRIMARY KEY (PNR, ANGNR));

INSERT INTO angestellte VALUES
  (3115, 'Meyer', 'Karlsruhe', 35),
  (3207, 'Müller', 'Mannheim', 30),
  (2814, 'Klein', 'Mannheim', 32),
  (3190, 'Maus', 'Karlsruhe', 30),
  (2314, 'Groß', 'Karlsruhe', 35),
  (1324, 'Schmitt', 'Heidelberg', 35),
  (1435, 'Mayerlein', 'Bruchsal', 32),
  (2412, 'Müller', 'Karlsruhe', 32),
  (2244, 'Schulz', 'Bruchsal', 31),
  (1237, 'Krämer', 'Ludwigshafen', 31),
  (3425, 'Meier', 'Pforzheim', 30),
  (2454, 'Schuster', 'Worms', 31);

INSERT INTO projekt VALUES
  ('p-1', 761235, 'Karlsruhe', 3115),
  ('p-2', 770008, 'Karlsruhe', 3115),
  ('p-3', 770114, 'Heidelberg', 1324),
  ('p-4', 770231, 'Mannheim', 2814);

INSERT INTO angpro VALUES
  (761235, 3207, 100),
  (761235, 3115, 50),
  (761235, 3190, 50),
  (761235, 1435, 40),
  (761235, 3425, 50),
  (770008, 2244, 20),
  (770008, 1237, 40),
  (770008, 2814, 70),
  (770008, 2454, 40),
  (770114, 2814, 30),
  (770114, 1435, 60),
  (770114, 1237, 60),
  (770114, 2454, 60),
  (770114, 3425, 50),
  (770114, 2412, 100),
  (770231, 3190, 50),
  (770231, 2314, 100),
  (770231, 2244, 80),
  (770231, 3115, 50),
  (770231, 1324, 100);

# Abfrage 1

SELECT NAME, ABTNR FROM angestellte WHERE WOHNORT='Karlsruhe';

# Abfrage 2

SELECT NAME, ABTNR FROM angestellte WHERE WOHNORT='Karlsruhe' OR ABTNR=30;

# Abfrage 3

SELECT ANGNR, NAME FROM angestellte WHERE ANGNR BETWEEN 1435 AND 2314;

# Abfrage 4

SELECT ANGNR FROM angestellte WHERE ABTNR IN (30, 35) AND WOHNORT IN ('Karlsruhe', 'Mannheim');

# Abfrage 5

SELECT PNR, PFILIALE FROM projekt WHERE PFILIALE LIKE '%ei%';

# Abfrage 6

SELECT ANGNR, NAME FROM angestellte WHERE NAME LIKE 'Me_er';

# Abfrage 7

SELECT NAME FROM angestellte WHERE NAME LIKE 'M__er%';

# Abfrage 8

SELECT ANGNR, NAME FROM angestellte WHERE ABTNR=30 ORDER BY NAME ASC, ANGNR ASC;

# Abfrage 9

SELECT PNAME FROM projekt;

# Abfrage 10

SELECT * FROM projekt WHERE PFILIALE='Karlsruhe';

# Abfrage 11

SELECT * FROM angestellte;

# Abfrage 12

SELECT DISTINCT PFILIALE FROM projekt;

# Abfrage 13

SELECT PNR, ANGNR, PROZARBZEIT*0.01 FROM angpro;

# Abfrage 14

SELECT PNR, ANGNR, 'Anteil=', PROZARBZEIT/100 FROM angpro;

# Abfrage 15A

SELECT COUNT(*) FROM angestellte;

# Abfrage 15B

SELECT COUNT(DISTINCT NAME) FROM angestellte;

# Abfrage 16

SELECT MAX(PROZARBZEIT) AS 'PROZ-ARBZEIT-MAX' FROM angpro;

# Abfrage 17

SELECT MAX(PROZARBZEIT) AS 'PROZ-ARBZEIT-MAX-761235' FROM angpro WHERE PNR=761235;

# Abfrage 18

SELECT SUM(PROZARBZEIT) AS 'PROZ-ARBZEIT-SUM-770008' FROM angpro WHERE PNR=770008;

# Abfrage 19

SELECT PNR, SUM(PROZARBZEIT) AS 'PROZ-ARBZEIT-PROJEKT' FROM angpro GROUP BY PNR;

# Abfrage 20

SELECT PNR FROM angpro GROUP BY PNR HAVING MAX(PROZARBZEIT)=100;

# Abfrage 21

SELECT PNR FROM angpro GROUP BY PNR HAVING COUNT(DISTINCT ANGNR)>=5;

# Abfrage 22

SELECT PNR, a.ANGNR, NAME, WOHNORT, ABTNR, PROZARBZEIT
  FROM angestellte a, angpro ap
  WHERE a.ANGNR=ap.ANGNR;

# Abfrage 23

SELECT PNR, NAME
  FROM angestellte a, angpro ap
  WHERE a.ANGNR=ap.ANGNR AND PROZARBZEIT=50;

# Abfrage 24

SELECT PNR, NAME
  FROM angestellte, projekt
  WHERE ANGNR <> PLEITER;

# Abfrage 25

SELECT NAME, PFILIALE
  FROM angestellte a, angpro ap, projekt p
  WHERE a.ANGNR=ap.ANGNR AND ap.PNR=p.PNR;

# Abfrage 26

SELECT a.NAME 'A-NAME', b.NAME 'B-NAME'
  FROM angestellte a, angestellte b
  WHERE a.WOHNORT=b.WOHNORT AND a.ANGNR<b.ANGNR;

# Abfrage 27

SELECT PNR, a.ANGNR, NAME, WOHNORT, ABTNR, PROZARBZEIT
  FROM angestellte a NATURAL JOIN angpro;

# Abfrage 28

SELECT PNR, NAME
  FROM angestellte NATURAL JOIN angpro
  WHERE PROZARBZEIT=50;

SELECT PNR, NAME
  FROM angestellte INNER JOIN angpro 
  ON (angestellte.ANGNR=angpro.ANGNR AND PROZARBZEIT=50);

# Abfrage 29

SELECT PNR, NAME
  FROM angestellte JOIN projekt
  ON (ANGNR <> PLEITER);

# Abfrage 30

SELECT NAME, PFILIALE
  FROM angestellte NATURAL JOIN angpro NATURAL JOIN projekt;

# Abfrage 31

SELECT a.NAME 'A-NAME', b.NAME 'B-NAME'
  FROM (angestellte a) JOIN (angestellte b) USING (WOHNORT)
  WHERE a.ANGNR < b.ANGNR;

# Abfrage 32/33

SELECT ANGNR FROM angpro WHERE PROZARBZEIT=100;

SELECT NAME FROM angestellte WHERE ANGNR IN (3207, 2412, 2314, 1324);

SELECT NAME 
  FROM angestellte, angpro
  WHERE PROZARBZEIT=100 AND angpro.ANGNR=angestellte.ANGNR;

SELECT NAME
  FROM angestellte
  WHERE ANGNR IN
    (SELECT ANGNR 
     FROM angpro 
     WHERE PROZARBZEIT=100);

# Abfrage 34

SELECT ANGNR, NAME FROM angestellte WHERE ANGNR IN
  (SELECT ANGNR FROM angpro WHERE PNR IN
    (SELECT PNR FROM projekt WHERE PFILIALE='Karlsruhe')); 

# Abfrage 35

SELECT DISTINCT a.ANGNR, a.NAME 
  FROM angestellte a, angpro ap, projekt p
  WHERE a.ANGNR=ap.ANGNR AND ap.PNR=p.PNR AND p.PFILIALE='Karlsruhe';

# Abfrage 36

SELECT DISTINCT PFILIALE
  FROM projekt b
  WHERE 1 <
    (SELECT COUNT(*) FROM projekt a WHERE a.PFILIALE = b.PFILIALE);

# Abfrage 37

SELECT NAME
  FROM angestellte
  WHERE NOT EXISTS 
    (SELECT PLEITER FROM projekt WHERE PLEITER=ANGNR);

# Abfrage 38

SELECT ANGNR
  FROM angestellte
  WHERE WOHNORT='Karlsruhe' 
UNION 
SELECT PLeiter
  FROM projekt 
  WHERE PFILIALE='Karlsruhe';

# Abfrage 39

# SELECT ANGNR 
#   FROM angestellte
#   WHERE WOHNORT='Karlsruhe'
# INTERSECT
# SELECT ANGNR
#   FROM angpro
#   GROUP BY ANGNR HAVING COUNT(*) > 1;

# Abfrage 40

# SELECT ANGNR
#   FROM angestellte
#   WHERE NAME like 'M%'
# EXCEPT
# SELECT PLEITER 
#   FROM projekt;

