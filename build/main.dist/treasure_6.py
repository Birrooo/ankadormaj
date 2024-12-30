import pytesseract
from PIL import ImageGrab, Image, ImageOps, ImageEnhance, ImageFilter
import time
import ctypes
import re
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import win32gui
import win32con
import os
import pyperclip
import cv2
import numpy as np
import random
from difflib import SequenceMatcher  # Pour la distance de Levenshtein simplifiée
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Controller, Key
import subprocess
import sys

# Chemin vers Tesseract (modifiez si nécessaire)
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'

keyboard = Controller()

DATABASE = [
    "Affiche de carte au trésor",
        "Aiguille à coudre",
        "Ancre dorée",
        "Anneau d'or",
        "Arbre à épines",
        "Arbre à moitié coupé",
        "Arbre à trous",
        "Arbre ensanglanté",
        "Arbre glacé",
        "Arche naturelle",
        "Balançoire macabre",
        "Ballons en forme de coeur",
        "Bannière bontarienne déchirée",
        "Bannière brâkmarienne déchirée",
        "Barque coulée",
        "Blé noir et blanc",
        "Bombe coeur",
        "Bonbon bleu",
        "Bougie dans un trou",
        "Boule dorée de marin",
        "Bouton de couture",
        "Buisson poupée sadida",
        "Cadran solaire",
        "Cairn",
        "Canard en plastique",
        "Canne à kebab",
        "Carapace de tortue",
        "Casque à cornes",
        "Ceinture cloutée",
        "Champignon rayé",
        "Chapeau dé",
        "Chaussette à pois",
        "Clef dorée",
        "Coquillage à pois",
        "Corne de likrone",
        "Crâ cramé",
        "Crâne dans un trou",
        "Crâne de Crâ",
        "Crâne de cristal",
        "Crâne de likrone",
        "Crâne de likrone dans la glace",
        "Crâne de renne",
        "Crâne de Roublard",
        "Croix en pierre brisée",
        "Dé en glace",
        "Dessin au pipi dans la neige",
        "Dessin de croix dans un cercle",
        "Dessin dragodinde",
        "Dessin koalak",
        "Dofus en bois",
        "Dolmen",
        "Échelle cassée",
        "Éolienne à quatre pales",
        "Épouvantail à pipe",
        "Étoile en papier plié",
        "Étoile jaune peinte",
        "Fer à cheval",
        "Filon de cristaux multicolores",
        "Flèche dans une pomme",
        "Fleur de nénuphar bleue",
        "Fleurs smiley",
        "Framboisier",
        "Girouette dragodinde",
        "Grand coquillage cassé",
        "Gravure d'aile",
        "Gravure d'arakne",
        "Gravure d'épée",
        "Gravure d'étoile",
        "Gravure d'œil",
        "Gravure de bouftou",
        "Gravure de boule de poche",
        "Gravure de chacha",
        "Gravure de clef",
        "Gravure de coeur",
        "Gravure de crâne",
        "Gravure de croix",
        "Gravure de Dofus",
        "Gravure de dragodinde",
        "Gravure de fantôme",
        "Gravure de Firefoux",
        "Gravure de flèche",
        "Gravure de fleur",
        "Gravure de Gelax",
        "Gravure de Kama",
        "Gravure de logo Ankama",
        "Gravure de lune",
        "Gravure de papatte",
        "Gravure de rose des vents",
        "Gravure de soleil",
        "Gravure de spirale",
        "Gravure de symbole de quête",
        "Gravure de symbole égal",
        "Gravure de tofu",
        "Gravure de wabbit",
        "Gravure de wukin",
        "Grelot",
        "Hache brisée",
        "Kaliptus à fleurs jaunes",
        "Kaliptus coupé",
        "Kaliptus grignoté",
        "Kama peint",
        "Lampion bleu",
        "Langue dans un trou",
        "Lanterne au crâne luminescent",
        "Logo Ankama peint",
        "Marionnette",
        "Menottes",
        "Minouki",
        "Moufles jaunes",
        "Moufles rouges",
        "Niche dans une caisse",
        "Oeil de shushu peint",
        "Oeuf dans un trou",
        "Ornement flocon",
        "Os dans la lave",
        "Paire de lunettes",
        "Palmier à feuilles carrées",
        "Palmier à feuilles déchirées",
        "Palmier à pois",
        "Palmier peint à rayures",
        "Palmier peint d'un chacha",
        "Palmier surchargé de noix de coco",
        "Panneau nonosse",
        "Peinture de Dofus",
        "Peluche de likrone",
        "Phorreur",
        "Phorreur",
        "Phorreur",
        "Phorreur",
        "Pioche plantée",
        "Poisson grillé embroché",
        "Poupée koalak",
        "Queue d'Osamodas",
        "Rocher à sédimentation verticale",
        "Rocher crâne",
        "Rocher dé",
        "Rocher Dofus",
        "Rocher percé",
        "Rocher taillé en arètes de poisson",
        "Rose des vents dorée",
        "Rose noire",
        "Ruban bleu noué",
        "Rune nimbos",
        "Sapin couché",
        "Serrure dorée",
        "Sève qui s'écoule",
        "Slip à petit coeur",
        "Soupe de bananagrumes",
        "Squelette d'Ouginak pendu",
        "Statue koalak",
        "Statue sidoa",
        "Statue wabbit",
        "Stèle chacha",
        "Sucre d'orge",
        "Symbole de quête peint",
        "Talisman en papier",
        "Tambour à rayures",
        "Tambour papatte",
        "Théière à rayures",
        "Tissu à carreaux noué",
        "Tombe gravée d'un bouclier",
        "Tombe inondée",
        "Tombe inondée de sang",
        "Torii cassé",
        "Trace de main en sang",
        "Tricycle",
        "Tube rempli de tofus"
]

def detecter_image_et_lancer_script():
    # Spécifie la zone à capturer : (left, top, width, height)
    zone = (2, 303, 209, 134)

    # Capture l'écran dans la zone spécifiée
    screenshot = pyautogui.screenshot(region=zone)

    # Convertir l'image en format numpy array pour OpenCV
    image = np.array(screenshot)

    # Convertir de RGB à BGR (car OpenCV utilise BGR)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Charger l'image de référence des points d'interrogation
    template = cv2.imread('refereindice.png', cv2.IMREAD_GRAYSCALE)

    # Convertir l'image capturée en niveaux de gris
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer le template matching
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)

    # Définir un seuil pour détecter la correspondance
    threshold = 0.8  # Ajuste ce seuil selon le cas

    # Trouver les positions où il y a une correspondance
    locations = np.where(result >= threshold)

    # Nombre de correspondances trouvées
    num_matches = len(locations[0])
    print(f"Nombre de correspondances détectées : {num_matches}")

    # Afficher les correspondances sur l'image
    for pt in zip(*locations[::-1]):
        cv2.rectangle(image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

    # Afficher l'image avec les rectangles dessinés autour des correspondances
    # Remplacer cv2.imshow par PIL Image.show
    # image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # image_pil.show()

    # Définir les coordonnées de la zone à capturer
    capture_box = (184, 279, 272, 344)
    # Logique pour lancer les scripts en fonction du nombre de correspondances
    if num_matches == 5:
        print("5 correspondances détectées, lancement de big6_treasure...")
        subprocess.run(["python", "treasure_6.py"])  # Remplace par ton script exact
    elif num_matches == 4:
        print("4 correspondances détectées, lancement de big5_treasure...")
        subprocess.run(["python", "treasure_5.py"])  # Remplace par ton script exact
    elif num_matches == 3:
        print("3 correspondances détectées, lancement de big4_treasure...")
        subprocess.run(["python", "treasure_4.py"])  # Remplace par ton script exact
    elif num_matches == 2:
        print("2 correspondances détectées, lancement de 3big_treasure...")
        subprocess.run(["python", "treasure_3.py"])  # Remplace par ton script exact
    elif num_matches == 1:
        print("1 correspondances détectées, lancement de big2_treasure...")
        subprocess.run(["python", "treasure_2.py"])  # Remplace par ton script exact
    else:
        print(f"Aucune action pour {num_matches} correspondances.")

        # Capture la zone spécifiée de l'écran
        screenshot = ImageGrab.grab(bbox=capture_box)
        
        # Recherche de l'image de référence dans la capture
        reference_image = "img/combat.png"
        print("Recherche de l'image de référence combat.png...")
        
        try:
            # Recherche de l'image dans la capture de l'écran
            location = pyautogui.locateOnScreen(reference_image)
            
            if location:
                print("Image de référence trouvée, lancement du script combat.py...")
                subprocess.run(["python", "combat.py"])  # Remplace par ton script exact
            else:
                print("Image de référence non trouvée, lancement du script treasure_1.py...")
                subprocess.run(["python", "treasure_1.py"])  # Remplace par ton script exact
        except Exception as e:
            print(f"Erreur lors de la recherche de l'image de référence : {e}")


# Fonction pour calculer la similarité (distance de Levenshtein)
def levenshtein_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Trouver le texte le plus proche dans la BDD
def find_closest_match(extracted_text, database):
    best_match = None
    highest_similarity = 0
    for entry in database:
        similarity = levenshtein_similarity(extracted_text, entry)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = entry
    return best_match, highest_similarity

# Fonction de pré-traitement de l'image (conversion en noir et blanc)
def preprocess_image(image):
    grayscale_image = image.convert("L")
    threshold = 128
    binarized_image = grayscale_image.point(lambda p: p > threshold and 255)
    return binarized_image

def clean_extracted_text(pos_text):
    # Remplacer les virgules suivies ou non d'espaces par un espace unique et normaliser les espaces
    pos_text = re.sub(r',\s*', ' ', pos_text)  # Remplace les virgules et espaces par un seul espace
    pos_text = re.sub(r'\.\s*$', '', pos_text).strip()  # Supprime les points finaux inutiles et espaces en fin de texte
    
    # Supprimer le signe - ou + seulement s'il suit immédiatement un chiffre et qu'il est à la fin du nombre (ex: 10- devient 10)
    pos_text = re.sub(r'(\d)([-+])$', r'\1', pos_text)  # Supprime le signe si un chiffre est suivi de - ou + à la fin du nombre
    pos_text = re.sub(r'(\d)([-+])(\d)', r'\1 \3', pos_text)  # Supprime le signe entre deux chiffres (ex: 0-1 devient 0 1)
    
    # Remplacer les multiples espaces par un seul espace
    pos_text = re.sub(r'\s+', ' ', pos_text)
    
    return pos_text

# Capture une zone de l'écran
def capture_zone(left, top, right, bottom):
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    if left < 0 or top < 0 or right > screen_width or bottom > screen_height:
        print("Erreur : La zone dépasse les limites de l'écran.")
        return None
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    return screenshot

def click(x, y):
    """Simule un clic à la position spécifiée"""
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_ABSOLUTE = 0x8000
    
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    
    normalized_x = int(x * 65535 / screen_width)
    normalized_y = int(y * 65535 / screen_height)
    
    ctypes.windll.user32.mouse_event(
        MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
        normalized_x,
        normalized_y,
        0,
        0
    )
    
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# Extraire le texte d'une image pour l'indice 1
def get_text_from_image(image):
    image = preprocess_image(image)
    text = pytesseract.image_to_string(image, lang='fra')
    return text.strip()

def get_text_from_image2(image):
    image = preprocess_image(image)
    text = pytesseract.image_to_string(image, lang='eng')
    return text.strip()

# Automatiser la saisie des coordonnées dans le navigateur
def manipulate_coordinates(extracted_text):
    global driver
    options = Options()
    
    # Ajouter des arguments pour éviter les erreurs de crash
    options.add_argument('--no-sandbox')  # Désactive le sandboxing
    options.add_argument('--ignore-certificate-errors')  # Ignore les erreurs de certificat
    options.add_argument('--disable-dev-shm-usage')  # Utilise un répertoire temporaire pour éviter les problèmes de mémoire partagée
    
    # Maximiser la fenêtre du navigateur
    options.add_argument('--start-maximized')
    
    # Utiliser le profil utilisateur de Brave
    options.add_argument('user-data-dir=C:\\Users\\ElMeroo\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default')
    
    # Spécifier l'emplacement de Brave (le chemin de l'exécutable)
    options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    
    # **Changer l'empreinte du navigateur** : Modifier l'user-agent pour simuler un autre navigateur
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # **Masquer les propriétés WebDriver** pour éviter la détection
    options.add_argument("--disable-blink-features=AutomationControlled")  # Masque l'indicateur WebDriver
    
    # **Utilisation d'un proxy pour changer l'adresse IP (si nécessaire)** 
    # options.add_argument('--proxy-server=http://your_proxy:port')
    
    # Initialiser le navigateur Brave avec ChromeDriver
    driver = webdriver.Chrome(options=options)
    driver.switch_to.window(driver.current_window_handle)
    
    # Mettre la fenêtre du navigateur au premier plan
    hwnd = win32gui.GetForegroundWindow()  # Récupérer la fenêtre active
    win32gui.SetForegroundWindow(hwnd)
    
    wait = WebDriverWait(driver, 10)
    try:
        # Ouvrir la page URL
        driver.get('https://dofusdb.fr/fr/tools/treasure-hunt')
        time.sleep(2)  # Attendre que la page se charge
        
        # Trouver les champs d'input de type "number"
        numberInputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="number"]')
        
        # Vérifier qu'il y a bien 2 champs
        if len(numberInputs) != 2:
            print(f"Attention: {len(numberInputs)} inputs trouvés au lieu de 2")
            return
        
        # Sélectionner les champs X et Y
        coordX, coordY = numberInputs[0], numberInputs[1]
        
        print(f"Texte extrait pour les coordonnées : {extracted_text}")
        
        # Extraire les coordonnées du texte
        coords = re.findall(r'\[(-?\d+),(-?\d+)\]', extracted_text)
        
        if len(coords) == 1:
            coord_x_value, coord_y_value = coords[0]
            
            # Mettre à jour les valeurs des champs
            coordX.clear()
            coordY.clear()
            coordX.send_keys(coord_x_value)
            coordY.send_keys(coord_y_value)
            print(f"Coordonnées mises à jour : X={coord_x_value}, Y={coord_y_value}")
        else:
            print("Erreur : Le texte extrait n'a pas le format attendu.")
    
    except Exception as e:
        print(f"Erreur pendant l'automatisation : {e}")
    
    finally:
        # Réduire la fenêtre du navigateur sans la fermer
        hwnd = win32gui.FindWindow(None, driver.title)
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        print("Fenêtre du navigateur réduite.")

