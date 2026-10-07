# 6GEI311 - Lab 2 - Partie 1
# Classe Admin : c'est lui qui assigne et ferme les tickets

from ticket import Ticket


class Admin:
    # compteur pour les id des admins
    id_suivant = 1

    def __init__(self, name, email):
        self.adminID = Admin.id_suivant
        Admin.id_suivant += 1
        self.name = name
        self.email = email

    def assignTicket(self, ticket, user):
        # l'admin recoit la demande mais c'est le ticket qui change son etat
        # assignTo retourne False si la transition est pas permise
        if ticket.assignTo(user):
            print(f"Ticket #{ticket.ticketID} assigné à {user.name}")

    def closeTicket(self, ticket):
        # on peut fermer seulement un ticket OUVERT (voir TRANSITIONS dans ticket.py)
        if ticket.updateStatus("FERME"):
            print(f"Ticket #{ticket.ticketID} fermé.")

    def viewAllTickets(self):
        # retourne la liste de tous les tickets crees
        return Ticket.all_tickets

    def __str__(self):
        return f"{self.name} (ID: {self.adminID}, {self.email})"
