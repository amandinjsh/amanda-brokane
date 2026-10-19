import datetime
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class Noma: #info par instr., nom., noom.dat.
    def __init__(self, kategorija="", nosaukums="", raksturojumi="", cena=0):
        self.produkta_kategorija = kategorija
        self.produkta_nosaukums = nosaukums
        self.tehniskie_raksturojumi = raksturojumi
        self.nomas_cena_diena = float(cena)
        self.produkts_pieejams = True

        self.nomnieks_vards = ""
        self.nomnieks_uzvards = ""
        self.nomnieks_pk = ""
        self.nomnieks_tel = ""
        self.nomas_sakuma_datums = ""
        self.nomas_beigu_datums = ""

    @staticmethod
    def datums(teksts):
        return datetime.datetime.strptime(teksts, "%d.%m.%Y").date()

    def iznomat(self, vards, uzvards, pk, tel, sakums, beigas):
        if not all([vards, uzvards, pk, tel, sakums, beigas]):
            raise ValueError("Aizpildi visus nomnieka un datumu laukus!")

        if self.datums(beigas) < self.datums(sakums):
            raise ValueError("Nomas beigu datums nevar būt pirms sākuma datuma!")

        self.nomnieks_vards = vards
        self.nomnieks_uzvards = uzvards
        self.nomnieks_pk = pk
        self.nomnieks_tel = tel
        self.nomas_sakuma_datums = sakums
        self.nomas_beigu_datums = beigas
        self.produkts_pieejams = False

    def atgriezt(self):
        self.produkts_pieejams = True
        self.nomnieks_vards = self.nomnieks_uzvards = ""
        self.nomnieks_pk = self.nomnieks_tel = ""
        self.nomas_sakuma_datums = self.nomas_beigu_datums = ""

    def Nomas_atlikusais_laiks(self):
        if self.produkts_pieejams:
            return None

        return (
            self.datums(self.nomas_beigu_datums)
            - datetime.date.today()
        ).days

    def Cena_kopa(self):
        if self.produkts_pieejams:
            return 0

        dienas = (
            self.datums(self.nomas_beigu_datums)
            - self.datums(self.nomas_sakuma_datums)
        ).days + 1

        return round(dienas * self.nomas_cena_diena, 2)

    def Produkta_info(self):
        pieejams = "Jā" if self.produkts_pieejams else "Nē"

        return (
            f"Kategorija: {self.produkta_kategorija}\n"
            f"Nosaukums: {self.produkta_nosaukums}\n"
            f"Raksturojumi: {self.tehniskie_raksturojumi}\n"
            f"Cena dienā: {self.nomas_cena_diena:.2f} EUR\n"
            f"Pieejams: {pieejams}"
        )

    def Nomnieks_info(self):
        if self.produkts_pieejams:
            return "Produkts pašlaik nav iznomāts."

        return (
            f"Vārds: {self.nomnieks_vards}\n"
            f"Uzvārds: {self.nomnieks_uzvards}\n"
            f"Personas kods: {self.nomnieks_pk}\n"
            f"Tālrunis: {self.nomnieks_tel}\n"
            f"Nomas sākums: {self.nomas_sakuma_datums}\n"
            f"Nomas beigas: {self.nomas_beigu_datums}\n"
            f"Atlikušās dienas: {self.Nomas_atlikusais_laiks()}\n"
            f"Cena kopā: {self.Cena_kopa():.2f} EUR"
        )

    def Produkta_info_print(self, cels):
        with open(cels, "w", encoding="utf-8") as fails:
            fails.write(self.Produkta_info())

    def Nomnieks_info_print(self, cels):
        with open(cels, "w", encoding="utf-8") as fails:
            fails.write(self.Nomnieks_info())

    def uz_vardnicu(self):
        return self.__dict__.copy()

    @classmethod
    def no_vardnicas(cls, dati):
        objekts = cls()
        objekts.__dict__.update(dati)
        return objekts


