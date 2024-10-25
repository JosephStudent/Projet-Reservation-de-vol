import tkinter as tk
from tkinter import messagebox
from reservation_system import Vol, Utilisateur, GestionVols


class Application(tk.Tk):
    def __init__(self, gestion_vols):
        super().__init__()
        self.title("Système de Réservation de Vols")
        self.geometry("600x400")
        self.gestion_vols = gestion_vols
        
        # Titre
        tk.Label(self, text="Liste des Vols Disponibles", font=("Helvetica", 16)).pack(pady=10)
        
        # Liste des vols
        self.vol_listbox = tk.Listbox(self, width=50, height=10)
        self.vol_listbox.pack(pady=10)
        
        # Charger les vols dans la liste
        self.charger_vols()
        
        # Formulaire pour l'utilisateur
        tk.Label(self, text="Nom de l'utilisateur:").pack()
        self.nom_entry = tk.Entry(self)
        self.nom_entry.pack(pady=5)
        
        tk.Label(self, text="Âge de l'utilisateur:").pack()
        self.age_entry = tk.Entry(self)
        self.age_entry.pack(pady=5)
        
        # Boutons pour réserver et annuler
        tk.Button(self, text="Réserver", command=self.reserver_vol).pack(pady=5)
        tk.Button(self, text="Annuler Réservation", command=self.annuler_reservation).pack(pady=5)
        
    def charger_vols(self):
        """Charge les vols disponibles dans la liste."""
        self.vol_listbox.delete(0, tk.END)
        for vol in self.gestion_vols.vols:
            self.vol_listbox.insert(tk.END, f"{vol.numero_vol} - {vol.depart} -> {vol.destination} (Sièges dispo: {vol.sieges_disponibles})")
    
    def get_selected_vol(self):
        """Récupère le vol sélectionné par l'utilisateur."""
        try:
            index = self.vol_listbox.curselection()[0]
            return self.gestion_vols.vols[index]
        except IndexError:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un vol.")
            return None
    
    def reserver_vol(self):
        """Réserve un siège sur le vol sélectionné pour l'utilisateur."""
        vol = self.get_selected_vol()
        if vol:
            nom = self.nom_entry.get()
            age = self.age_entry.get()
            if nom and age.isdigit():
                utilisateur = Utilisateur(nom=nom, age=int(age))
                message = utilisateur.ajouter_reservation(vol)
                messagebox.showinfo("Résultat de la réservation", message)
                self.charger_vols()
                self.gestion_vols.sauvegarder_vols()
            else:
                messagebox.showwarning("Erreur", "Veuillez entrer un nom et un âge valides.")
    
    def annuler_reservation(self):
        """Annule la réservation de l'utilisateur sur le vol sélectionné."""
        vol = self.get_selected_vol()
        if vol:
            nom = self.nom_entry.get()
            age = self.age_entry.get()
            if nom and age.isdigit():
                utilisateur = Utilisateur(nom=nom, age=int(age))
                message = utilisateur.annuler_reservation(vol)
                messagebox.showinfo("Résultat de l'annulation", message)
                self.charger_vols()
                self.gestion_vols.sauvegarder_vols()
            else:
                messagebox.showwarning("Erreur", "Veuillez entrer un nom et un âge valides.")

# Initialisation de la gestion des vols
gestion_vols = GestionVols("vols.csv")

# Lancement de l'application Tkinter
app = Application(gestion_vols)
app.mainloop()
