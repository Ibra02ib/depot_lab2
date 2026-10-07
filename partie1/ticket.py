# 6GEI311 - Lab 2 - Partie 1
# Classe Ticket : contient les infos du ticket et gere son statut

from datetime import datetime


class Ticket:
    # liste de tous les tickets (sert pour viewAllTickets)
    all_tickets = []
    id_suivant = 1

    # pour chaque statut, les statuts ou on a le droit d'aller ensuite
    # - on ne peut pas sauter VALIDATION
    # - on peut fermer seulement un ticket OUVERT
    # - ASSIGNE -> ASSIGNE c'est pour reassigner a quelqu'un d'autre
    # - VALIDATION -> ASSIGNE c'est quand la validation echoue
    TRANSITIONS = {
        "OUVERT": ["ASSIGNE", "FERME"],
        "ASSIGNE": ["VALIDATION", "ASSIGNE"],
        "VALIDATION": ["TERMINE", "ASSIGNE"],
        "TERMINE": [],   # fini, on peut plus rien faire
        "FERME": [],     # fini aussi
    }

    def __init__(self, title, description, priority):
        self.ticketID = Ticket.id_suivant
        Ticket.id_suivant += 1
        self.title = title
        self.description = description
        self.priority = priority
        self.creationDate = datetime.now()
        self.updateDate = datetime.now()
        self.status = "OUVERT"   # un ticket commence toujours OUVERT
        self.comment = []
        self.creator = None
        self.assignedTo = None
        Ticket.all_tickets.append(self)

    def assignTo(self, user):
        # on verifie d'abord si on peut passer a ASSIGNE,
        # sinon on changerait la personne meme si c'est refuse
        if self.updateStatus("ASSIGNE"):
            self.assignedTo = user
            return True
        return False

    def updateStatus(self, status):
        # on regarde si le nouveau statut est dans la liste permise
        permis = Ticket.TRANSITIONS[self.status]
        if status not in permis:
            print(f"Transition refusée : {self.status} -> {status}")
            return False
        self.status = status
        self.updateDate = datetime.now()
        return True

    def addComment(self, comment):
        self.comment.append(comment)
        self.updateDate = datetime.now()

    def __str__(self):
        return f"{self.title} (ID: {self.ticketID}, {self.status})"
