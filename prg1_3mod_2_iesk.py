import json
import os

#karte
MAPE = "prg1_3mod_2_iesk"
if not os.path.exists(MAPE):
    os.makedirs(MAPE)


class Skolens:
    def __init__(self, vards, uzvards, klase):
        self.vards = vards
        self.uzvards = uzvards
        self.klase = klase


class SkolenuRegistrs:
    def __init__(self):
        self.skoleni = []

    def pievienot(self, skolens):
        self.skoleni.append(skolens)

    def dzest(self, uzvards):
        self.skoleni = [s for s in self.skoleni if s.uzvards != uzvards]

    def sakartot_alfabetiski(self):
        return sorted(
            self.skoleni,
            key=lambda s: (s.uzvards.lower(), s.vards.lower())
        )

    def sadalit_pa_klasem(self):
        klases = {}
        for s in self.skoleni:
            klases.setdefault(s.klase, []).append(s)
        for klase in klases:
            klases[klase] = sorted(
                klases[klase],
                key=lambda s: (s.uzvards.lower(), s.vards.lower())
            )
        return klases

    def saglabat(self, fails="skoleni.json"):
        pilns_cels = os.path.join(MAPE, fails)
        dati = [
            {"vards": s.vards, "uzvards": s.uzvards, "klase": s.klase}
            for s in self.skoleni
        ]
        with open(pilns_cels, "w", encoding="utf-8") as f:
            json.dump(dati, f, ensure_ascii=False, indent=2)

    def ieladet(self, fails="skoleni.json"):
        pilns_cels = os.path.join(MAPE, fails)
        try:
            with open(pilns_cels, "r", encoding="utf-8") as f:
                dati = json.load(f)
                self.skoleni = [
                    Skolens(d["vards"], d["uzvards"], d["klase"])
                    for d in dati
                ]
            return True
        except FileNotFoundError:
            return False

    def saglabat_txt_alfabetiski(self, fails="skoleni_alfabetiski.txt"):
        with open(os.path.join(MAPE, fails), "w", encoding="utf-8") as f:
            for s in self.sakartot_alfabetiski():
                f.write(f"{s.uzvards} {s.vards} – {s.klase}\n")

    def saglabat_txt_pa_klasem(self, fails="skoleni_pa_klasem.txt"):
        with open(os.path.join(MAPE, fails), "w", encoding="utf-8") as f:
            klases = self.sadalit_pa_klasem()
            for klase in sorted(klases):
                f.write(f"[{klase}]\n")
                for s in klases[klase]:
                    f.write(f"{s.uzvards} {s.vards}\n")
                f.write("\n")


#automatiiski labo 1.burutu uz lielo
def ievade():
    vards = input("Ievadi vārdu: ").strip().capitalize()
    uzvards = input("Ievadi uzvārdu: ").strip().capitalize()
    klase = input("Ievadi klasi (piem. 1A): ").strip().upper()

    if not vards or not uzvards or not klase:
        print("Kļūda: visi lauki ir obligāti")
        return None

    if not vards.isalpha() or not uzvards.isalpha():
        print("Kļūda: vārdā un uzvārdā drīkst būt tikai burti")
        return None

    #cipars + burts
    if len(klase) != 2 or not klase[0].isdigit() or not klase[1].isalpha():
        print("Kļūda: klasei jābūt formātā, piemēram, 1A")
        return None

    return Skolens(vards, uzvards, klase)


#tas kas paradas terminali
registrs = SkolenuRegistrs()
ir_dati = registrs.ieladet()

if not ir_dati:
    registrs.pievienot(Skolens("Anna", "Bērziņa", "1A"))
    registrs.pievienot(Skolens("Jānis", "Kalniņš", "1B"))
    registrs.pievienot(Skolens("Līga", "Ozola", "1A"))
    registrs.saglabat()

while True:
    print("\n--- SKOLĒNU REĢISTRĀCIJAS SISTĒMA ---")
    print("1 - Pievienot skolēnu")
    print("2 - Dzēst skolēnu pēc uzvārda")
    print("3 - Rādīt alfabētiski")
    print("4 - Rādīt pa klasēm")
    print("5 - Saglabāt un iziet")

    izvele = input("Izvēle: ")

    if izvele == "1":
        skolens = ievade()
        if skolens:
            registrs.pievienot(skolens)
            print("Skolēns pievienots")

    elif izvele == "2":
        uzvards = input("Ievadi uzvārdu dzēšanai: ").strip().capitalize()
        registrs.dzest(uzvards)
        print("Skolēns dzēsts (ja eksistēja)")

    elif izvele == "3":
        for s in registrs.sakartot_alfabetiski():
            print(f"{s.uzvards} {s.vards} – {s.klase}")

    elif izvele == "4":
        klases = registrs.sadalit_pa_klasem()
        for klase in sorted(klases):
            print(f"[{klase}]")
            for s in klases[klase]:
                print(f"  {s.uzvards} {s.vards}")

    elif izvele == "5":
        registrs.saglabat()
        registrs.saglabat_txt_alfabetiski()
        registrs.saglabat_txt_pa_klasem()
        print("Dati saglabāti. Izveidoti visi faili.")
        break

    else:
        print("Nepareiza izvēle")