# Fonction pour fermer le navigateur
def close_browser():
    global driver
    try:
        if driver:
            driver.quit()  # Ferme le navigateur et l'instance du WebDriver
            print("Navigateur fermé.")
    except Exception as e:
        print(f"Erreur lors de la fermeture du navigateur : {e}")

# Comparer deux images pour trouver une correspondance
def compare_images(image1, image2):
    image1_cv, image2_cv = np.array(image1), np.array(image2)
    image1_gray = cv2.cvtColor(image1_cv, cv2.COLOR_RGB2GRAY)
    image2_gray = cv2.cvtColor(image2_cv, cv2.COLOR_RGB2GRAY)
    similarity = cv2.matchTemplate(image1_gray, image2_gray, cv2.TM_CCOEFF_NORMED)
    return similarity.max()

# Rechercher une image correspondante dans un dossier
def find_matching_image(captured_image, folder_path="arrows"):
    best_match, highest_similarity = None, 0
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg')):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            similarity = compare_images(captured_image, image)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = filename
    return best_match, highest_similarity

# Action delay (ajouté pour simuler un retard humain)
def human_delay():
    time.sleep(random.uniform(0.5, 1.5))

# Fonction pour appuyer sur la flèche correspondante pendant 1 seconde
def press_arrow(direction):
    # Identifier les flèches sur la page
    arrows = driver.find_elements(By.CSS_SELECTOR, 'i.fa')

    arrowUp = arrows[0]
    arrowRight = arrows[1]
    arrowLeft = arrows[2]
    arrowDown = arrows[3]

    human_delay()

    action = ActionChains(driver)

    # Déterminer la flèche à appuyer en fonction de la direction
    if direction == 'up':
        action.move_to_element(arrowUp).click().perform()
        print("Flèche Haut appuyée.")
        time.sleep(1)  # Appuyer pendant 1 seconde
    elif direction == 'right':
        action.move_to_element(arrowRight).click().perform()
        print("Flèche Droite appuyée.")
        time.sleep(1)  # Appuyer pendant 1 seconde
    elif direction == 'left':
        action.move_to_element(arrowLeft).click().perform()
        print("Flèche Gauche appuyée.")
        time.sleep(1)  # Appuyer pendant 1 seconde
    elif direction == 'down':
        action.move_to_element(arrowDown).click().perform()
        print("Flèche Bas appuyée.")
        time.sleep(1)  # Appuyer pendant 1 seconde
    else:
        print("Direction inconnue.")

# Mettre au premier plan la fenêtre Dofus
def find_dofus_window():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Release" in title:
                windows.append(hwnd)
    windows = []
    win32gui.EnumWindows(callback, windows)
    if not windows:
        raise Exception("Fenêtre Dofus non trouvée")
    hwnd = windows[0]
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    return hwnd

# Mettre au premier plan la fenêtre Dofus
def find_browser_window():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Chasse" in title:
                windows.append(hwnd)
    windows = []
    win32gui.EnumWindows(callback, windows)
    if not windows:
        raise Exception("Fenêtre de Chasse au trésor non trouvée")
    hwnd = windows[0]
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    return hwnd

# Programme principal
def main():
    print("Démarrage du script.")
    time.sleep(2)

    # Capture de la première zone pour extraire les coordonnées
    first_zone_bbox = (30, 207, 208, 249)
    print(f"Capture de la première zone : {first_zone_bbox}")
    image = capture_zone(*first_zone_bbox)
    if not image:
        print("Erreur de capture de la première zone.")
        return
    # Extraction du texte
    text = get_text_from_image2(image).replace('i', '1').replace('I', '1')
    print(f"Texte extrait : {text}")