class NomasLietotne:
    def __init__(self, logs):
        self.logs = logs
        self.logs.title("Instrumentu un tehnikas uzskaites sistēma")
        self.logs.geometry("800x650")

        self.fails = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "nomas_dati.json"
        )

        self.produkti = []
        self.ieladet()

        cilnes = ttk.Notebook(logs)
        cilnes.pack(fill="both", expand=True, padx=12, pady=12)

        ievade = ttk.Frame(cilnes, padding=15)
        izvade = ttk.Frame(cilnes, padding=15)
        atskaites = ttk.Frame(cilnes, padding=15)

        cilnes.add(ievade, text="1. Datu ievade")
        cilnes.add(izvade, text="2. Datu izvade")
        cilnes.add(atskaites, text="3. Datu printēšana")

        lauki = [
            ("kategorija", "Produkta kategorija"),
            ("nosaukums", "Produkta nosaukums"),
            ("raksturojumi", "Tehniskie raksturojumi"),
            ("cena", "Nomas cena dienā (EUR)"),
            ("vards", "Nomnieka vārds (ja iznomāts)"),
            ("uzvards", "Nomnieka uzvārds"),
            ("pk", "Nomnieka personas kods"),
            ("tel", "Nomnieka tālrunis"),
            ("sakums", "Nomas sākums (DD.MM.GGGG)"),
            ("beigas", "Nomas beigas (DD.MM.GGGG)")
        ]

        self.ievades_lauki = {}

        for rinda, (atslega, virsraksts) in enumerate(lauki):
            ttk.Label(
                ievade, text=virsraksts
            ).grid(row=rinda, column=0, sticky="w", pady=6)

            lauks = ttk.Entry(ievade, width=40)
            lauks.grid(row=rinda, column=1, sticky="ew", pady=6)
            self.ievades_lauki[atslega] = lauks

        ttk.Button(
            ievade,
            text="Pievienot produktu",
            command=self.pievienot
        ).grid(row=len(lauki), column=0, columnspan=2, pady=15)

        ttk.Label(
            izvade, text="Izvēlies instrumentu:"
        ).pack(anchor="w")

        self.saraksts = tk.Listbox(izvade, height=10)
        self.saraksts.pack(fill="x", pady=8)

        ttk.Button(
            izvade,
            text="Parādīt informāciju",
            command=self.paradit
        ).pack(anchor="w", pady=3)

        ttk.Button(
            izvade,
            text="Atzīmēt kā atgrieztu",
            command=self.atgriezt
        ).pack(anchor="w", pady=3)

        ttk.Button(
            izvade,
            text="Dzēst izvēlēto",
            command=self.dzest
        ).pack(anchor="w", pady=3)

        self.rezultats = tk.Text(izvade, height=14, width=80)
        self.rezultats.pack(fill="both", expand=True, pady=8)

        ttk.Label(
            atskaites,
            text="Vispirms izvēlies produktu cilnē 'Datu izvade'."
        ).pack(anchor="w")

        ttk.Button(
            atskaites,
            text="Saglabāt produkta TXT atskaiti",
            command=lambda: self.atskaite("produkts")
        ).pack(anchor="w", pady=12)

        ttk.Button(
            atskaites,
            text="Saglabāt nomnieka TXT atskaiti",
            command=lambda: self.atskaite("nomnieks")
        ).pack(anchor="w", pady=12)

        self.atjaunot_sarakstu()

    def ieladet(self):
        if os.path.exists(self.fails):
            try:
                with open(self.fails, "r", encoding="utf-8") as fails:
                    dati = json.load(fails)

                self.produkti = [
                    Noma.no_vardnicas(x) for x in dati
                ]

            except (OSError, ValueError, TypeError):
                self.produkti = []
                messagebox.showerror(
                    "Kļūda",
                    "Neizdevās nolasīt nomas_dati.json"
                )

    def saglabat(self):
        with open(self.fails, "w", encoding="utf-8") as fails:
            json.dump(
                [x.uz_vardnicu() for x in self.produkti],
                fails,
                ensure_ascii=False,
                indent=2
            )

    def atjaunot_sarakstu(self):
        self.saraksts.delete(0, tk.END)

        for produkts in self.produkti:
            statuss = (
                "Pieejams" if produkts.produkts_pieejams
                else "Iznomāts"
            )

            self.saraksts.insert(
                tk.END,
                f"{produkts.produkta_nosaukums} — {statuss}"
            )

    def pievienot(self):
        d = {
            k: v.get().strip()
            for k, v in self.ievades_lauki.items()
        }

        try:
            if not d["kategorija"] or not d["nosaukums"]:
                raise ValueError(
                    "Ievadi produkta kategoriju un nosaukumu!"
                )

            cena = float(d["cena"].replace(",", "."))

            if not (0 <= cena < float("inf")):
                raise ValueError(
                    "Cena nedrīkst būt negatīva!"
                )

            produkts = Noma(
                d["kategorija"],
                d["nosaukums"],
                d["raksturojumi"],
                cena
            )

            if any(d[x] for x in (
                "vards", "uzvards", "pk",
                "tel", "sakums", "beigas"
            )):
                produkts.iznomat(
                    d["vards"],
                    d["uzvards"],
                    d["pk"],
                    d["tel"],
                    d["sakums"],
                    d["beigas"]
                )

            self.produkti.append(produkts)
            self.saglabat()
            self.atjaunot_sarakstu()

            for lauks in self.ievades_lauki.values():
                lauks.delete(0, tk.END)

            messagebox.showinfo(
                "Gatavs", "Produkts pievienots!"
            )

        except (ValueError, OSError) as kluda:
            messagebox.showerror("Kļūda", str(kluda))

    def izveletais(self):
        if not self.saraksts.curselection():
            messagebox.showwarning(
                "Uzmanību",
                "Vispirms izvēlies produktu sarakstā!"
            )
            return None

        return self.produkti[
            self.saraksts.curselection()[0]
        ]

    def paradit(self):
        produkts = self.izveletais()

        if produkts is not None:
            self.rezultats.delete("1.0", tk.END)
            self.rezultats.insert(
                tk.END,
                produkts.Produkta_info()
                + "\n\n"
                + produkts.Nomnieks_info()
            )

    def atgriezt(self):
        produkts = self.izveletais()

        if produkts is not None:
            produkts.atgriezt()
            self.saglabat()
            self.atjaunot_sarakstu()
            self.rezultats.delete("1.0", tk.END)

            messagebox.showinfo(
                "Gatavs",
                "Produkts atzīmēts kā pieejams!"
            )

    def dzest(self):
        produkts = self.izveletais()

        if produkts is not None and messagebox.askyesno(
            "Apstiprināt",
            "Dzēst šo produktu?"
        ):
            self.produkti.remove(produkts)
            self.saglabat()
            self.atjaunot_sarakstu()
            self.rezultats.delete("1.0", tk.END)

    def atskaite(self, veids):
        produkts = self.izveletais()

        if produkts is None:
            return

        cels = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Teksta datne", "*.txt")]
        )

        if cels:
            try:
                if veids == "produkts":
                    produkts.Produkta_info_print(cels)
                else:
                    produkts.Nomnieks_info_print(cels)

                messagebox.showinfo(
                    "Gatavs",
                    "Atskaite saglabāta!"
                )

            except OSError as kluda:
                messagebox.showerror("Kļūda", str(kluda))


if __name__ == "__main__":
    logs = tk.Tk()
    NomasLietotne(logs)
    logs.mainloop()