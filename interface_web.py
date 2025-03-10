from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)


def choix(texte_input):
    choix_utilisateur = request.form.get('choix')
    if choix_utilisateur in ['y', 'n']:
        return choix_utilisateur
    return None


def gestion_anomalie():
    Liste_dysfonctionnement = ["Synchronisation", "Refresh Sapristi", "Casse", "Aucune donnée"]
    return Liste_dysfonctionnement


def upinfo(rap, d_rapport_str, d_actuelle):
    jour, mois, annee = d_rapport_str.split("/")
    d_rapport = datetime(int(annee), int(mois), int(jour))
    dif = (d_rapport - d_actuelle).days
    inf_dysfonctionnement = "RAS"
    text_choix = "L'anomalie est-elle vérifiée ?"

    if dif not in [0, -1]:
        if dif != -3 and d_rapport.strftime("%A") != 'Friday':
            print(f"--- Status {rap}: anomalie ({dif}j) ---")
            if choix(text_choix) == 'n':
                inf_dysfonctionnement = gestion_anomalie()
        else:
            print(f"Rapport Status {rap}: RAS")
    else:
        print(f"Rapport Status {rap}: RAS")

    return rap, d_rapport.strftime("%d/%m/%Y"), d_actuelle.strftime("%d/%m/%Y"), dif, inf_dysfonctionnement, 1, 0


@app.route('/', methods=['GET', 'POST'])
def index():
    info = None
    if request.method == 'POST':
        date_rapport_str = request.form['date_rapport']
        date_actuelle = datetime.now()

        Liste_de_rapport = ["Rapport A", "Rapport B"]
        for rapport in Liste_de_rapport:
            info = upinfo(rapport, date_rapport_str, date_actuelle)

        # Récupérer le choix de l'utilisateur pour transférer les données
        confirmation = request.form.get('confirmation')
        if confirmation == 'y':
            transfer_message = "Données transférées."
        else:
            transfer_message = "Transfert annulé."

        return render_template('index.html', info=info, transfer_message=transfer_message)

    return render_template('index.html', info=info)


if __name__ == '__main__':
    app.run(debug=True)