#########################################################################################################################
#                                                           INDICE 1                                                    #
#########################################################################################################################
    # Capture de la flèche indice 1
    fl1_zone_bbox = (13, 274, 34, 307)  # Remplacé etp2fl1_zone_bbox par fl1_zone_bbox
    print(f"Capture de la direction du premier indice : {fl1_zone_bbox}")
    fl1_image = capture_zone(*fl1_zone_bbox)  # Utilisation de fl1_zone_bbox
    file_name = f"indice_1.png"
    fl1_image.save(file_name)
    if not fl1_image:
        print("Erreur de capture de la direction du premier indice.")
        return

    # Log pour la flèche indice 1
    print("Log de flèche indice 1 extraite :")
    print(get_text_from_image(fl1_image))  # Affiche le texte extrait de la deuxième zone

    # Comparaison des images capturées pour la flèche indice 1
    best_match, similarity = find_matching_image(fl1_image)  # Utilisation de fl1_image
    if best_match:
        print(f"Meilleure correspondance trouvée : {best_match} ({similarity:.2f})")
    else:
        print("Aucune correspondance trouvée.")

    # Déterminer la direction à partir de la flèche capturée sur le premier indice
    direction = None
    if "arrow_up" in best_match:
        direction = 'up'
    elif "arrow_right" in best_match:
        direction = 'right'
    elif "arrow_left" in best_match:
        direction = 'left'
    elif "arrow_down" in best_match:
        direction = 'down'

    # Capture du premier indice
    in1_zone_bbox = (33, 276, 188, 305) # Remplacé etp2in1_zone_bbox par in1_zone_bbox
    print(f"Capture du premier indice : {in1_zone_bbox}")
    in1_image = capture_zone(*in1_zone_bbox)  # Utilisation de in1_zone_bbox
    file_name = f"vindice_1.png"
    in1_image.save(file_name)
    if not in1_image:
        print("Erreur de capture du premier indice.")
        return

    # Extraire et loguer le texte du premier indice
    extracted_text = get_text_from_image(in1_image)  # Utilisation de in1_image
    print(f"Direction de la flèche : {extracted_text}")

    # Comparer le texte extrait avec la base de données
    closest_match, similarity = find_closest_match(extracted_text, DATABASE)
    if closest_match:
        print(f"Texte le plus proche trouvé : {closest_match} (similarité : {similarity:.2f})")
    else:
        print("Aucun texte correspondant trouvé dans la base de données.")

    if direction:
        # Ouvrir le navigateur et manipuler les coordonnées
        manipulate_coordinates(text)

        # Appuyer sur la flèche correspondant à la direction trouvée
        press_arrow(direction)
        time.sleep(0.5)

        # Trouver le champ de recherche et taper le texte trouvé
        try:
            search_field = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
            search_field.clear()
            search_field.send_keys(closest_match)
            print(f"Texte le plus proche entré dans la barre de recherche : {closest_match}")
            
            # Appuyer sur la touche Flèche Bas et Entrée
            time.sleep(1)  # Attendre pour simuler un délai humain
            search_field.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            click(889, 700)
            time.sleep(1)
            print("Flèche Bas et Entrée appuyées dans le champ de recherche.")
        except Exception as e:
            print(f"Erreur lors de la saisie dans le champ de recherche : {e}")
        
        # Vérification de l'apparition de phorreur.png après le clic
        # Capture de la zone pour détecter phorreur.png
        phorreur_image = capture_zone(656, 682, 1027, 788)
        phorreur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'phorreur.png')

        # Trouver la meilleure correspondance
        best_match_phorreur, similarity = find_matching_image(phorreur_image, folder_path=os.path.dirname(phorreur_path))

        # Ajouter un log détaillé de similarité
        print(f"Similarité calculée : {similarity:.2f}")

        # Vérifier si la correspondance est assez bonne
        if best_match_phorreur and similarity > 0.9:  # Seuil augmenté
            print(f"Meilleure correspondance trouvée : {best_match_phorreur} ({similarity:.2f})")
            print("Image phorreur.png détectée. Abandon de la chasse pour en lancer une nouvelle...")
            find_dofus_window()
            print("Fenêtre Dofus mise au premier plan.")
            time.sleep(0.5)
            click(276, 172)
            time.sleep(0.5)
            click(372, 413)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            time.sleep(0.5)
            subprocess.Popen(["python", "start_treasure.py"]) # Le best_match envoie au script find_phorreur.py le dernier résultat du direction de l'indice donc pour le phorreur
            sys.exit()
        else:
            print("Aucune image phorreur.png trouvée. Le script continue.")

        # Mettre la fenêtre Dofus au premier plan après avoir effectué l'action sur la flèche
        try:
            find_dofus_window()
            print("Fenêtre Dofus mise au premier plan.")
            click(346, 1070)
            time.sleep(0.5)
            keyboard.press(Key.ctrl)  # Appuyer sur la touche Ctrl
            keyboard.press('v')       # Appuyer sur la touche V
            keyboard.release('v')     # Relâcher la touche V
            keyboard.release(Key.ctrl)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            # Après avoir collé avec CTRL-V :
            time.sleep(0.5)  # Attendre un moment pour s'assurer que le texte est collé
            clipboard_text = pyperclip.paste()  # Récupérer le texte du presse-papiers

            # Extraire uniquement ce qui est après "/travel"
            if "/travel" in clipboard_text:
                extracted_text = clipboard_text.split("/travel", 1)[1].strip()  # Garder tout après "/travel"
                print(f"Texte extrait : {extracted_text}")
            else:
                print("Le texte du presse-papiers ne contient pas '/travel'.")
        except Exception as e:
            print(str(e))

    # Fonction pour capturer et extraire le texte de l'écran avec les filtres appliqués
    def extract_text_from_screen(pos_zone_bbox):
        try:
            # Capture la zone de l'écran et augmenter la résolution
            screenshot = pyautogui.screenshot(region=pos_zone_bbox).resize((400, 400), Image.Resampling.LANCZOS)
            
            # Convertir l'image en niveaux de gris
            gray_screenshot = screenshot.convert("L")
            
            # Appliquer un seuil pour binariser l'image (noir et blanc)
            threshold = 150  # Réduction du seuil pour mieux capter les contrastes
            binarized_screenshot = gray_screenshot.point(lambda p: p > threshold and 255)

            # Augmenter le contraste pour améliorer la lisibilité
            enhancer = ImageEnhance.Contrast(binarized_screenshot)
            enhanced_screenshot = enhancer.enhance(2.0)  # Augmenter le contraste pour rendre le texte plus visible

            # Utilisation de pytesseract pour extraire le texte
            custom_config = r'--oem 3 --psm 6'  # Mode PSM pour texte horizontal (ligne unique)
            text = pytesseract.image_to_string(enhanced_screenshot, config=custom_config)
            
            print(f"Texte brut extrait : {text}")  # Afficher le texte extrait pour débogage
            
            return text
        except Exception as e:
            print(f"Erreur lors de la capture ou de l'extraction du texte : {e}")
            return ""

    # Fonction pour nettoyer et formater le texte extrait
    def clean_text(text):
        # Remplacer les 'G' par '6' et les 'O' par '0'
        text = text.replace("G", "6").replace("O", "0")

        # Supprimer les lettres et autres caractères non numériques, mais garder les signes - et .
        text = re.sub(r'[^0-9\s,-]', '', text)  # Garder les chiffres, espaces, virgules, signes - et .

        # Remplacer les virgules par des espaces
        text = text.replace(",", " ")

        # Supprimer les espaces multiples
        text = ' '.join(text.split())

        # S'assurer qu'il y a un espace entre chaque nombre et que les signes négatifs sont bien placés
        text = re.sub(r'\s-', ' -', text)  # Retirer les espaces avant les signes -

        # Supprimer tout tiret supplémentaire à la fin du texte
        text = text.rstrip('-')

        # Gérer les cas où des signes négatifs sont associés à des nombres
        # Assurer une bonne séparation des chiffres négatifs
        numbers = re.findall(r'-?\d+', text)  # Trouver tous les nombres, y compris ceux avec un signe -

        # Afficher les nombres trouvés pour débogage
        print(f"Nombre(s) extrait(s) : {numbers}")
        
        # Toujours garder les deux premiers nombres
        if len(numbers) >= 2:
            return " ".join(numbers[:2])  # Retourner les deux premiers nombres
        else:
            print("Erreur: le texte ne contient pas exactement deux nombres.")
            return ""  # Si ce n'est pas deux nombres, on renvoie une chaîne vide

    # Capture de la position actuelle
    pos_zone_bbox = (6, 71, 87, 97)  # Modifié quator_zone_bbox en pos_zone_bbox
    print(f"Position actuelle : {pos_zone_bbox}")

    # On initialise pos_text comme une chaîne vide pour entrer dans la boucle
    pos_text = ""
    start_time = time.time()  # Commencer le chronomètre
    timeout = 6220  # Timeout de 1 minute

    # Répéter la capture toutes les secondes jusqu'à ce que les textes correspondent
    while pos_text != extracted_text:
        pos = capture_zone(*pos_zone_bbox)  # Utilisation de pos_zone_bbox ici
        if not pos:
            print("Erreur de capture de la première zone.")
            return

        try:                    
            # Extraire et nettoyer le texte de la zone d'écran
            pos_text = extract_text_from_screen(pos_zone_bbox)
            
            # Nettoyer le texte extrait
            pos_text = clean_text(pos_text)

            # Afficher le texte extrait nettoyé
            print(f"Texte extrait nettoyé : {pos_text}")

        except Exception as e:
            print(f"Erreur lors de l'extraction du texte de la capture : {str(e)}")
            return


        # Vérification des correspondances
        if pos_text == extracted_text:
            print("Les textes correspondent. Clic sur la position le jalon 1.")
            click(266, 293) # Fonction pour effectuer le clic
            # Attente pour bien capturer la prochaine direction
            time.sleep(0.5)
            break  # Sortir de la boucle une fois que les textes correspondent

        # Vérifier si 1 minute est écoulée
        if time.time() - start_time > timeout:
            print("Les textes ne correspondent pas dans le temps imparti. Abandon de la chasse au trésor")
            click(274, 173)  # Effectuer le clic après 1 minute
            time.sleep(0.5)
            click(370, 414)
            time.sleep(0.5)
            print("Le programme s'arrête dû à l'abandon de la quête")
            sys.exit()
            break  # Sortir de la boucle après le clic

    # Si la boucle termine sans que les textes ne correspondent, aucun clic n'est effectué.
    if pos_text != extracted_text:
        print("Les textes ne correspondent toujours pas après plusieurs tentatives. Aucun clic effectué.")


