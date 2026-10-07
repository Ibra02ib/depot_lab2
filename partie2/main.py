# 6GEI311 - Lab 2 - Partie 2
# Programme principal : on se connecte comme utilisateur ou developpeur,
# puis on a un menu different selon le type de compte

from ticket import Ticket
from user import User
from developer import Developer
from piece_jointe import TextePieceJointe, ImagePieceJointe, VideoPieceJointe


# choisir un element dans une liste, retourne None si probleme
def choisir_dans_liste(liste, nom_du_type):
    if len(liste) == 0:
        print(f"Aucun {nom_du_type} n'existe encore.")
        return None

    print(f"\nChoisis un {nom_du_type} :")
    for i in range(len(liste)):
        print(f"{i + 1}. {liste[i]}")

    choix = input("Ton choix : ")
    if not choix.isdigit():
        print("Entrée invalide.")
        return None

    index = int(choix) - 1
    if index < 0 or index >= len(liste):
        print("Numéro invalide.")
        return None

    return liste[index]


def ajouter_contenu_a_ticket(ticket):
    print("Type de contenu : 1. Texte  2. Image  3. Vidéo")
    type_choix = input("Ton choix : ")
    chemin = input("Chemin du fichier : ")

    # on cree la bonne sorte de piece jointe selon le choix
    piece = None
    if type_choix == "1":
        piece = TextePieceJointe(chemin)
    elif type_choix == "2":
        piece = ImagePieceJointe(chemin)
    elif type_choix == "3":
        piece = VideoPieceJointe(chemin)
    else:
        print("Type invalide.")

    if piece is not None:
        ticket.ajouterContenu(piece)
        print("Contenu ajouté au ticket.")


# demande titre et priorite et met a jour le ticket (utilise dans les 2 menus)
def mettre_a_jour(current_user, ticket):
    nouveau_titre = input("Nouveau titre (vide = pas de changement) : ")
    nouvelle_prio = input("Nouvelle priorité (vide = pas de changement) : ")
    if nouveau_titre == "":
        nouveau_titre = None
    if nouvelle_prio == "":
        nouvelle_prio = None
    current_user.updateTicket(ticket, nouveau_titre, nouvelle_prio)
    print("Ticket mis à jour.")


#  Connexion 

def afficher_menu_connexion():
    print("\n Gestionnaire de tickets UQAC")
    print("1. Je suis un utilisateur")
    print("2. Je suis un développeur")
    print("3. Quitter")


def connexion_utilisateur(users):
    print("1. Me connecter avec un compte existant")
    print("2. Créer un nouveau compte utilisateur")
    choix = input("Ton choix : ")

    if choix == "1":
        return choisir_dans_liste(users, "utilisateur")
    elif choix == "2":
        name = input("Nom : ")
        email = input("Email : ")
        role = input("Rôle : ")
        nouveau_user = User(name, email, role)
        users.append(nouveau_user)
        print("Utilisateur créé avec succès.")
        return nouveau_user
    else:
        print("Choix invalide.")
        return None


def connexion_developpeur(developers):
    print("1. Me connecter avec un compte existant")
    print("2. Créer un nouveau compte développeur")
    choix = input("Ton choix : ")

    if choix == "1":
        return choisir_dans_liste(developers, "développeur")
    elif choix == "2":
        name = input("Nom : ")
        email = input("Email : ")
        nouveau_dev = Developer(name, email)
        developers.append(nouveau_dev)
        print("Développeur créé avec succès.")
        return nouveau_dev
    else:
        print("Choix invalide.")
        return None


# Menu utilisateur 
# un user voit seulement SES tickets (created_tickets)

def afficher_menu_utilisateur():
    print("\n Menu utilisateur ")
    print("1. Créer un ticket")
    print("2. Ajouter du contenu à un de mes tickets")
    print("3. Afficher un de mes tickets")
    print("4. Mettre à jour un de mes tickets")
    print("5. Ajouter un commentaire à un de mes tickets")
    print("6. Me déconnecter")


