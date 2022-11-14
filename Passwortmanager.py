# Passwortmanager für WPF Python Montag Lorenz Hankel FA-B-01


import base64
import os
import sys
from copy import deepcopy
from pathlib import Path

# Für Windows und Python 3.x wurde pycryptodome anstatt pycrypto benutzt (pip install pycryptodome)
# from Crypto.Cipher import DES # War mir jetzt zu viel Arbeit. Ein andern Mal. TODO: Ordentliche Verschlüsselung statt Base64
# Passwort Klasse definieren


class Passwort():
    def __init__(self, index: int, name: str, passwort: str, url: str, hinweis: str):
        self.index = index
        self.name = name
        self.passwort = passwort
        self.url = url
        self.hinweis = hinweis

    def set_index(self, index: int):
        self.index = index

    def set_name(self, name: str):
        self.name = name

    def set_passwort(self, passwort: str):
        self.passwort = passwort

    def set_url(self, url: str):
        self.url = url

    def set_hinweis(self, hinweis: str):
        self.hinweis = hinweis

    def get_index(self):
        return self.index

    def get_name(self):
        return self.name

    def get_passwort(self):
        return self.passwort

    def get_url(self):
        return self.url

    def get_hinweis(self):
        return self.hinweis

    def __str__(self):
        sep = ":"
        # return (f"{str(self.index) + sep + str(self.name) + sep + str(self.passwort) + sep + str(self.url) + sep + str(self.hinweis)}")
        return (str(self.index) + ":" + str(self.name) + ":" + str(self.passwort) + ":" + str(self.url) + ":" + str(self.hinweis))


def master_Passwort_anlegen():
    # Neues Passwort vom Nutzer abfragen
    pw = bytes(input(
        "Bitte geben Sie das neue Master-Passwort an. Vergessen Sie es nicht!\n"), "utf-8")
    __pw_enc = base64.b64encode(pw)
    # nun das verschlüsselte Passwort in Datei schreiben.
    datei = open("./login.txt", "w")
    datei.write((__pw_enc).decode("utf-8"))
    datei.close()


def ersteinrichtung(pw_liste, einstellungen):
    print("\nErsteinrichtung starten... \n")
    # Dateiname abfragen
    datenbank_datei_name: str = input(
        "Bitte geben Sie den neuen Namen der Passwort-Datenbank an.\n")
    print(str("Neue Datenbank Dateiname: " + datenbank_datei_name))
    Einstellungen_Datei_Speichern(einstellungen)
    print(einstellungen)
    # Neues Master Passwort anlegen
    master_Passwort_anlegen()
    # Passwort Liste mit Test-Daten füllen
    Teste_Liste_erstellen()
    # Passwort Datei schreiben mit den angelegten Test-Daten
    Passwort_Datei_Schreiben(pw_liste, datenbank_datei_name)
    Datei_Lesen(pw_liste)
    print("\nErsteinrichtung beendet. \n")


def master_Passwort_pruefen():
    datei = open("./login.txt", "r")
    __login = bytes(datei.read(), "utf-8")
    pw = bytes(input("\nBitte geben Sie Ihr Master Passwort ein.\n"), "utf-8")
    if base64.b64decode(__login) != pw:
        print("Passwort ist falsch")
        exit()
    else:
        print("Zugangsdaten sind korrekt.")
        return pw


def einrichtung_pruefen():
    __master_datei = Path("./login.txt")
    __passwort_datei = Path("./passwords.txt")
    if __master_datei.is_file() == False and __passwort_datei.is_file() == False:
        ersteinrichtung(pw_liste)
    elif __master_datei.is_file() and __passwort_datei.is_file() == False:
        print("\nMaster Login Datei fehlt. Setze Installation zurück.\n")
        os.remove("./login.txt")
        ersteinrichtung(pw_liste)
    else:
        print("\nSystem in Ordnung.\n")
        pw = master_Passwort_pruefen()
        Datei_Lesen(pw_liste)
        return pw


def datensatz_loeschen(pw_liste, index_loeschen: int, datenbank_datei):
    print("\nDS mit folgenden Index werden gesucht: " + str(index_loeschen) + "\n")
    vgl_liste = deepcopy(pw_liste)  # zum Vergleichen später
    listen_index: int = -1
    count: int = 0
    for i in pw_liste:
        # print(str("\nAktueller Index zum Vergleich: " + Passwort.get_index(i)) + "\n")
        if int(Passwort.get_index(i)) == int(index_loeschen):
            print("\nFolgender DS wird gelöscht: " + str(index_loeschen) + "\n")
            listen_index = count
            break
        else:
            count += 1
    if listen_index != -1:
        del (pw_liste[listen_index])
        Passwort_Datei_Schreiben(pw_liste, datenbank_datei)
        Datei_Lesen(pw_liste)
        print("Es wurden " + str((int(len(vgl_liste)) - int(len(pw_liste)))
                                 ) + " Elemente aus der Datenbank gelöscht.")
    else:
        print("Kein entsprechendes Element in der Datenbank gefunden")


