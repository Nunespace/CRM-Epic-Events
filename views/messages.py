class Messages:
    def messages_ok(self, table, message_number):
        if message_number == 1:
            if table == "client":
                print("Le client a bien été enregistré.")
            elif table == "event":
                print("L'évènement a bien été enregistré.")
            elif table == "contract":
                print("Le contrat a bien été enregistré.")
            elif table == "staff":
                print("Le collaborateur a bien été enregistré.")

        if message_number == 2:
            if table == "client":
                print("Le client a bien été modifié.")
            elif table == "event":
                print("L'évènement a bien été modifié.")
            elif table == "contract":
                print("Le contrat a bien été modifié.")
            elif table == "staff":
                print("Le collaborateur a bien été modifié.")

    def message_error(self, table, message_number):
        if message_number == 1:
            print("Email ou mot de passe invalide")
        elif message_number == 2:
            print(
                "Veuillez fermer l'application et vous authentifier de nouveau avec la commande : "
                "'pipenv run python main.py'"
            )
        elif message_number == 3:
            print(
                "Une erreur s'est produite : id ou nom inconnu. Veuillez recommencer."
            )

        elif message_number == 4:
            if table == "client":
                print("Ce client est inconnu.")
            if table == "event":
                print("Cet évènement est inconnu.")
            if table == "contract":
                print("Ce contrat est inexistant.")
            if table == "staff":
                print("Ce collaborateur est inconnu.")

        elif message_number == 5:
            print("Vous n'êtes pas autorisé(e) à effectuer cette action.")
