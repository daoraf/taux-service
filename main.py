from datetime import datetime


def gestion_anomalie():
    """Affiche une liste de dysfonctionnements et demande à l'utilisateur de sélectionner une option."""
    Liste_dysfonctionnement = ["Synchronisation", "Refresh Sapristi", "Casse", "Aucune donnée"]
    print("\n--- Liste des dysfonctionnements ---")
    for i, dysfonctionnement in enumerate(Liste_dysfonctionnement, start=1):
        print(f"{i}: {dysfonctionnement}")

    while True:
        try:
            choix_utilisateur = int(input(f"Sélectionnez le dysfonctionnement (1-{len( Liste_dysfonctionnement)}) : "))
            if 1 <= choix_utilisateur <= len(Liste_dysfonctionnement):
                return Liste_dysfonctionnement[choix_utilisateur - 1]
            else:
                print("Veuillez entrer un nombre valide entre 1 et 4.")
        except ValueError:
            print("Entrée invalide, veuillez entrer un chiffre.")


def choix(texte_input):
    """Demande à l'utilisateur un choix 'y' ou 'n' et s'assure que l'entrée est valide."""
    while True:
        reponse = input(f"{texte_input}\nSi oui, tapez 'y', sinon 'n' : ").strip().lower()
        if reponse in ['y', 'n']:
            return reponse
        print("Réponse invalide ! Veuillez entrer 'y' ou 'n'.")


def upinfo(rap, d_rapport_str, d_actuelle):
    """Analyse la date du rapport par rapport à la date actuelle et détecte les anomalies."""
    try:
        jour, mois, annee = map(int, d_rapport_str.split("/"))
        d_rapport = datetime(annee, mois, jour)
    except ValueError:
        print("Format de date invalide. Utilisez le format JJ/MM/AAAA.")
        return None

    dif = ((d_rapport - d_actuelle).days + 1)
    info_dysfonctionnement = "RAS"
    ok = 1
    nok = 0
    texte_choix = "L'anomalie est-elle vérifiée ?"

    if dif not in [0, -1]:
        if dif != -3 and d_rapport.strftime("%A") != 'Friday':
            print(f"\n--- Statut {rap} : anomalie détectée ({dif} jours d'écart) ---")
            if choix(texte_choix) == 'n':
                info_dysfonctionnement = gestion_anomalie()
                ok = 0
                nok = 1
        else:
            print(f"\nStatus {rap} : {info_dysfonctionnement}")
    else:
        print(f"\nStatus {rap} : R{info_dysfonctionnement}")

    return rap, d_rapport.strftime("%d/%m/%Y"), d_actuelle.strftime("%d/%m/%Y"), dif, info_dysfonctionnement, ok, nok


# Liste des rapports
Liste_de_rapport = ["Rapport A", "Rapport B"]
date_actuelle = datetime.now()
texte_confirmation_update_data = "Transférer les données ?"

for rapport in Liste_de_rapport:
    date_rapport_input = input(f"\nVeuillez saisir la date mentionnée sur le rapport {rapport} (JJ/MM/AAAA) : ")

    info = upinfo(rapport, date_rapport_input, date_actuelle)
    if info is None:
        print("Erreur lors du traitement du rapport. Passage au suivant...\n")
        continue  # Passe au rapport suivant en cas d'erreur de date

    print("\nDonnées récupérées :", *info)

    if choix(texte_confirmation_update_data) == "y":
        print("Données transférées avec succès.")
    else:
        print("Transfert annulé.")

    print("\n" + "*" * 50)
