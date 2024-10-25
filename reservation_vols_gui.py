import tkinter as tk
from tkinter import messagebox
from reservation_system import Vol, Utilisateur, GestionVols


class Application(tk.Tk):
    def __init__(self, gestion_vols):
        super().__init__()
        self.title("Système de Réservation de Vols")
        self.geometry("600x400")
        self.gestion_vols = gestion_vols
        
        # Initialise l'utilisateur ici une seule fois
        self.utilisateur = None
        
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
        
        # Boutons pour réserver, annuler, et afficher l'historique
        tk.Button(self, text="Réserver", command=self.reserver_vol).pack(pady=5)
        tk.Button(self, text="Annuler Réservation", command=self.annuler_reservation).pack(pady=5)
        tk.Button(self, text="Voir l'Historique", command=self.afficher_historique).pack(pady=5)
        
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
        nom = self.nom_entry.get()
        age = self.age_entry.get()
        
        if not self.utilisateur and nom and age.isdigit():
            # Créer un nouvel utilisateur une seule fois, et l'utiliser pour toutes les actions
            self.utilisateur = Utilisateur(nom=nom, age=int(age))
        
        if vol and self.utilisateur:
            message = self.utilisateur.ajouter_reservation(vol)
            messagebox.showinfo("Résultat de la réservation", message)
            self.charger_vols()
            self.gestion_vols.sauvegarder_vols()
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom et un âge valides.")
    
    def annuler_reservation(self):
        """Annule la réservation de l'utilisateur sur le vol sélectionné."""
        vol = self.get_selected_vol()
        nom = self.nom_entry.get()
        age = self.age_entry.get()
        
        if vol and self.utilisateur:
            # Utilise l'utilisateur déjà initialisé pour annuler
            message = self.utilisateur.annuler_reservation(vol, nom, int(age))
            messagebox.showinfo("Résultat de l'annulation", message)
            self.charger_vols()
            self.gestion_vols.sauvegarder_vols()
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom, un âge valides, et sélectionner un vol.")
    
    def afficher_historique(self):
        """Affiche l'historique des réservations de l'utilisateur."""
        if not self.utilisateur or len(self.utilisateur.reservations) == 0:
            messagebox.showinfo("Historique des réservations", "Aucune réservation en cours.")
            return
        
        # Créer une nouvelle fenêtre pour afficher l'historique
        historique_fenetre = tk.Toplevel(self)
        historique_fenetre.title("Historique des Réservations")
        historique_fenetre.geometry("400x300")
        
        # Liste des réservations
        historique_listbox = tk.Listbox(historique_fenetre, width=50, height=10)
        historique_listbox.pack(pady=10)
        
        # Charger les réservations dans la liste
        for vol in self.utilisateur.reservations:
            historique_listbox.insert(tk.END, f"{vol.numero_vol} - {vol.depart} -> {vol.destination} (Sièges dispo: {vol.sieges_disponibles})")
        
        # Bouton pour annuler une réservation depuis l'historique
        def annuler_historique_reservation():
            try:
                index = historique_listbox.curselection()[0]
                vol_selectionne = self.utilisateur.reservations[index]
                # Annuler la réservation
                message = self.utilisateur.annuler_reservation(vol_selectionne, self.utilisateur.nom, self.utilisateur.age)
                messagebox.showinfo("Résultat de l'annulation", message)
                historique_listbox.delete(index)
                self.charger_vols()
                self.gestion_vols.sauvegarder_vols()
            except IndexError:
                messagebox.showwarning("Avertissement", "Veuillez sélectionner une réservation.")
        
        # Bouton d'annulation de réservation dans l'historique
        tk.Button(historique_fenetre, text="Annuler Réservation", command=annuler_historique_reservation).pack(pady=5)

# Initialisation de la gestion des vols
gestion_vols = GestionVols("vols.csv")

# Lancement de l'application Tkinter
app = Application(gestion_vols)
app.mainloop()