#########################################################################################################################
#                                                           INDICE 2                                                    #
#########################################################################################################################
    # Capture de la flèche indice 2 (au lieu de fl1)
    fl2_zone_bbox = (1, 306, 35, 342)  # Nouvelle zone de capture pour fl2
    print(f"Capture de la direction du deuxième indice : {fl2_zone_bbox}")
    fl2_image = capture_zone(*fl2_zone_bbox)  # Utilisation de fl2_zone_bbox
    file_name = f"indice_2.png"
    fl2_image.save(file_name)
    if not fl2_image:
        print("Erreur de capture de la direction du deuxième indice.")
        return

    # Log pour la flèche indice 2
    print("Log de flèche indice 2 extraite :")
    print(get_text_from_image(fl2_image))  # Affiche le texte extrait de la zone fl2

    # Comparaison des images capturées pour la flèche indice 2
    best_match, similarity = find_matching_image(fl2_image)  # Utilisation de fl2_image
    if best_match:
        print(f"Meilleure correspondance trouvée : {best_match} ({similarity:.2f})")
    else:
        print("Aucune correspondance trouvée.")

    # Déterminer la direction à partir de la flèche capturée sur le deuxième indice
    direction = None
    if "arrow_up" in best_match:
        direction = 'up'
    elif "arrow_right" in best_match:
        direction = 'right'
    elif "arrow_left" in best_match:
        direction = 'left'
    elif "arrow_down" in best_match:
        direction = 'down'

    # Capture du deuxième indice (au lieu de in1)
    in2_zone_bbox = (28, 305, 188, 341)  # Nouvelle zone de capture pour in2
    print(f"Capture du deuxième indice : {in2_zone_bbox}")
    in2_image = capture_zone(*in2_zone_bbox)  # Utilisation de in2_zone_bbox
    file_name = f"vindice_2.png"
    in2_image.save(file_name)
    if not in2_image:
        print("Erreur de capture du deuxième indice.")
        return

    # Extraire et loguer le texte du deuxième indice
    extracted_text = get_text_from_image(in2_image)  # Utilisation de in2_image
    print(f"Direction de la flèche : {extracted_text}")

    # Comparer le texte extrait avec la base de données
    closest_match, similarity = find_closest_match(extracted_text, DATABASE)
    if closest_match:
        print(f"Texte le plus proche trouvé : {closest_match} (similarité : {similarity:.2f})")
    else:
        print("Aucun texte correspondant trouvé dans la base de données.")

    find_browser_window() # On re go sur le navigateur
    print("Fenêtre de navigateur mise au premier plan.")

    # Appuyer sur la flèche correspondant à la direction trouvée
    press_arrow(direction)
    time.sleep(0.5)

        # Trouver le champ de recherche et taper le texte trouvé
    try:
            search_field = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
            search_field.clear()
            search_field.send_keys(closest_match)
            print(f"Texte le plus proche entré dans la barre de recherche : {closest_match}")
            
            # Appuyer sur la touche Flèche Bas et Entrée
            time.sleep(1)  # Attendre pour simuler un délai humain
            search_field.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            click(889, 700)
            time.sleep(1)
            print("Flèche Bas et Entrée appuyées dans le champ de recherche.")
    except Exception as e:
            print(f"Erreur lors de la saisie dans le champ de recherche : {e}")
    
            # Vérification de l'apparition de phorreur.png après le clic
        # Capture de la zone pour détecter phorreur.png
    phorreur_image = capture_zone(655, 681, 750, 778)
    phorreur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'phorreur.png')

        # Trouver la meilleure correspondance
    best_match_phorreur, similarity = find_matching_image(phorreur_image, folder_path=os.path.dirname(phorreur_path))

        # Ajouter un log détaillé de similarité
    print(f"Similarité calculée : {similarity:.2f}")

        # Vérifier si la correspondance est assez bonne
    if best_match_phorreur and similarity > 0.9:  # Seuil augmenté
            print(f"Meilleure correspondance trouvée : {best_match_phorreur} ({similarity:.2f})")
            print("Image phorreur.png détectée. Abandon de la chasse pour en lancer une nouvelle...")
            find_dofus_window()
            print("Fenêtre Dofus mise au premier plan.")
            time.sleep(0.5)
            click(276, 172)
            time.sleep(0.5)
            click(372, 413)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            time.sleep(0.5)
            subprocess.Popen(["python", "start_treasure.py"]) # Le best_match envoie au script find_phorreur.py le dernier résultat du direction de l'indice donc pour le phorreur
            sys.exit()
    else:
            print("Aucune image phorreur.png trouvée. Le script continue.")

        # Mettre la fenêtre Dofus au premier plan après avoir effectué l'action sur la flèche
    try:
            find_dofus_window()
            print("Fenêtre Dofus mise au premier plan.")
            click(346, 1070)
            time.sleep(0.5)
            keyboard.press(Key.ctrl)  # Appuyer sur la touche Ctrl
            keyboard.press('v')       # Appuyer sur la touche V
            keyboard.release('v')     # Relâcher la touche V
            keyboard.release(Key.ctrl)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            # Après avoir collé avec CTRL-V :
            time.sleep(0.5)  # Attendre un moment pour s'assurer que le texte est collé
            clipboard_text = pyperclip.paste()  # Récupérer le texte du presse-papiers

            # Extraire uniquement ce qui est après "/travel"
            if "/travel" in clipboard_text:
                extracted_text = clipboard_text.split("/travel", 1)[1].strip()  # Garder tout après "/travel"
                print(f"Texte extrait : {extracted_text}")
            else:
                print("Le texte du presse-papiers ne contient pas '/travel'.")
    except Exception as e:
            print(str(e))

    # Fonction pour capturer et extraire le texte de l'écran avec les filtres appliqués
    def extract_text_from_screen(pos_zone_bbox):
        try:
            # Capture la zone de l'écran et augmenter la résolution
            screenshot = pyautogui.screenshot(region=pos_zone_bbox).resize((400, 400), Image.Resampling.LANCZOS)
            
            # Convertir l'image en niveaux de gris
            gray_screenshot = screenshot.convert("L")
            
            # Appliquer un seuil pour binariser l'image (noir et blanc)
            threshold = 150  # Réduction du seuil pour mieux capter les contrastes
            binarized_screenshot = gray_screenshot.point(lambda p: p > threshold and 255)

            # Augmenter le contraste pour améliorer la lisibilité
            enhancer = ImageEnhance.Contrast(binarized_screenshot)
            enhanced_screenshot = enhancer.enhance(2.0)  # Augmenter le contraste pour rendre le texte plus visible

            # Utilisation de pytesseract pour extraire le texte
            custom_config = r'--oem 3 --psm 6'  # Mode PSM pour texte horizontal (ligne unique)
            text = pytesseract.image_to_string(enhanced_screenshot, config=custom_config)
            
            print(f"Texte brut extrait : {text}")  # Afficher le texte extrait pour débogage
            
            return text
        except Exception as e:
            print(f"Erreur lors de la capture ou de l'extraction du texte : {e}")
            return ""

    # Fonction pour nettoyer et formater le texte extrait
    def clean_text(text):
        # Remplacer les 'G' par '6' et les 'O' par '0'
        text = text.replace("G", "6").replace("O", "0")

        # Supprimer les lettres et autres caractères non numériques, mais garder les signes - et .
        text = re.sub(r'[^0-9\s,-]', '', text)  # Garder les chiffres, espaces, virgules, signes - et .

        # Remplacer les virgules par des espaces
        text = text.replace(",", " ")

        # Supprimer les espaces multiples
        text = ' '.join(text.split())

        # S'assurer qu'il y a un espace entre chaque nombre et que les signes négatifs sont bien placés
        text = re.sub(r'\s-', ' -', text)  # Retirer les espaces avant les signes -

        # Supprimer tout tiret supplémentaire à la fin du texte
        text = text.rstrip('-')

        # Gérer les cas où des signes négatifs sont associés à des nombres
        # Assurer une bonne séparation des chiffres négatifs
        numbers = re.findall(r'-?\d+', text)  # Trouver tous les nombres, y compris ceux avec un signe -

        # Afficher les nombres trouvés pour débogage
        print(f"Nombre(s) extrait(s) : {numbers}")
        
        # Toujours garder les deux premiers nombres
        if len(numbers) >= 2:
            return " ".join(numbers[:2])  # Retourner les deux premiers nombres
        else:
            print("Erreur: le texte ne contient pas exactement deux nombres.")
            return ""  # Si ce n'est pas deux nombres, on renvoie une chaîne vide

    # Capture de la position actuelle
    pos_zone_bbox = (6, 71, 87, 97)  # Modifié quator_zone_bbox en pos_zone_bbox
    print(f"Position actuelle : {pos_zone_bbox}")

    # On initialise pos_text comme une chaîne vide pour entrer dans la boucle
    pos_text = ""
    start_time = time.time()  # Commencer le chronomètre
    timeout = 60  # Timeout de 1 minute

    # Répéter la capture toutes les secondes jusqu'à ce que les textes correspondent
    while pos_text != extracted_text:
        pos = capture_zone(*pos_zone_bbox)  # Utilisation de pos_zone_bbox ici
        if not pos:
            print("Erreur de capture de la première zone.")
            return

        try:                    
            # Extraire et nettoyer le texte de la zone d'écran
            pos_text = extract_text_from_screen(pos_zone_bbox)
            
            # Nettoyer le texte extrait
            pos_text = clean_text(pos_text)

            # Afficher le texte extrait nettoyé
            print(f"Texte extrait nettoyé : {pos_text}")

        except Exception as e:
            print(f"Erreur lors de l'extraction du texte de la capture : {str(e)}")
            return


        # Vérification des correspondances
        if pos_text == extracted_text:
            print("Les textes correspondent. Clic sur la position le jalon 2.") 
            click(266, 323) # Fonction pour effectuer le clic
            # Attente pour bien capturer la prochaine direction
            time.sleep(0.5)
            break  # Sortir de la boucle une fois que les textes correspondent

        # Vérifier si 1 minute est écoulée
        if time.time() - start_time > timeout:
            print("Les textes ne correspondent pas dans le temps imparti. Abandon de la chasse au trésor")
            click(274, 173)  # Effectuer le clic après 1 minute
            time.sleep(0.5)
            click(370, 414)
            time.sleep(0.5)
            print("Le programme s'arrête dû à l'abandon de la quête")
            sys.exit()
            break  # Sortir de la boucle après le clic

    # Si la boucle termine sans que les textes ne correspondent, aucun clic n'est effectué.
    if pos_text != extracted_text:
        print("Les textes ne correspondent toujours pas après plusieurs tentatives. Aucun clic effectué.")