def datensatz_aendern(pw_liste, index_aendern: int, datenbank_datei):
    print("\nDS mit folgenden Index werden gesucht: " + str(index_aendern) + "\n")
    for i in pw_liste:
        if int(Passwort.get_index(i)) == int(index_aendern):
            neu_name = str(
                input("\nGeben Sie den neuen Namen ein, falls Sie ihn ändern wollen.\n"))
            if neu_name != "":
                Passwort.set_name(i, neu_name)
            neu_passwort = str(
                input("\nGeben Sie das neue Passwort ein, falls Sie es ändern wollen.\n"))
            if neu_passwort != "":
                Passwort.set_passwort(i, neu_passwort)
            neu_url = str(
                input("\nGeben Sie neue URL ein, falls Sie sie ändern wollen.\n"))
            if neu_url != "":
                Passwort.set_url(i, neu_url)
            neu_hinweis = str(
                input("\nGeben Sie die neuen Hinweise ein, falls Sie ihn ändern wollen\n"))
            if neu_hinweis != "":
                Passwort.set_hinweis(i, neu_hinweis)
            break
    Passwort_Datei_Schreiben(pw_liste, datenbank_datei)
    Datei_Lesen(pw_liste)

# Funktion um die pw_liste zu sortieren nach den vergebenen Indezes.


def Passwortliste_sortieren(pw_liste):
    pw_liste.sort(key=lambda x: x.index, reverse=False)
    return pw_liste


def Datei_Lesen(pw_liste):
    datei = base64.b64decode(open("./passwords.txt", "r", encoding="utf-8"))
    Lines = datei.readlines()
    pw_attribute = []
    # die alte Liste leeren um Sie auf die Neu-Befüllung vorzubereiten.
    pw_liste.clear()
    for line in Lines:
        # Abfangen von Leerzeilen (Code verhielt sich unberechenbar)
        if len(line.strip()) != 0:
            pw_attribute.clear()
            pw_attribute = line.split(":")
            pw = Passwort(pw_attribute[0], pw_attribute[1],
                          pw_attribute[2], pw_attribute[3], pw_attribute[4])
            pw_liste.append(pw)
    pw_liste = Passwortliste_sortieren(pw_liste)
    datei.close

# Schreiben einer Passwort Datei


def Passwort_Datei_Schreiben(pw_liste, datenbank_datei_name: str):
    pfad: str = str("./" + datenbank_datei_name)
    datei = open(pfad, "w")
    for x in pw_liste:
        schreiben = base64.b64encode(bytes(str(x), "utf-8"))
        datei.write(str(schreiben) + "\n")
    datei.close()

# Soll die settings.cfg Einstellungsdatei speichern / überschreiben


def Einstellungen_Datei_Speichern(einstellungen):
    pfad: str = str("./settings.cfg")  # Erstmal Standard Dateiname.
    datei = open(pfad, "w")
    for key, value in einstellungen.items():
        print(key, value)
        datei.write(key + ":" + value)
    datei.close()


# Testet das Erstellen und füllen der Passwort Liste
def Teste_Liste_erstellen():
    for i in range(1, 3):
        ein_Passwort = Passwort(i, "EinPasswortName" + str(i), "Das Passwort" +
                                str(i), "Die URL" + str(i), "Ein Hinweis" + str(i))
        pw_liste.append(ein_Passwort)


def Ausgabe_Pw_Liste(pw_liste):
    print("-------------------------------------------------------------------------------------")
    print("Index\tName\t\tPasswort\t\tURL\t\tHinweis")
    print("-------------------------------------------------------------------------------------")
    for i in pw_liste:
        index = Passwort.get_index(i)
        name = Passwort.get_name(i)
        passwort = Passwort.get_passwort(i)
        url = Passwort.get_url(i)
        hinweis = Passwort.get_hinweis(i)
        print(str(index) + "\t" + str(name) + "\t\t" +
              str(passwort) + "\t\t" + str(url) + "\t\t" + str(hinweis))


def finde_naechsten_index():
    # liste mit allen Indezes anlegen
    index_list = []
    for i in pw_liste:
        index_list.append(Passwort.get_index(i))
    # Liste sortieren um Maximum zu finden
    index_list.sort()
    if not index_list:
        next_index = 1
    else:
        for z in index_list:
            if (int(z) + 1) not in index_list:
                next_index: int = (int(z)+1)
            else:
                next_index: int = int(index_list[-1]) + 1
    return next_index


