# 6GEI311 - Lab 2 - Partie 2
# Classe Ticket : description (String) remplacee par une liste de pieces jointes

from datetime import datetime


class Ticket:
    all_tickets = []
    id_suivant = 1

    # statuts permis apres chaque statut (meme table que la partie 1)
    TRANSITIONS = {
        "OUVERT": ["ASSIGNE", "FERME"],
        "ASSIGNE": ["VALIDATION", "ASSIGNE"],     # ASSIGNE -> ASSIGNE = reassigner
        "VALIDATION": ["TERMINE", "ASSIGNE"],     # retour a ASSIGNE si validation ratee
        "TERMINE": [],
        "FERME": [],
    }

    def __init__(self, title, priority):
        self.ticketID = Ticket.id_suivant
        Ticket.id_suivant += 1
        self.title = title
        self.priority = priority
        self.creationDate = datetime.now()
        self.updateDate = datetime.now()
        self.status = "OUVERT"
        self.comment = []
        self.creator = None
        self.assignedTo = None     # association "assignedTo" (0..1)
        self.pieces_jointes = []   # composition avec PieceJointe
        Ticket.all_tickets.append(self)

    def assignTo(self, user):
        # on change assignedTo seulement si la transition passe
        if self.updateStatus("ASSIGNE"):
            self.assignedTo = user
            return True
        return False

    def updateStatus(self, status):
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

    def ajouterContenu(self, piece):
        # le ticket gere lui-meme sa liste de pieces jointes (Createur / Expert)
        self.pieces_jointes.append(piece)
        self.updateDate = datetime.now()

    def __str__(self):
        return f"{self.title} (ID: {self.ticketID}, {self.status})"