#########################################################################################################################
#                                                           INDICE 3                                                    #
#########################################################################################################################
    # Capture de la flèche indice 3 (au lieu de fl2)
    fl3_zone_bbox = (1, 337, 35, 371)  # Nouvelle zone de capture pour fl3
    print(f"Capture de la direction du troisième indice : {fl3_zone_bbox}")
    fl3_image = capture_zone(*fl3_zone_bbox)  # Utilisation de fl3_zone_bbox
    file_name = f"indice_3.png"
    fl3_image.save(file_name)
    if not fl3_image:
        print("Erreur de capture de la direction du troisième indice.")
        return

    # Log pour la flèche indice 3
    print("Log de flèche indice 3 extraite :")
    print(get_text_from_image(fl3_image))  # Affiche le texte extrait de la zone fl3

    # Comparaison des images capturées pour la flèche indice 3
    best_match, similarity = find_matching_image(fl3_image)  # Utilisation de fl3_image
    if best_match:
        print(f"Meilleure correspondance trouvée : {best_match} ({similarity:.2f})")
    else:
        print("Aucune correspondance trouvée.")

    # Déterminer la direction à partir de la flèche capturée sur le troisième indice
    direction = None
    if "arrow_up" in best_match:
        direction = 'up'
    elif "arrow_right" in best_match:
        direction = 'right'
    elif "arrow_left" in best_match:
        direction = 'left'
    elif "arrow_down" in best_match:
        direction = 'down'

    # Capture du troisième indice (au lieu de in2)
    in3_zone_bbox = (30, 334, 192, 366)  # Nouvelle zone de capture pour in3
    print(f"Capture du troisième indice : {in3_zone_bbox}")
    in3_image = capture_zone(*in3_zone_bbox)  # Utilisation de in3_zone_bbox
    file_name = f"vindice_3.png"
    in3_image.save(file_name)
    if not in3_image:
        print("Erreur de capture du troisième indice.")
        return

    # Extraire et loguer le texte du troisième indice
    extracted_text = get_text_from_image(in3_image)  # Utilisation de in3_image
    print(f"Direction de la flèche : {extracted_text}")

    # Comparer le texte extrait avec la base de données
    closest_match, similarity = find_closest_match(extracted_text, DATABASE)
    if closest_match:
        print(f"Texte le plus proche trouvé : {closest_match} (similarité : {similarity:.2f})")
    else:
        print("Aucun texte correspondant trouvé dans la base de données.")

    find_browser_window()  # On remet le navigateur au premier plan
    print("Fenêtre de navigateur mise au premier plan.")

    # Appuyer sur la flèche correspondant à la direction trouvée
    press_arrow(direction)
    time.sleep(0.5)

    # Trouver le champ de recherche et taper le texte trouvé
    try:
        search_field = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_field.clear()
        search_field.send_keys(closest_match)
        print(f"Texte le plus proche entré dans la barre de recherche : {closest_match}")
        
        # Appuyer sur la touche Flèche Bas et Entrée
        time.sleep(1)  # Attendre pour simuler un délai humain
        search_field.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        click(889, 700)
        time.sleep(1)
        print("Flèche Bas et Entrée appuyées dans le champ de recherche.")
    except Exception as e:
        print(f"Erreur lors de la saisie dans le champ de recherche : {e}")
    
    # Vérification de l'apparition de phorreur.png après le clic
        # Capture de la zone pour détecter phorreur.png
    phorreur_image = capture_zone(655, 681, 750, 778)
    phorreur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'phorreur.png')

        # Trouver la meilleure correspondance
    best_match_phorreur, similarity = find_matching_image(phorreur_image, folder_path=os.path.dirname(phorreur_path))

        # Ajouter un log détaillé de similarité
    print(f"Similarité calculée : {similarity:.2f}")

        # Vérifier si la correspondance est assez bonne
    if best_match_phorreur and similarity > 0.9:  # Seuil augmenté
            print(f"Meilleure correspondance trouvée : {best_match_phorreur} ({similarity:.2f})")
            print("Image phorreur.png détectée. Abandon de la chasse pour en lancer une nouvelle...")
            find_dofus_window()
            print("Fenêtre Dofus mise au premier plan.")
            time.sleep(0.5)
            click(276, 172)
            time.sleep(0.5)
            click(372, 413)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            time.sleep(0.5)
            subprocess.Popen(["python", "start_treasure.py"]) # Le best_match envoie au script find_phorreur.py le dernier résultat du direction de l'indice donc pour le phorreur
            sys.exit()
    else:
            print("Aucune image phorreur.png trouvée. Le script continue.")

    # Mettre la fenêtre Dofus au premier plan après avoir effectué l'action sur la flèche
    try:
        find_dofus_window()
        print("Fenêtre Dofus mise au premier plan.")
        click(346, 1070)
        time.sleep(0.5)
        keyboard.press(Key.ctrl)  # Appuyer sur la touche Ctrl
        keyboard.press('v')       # Appuyer sur la touche V
        keyboard.release('v')     # Relâcher la touche V
        keyboard.release(Key.ctrl)
        time.sleep(0.5)
        keyboard.press(Key.enter)  # Appuyer sur la touche Enter
        keyboard.release(Key.enter)
        time.sleep(0.5)
        keyboard.press(Key.enter)  # Appuyer sur la touche Enter
        keyboard.release(Key.enter)
        # Après avoir collé avec CTRL-V :
        time.sleep(0.5)  # Attendre un moment pour s'assurer que le texte est collé
        clipboard_text = pyperclip.paste()  # Récupérer le texte du presse-papiers

        # Extraire uniquement ce qui est après "/travel"
        if "/travel" in clipboard_text:
            extracted_text = clipboard_text.split("/travel", 1)[1].strip()  # Garder tout après "/travel"
            print(f"Texte extrait : {extracted_text}")
        else:
            print("Le texte du presse-papiers ne contient pas '/travel'.")
    except Exception as e:
        print(str(e))

    # Fonction pour capturer et extraire le texte de l'écran avec les filtres appliqués
    def extract_text_from_screen(pos_zone_bbox):
        try:
            # Capture la zone de l'écran et augmenter la résolution
            screenshot = pyautogui.screenshot(region=pos_zone_bbox).resize((400, 400), Image.Resampling.LANCZOS)
            
            # Convertir l'image en niveaux de gris
            gray_screenshot = screenshot.convert("L")
            
            # Appliquer un seuil pour binariser l'image (noir et blanc)
            threshold = 150  # Réduction du seuil pour mieux capter les contrastes
            binarized_screenshot = gray_screenshot.point(lambda p: p > threshold and 255)

            # Augmenter le contraste pour améliorer la lisibilité
            enhancer = ImageEnhance.Contrast(binarized_screenshot)
            enhanced_screenshot = enhancer.enhance(2.0)  # Augmenter le contraste pour rendre le texte plus visible

            # Utilisation de pytesseract pour extraire le texte
            custom_config = r'--oem 3 --psm 6'  # Mode PSM pour texte horizontal (ligne unique)
            text = pytesseract.image_to_string(enhanced_screenshot, config=custom_config)
            
            print(f"Texte brut extrait : {text}")  # Afficher le texte extrait pour débogage
            
            return text
        except Exception as e:
            print(f"Erreur lors de la capture ou de l'extraction du texte : {e}")
            return ""

    # Fonction pour nettoyer et formater le texte extrait
    def clean_text(text):
        # Remplacer les 'G' par '6' et les 'O' par '0'
        text = text.replace("G", "6").replace("O", "0")

        # Supprimer les lettres et autres caractères non numériques, mais garder les signes - et .
        text = re.sub(r'[^0-9\s,-]', '', text)  # Garder les chiffres, espaces, virgules, signes - et .

        # Remplacer les virgules par des espaces
        text = text.replace(",", " ")

        # Supprimer les espaces multiples
        text = ' '.join(text.split())

        # S'assurer qu'il y a un espace entre chaque nombre et que les signes négatifs sont bien placés
        text = re.sub(r'\s-', ' -', text)  # Retirer les espaces avant les signes -

        # Supprimer tout tiret supplémentaire à la fin du texte
        text = text.rstrip('-')

        # Gérer les cas où des signes négatifs sont associés à des nombres
        # Assurer une bonne séparation des chiffres négatifs
        numbers = re.findall(r'-?\d+', text)  # Trouver tous les nombres, y compris ceux avec un signe -

        # Afficher les nombres trouvés pour débogage
        print(f"Nombre(s) extrait(s) : {numbers}")
        
        # Toujours garder les deux premiers nombres
        if len(numbers) >= 2:
            return " ".join(numbers[:2])  # Retourner les deux premiers nombres
        else:
            print("Erreur: le texte ne contient pas exactement deux nombres.")
            return ""  # Si ce n'est pas deux nombres, on renvoie une chaîne vide

    # Capture de la position actuelle
    pos_zone_bbox = (6, 71, 87, 97)  # Modifié quator_zone_bbox en pos_zone_bbox
    print(f"Position actuelle : {pos_zone_bbox}")

    # On initialise pos_text comme une chaîne vide pour entrer dans la boucle
    pos_text = ""
    start_time = time.time()  # Commencer le chronomètre
    timeout = 60  # Timeout de 1 minute

    # Répéter la capture toutes les secondes jusqu'à ce que les textes correspondent
    while pos_text != extracted_text:
        pos = capture_zone(*pos_zone_bbox)  # Utilisation de pos_zone_bbox ici
        if not pos:
            print("Erreur de capture de la première zone.")
            return

        try:                    
            # Extraire et nettoyer le texte de la zone d'écran
            pos_text = extract_text_from_screen(pos_zone_bbox)
            
            # Nettoyer le texte extrait
            pos_text = clean_text(pos_text)

            # Afficher le texte extrait nettoyé
            print(f"Texte extrait nettoyé : {pos_text}")

        except Exception as e:
            print(f"Erreur lors de l'extraction du texte de la capture : {str(e)}")
            return


        # Vérification des correspondances
        if pos_text == extracted_text:
            print("Les textes correspondent. Clic sur la position le jalon 3.")  
            click(266, 353) # Fonction pour effectuer le clic
            # Attente pour bien capturer la prochaine direction
            time.sleep(0.5)
            break  # Sortir de la boucle une fois que les textes correspondent


        # Vérifier si 1 minute est écoulée
        if time.time() - start_time > timeout:
            print("Les textes ne correspondent pas dans le temps imparti. Abandon de la chasse au trésor")
            click(274, 173)  # Effectuer le clic après 1 minute
            time.sleep(0.5)
            click(370, 414)
            time.sleep(0.5)
            print("Le programme s'arrête dû à l'abandon de la quête")
            sys.exit()
            break  # Sortir de la boucle après le clic

    # Si la boucle termine sans que les textes ne correspondent, aucun clic n'est effectué.
    if pos_text != extracted_text:
        print("Les textes ne correspondent toujours pas après plusieurs tentatives. Aucun clic effectué.")

