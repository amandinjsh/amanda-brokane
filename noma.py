
from datetime import datetime, date  


class Noma:
    #  Noma() vai Noma(ar datiem)
    def __init__(self, kategorija="", nosaukums="", raksturojumi="", cena=0):
        self.kategorija = kategorija
        self.nosaukums = nosaukums
        self.raksturojumi = raksturojumi
        self.cena = float(cena)
        self.pieejams = True
        self.vards = self.uzvards = self.pk = self.tel = ""
        self.sakums = self.beigas = None

    # nomnieki un datumus
    def iznomat(self, vards, uzvards, pk, tel, sakums, beigas):
        sakums = datetime.strptime(sakums, "%d.%m.%Y").date()
        beigas = datetime.strptime(beigas, "%d.%m.%Y").date()
        if beigas < sakums:
            raise ValueError("Beigu datums ir pirms sākuma!")
        if not all((vards, uzvards, pk, tel)):
            raise ValueError("Trūkst nomnieka datu!")
        self.vards, self.uzvards = vards, uzvards
        self.pk, self.tel = pk, tel
        self.sakums, self.beigas = sakums, beigas
        self.pieejams = False

    # cik dienas palikušas
    def Nomas_atlikusais_laiks(self):
        if self.pieejams:
            return 0
        return max(0, (self.beigas - date.today()).days)

    # nomas maksu
    def Cena_kopa(self):
        if self.pieejams:
            return 0
        return round(((self.beigas - self.sakums).days + 1) * self.cena, 2)

    # Atgriež tekstu ar produkta informāciju
    def Produkta_info(self):
        return (f"Kategorija: {self.kategorija}\nNosaukums: {self.nosaukums}\n"
                f"Raksturojumi: {self.raksturojumi}\nCena dienā: {self.cena:.2f} EUR\n"
                f"Pieejams: {'Jā' if self.pieejams else 'Nē'}")

    # Atgriež tekstu ar nomnieka informāciju
    def Nomnieks_info(self):
        if self.pieejams:
            return "Produkts nav iznomāts."
        return (f"Nomnieks: {self.vards} {self.uzvards}\n"
                f"Personas kods: {self.pk}\nTālrunis: {self.tel}\n"
                f"Noma: {self.sakums:%d.%m.%Y} – {self.beigas:%d.%m.%Y}\n"
                f"Atlikušās dienas: {self.Nomas_atlikusais_laiks()}\n"
                f"Cena kopā: {self.Cena_kopa():.2f} EUR")

    # Saglabā produkta atskaiti txt failā
    def Produkta_info_print(self, fails):
        with open(fails, "w", encoding="utf-8") as f:
            f.write(self.Produkta_info())

    # Saglabā nomnieka atskaiti txt failā
    def Nomnieks_info_print(self, fails):
        with open(fails, "w", encoding="utf-8") as f:
            f.write(self.Nomnieks_info())

# Piedāvā izvēlēties instrumentu pēc numura
def izveleties(produkti):
    if not produkti:
        print("Instrumentu saraksts ir tukšs.")
        return None
    for nr, p in enumerate(produkti, 1):
        print(f"{nr}. {p.nosaukums}")
    nr = int(input("Instrumenta numurs: "))
    if not 1 <= nr <= len(produkti):
        raise ValueError("Nepareizs numurs!")
    return produkti[nr - 1]

# Galvenā izvēlne
produkti = []
while True:
    print("\n1 - Datu ievade | 2 - Datu izvade | 3 - Datu printēšana | 0 - Iziet")
    izvele = input("Izvēle: ")
    if izvele == "0":
        break
    try:
        if izvele == "1":  # Ievada jaunu instrumentu
            p = Noma(input("Kategorija: "), input("Nosaukums: "),
                     input("Raksturojumi: "), input("Cena dienā: "))
            if p.cena < 0 or not p.nosaukums:
                raise ValueError("Nepareizs nosaukums vai cena!")
            if input("Uzreiz iznomāt? (j/n): ").lower() == "j":
                dati = [input(teksts) for teksts in (
                    "Vārds: ", "Uzvārds: ", "Personas kods: ", "Tālrunis: ",
                    "Sākums (DD.MM.GGGG): ", "Beigas (DD.MM.GGGG): ")]
                p.iznomat(*dati)
            produkti.append(p)
            print("Produkts pievienots!")
        elif izvele == "2":  # Parāda informāciju
            p = izveleties(produkti)
            if p:
                print(p.Produkta_info() + "\n" + p.Nomnieks_info())
        elif izvele == "3":  # Saglabā txt atskaiti
            p = izveleties(produkti)
            if p:
                veids = input("1 - Produkts, 2 - Nomnieks: ")
                if veids not in ("1", "2"):
                    print("Nepareiza izvēle!")
                    continue
                fails = input("TXT faila nosaukums: ")
                if not fails.endswith(".txt"):
                    fails += ".txt"
                if veids == "1":
                    p.Produkta_info_print(fails)
                else:
                    p.Nomnieks_info_print(fails)
                print("Atskaite saglabāta:", fails)
        else:
            print("Nepareiza izvēle!")
    except (ValueError, OSError) as kluda:
        print("Kļūda:", kluda)