def menu_utilisateur(current_user):
    while True:
        afficher_menu_utilisateur()
        choix = input("Ton choix : ")

        if choix == "1":
            title = input("Titre : ")
            priority = input("Priorité : ")
            nouveau_ticket = Ticket(title, priority)
            current_user.createTicket(nouveau_ticket)
            print("Ticket créé avec succès.")

        elif choix == "2":
            ticket = choisir_dans_liste(current_user.created_tickets, "ticket")
            if ticket is not None:
                ajouter_contenu_a_ticket(ticket)

        elif choix == "3":
            ticket = choisir_dans_liste(current_user.created_tickets, "ticket")
            if ticket is not None:
                current_user.viewTicket(ticket)

        elif choix == "4":
            ticket = choisir_dans_liste(current_user.created_tickets, "ticket")
            if ticket is not None:
                mettre_a_jour(current_user, ticket)

        elif choix == "5":
            ticket = choisir_dans_liste(current_user.created_tickets, "ticket")
            if ticket is not None:
                commentaire = input("Commentaire : ")
                ticket.addComment(commentaire)
                print("Commentaire ajouté.")

        elif choix == "6":
            print(f"À bientôt, {current_user.name}.")
            break

        else:
            print("Choix invalide.")


# Menu developpeur 
# un dev a acces a tous les tickets (viewAllTickets)

def afficher_menu_developpeur():
    print("\n Menu développeur")
    print("1. Créer un ticket")
    print("2. Ajouter du contenu à un ticket")
    print("3. Afficher un ticket")
    print("4. Mettre à jour un ticket")
    print("5. Ajouter un commentaire à un ticket")
    print("6. Assigner un ticket")
    print("7. Mettre un ticket en validation")
    print("8. Terminer un ticket")
    print("9. Fermer un ticket")   # seulement si OUVERT
    print("10. Afficher tous les tickets")
    print("11. Me déconnecter")


def menu_developpeur(current_user, developers):
    while True:
        afficher_menu_developpeur()
        choix = input("Ton choix : ")

        if choix == "1":
            title = input("Titre : ")
            priority = input("Priorité : ")
            nouveau_ticket = Ticket(title, priority)
            current_user.createTicket(nouveau_ticket)
            print("Ticket créé avec succès.")

        elif choix == "2":
            ticket = choisir_dans_liste(current_user.viewAllTickets(), "ticket")
            if ticket is not None:
                ajouter_contenu_a_ticket(ticket)

        elif choix == "3":
            ticket = choisir_dans_liste(current_user.viewAllTickets(), "ticket")
            if ticket is not None:
                current_user.viewTicket(ticket)

        elif choix == "4":
            ticket = choisir_dans_liste(current_user.viewAllTickets(), "ticket")
            if ticket is not None:
                mettre_a_jour(current_user, ticket)

        elif choix == "5":
            ticket = choisir_dans_liste(current_user.viewAllTickets(), "ticket")
            if ticket is not None:
                commentaire = input("Commentaire : ")
                ticket.addComment(commentaire)
                print("Commentaire ajouté.")

        elif choix == "6":
            ticket = choisir_dans_liste(current_user.viewAllTickets(), "ticket")
            if ticket is not None:
                # on assigne a un membre de l'equipe donc a un developpeur
                print("À quel développeur assigner ce ticket ?")
                dev_cible = choisir_dans_liste(developers, "développeur")
                if dev_cible is not None:
                    current_user.assignTicket(ticket, dev_cible)

        elif choix == "7":
            ticket = choisir_dans_liste(current_user.viewAllTickets(), "ticket")
            if ticket is not None:
                if ticket.updateStatus("VALIDATION"):
                    print("Ticket mis en validation.")

        elif choix == "8":
            ticket = choisir_dans_liste(current_user.viewAllTickets(), "ticket")
            if ticket is not None:
                if ticket.updateStatus("TERMINE"):
                    print("Ticket terminé.")

        elif choix == "9":
            ticket = choisir_dans_liste(current_user.viewAllTickets(), "ticket")
            if ticket is not None:
                current_user.closeTicket(ticket)

        elif choix == "10":
            tickets = current_user.viewAllTickets()
            if len(tickets) == 0:
                print("Aucun ticket n'existe encore.")
            else:
                print("\n=== Tous les tickets ===")
                for t in tickets:
                    print(f"#{t.ticketID} - {t.title} - Statut: {t.status}")

        elif choix == "11":
            print(f"À bientôt, {current_user.name}.")
            break

        else:
            print("Choix invalide.")




def main():
    users = []
    developers = []

    while True:
        afficher_menu_connexion()
        choix = input("Ton choix : ")

        if choix == "1":
            current_user = connexion_utilisateur(users)
            if current_user is not None:
                menu_utilisateur(current_user)
        elif choix == "2":
            current_user = connexion_developpeur(developers)
            if current_user is not None:
                menu_developpeur(current_user, developers)
        elif choix == "3":
            print("Au revoir.")
            break
        else:
            print("Choix invalide.")


main()
