# 6GEI311 - Lab 2 - Partie 2
# Classe User : utilisateur de base (Developer herite de cette classe)

from datetime import datetime


class User:
    # un seul compteur pour User ET Developer, comme ca pas deux personnes
    # avec le meme id
    id_suivant = 1

    def __init__(self, name, email, role):
        self.userID = User.id_suivant
        User.id_suivant += 1
        self.name = name
        self.email = email
        self.role = role
        self.created_tickets = []   # association "creates"

    def createTicket(self, ticket):
        ticket.creator = self
        self.created_tickets.append(ticket)

    def viewTicket(self, ticket):
        print(f"Ticket #{ticket.ticketID} - {ticket.title}")
        print(f"Statut: {ticket.status} | Priorité: {ticket.priority}")

        # la description c'est maintenant les pieces jointes
        # chaque piece sait se charger toute seule (polymorphisme)
        if len(ticket.pieces_jointes) > 0:
            print("Contenu :")
            for piece in ticket.pieces_jointes:
                piece.charger()
        else:
            print("Contenu : (aucun)")

        if len(ticket.comment) > 0:
            print("Commentaires :")
            for c in ticket.comment:
                print(f"  - {c}")

    def updateTicket(self, ticket, title=None, priority=None):
        if title:
            ticket.title = title
        if priority:
            ticket.priority = priority
        ticket.updateDate = datetime.now()

    def __str__(self):
        return f"{self.name} (ID: {self.userID}, {self.role})"
