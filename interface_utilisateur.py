from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup


class RapportApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.rapport_actuel = "Rapport A"  # Rapport en cours de traitement
        self.date_actuelle = datetime.now()
        self.liste_dysfonctionnements = ["Synchronisation", "Refresh Sapristi", "Casse", "Aucune donnée"]

        self.add_widget(Label(text=f"Entrer la date du {self.rapport_actuel} (JJ/MM/AAAA) :"))
        self.date_input = TextInput(hint_text="JJ/MM/AAAA", multiline=False)
        self.add_widget(self.date_input)

        self.valider_button = Button(text="Valider la date")
        self.valider_button.bind(on_press=self.verifier_date)
        self.add_widget(self.valider_button)

        self.result_label = Label(text="")
        self.add_widget(self.result_label)

        self.spinner = Spinner(text="Sélectionnez une anomalie", values=self.liste_dysfonctionnements)
        self.spinner.disabled = True
        self.add_widget(self.spinner)

        self.transfert_button = Button(text="Transférer les données", disabled=True)
        self.transfert_button.bind(on_press=self.transferer_donnees)
        self.add_widget(self.transfert_button)

    def verifier_date(self, instance):
        d_rapport_str = self.date_input.text
        try:
            jour, mois, annee = map(int, d_rapport_str.split("/"))
            d_rapport = datetime(annee, mois, jour)
        except ValueError:
            self.afficher_popup("Format de date invalide ! Utilisez JJ/MM/AAAA.")
            return

        dif = ((d_rapport - self.date_actuelle).days + 1)

        if dif not in [0, -1] and not (dif == -3 or d_rapport.strftime("%A") == 'Friday'):
            self.result_label.text = f"Anomalie détectée ({dif} jours d'écart). Sélectionnez un problème."
            self.spinner.disabled = False
            self.transfert_button.disabled = False
        else:
            self.result_label.text = f"Statut {self.rapport_actuel} : RAS"
            self.transfert_button.disabled = False

    def transferer_donnees(self, instance):
        anomalie_selectionnee = self.spinner.text if self.spinner.text != "Sélectionnez une anomalie" else "RAS"
        self.afficher_popup(
            f"Données transférées avec succès !\nRapport: {self.rapport_actuel}\nAnomalie: {anomalie_selectionnee}")

    def afficher_popup(self, message):
        popup = Popup(title="Information",
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


class RapportAppMain(App):
    def build(self):
        return RapportApp()


if __name__ == "__main__":
    RapportAppMain().run()