def neuen_Datensatz_anlegen(pw_liste, datenbank_datei_name):
    index: int = finde_naechsten_index()
    name: str = str(
        input("Geben Sie Ihren Accountnamen für den neuen Datensatz ein.\n"))
    passwort: str = str(
        input("Geben Sie Ihr Passwort für den neuen Datensatz ein.\n"))
    url: str = str(input("Geben Sie die URL für den neuen Datensatz ein.\n"))
    hinweis: str = str(
        input("(optional) Geben Sie einen Hinweis für den neuen Datensatz ein.\n"))
    if hinweis == "":
        hinweis = "/"
    ein_Passwort = Passwort(index, name, passwort, url, hinweis)
    pw_liste.append(ein_Passwort)
    pw_liste = Passwortliste_sortieren(pw_liste)
    Passwort_Datei_Schreiben(pw_liste, datenbank_datei_name)
    Datei_Lesen(pw_liste)


def auswahl_Menue(pw_liste, datenbank_datei_name):
    print("\n1) Zeige existierende Passwörter")
    print("2) Füge ein neues Passwort hinzu")
    print("3) Lösche ein Passwort")
    print("4) Aktualisiere Passwort")
    print("5) Alles Speichern")
    print("6) Beende\n")
    auswahl: int = 0
    while auswahl < 1 or auswahl > 6:
        auswahl: int = int(input())
        if auswahl < 1 or auswahl > 6 and auswahl not in [1, 2, 3, 4, 5, 6]:
            print("Keine zulässige Eingabe!\nBitte eine Zahl zwischen 1 und 5 eingeben.")
    match auswahl:
        # Liste ausgeben
        case 1:
            Ausgabe_Pw_Liste(pw_liste)
        # Neuen Datensatz anlegen
        case 2:
            neuen_Datensatz_anlegen(pw_liste, datenbank_datei_name)
        # Lösche einen Datensatz
        case 3:
            datensatz_loeschen(pw_liste, int(input(
                "\nBitte geben Sie den Index des zu löschenden Passwortes ein.\n")), datenbank_datei_name)
        # Ändere einen Datensatz
        case 4:
            datensatz_aendern(pw_liste, int(input(
                "\nBitte geben Sie den Index des zu ändernden Passwortes ein.\n")), datenbank_datei_name)
        # DB Datei manuell überschreiben
        case 5:
            Passwort_Datei_Schreiben(pw_liste, datenbank_datei_name)
        # Beenden
        case 6:
            sys.exit()


def startbildschirm():
    settings_datei = "./settings.cfg"
    einstellungen = einstellungen_laden()  # Dictionary initialisieren
    print("=====================")
    print("   Passwortmanager")
    print("=====================")
    # Darstellen der Optionen
    print("\n1) Neue Passwort-Datenbank erstellen\n2) Vorhandene Datenbank nutzen\n3) Abbrechen")
    # Auswahl der Optionen
    auswahl: int = int(input("\nWählen Sie eine der Optionen aus\n"))
    match auswahl:
        case 1:
            print(
                "Neue Datenbank wird angelegt.\nFalls vorhanden, wird die alte Datenbank gelöscht.")
            ersteinrichtung(pw_liste, einstellungen)
        case 2:
            print("Vorhandene Datenbank wird genutzt.")
            einrichtung_pruefen()
        case 3:
            print("Programm wird beendet.")
            sys.exit()


def einstellungen_laden():
    datei = open("./settings.cfg", 'r')
    Lines = datei.readlines()
    # Hier weitere Keys einfüllen, für mehr Settings wenn nötig
    einstellungen = {"datenbank_datei": "passwords.txt"}
    # Datei mit Einstellungen iterieren um Einstellungs-Variablen zu füllen
    for line in Lines:
        if len(line.strip()) != 0:
            if line.split(":")[0] == "datenbank_datei":
                # print(line.split(":"))
                einstellungen["datenbank_datei"] = line.split(":")[1]
    return einstellungen

# Oben Methoden / Funktionen
# ------------------------------------------------------------------------------------------------------------------------
# Unten Logik / Ablauf Planung


# Liste für Passwörter definieren
pw_liste = []
einstellungen = einstellungen_laden()
datenbank_datei_name = einstellungen['datenbank_datei']
# Startbildschirm zeigen
startbildschirm()  # zum Debuggen von PW Variable.
# Ausgabe der formatierten Daten aus der Passwort Datei.
Ausgabe_Pw_Liste(pw_liste)
# Hauptschleife
while True:
    auswahl_Menue(pw_liste, datenbank_datei_name)