#########################################################################################################################
#                                                           INDICE 4                                                    #
#########################################################################################################################
    # Capture de la flèche indice 4 (au lieu de fl3)
    fl4_zone_bbox = (2, 360, 35, 401)  # Nouvelle zone de capture pour fl4
    print(f"Capture de la direction du quatrième indice : {fl4_zone_bbox}")
    fl4_image = capture_zone(*fl4_zone_bbox)  # Utilisation de fl4_zone_bbox
    file_name = f"indice_4.png"
    fl4_image.save(file_name)
    if not fl4_image:
        print("Erreur de capture de la direction du quatrième indice.")
        return

    # Log pour la flèche indice 4
    print("Log de flèche indice 4 extraite :")
    print(get_text_from_image(fl4_image))  # Affiche le texte extrait de la zone fl4

    # Comparaison des images capturées pour la flèche indice 4
    best_match, similarity = find_matching_image(fl4_image)  # Utilisation de fl4_image
    if best_match:
        print(f"Meilleure correspondance trouvée : {best_match} ({similarity:.2f})")
    else:
        print("Aucune correspondance trouvée.")

    # Déterminer la direction à partir de la flèche capturée sur le quatrième indice
    direction = None
    if "arrow_up" in best_match:
        direction = 'up'
    elif "arrow_right" in best_match:
        direction = 'right'
    elif "arrow_left" in best_match:
        direction = 'left'
    elif "arrow_down" in best_match:
        direction = 'down'

    # Capture du quatrième indice (au lieu de in3)
    in4_zone_bbox = (31, 364, 192, 395)  # Nouvelle zone de capture pour in4
    print(f"Capture du quatrième indice : {in4_zone_bbox}")
    in4_image = capture_zone(*in4_zone_bbox)  # Utilisation de in4_zone_bbox
    file_name = f"vindice_4.png"
    in4_image.save(file_name)
    if not in4_image:
        print("Erreur de capture du quatrième indice.")
        return

    # Extraire et loguer le texte du quatrième indice
    extracted_text = get_text_from_image(in4_image)  # Utilisation de in4_image
    print(f"Direction de la flèche : {extracted_text}")

    # Comparer le texte extrait avec la base de données
    closest_match, similarity = find_closest_match(extracted_text, DATABASE)
    if closest_match:
        print(f"Texte le plus proche trouvé : {closest_match} (similarité : {similarity:.2f})")
    else:
        print("Aucun texte correspondant trouvé dans la base de données.")

    find_browser_window()  # Remettre le navigateur au premier plan
    print("Fenêtre de navigateur mise au premier plan.")

    # Appuyer sur la flèche correspondant à la direction trouvée
    press_arrow(direction)
    time.sleep(0.5)

    # Trouver le champ de recherche et taper le texte trouvé
    try:
        search_field = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_field.clear()
        search_field.send_keys(closest_match)
        print(f"Texte le plus proche entré dans la barre de recherche : {closest_match}")
        
        # Appuyer sur la touche Flèche Bas et Entrée
        time.sleep(1)  # Attendre pour simuler un délai humain
        search_field.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        click(889, 700)
        time.sleep(1)
        print("Flèche Bas et Entrée appuyées dans le champ de recherche.")
    except Exception as e:
        print(f"Erreur lors de la saisie dans le champ de recherche : {e}")
    
    # Vérification de l'apparition de phorreur.png après le clic
        # Capture de la zone pour détecter phorreur.png
    phorreur_image = capture_zone(655, 681, 750, 778)
    phorreur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'phorreur.png')

        # Trouver la meilleure correspondance
    best_match_phorreur, similarity = find_matching_image(phorreur_image, folder_path=os.path.dirname(phorreur_path))

        # Ajouter un log détaillé de similarité
    print(f"Similarité calculée : {similarity:.2f}")

        # Vérifier si la correspondance est assez bonne
    if best_match_phorreur and similarity > 0.9:  # Seuil augmenté
            print(f"Meilleure correspondance trouvée : {best_match_phorreur} ({similarity:.2f})")
            print("Image phorreur.png détectée. Abandon de la chasse pour en lancer une nouvelle...")
            find_dofus_window()
            print("Fenêtre Dofus mise au premier plan.")
            time.sleep(0.5)
            click(276, 172)
            time.sleep(0.5)
            click(372, 413)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            time.sleep(0.5)
            subprocess.Popen(["python", "start_treasure.py"]) # Le best_match envoie au script find_phorreur.py le dernier résultat du direction de l'indice donc pour le phorreur
            sys.exit()
    else:
            print("Aucune image phorreur.png trouvée. Le script continue.")

    # Mettre la fenêtre Dofus au premier plan après avoir effectué l'action sur la flèche
    try:
        find_dofus_window()
        print("Fenêtre Dofus mise au premier plan.")
        click(346, 1070)
        time.sleep(0.5)
        keyboard.press(Key.ctrl)  # Appuyer sur la touche Ctrl
        keyboard.press('v')       # Appuyer sur la touche V
        keyboard.release('v')     # Relâcher la touche V
        keyboard.release(Key.ctrl)
        time.sleep(0.5)
        keyboard.press(Key.enter)  # Appuyer sur la touche Enter
        keyboard.release(Key.enter)
        time.sleep(0.5)
        keyboard.press(Key.enter)  # Appuyer sur la touche Enter
        keyboard.release(Key.enter)
        time.sleep(0.5)  # Attendre un moment pour s'assurer que le texte est collé
        clipboard_text = pyperclip.paste()  # Récupérer le texte du presse-papiers

        # Extraire uniquement ce qui est après "/travel"
        if "/travel" in clipboard_text:
            extracted_text = clipboard_text.split("/travel", 1)[1].strip()  # Garder tout après "/travel"
            print(f"Texte extrait : {extracted_text}")
        else:
            print("Le texte du presse-papiers ne contient pas '/travel'.")
    except Exception as e:
        print(str(e))

    # Fonction pour capturer et extraire le texte de l'écran avec les filtres appliqués
    def extract_text_from_screen(pos_zone_bbox):
        try:
            # Capture la zone de l'écran et augmenter la résolution
            screenshot = pyautogui.screenshot(region=pos_zone_bbox).resize((400, 400), Image.Resampling.LANCZOS)
            
            # Convertir l'image en niveaux de gris
            gray_screenshot = screenshot.convert("L")
            
            # Appliquer un seuil pour binariser l'image (noir et blanc)
            threshold = 150  # Réduction du seuil pour mieux capter les contrastes
            binarized_screenshot = gray_screenshot.point(lambda p: p > threshold and 255)

            # Augmenter le contraste pour améliorer la lisibilité
            enhancer = ImageEnhance.Contrast(binarized_screenshot)
            enhanced_screenshot = enhancer.enhance(2.0)  # Augmenter le contraste pour rendre le texte plus visible

            # Utilisation de pytesseract pour extraire le texte
            custom_config = r'--oem 3 --psm 6'  # Mode PSM pour texte horizontal (ligne unique)
            text = pytesseract.image_to_string(enhanced_screenshot, config=custom_config)
            
            print(f"Texte brut extrait : {text}")  # Afficher le texte extrait pour débogage
            
            return text
        except Exception as e:
            print(f"Erreur lors de la capture ou de l'extraction du texte : {e}")
            return ""

    # Fonction pour nettoyer et formater le texte extrait
    def clean_text(text):
        # Remplacer les 'G' par '6' et les 'O' par '0'
        text = text.replace("G", "6").replace("O", "0")

        # Supprimer les lettres et autres caractères non numériques, mais garder les signes - et .
        text = re.sub(r'[^0-9\s,-]', '', text)  # Garder les chiffres, espaces, virgules, signes - et .

        # Remplacer les virgules par des espaces
        text = text.replace(",", " ")

        # Supprimer les espaces multiples
        text = ' '.join(text.split())

        # S'assurer qu'il y a un espace entre chaque nombre et que les signes négatifs sont bien placés
        text = re.sub(r'\s-', ' -', text)  # Retirer les espaces avant les signes -

        # Supprimer tout tiret supplémentaire à la fin du texte
        text = text.rstrip('-')

        # Gérer les cas où des signes négatifs sont associés à des nombres
        # Assurer une bonne séparation des chiffres négatifs
        numbers = re.findall(r'-?\d+', text)  # Trouver tous les nombres, y compris ceux avec un signe -

        # Afficher les nombres trouvés pour débogage
        print(f"Nombre(s) extrait(s) : {numbers}")
        
        # Toujours garder les deux premiers nombres
        if len(numbers) >= 2:
            return " ".join(numbers[:2])  # Retourner les deux premiers nombres
        else:
            print("Erreur: le texte ne contient pas exactement deux nombres.")
            return ""  # Si ce n'est pas deux nombres, on renvoie une chaîne vide

    # Capture de la position actuelle
    pos_zone_bbox = (6, 71, 87, 97)  # Modifié quator_zone_bbox en pos_zone_bbox
    print(f"Position actuelle : {pos_zone_bbox}")

    # On initialise pos_text comme une chaîne vide pour entrer dans la boucle
    pos_text = ""
    start_time = time.time()  # Commencer le chronomètre
    timeout = 60  # Timeout de 1 minute

    # Répéter la capture toutes les secondes jusqu'à ce que les textes correspondent
    while pos_text != extracted_text:
        pos = capture_zone(*pos_zone_bbox)  # Utilisation de pos_zone_bbox ici
        if not pos:
            print("Erreur de capture de la première zone.")
            return

        try:                    
            # Extraire et nettoyer le texte de la zone d'écran
            pos_text = extract_text_from_screen(pos_zone_bbox)
            
            # Nettoyer le texte extrait
            pos_text = clean_text(pos_text)

            # Afficher le texte extrait nettoyé
            print(f"Texte extrait nettoyé : {pos_text}")

        except Exception as e:
            print(f"Erreur lors de l'extraction du texte de la capture : {str(e)}")
            return


        # Vérification des correspondances
        if pos_text == extracted_text:
            print("Les textes correspondent. Clic sur la position du jalon 4.")
            click(265, 379)  # Nouvelle position pour le quatrième indice
            time.sleep(0.5)
            break

        # Vérifier si 1 minute est écoulée
        if time.time() - start_time > timeout:
            print("Les textes ne correspondent pas dans le temps imparti. Abandon de la chasse au trésor")
            click(274, 173)  # Effectuer le clic après 1 minute
            time.sleep(0.5)
            click(370, 414)
            time.sleep(0.5)
            print("Le programme s'arrête dû à l'abandon de la quête")
            sys.exit()
            break  # Sortir de la boucle après le clic

    # Si la boucle termine sans que les textes ne correspondent, aucun clic n'est effectué.
    if pos_text != extracted_text:
        print("Les textes ne correspondent toujours pas après plusieurs tentatives. Aucun clic effectué.")


