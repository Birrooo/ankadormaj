import customtkinter
from PIL import Image, ImageTk
import requests
import hashlib
import subprocess  # Importer subprocess pour exécuter des scripts Python
import os
import signal

# Configuration de l'interface
customtkinter.set_appearance_mode("dark")
root = customtkinter.CTk()
root.geometry("500x350")
root.title("Treasure 3.0")

# Obtenez le chemin absolu de l'icône
icon_path = os.path.abspath("app/ankago.ico")

# Appliquez l'icône au format .ico
root.iconbitmap(icon_path)

# Authentification avec KeyAuth
class KeyAuth:
    def __init__(self, name, ownerid, version, hash_to_check):
        self.name = name
        self.ownerid = ownerid
        self.version = version
        self.hash_to_check = hash_to_check
        self.api_url = "https://keyauth.win/api/1.1/"
        self.sessionid = None

    def init(self):
        data = {
            "type": "init",
            "name": self.name,
            "ownerid": self.ownerid,
            "version": self.version,
            "hash": self.hash_to_check
        }
        response = requests.post(self.api_url, data=data)
        result = response.json()
        
        if result['success']:
            print("[+] Session initialisée !")
            self.sessionid = result['sessionid']
        else:
            print(f"[-] Erreur : {result['message']}")

    def login(self, username, password):
        if not self.sessionid:
            print("[-] Erreur : Session non initialisée.")
            return False
        
        data = {
            "type": "login",
            "username": username,
            "pass": password,
            "name": self.name,
            "ownerid": self.ownerid,
            "version": self.version,
            "hash": self.hash_to_check,
            "sessionid": self.sessionid
        }
        response = requests.post(self.api_url, data=data)
        result = response.json()
        
        if result['success']:
            print("[+] Connexion réussie !")
            print(f"Message : {result['message']}")
            return True
        else:
            print(f"[-] Erreur : {result['message']}")
            return False

# Initialisation KeyAuth
keyauthapp = KeyAuth(
    name="Dokkanuro's Application",
    ownerid="EkOJr2Ucqo",
    version="1.0",
    hash_to_check=hashlib.md5(__file__.encode()).hexdigest()
)

keyauthapp.init()

# Fonction de login
def login():
    username = entry1.get()
    password = entry2.get()
    if keyauthapp.login(username, password):
        label_status.configure(text="Login réussi !", text_color="green")
        root.destroy()  # Ferme la fenêtre principale d'authentification
        open_new_window()  # Ouvre la nouvelle fenêtre après fermeture de la fenêtre principale
    else:
        label_status.configure(text="Login échoué.", text_color="red")

# Nouvelle fenêtre après login réussi
def open_new_window():
    # Crée une nouvelle fenêtre avec un fond noir
    new_window = customtkinter.CTk()
    new_window.geometry("297x225")  # Ajuste la taille de la fenêtre si nécessaire
    new_window.title("TREASURE BETA")
    
    # Définir l'icône de la nouvelle fenêtre
    new_window.iconbitmap("app/ankago.ico")  # Ajout de l'icône

    # Définir le fond de la fenêtre en noir
    new_window.configure(fg_color="#000000")  # Couleur de fond noire

    # Logo de l'application (ankador.png)
    logo_pil_image = Image.open("app/ankador.png")  # Utilisation de ankador.png comme logo dans la fenêtre
    logo_resized_image = logo_pil_image.resize((80, 80))  # Redimensionner le logo (ajuste selon besoin)
    logo_tk_image = ImageTk.PhotoImage(logo_resized_image)

    # Crée un Label pour afficher le logo et garder la référence à l'image
    logo_label = customtkinter.CTkLabel(new_window, image=logo_tk_image, text="", fg_color="#000000")  # Fond noir pour le label aussi
    logo_label.pack(pady=20)

    # Variable pour suivre l'état du bouton (START ou STOP)
    is_running = False
    process = None  # Variable pour stocker le processus lancé

    # Fonction pour gérer le changement de texte du bouton
    def toggle_button():
        nonlocal is_running, process  # Permet de modifier la variable is_running et process
        if is_running:
            button_start.configure(text="START", command=toggle_button)  # Change en START
            if process:
                print("Arrêt de l'application.")
                process.terminate()  # Arrêter le processus
                process = None
        else:
            button_start.configure(text="STOP", command=toggle_button)  # Change en STOP
            print("Lancement de l'application.")
            process = subprocess.Popen(["python", "testwb.py"])  # Lance le script testwb.py
        is_running = not is_running  # Inverse l'état de is_running

    # Crée un bouton "START" avec texte blanc
    button_start = customtkinter.CTkButton(new_window, text="START", command=toggle_button, text_color="#ffffff", fg_color="#444444")
    button_start.pack(pady=30)

    # Fonction pour gérer le raccourci clavier F10 pour arrêter le processus
    def on_f10(event):
        nonlocal is_running, process
        if is_running:
            button_start.configure(text="START", command=toggle_button)  # Change en START
            if process:
                print("Arrêt de l'application (via F10).")
                process.terminate()  # Arrêter le processus
                process = None
            is_running = False  # Mettre à jour l'état du bouton
        else:
            print("Rien à arrêter, l'application n'est pas en cours d'exécution.")

    # Lier la touche F10 à la fonction on_f10
    new_window.bind("<F10>", on_f10)

    # Lance la boucle principale pour la nouvelle fenêtre
    new_window.mainloop()


# Interface graphique
frame = customtkinter.CTkFrame(master=root, fg_color="#000000")
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Logo de l'application dans la fenêtre de login (ankador.png)
logo_pil_image = Image.open("app/ankador.png")  # Utilisation de ankador.png comme logo dans la fenêtre de login
logo_resized_image = logo_pil_image.resize((80, 80))
logo_tk_image = ImageTk.PhotoImage(logo_resized_image)

# Garder la référence à l'image pour éviter qu'elle ne soit supprimée
logo_label = customtkinter.CTkLabel(master=frame, image=logo_tk_image, text="")
logo_label.image = logo_tk_image  # Assurez-vous de garder une référence à l'image
logo_label.pack(pady=10)

# Titre
label = customtkinter.CTkLabel(master=frame, text="Treasure by Lapsu$", font=("Roboto", 24), text_color="#ffffff")
label.pack(pady=12, padx=10)

# Champs de saisie
entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username", text_color="#ffffff", fg_color="#333333")
entry1.pack(pady=12, padx=10)

# Donne le focus au champ username pour qu'il soit prêt à l'utilisation
entry1.focus_set()  # Cette ligne permet d'activer le champ Username dès l'ouverture de l'application

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*", text_color="#ffffff", fg_color="#333333")
entry2.pack(pady=12, padx=10)

# Bouton Login
button = customtkinter.CTkButton(master=frame, text="Login", command=login, text_color="#ffffff", fg_color="#444444")
button.pack(pady=12, padx=10)

# Label de statut
label_status = customtkinter.CTkLabel(master=frame, text="", font=("Roboto", 14), text_color="#ffffff")
label_status.pack(pady=12, padx=10)

root.mainloop()
