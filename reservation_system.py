import csv

class Vol:
    def __init__(self, numero_vol, depart, destination, nb_sieges, sieges_disponibles=None):
        self.numero_vol = numero_vol
        self.depart = depart
        self.destination = destination
        self.nb_sieges = nb_sieges
        self.sieges_disponibles = sieges_disponibles if sieges_disponibles is not None else nb_sieges

    def verifier_disponibilite(self):
        return self.sieges_disponibles > 0

    def reserver_siege(self):
        if self.verifier_disponibilite():
            self.sieges_disponibles -= 1
            return "Réservation réussie."
        else:
            return "Aucun siège disponible pour ce vol."

    def annuler_reservation(self):
        if self.sieges_disponibles < self.nb_sieges:
            self.sieges_disponibles += 1
            return "Annulation réussie."
        else:
            return "Aucune réservation à annuler pour ce vol."

    def to_dict(self):
        """Convertit les attributs de l'objet en dictionnaire pour faciliter la sauvegarde en CSV."""
        return {
            "numero_vol": self.numero_vol,
            "depart": self.depart,
            "destination": self.destination,
            "nb_sieges": self.nb_sieges,
            "sieges_disponibles": self.sieges_disponibles
        }

    @classmethod
    def from_dict(cls, data):
        """Crée un objet Vol à partir d'un dictionnaire."""
        return cls(
            numero_vol=data["numero_vol"],
            depart=data["depart"],
            destination=data["destination"],
            nb_sieges=int(data["nb_sieges"]),
            sieges_disponibles=int(data["sieges_disponibles"])
        )
   
    def __str__(self):
        return f"Vol {self.numero_vol}: {self.depart} -> {self.destination}, Sièges disponibles: {self.sieges_disponibles}/{self.nb_sieges}"

class Utilisateur:
    def __init__(self, nom, age):
        self.nom = nom
        self.age = age
        self.reservations = []

    def ajouter_reservation(self, vol):
        """Ajoute une réservation pour un vol donné."""
        resultat = vol.reserver_siege()
        if resultat == "Réservation réussie.":
           self.reservations.append(vol)
           return f"{self.nom} a réservé avec succès un siège sur le vol {vol.numero_vol}."
        else:
           return f"Échec de la réservation pour {self.nom} : {resultat}"


    def annuler_reservation(self, vol, nom, age):
        """Annule une réservation pour un vol donné uniquement si le nom et l'âge correspondent."""
        if self.nom == nom and self.age == age:
           for v in self.reservations:
               if v.numero_vol == vol.numero_vol:
                  resultat = v.annuler_reservation()
                  if "Réussie" in resultat:
                      self.reservations.remove(v)
                      return f"{self.nom} a annulé sa réservation sur le vol {vol.numero_vol}."
                  else:
                      return f"Échec de l'annulation pour {self.nom} : {resultat}"
           return f"{self.nom} n'a pas de réservation sur le vol {vol.numero_vol}."
        else:
           return "Les informations de l'utilisateur ne correspondent pas. Annulation refusée."

    def __str__(self):
        return f"Utilisateur {self.nom}, Âge: {self.age}, Réservations: {[str(vol) for vol in self.reservations]}"

class GestionVols:
    def __init__(self, fichier_csv):
        self.fichier_csv = fichier_csv
        self.vols = self.charger_vols()

    def charger_vols(self):
        vols = []
        try:
            with open(self.fichier_csv, mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    vols.append(Vol.from_dict(row))
        except FileNotFoundError:
            print(f"Fichier {self.fichier_csv} non trouvé. Création d'un nouveau fichier.")
        return vols

    def sauvegarder_vols(self):
        with open(self.fichier_csv, mode='w', newline='') as csvfile:
            fieldnames = ["numero_vol", "depart", "destination", "nb_sieges", "sieges_disponibles"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for vol in self.vols:
                writer.writerow(vol.to_dict())

    def ajouter_vol(self, vol):
        self.vols.append(vol)
        self.sauvegarder_vols()

    def afficher_vols(self):
        for vol in self.vols:
            print(vol)