#########################################################################################################################
#                                                           INDICE 5                                                    #
#########################################################################################################################
    # Capture de la flèche indice 5 (au lieu de fl4)
    fl5_zone_bbox = (1, 387, 33, 425)  # Nouvelle zone de capture pour fl5
    print(f"Capture de la direction du cinquième indice : {fl5_zone_bbox}")
    fl5_image = capture_zone(*fl5_zone_bbox)  # Utilisation de fl5_zone_bbox
    file_name = f"indice_5.png"
    fl5_image.save(file_name)
    if not fl5_image:
        print("Erreur de capture de la direction du cinquième indice.")
        return

    # Log pour la flèche indice 5
    print("Log de flèche indice 5 extraite :")
    print(get_text_from_image(fl5_image))  # Affiche le texte extrait de la zone fl5

    # Comparaison des images capturées pour la flèche indice 5
    best_match, similarity = find_matching_image(fl5_image)  # Utilisation de fl5_image
    if best_match:
        print(f"Meilleure correspondance trouvée : {best_match} ({similarity:.2f})")
    else:
        print("Aucune correspondance trouvée.")

    # Déterminer la direction à partir de la flèche capturée sur le cinquième indice
    direction = None
    if "arrow_up" in best_match:
        direction = 'up'
    elif "arrow_right" in best_match:
        direction = 'right'
    elif "arrow_left" in best_match:
        direction = 'left'
    elif "arrow_down" in best_match:
        direction = 'down'

    # Capture du cinquième indice (au lieu de in4)
    in5_zone_bbox = (33, 388, 192, 421)  # Nouvelle zone de capture pour in5
    print(f"Capture du cinquième indice : {in5_zone_bbox}")
    in5_image = capture_zone(*in5_zone_bbox)  # Utilisation de in5_zone_bbox
    file_name = f"vindice_5.png"
    in5_image.save(file_name)
    if not in5_image:
        print("Erreur de capture du cinquième indice.")
        return

    # Extraire et loguer le texte du cinquième indice
    extracted_text = get_text_from_image(in5_image)  # Utilisation de in5_image
    print(f"Direction de la flèche : {extracted_text}")

    # Comparer le texte extrait avec la base de données
    closest_match, similarity = find_closest_match(extracted_text, DATABASE)
    if closest_match:
        print(f"Texte le plus proche trouvé : {closest_match} (similarité : {similarity:.2f})")
    else:
        print("Aucun texte correspondant trouvé dans la base de données.")

    find_browser_window()  # Remettre le navigateur au premier plan
    print("Fenêtre de navigateur mise au premier plan.")

    # Appuyer sur la flèche correspondant à la direction trouvée
    press_arrow(direction)
    time.sleep(0.5)

    # Trouver le champ de recherche et taper le texte trouvé
    try:
        search_field = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_field.clear()
        search_field.send_keys(closest_match)
        print(f"Texte le plus proche entré dans la barre de recherche : {closest_match}")
        
        # Appuyer sur la touche Flèche Bas et Entrée
        time.sleep(1)
        search_field.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        click(889, 700)
        time.sleep(1)
        print("Flèche Bas et Entrée appuyées dans le champ de recherche.")
    except Exception as e:
        print(f"Erreur lors de la saisie dans le champ de recherche : {e}")
    
    # Vérification de l'apparition de phorreur.png après le clic
        # Capture de la zone pour détecter phorreur.png
    phorreur_image = capture_zone(655, 681, 750, 778)
    phorreur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'phorreur.png')

        # Trouver la meilleure correspondance
    best_match_phorreur, similarity = find_matching_image(phorreur_image, folder_path=os.path.dirname(phorreur_path))

        # Ajouter un log détaillé de similarité
    print(f"Similarité calculée : {similarity:.2f}")

        # Vérifier si la correspondance est assez bonne
    if best_match_phorreur and similarity > 0.9:  # Seuil augmenté
            print(f"Meilleure correspondance trouvée : {best_match_phorreur} ({similarity:.2f})")
            print("Image phorreur.png détectée. Abandon de la chasse pour en lancer une nouvelle...")
            find_dofus_window()
            print("Fenêtre Dofus mise au premier plan.")
            time.sleep(0.5)
            click(276, 172)
            time.sleep(0.5)
            click(372, 413)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            time.sleep(0.5)
            subprocess.Popen(["python", "start_treasure.py"]) # Le best_match envoie au script find_phorreur.py le dernier résultat du direction de l'indice donc pour le phorreur
            sys.exit()
    else:
            print("Aucune image phorreur.png trouvée. Le script continue.")

    # Mettre la fenêtre Dofus au premier plan après avoir effectué l'action sur la flèche
    try:
        find_dofus_window()
        print("Fenêtre Dofus mise au premier plan.")
        click(346, 1070)
        time.sleep(0.5)
        keyboard.press(Key.ctrl)
        keyboard.press('v')
        keyboard.release('v')
        keyboard.release(Key.ctrl)
        time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        clipboard_text = pyperclip.paste()

        # Extraire uniquement ce qui est après "/travel"
        if "/travel" in clipboard_text:
            extracted_text = clipboard_text.split("/travel", 1)[1].strip()
            print(f"Texte extrait : {extracted_text}")
        else:
            print("Le texte du presse-papiers ne contient pas '/travel'.")
    except Exception as e:
        print(str(e))

    # Fonction pour capturer et extraire le texte de l'écran avec les filtres appliqués
    def extract_text_from_screen(pos_zone_bbox):
        try:
            # Capture la zone de l'écran et augmenter la résolution
            screenshot = pyautogui.screenshot(region=pos_zone_bbox).resize((400, 400), Image.Resampling.LANCZOS)
            
            # Convertir l'image en niveaux de gris
            gray_screenshot = screenshot.convert("L")
            
            # Appliquer un seuil pour binariser l'image (noir et blanc)
            threshold = 150  # Réduction du seuil pour mieux capter les contrastes
            binarized_screenshot = gray_screenshot.point(lambda p: p > threshold and 255)

            # Augmenter le contraste pour améliorer la lisibilité
            enhancer = ImageEnhance.Contrast(binarized_screenshot)
            enhanced_screenshot = enhancer.enhance(2.0)  # Augmenter le contraste pour rendre le texte plus visible

            # Utilisation de pytesseract pour extraire le texte
            custom_config = r'--oem 3 --psm 6'  # Mode PSM pour texte horizontal (ligne unique)
            text = pytesseract.image_to_string(enhanced_screenshot, config=custom_config)
            
            print(f"Texte brut extrait : {text}")  # Afficher le texte extrait pour débogage
            
            return text
        except Exception as e:
            print(f"Erreur lors de la capture ou de l'extraction du texte : {e}")
            return ""

    # Fonction pour nettoyer et formater le texte extrait
    def clean_text(text):
        # Remplacer les 'G' par '6' et les 'O' par '0'
        text = text.replace("G", "6").replace("O", "0")

        # Supprimer les lettres et autres caractères non numériques, mais garder les signes - et .
        text = re.sub(r'[^0-9\s,-]', '', text)  # Garder les chiffres, espaces, virgules, signes - et .

        # Remplacer les virgules par des espaces
        text = text.replace(",", " ")

        # Supprimer les espaces multiples
        text = ' '.join(text.split())

        # S'assurer qu'il y a un espace entre chaque nombre et que les signes négatifs sont bien placés
        text = re.sub(r'\s-', ' -', text)  # Retirer les espaces avant les signes -

        # Supprimer tout tiret supplémentaire à la fin du texte
        text = text.rstrip('-')

        # Gérer les cas où des signes négatifs sont associés à des nombres
        # Assurer une bonne séparation des chiffres négatifs
        numbers = re.findall(r'-?\d+', text)  # Trouver tous les nombres, y compris ceux avec un signe -

        # Afficher les nombres trouvés pour débogage
        print(f"Nombre(s) extrait(s) : {numbers}")
        
        # Toujours garder les deux premiers nombres
        if len(numbers) >= 2:
            return " ".join(numbers[:2])  # Retourner les deux premiers nombres
        else:
            print("Erreur: le texte ne contient pas exactement deux nombres.")
            return ""  # Si ce n'est pas deux nombres, on renvoie une chaîne vide

    # Capture de la position actuelle
    pos_zone_bbox = (6, 71, 87, 97)  # Modifié quator_zone_bbox en pos_zone_bbox
    print(f"Position actuelle : {pos_zone_bbox}")

    # On initialise pos_text comme une chaîne vide pour entrer dans la boucle
    pos_text = ""
    start_time = time.time()  # Commencer le chronomètre
    timeout = 60  # Timeout de 1 minute

    # Répéter la capture toutes les secondes jusqu'à ce que les textes correspondent
    while pos_text != extracted_text:
        pos = capture_zone(*pos_zone_bbox)  # Utilisation de pos_zone_bbox ici
        if not pos:
            print("Erreur de capture de la première zone.")
            return

        try:                    
            # Extraire et nettoyer le texte de la zone d'écran
            pos_text = extract_text_from_screen(pos_zone_bbox)
            
            # Nettoyer le texte extrait
            pos_text = clean_text(pos_text)

            # Afficher le texte extrait nettoyé
            print(f"Texte extrait nettoyé : {pos_text}")

        except Exception as e:
            print(f"Erreur lors de l'extraction du texte de la capture : {str(e)}")
            return


        # Vérification des correspondances
        if pos_text == extracted_text:
            print("Les textes correspondent. Clic sur la position du jalon 5.")
            click(265, 407)  # Nouvelle position pour le cinquième indice
            time.sleep(0.5)
            break

        # Vérifier si 1 minute est écoulée
        if time.time() - start_time > timeout:
            print("Les textes ne correspondent pas dans le temps imparti. Abandon de la chasse au trésor")
            click(274, 173)  # Effectuer le clic après 1 minute
            time.sleep(0.5)
            click(370, 414)
            time.sleep(0.5)
            print("Le programme s'arrête dû à l'abandon de la quête")
            sys.exit()
            break  # Sortir de la boucle après le clic

    # Si la boucle termine sans que les textes ne correspondent, aucun clic n'est effectué.
    if pos_text != extracted_text:
        print("Les textes ne correspondent toujours pas après plusieurs tentatives. Aucun clic effectué.")

