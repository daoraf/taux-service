from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)


def gestion_anomalie():
    """Retourne une liste de dysfonctionnements sélectionnée par l'utilisateur."""
    Liste_dysfonctionnement = ["Synchronisation", "Refresh Sapristi", "Casse", "Aucune donnée"]
    return Liste_dysfonctionnement


def choix(texte_input):
    """Retourne la réponse de l'utilisateur 'y' ou 'n'."""
    return request.form.get('choix')


def upinfo(rap, d_rapport_str, d_actuelle):
    """Analyse la date du rapport par rapport à la date actuelle et détecte les anomalies."""
    try:
        jour, mois, annee = map(int, d_rapport_str.split("/"))
        d_rapport = datetime(annee, mois, jour)
    except ValueError:
        return None

    dif = ((d_rapport - d_actuelle).days + 1)
    info_dysfonctionnement = "RAS"

    if dif not in [0, -1]:
        if dif != -3 and d_rapport.strftime("%A") != 'Friday':
            # Anomalie détectée, rediriger l'utilisateur pour qu'il choisisse un dysfonctionnement
            return True  # Signale qu'une anomalie est détectée et qu'il faut choisir un dysfonctionnement
        else:
            info_dysfonctionnement = "RAS"
    else:
        info_dysfonctionnement = "RAS"

    return rap, d_rapport.strftime("%d/%m/%Y"), d_actuelle.strftime("%d/%m/%Y"), dif, info_dysfonctionnement


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        date_rapport_input = request.form['date_rapport']
        rapport = request.form['rapport']
        date_actuelle = datetime.now()

        info = upinfo(rapport, date_rapport_input, date_actuelle)

        if info is None:
            return "Erreur lors du traitement du rapport. Essayez à nouveau."

        if info is True:
            # Si une anomalie est détectée, rediriger vers la gestion des anomalies
            return redirect(url_for('gestion_anomalie', rapport=rapport, date_rapport=date_rapport_input))

        return render_template('resultat.html', info=info)

    return render_template('index.html')


@app.route('/gestion_anomalie', methods=['GET', 'POST'])
def gestion_anomalie():
    if request.method == 'POST':
        # Récupérer l'anomalie choisie par l'utilisateur
        anomalie = request.form.get('dysfonctionnement')
        rapport = request.args.get('rapport')
        date_rapport = request.args.get('date_rapport')

        if anomalie:
            # Si un dysfonctionnement est choisi, afficher un message de confirmation
            return render_template('confirmation.html', anomalie=anomalie, rapport=rapport, date_rapport=date_rapport)

    # Afficher le formulaire pour choisir une anomalie
    anomalies = gestion_anomalie()
    return render_template('gestion_anomalie.html', anomalies=anomalies)


@app.route('/confirmation', methods=['GET'])
def confirmation():
    anomalie = request.args.get('anomalie')
    rapport = request.args.get('rapport')
    date_rapport = request.args.get('date_rapport')
    return render_template('confirmation.html', anomalie=anomalie, rapport=rapport, date_rapport=date_rapport)


if __name__ == '__main__':
    app.run(debug=True)
