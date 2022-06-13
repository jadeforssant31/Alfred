import pymysql
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.label import Label
from database import *
from database import proposition

# Step 1 : connexion à la base de donnée et Variable globale
    # Variable globale
nbr_excecution = 0
compt = 0

    # connexion a mysql
mypass = "Popsy123"
mydatabase = "base_d_alfred"

con = pymysql.connect(host="localhost", user="root", password=mypass, database=mydatabase)
cur = con.cursor()
con.commit()
    # initialisation de la bd
if(nbr_excecution == 0):
    initialisation()
    nbr_excecution +=1

# Step 2: Création des fenêtres différentes classes et methodes associées

    # fenêtre principale après connexion  Ma majeure/Resultat/Info Majeures/Paramètres
class MainWindow(Screen):
    pass

    # fenêtre des propositions Oui/Neutre/Non
class MajeureWindow(Screen):
    box = ObjectProperty()
    #proposition = StringProperty(proposition("proposition.txt").get_new_proposition()[0])
    proposition = StringProperty(allPropositions[0])

    def update_text(self, label_text):
        self.box.text = label_text

    def new_proposition(self):
        global compt
        compt += 1
        self.proposition = allPropositions[compt]
        if (compt == len(allPropositions)-1):
            compt = 0
            sm.current = "Accueil"
            result_dispo()

    # fenêtre Info Majeures
class InfoWindow(Screen):
   pass

    # La classe qui permet de gerer le passage d'une fenêtre à l'autre : les transitions
class WindowManager(ScreenManager):
    pass
    # fenêtre Paramètres appli
class ParametresWindow(Screen):
    pass

    # fenêtre resultat
class ResultWindow(Screen):
    pass

    # fenêtre login
class LoginWindow(Screen):
    intermediaire = ObjectProperty(None) # intermediaire est la variable qui nous permet d'utiliser le user_name collecté sur la fênetre create account et stocké dans la bd
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            self.intermediaire.text = "Bonjour " + db.give_user_name(self.email.text) + ", \nRépond aux affirmations et obtient le resultat dans la section RESULTAT"
            self.reset()
            sm.current = "Accueil"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
# fenêtre de creation de compte
class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""
# fonction appelé en cas d'erreur de replissage des champs de saisie
def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid email or password.'),
                  size_hint=(.7, .7), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(.7, .7), size=(400, 400))

    pop.open()

def result_dispo():
    pop = Popup(title='Bravo!',
                  content=Label(text='Success! \n Les resultats de votre dernier test\n sont disponible dans la section Resultat'),
                  size_hint=(.8, .7), size=(400, 400))

    pop.open()


# liaison avec le fichier kv
kv = Builder.load_file("Alfred.kv")
db=DataBase("users.txt")

# A sm on affecte une instance de windowManager classe qui nous permet de gérer le passage d'une fenêtre à l'autre
sm = WindowManager()

# On ajoute toutes les fenêtres devant être ajoutées
screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="Accueil"),MajeureWindow(name="Majeure"),ParametresWindow(name="param"),ResultWindow(name="result"),InfoWindow(name="Info")]
for screen in screens:
    sm.add_widget(screen)

# On definit la première fenêtre qui va s'afficher
sm.current = "create"

# on definit le constructeur de l'appli
class AlfredApp(App):
    def build(self):
        return sm

# On run l'appli
if __name__ == "__main__":
    Window.size = (397, 550)
    #Window.clearcolor = (1,1,1,1)
    AlfredApp().run()

