# 6GEI311 - Lab 2 - Partie 1
# Classe User : un utilisateur qui peut creer, voir et modifier des tickets

from datetime import datetime


class User:
    # compteur partage par tous les users pour donner un id unique
    id_suivant = 1

    def __init__(self, name, email, role):
        self.userID = User.id_suivant
        User.id_suivant += 1
        self.name = name
        self.email = email
        self.role = role
        # liste des tickets que ce user a crees (association "creates")
        self.created_tickets = []

    def createTicket(self, ticket):
        # on fait le lien dans les deux sens : le ticket connait son createur
        # et le user garde le ticket dans sa liste
        ticket.creator = self
        self.created_tickets.append(ticket)

    def viewTicket(self, ticket):
        print(f"Ticket #{ticket.ticketID} - {ticket.title}")
        print(f"Statut: {ticket.status} | Priorité: {ticket.priority}")
        print(f"Description: {ticket.description}")
        # on affiche aussi les commentaires sinon on ne les voit jamais
        if len(ticket.comment) > 0:
            print("Commentaires :")
            for c in ticket.comment:
                print(f"  - {c}")

    def updateTicket(self, ticket, title=None, description=None, priority=None):
        # on change seulement ce qui a ete donne (None = on touche pas)
        if title:
            ticket.title = title
        if description:
            ticket.description = description
        if priority:
            ticket.priority = priority
        ticket.updateDate = datetime.now()

    def __str__(self):
        return f"{self.name} (ID: {self.userID}, {self.role})"
