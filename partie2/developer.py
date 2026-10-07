# 6GEI311 - Lab 2 - Partie 2
# Classe Developer (avant c'etait Admin)
# herite de User : un dev peut faire tout ce qu'un user fait + assigner/fermer

from ticket import Ticket
from user import User


class Developer(User):
    def __init__(self, name, email):
        # pas besoin de redefinir name, email, id : on appelle le constructeur de User
        super().__init__(name, email, role="Développeur")

    def assignTicket(self, ticket, user):
        # le dev recoit la demande, le ticket fait le changement d'etat
        if ticket.assignTo(user):
            print(f"Ticket #{ticket.ticketID} assigné à {user.name}")

    def closeTicket(self, ticket):
        # fermeture possible seulement depuis OUVERT
        if ticket.updateStatus("FERME"):
            print(f"Ticket #{ticket.ticketID} fermé.")

    def viewAllTickets(self):
        return Ticket.all_tickets