#########################################################################################################################
#                                                           INDICE 6                                                    #
#########################################################################################################################
    # Capture de la flèche indice 6 (au lieu de fl5)
    fl6_zone_bbox = (1, 415, 33, 451)  # Nouvelle zone de capture pour fl6
    print(f"Capture de la direction du sixième indice : {fl6_zone_bbox}")
    fl6_image = capture_zone(*fl6_zone_bbox)  # Utilisation de fl6_zone_bbox
    file_name = f"indice_6.png"
    fl6_image.save(file_name)
    if not fl6_image:
        print("Erreur de capture de la direction du sixième indice.")
        return

    # Log pour la flèche indice 6
    print("Log de flèche indice 6 extraite :")
    print(get_text_from_image(fl6_image))  # Affiche le texte extrait de la zone fl6

    # Comparaison des images capturées pour la flèche indice 6
    best_match, similarity = find_matching_image(fl6_image)  # Utilisation de fl6_image
    if best_match:
        print(f"Meilleure correspondance trouvée : {best_match} ({similarity:.2f})")
    else:
        print("Aucune correspondance trouvée.")

    # Déterminer la direction à partir de la flèche capturée sur le sixième indice
    direction = None
    if "arrow_up" in best_match:
        direction = 'up'
    elif "arrow_right" in best_match:
        direction = 'right'
    elif "arrow_left" in best_match:
        direction = 'left'
    elif "arrow_down" in best_match:
        direction = 'down'

    # Capture du sixième indice (au lieu de in5)
    in6_zone_bbox = (31, 422, 206, 451)  # Nouvelle zone de capture pour in6
    print(f"Capture du sixième indice : {in6_zone_bbox}")
    in6_image = capture_zone(*in6_zone_bbox)  # Utilisation de in6_zone_bbox
    file_name = f"vindice_6.png"
    in6_image.save(file_name)
    if not in6_image:
        print("Erreur de capture du sixième indice.")
        return

    # Extraire et loguer le texte du sixième indice
    extracted_text = get_text_from_image(in6_image)  # Utilisation de in6_image
    print(f"Direction de la flèche : {extracted_text}")

    # Comparer le texte extrait avec la base de données
    closest_match, similarity = find_closest_match(extracted_text, DATABASE)
    if closest_match:
        print(f"Texte le plus proche trouvé : {closest_match} (similarité : {similarity:.2f})")
    else:
        print("Aucun texte correspondant trouvé dans la base de données.")

    find_browser_window()  # Remettre le navigateur au premier plan
    print("Fenêtre de navigateur mise au premier plan.")

    # Appuyer sur la flèche correspondant à la direction trouvée
    press_arrow(direction)
    time.sleep(0.5)

    # Trouver le champ de recherche et taper le texte trouvé
    try:
        search_field = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_field.clear()
        search_field.send_keys(closest_match)
        print(f"Texte le plus proche entré dans la barre de recherche : {closest_match}")
        
        # Appuyer sur la touche Flèche Bas et Entrée
        time.sleep(1)
        search_field.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        click(889, 700)
        time.sleep(1)
        print("Flèche Bas et Entrée appuyées dans le champ de recherche.")
    except Exception as e:
        print(f"Erreur lors de la saisie dans le champ de recherche : {e}")
    
    # Vérification de l'apparition de phorreur.png après le clic
        # Capture de la zone pour détecter phorreur.png
    phorreur_image = capture_zone(655, 681, 750, 778)
    phorreur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'phorreur.png')

        # Trouver la meilleure correspondance
    best_match_phorreur, similarity = find_matching_image(phorreur_image, folder_path=os.path.dirname(phorreur_path))

        # Ajouter un log détaillé de similarité
    print(f"Similarité calculée : {similarity:.2f}")

        # Vérifier si la correspondance est assez bonne
    if best_match_phorreur and similarity > 0.9:  # Seuil augmenté
            print(f"Meilleure correspondance trouvée : {best_match_phorreur} ({similarity:.2f})")
            print("Image phorreur.png détectée. Abandon de la chasse pour en lancer une nouvelle...")
            find_dofus_window()
            print("Fenêtre Dofus mise au premier plan.")
            time.sleep(0.5)
            click(276, 172)
            time.sleep(0.5)
            click(372, 413)
            time.sleep(0.5)
            keyboard.press(Key.enter)  # Appuyer sur la touche Enter
            keyboard.release(Key.enter)
            time.sleep(0.5)
            subprocess.Popen(["python", "start_treasure.py"]) # Le best_match envoie au script find_phorreur.py le dernier résultat du direction de l'indice donc pour le phorreur
            sys.exit()
    else:
            print("Aucune image phorreur.png trouvée. Le script continue.")

    # Mettre la fenêtre Dofus au premier plan après avoir effectué l'action sur la flèche
    try:
        find_dofus_window()
        print("Fenêtre Dofus mise au premier plan.")
        click(346, 1070)
        time.sleep(0.5)
        keyboard.press(Key.ctrl)
        keyboard.press('v')
        keyboard.release('v')
        keyboard.release(Key.ctrl)
        time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        clipboard_text = pyperclip.paste()

        # Extraire uniquement ce qui est après "/travel"
        if "/travel" in clipboard_text:
            extracted_text = clipboard_text.split("/travel", 1)[1].strip()
            print(f"Texte extrait : {extracted_text}")
        else:
            print("Le texte du presse-papiers ne contient pas '/travel'.")
    except Exception as e:
        print(str(e))

    # Fonction pour capturer et extraire le texte de l'écran avec les filtres appliqués
    def extract_text_from_screen(pos_zone_bbox):
        try:
            # Capture la zone de l'écran et augmenter la résolution
            screenshot = pyautogui.screenshot(region=pos_zone_bbox).resize((400, 400), Image.Resampling.LANCZOS)
            
            # Convertir l'image en niveaux de gris
            gray_screenshot = screenshot.convert("L")
            
            # Appliquer un seuil pour binariser l'image (noir et blanc)
            threshold = 150  # Réduction du seuil pour mieux capter les contrastes
            binarized_screenshot = gray_screenshot.point(lambda p: p > threshold and 255)

            # Augmenter le contraste pour améliorer la lisibilité
            enhancer = ImageEnhance.Contrast(binarized_screenshot)
            enhanced_screenshot = enhancer.enhance(2.0)  # Augmenter le contraste pour rendre le texte plus visible

            # Utilisation de pytesseract pour extraire le texte
            custom_config = r'--oem 3 --psm 6'  # Mode PSM pour texte horizontal (ligne unique)
            text = pytesseract.image_to_string(enhanced_screenshot, config=custom_config)
            
            print(f"Texte brut extrait : {text}")  # Afficher le texte extrait pour débogage
            
            return text
        except Exception as e:
            print(f"Erreur lors de la capture ou de l'extraction du texte : {e}")
            return ""

    # Fonction pour nettoyer et formater le texte extrait
    def clean_text(text):
        # Remplacer les 'G' par '6' et les 'O' par '0'
        text = text.replace("G", "6").replace("O", "0")

        # Supprimer les lettres et autres caractères non numériques, mais garder les signes - et .
        text = re.sub(r'[^0-9\s,-]', '', text)  # Garder les chiffres, espaces, virgules, signes - et .

        # Remplacer les virgules par des espaces
        text = text.replace(",", " ")

        # Supprimer les espaces multiples
        text = ' '.join(text.split())

        # S'assurer qu'il y a un espace entre chaque nombre et que les signes négatifs sont bien placés
        text = re.sub(r'\s-', ' -', text)  # Retirer les espaces avant les signes -

        # Supprimer tout tiret supplémentaire à la fin du texte
        text = text.rstrip('-')

        # Gérer les cas où des signes négatifs sont associés à des nombres
        # Assurer une bonne séparation des chiffres négatifs
        numbers = re.findall(r'-?\d+', text)  # Trouver tous les nombres, y compris ceux avec un signe -

        # Afficher les nombres trouvés pour débogage
        print(f"Nombre(s) extrait(s) : {numbers}")
        
        # Toujours garder les deux premiers nombres
        if len(numbers) >= 2:
            return " ".join(numbers[:2])  # Retourner les deux premiers nombres
        else:
            print("Erreur: le texte ne contient pas exactement deux nombres.")
            return ""  # Si ce n'est pas deux nombres, on renvoie une chaîne vide

    # Capture de la position actuelle
    pos_zone_bbox = (6, 71, 87, 97)  # Modifié quator_zone_bbox en pos_zone_bbox
    print(f"Position actuelle : {pos_zone_bbox}")

    # On initialise pos_text comme une chaîne vide pour entrer dans la boucle
    pos_text = ""
    start_time = time.time()  # Commencer le chronomètre
    timeout = 60  # Timeout de 1 minute

    # Répéter la capture toutes les secondes jusqu'à ce que les textes correspondent
    while pos_text != extracted_text:
        pos = capture_zone(*pos_zone_bbox)  # Utilisation de pos_zone_bbox ici
        if not pos:
            print("Erreur de capture de la première zone.")
            return

        try:                    
            # Extraire et nettoyer le texte de la zone d'écran
            pos_text = extract_text_from_screen(pos_zone_bbox)
            
            # Nettoyer le texte extrait
            pos_text = clean_text(pos_text)

            # Afficher le texte extrait nettoyé
            print(f"Texte extrait nettoyé : {pos_text}")

        except Exception as e:
            print(f"Erreur lors de l'extraction du texte de la capture : {str(e)}")
            return


        # Vérification des correspondances
        if pos_text == extracted_text:
            print("Les textes correspondent. Clic sur la position du jalon 6.")
            click(264, 435)  # Nouvelle position pour le sixième indice
            time.sleep(1)
            break

        # Vérifier si 1 minute est écoulée
        if time.time() - start_time > timeout:
            print("Les textes ne correspondent pas dans le temps imparti. Abandon de la chasse au trésor")
            click(274, 173)  # Effectuer le clic après 1 minute
            time.sleep(0.5)
            click(370, 414)
            time.sleep(0.5)
            print("Le programme s'arrête dû à l'abandon de la quête")
            sys.exit()
            break  # Sortir de la boucle après le clic

    # Si la boucle termine sans que les textes ne correspondent, aucun clic n'est effectué.
    if pos_text != extracted_text:
        print("Les textes ne correspondent toujours pas après plusieurs tentatives. Aucun clic effectué.")

    # Clic sur le bouton valider pour passer à l'étape suivante
    click(227, 475)
    close_browser()  # Fermer le navigateur
    time.sleep(2)
    detecter_image_et_lancer_script()

if __name__ == "__main__":
    main()