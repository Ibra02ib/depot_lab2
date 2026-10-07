# 6GEI311 - Lab 2 - Partie 1
# Programme principal : menu pour tester les classes User, Admin et Ticket

from ticket import Ticket
from user import User
from admin import Admin


def afficher_menu():
    print("\nGestionnaire de tickets UQAC")
    print("1. Créer un utilisateur")
    print("2. Créer un admin")
    print("3. Créer un ticket")
    print("4. Afficher un ticket")
    print("5. Mettre à jour un ticket")
    print("6. Ajouter un commentaire à un ticket")
    print("7. Assigner un ticket")
    print("8. Mettre un ticket en validation")
    print("9. Terminer un ticket")
    print("10. Fermer un ticket")   # seulement si le ticket est encore OUVERT
    print("11. Afficher tous les tickets")
    print("12. Quitter")


# fonction pour choisir un element dans une liste (user, admin, ticket...)
# retourne None si la liste est vide ou si le choix est mauvais
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

    index = int(choix) - 1   # -1 parce que la liste commence a 0
    if index < 0 or index >= len(liste):
        print("Numéro invalide.")
        return None

    return liste[index]


def main():
    users = []
    admins = []

    while True:
        afficher_menu()
        choix = input("Ton choix : ")

        if choix == "1":  # creer un user
            name = input("Nom : ")
            email = input("Email : ")
            role = input("Rôle : ")
            users.append(User(name, email, role))
            print("Utilisateur créé avec succès.")

        elif choix == "2":  # creer un admin
            name = input("Nom : ")
            email = input("Email : ")
            admins.append(Admin(name, email))
            print("Admin créé avec succès.")

        elif choix == "3":  # creer un ticket
            # on choisit le createur AVANT de creer le ticket,
            # sinon on se retrouvait avec un ticket sans createur
            print("Qui crée ce ticket ?")
            createur = choisir_dans_liste(users, "utilisateur")
            if createur is not None:
                title = input("Titre : ")
                description = input("Description : ")
                priority = input("Priorité : ")
                nouveau_ticket = Ticket(title, description, priority)
                createur.createTicket(nouveau_ticket)
                print("Ticket créé avec succès.")

        elif choix == "4":  # afficher un ticket
            ticket = choisir_dans_liste(Ticket.all_tickets, "ticket")
            if ticket is not None:
                print("Qui consulte ce ticket ?")
                user = choisir_dans_liste(users, "utilisateur")
                if user is not None:
                    user.viewTicket(ticket)

        elif choix == "5":  # mettre a jour un ticket
            ticket = choisir_dans_liste(Ticket.all_tickets, "ticket")
            if ticket is not None:
                print("Qui fait la mise à jour ?")
                user = choisir_dans_liste(users, "utilisateur")
                if user is not None:
                    nouveau_titre = input("Nouveau titre (vide = pas de changement) : ")
                    nouvelle_desc = input("Nouvelle description (vide = pas de changement) : ")
                    nouvelle_prio = input("Nouvelle priorité (vide = pas de changement) : ")
                    # si l'input est vide on envoie None pour pas ecraser la valeur
                    if nouveau_titre == "":
                        nouveau_titre = None
                    if nouvelle_desc == "":
                        nouvelle_desc = None
                    if nouvelle_prio == "":
                        nouvelle_prio = None
                    user.updateTicket(ticket, nouveau_titre, nouvelle_desc, nouvelle_prio)
                    print("Ticket mis à jour.")

        elif choix == "6":  # ajouter un commentaire
            ticket = choisir_dans_liste(Ticket.all_tickets, "ticket")
            if ticket is not None:
                commentaire = input("Commentaire : ")
                ticket.addComment(commentaire)
                print("Commentaire ajouté.")

        elif choix == "7":  # assigner un ticket
            ticket = choisir_dans_liste(Ticket.all_tickets, "ticket")
            if ticket is not None:
                admin = choisir_dans_liste(admins, "admin")
                if admin is not None:
                    print("À qui assigner ce ticket ?")
                    user = choisir_dans_liste(users, "utilisateur")
                    if user is not None:
                        admin.assignTicket(ticket, user)

        elif choix == "8":  # mettre en validation
            ticket = choisir_dans_liste(Ticket.all_tickets, "ticket")
            if ticket is not None:
                # updateStatus retourne False si c'est pas permis
                if ticket.updateStatus("VALIDATION"):
                    print("Ticket mis en validation.")

        elif choix == "9":  # terminer un ticket
            ticket = choisir_dans_liste(Ticket.all_tickets, "ticket")
            if ticket is not None:
                if ticket.updateStatus("TERMINE"):
                    print("Ticket terminé.")

        elif choix == "10":  # fermer un ticket
            ticket = choisir_dans_liste(Ticket.all_tickets, "ticket")
            if ticket is not None:
                admin = choisir_dans_liste(admins, "admin")
                if admin is not None:
                    admin.closeTicket(ticket)

        elif choix == "11":  # afficher tous les tickets
            admin = choisir_dans_liste(admins, "admin")
            if admin is not None:
                tickets = admin.viewAllTickets()
                if len(tickets) == 0:
                    print("Aucun ticket n'existe encore.")
                else:
                    print("\n=== Tous les tickets ===")
                    for t in tickets:
                        print(f"#{t.ticketID} - {t.title} - Statut: {t.status}")

        elif choix == "12":
            print("Au revoir.")
            break

        else:
            print("Choix invalide.")


main()
