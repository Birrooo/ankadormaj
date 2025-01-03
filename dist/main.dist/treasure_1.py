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
from selenium.webdriver.support import expected_conditions as EC
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

# Fonction pour obtenir le chemin correct des ressources
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # Si l'exécutable est en cours d'exécution
        base_path = sys._MEIPASS  # Dossier temporaire d'extraction
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Fonction principale pour détecter l'image et lancer un script
def detecter_image_et_lancer_script():
    zone = (15, 299, 83, 454)
    screenshot = pyautogui.screenshot(region=zone)
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Charger l'image de référence
    template_path = get_resource_path('refereindice.png')
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    locations = np.where(result >= threshold)
    num_matches = len(locations[0])

    print(f"Nombre de correspondances détectées : {num_matches}")

    for pt in zip(*locations[::-1]):
        cv2.rectangle(image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

    capture_box = (128, 273, 290, 367)

    try:
        # Sélection du script à exécuter en fonction du nombre de correspondances
        if num_matches == 5:
            script_name = 'treasure_6.py'
        elif num_matches == 4:
            script_name = 'treasure_5.py'
        elif num_matches == 3:
            script_name = 'treasure_4.py'
        elif num_matches == 2:
            script_name = 'treasure_3.py'
        elif num_matches == 1:
            script_name = 'treasure_2.py'
        else:
            # Capture d'écran pour détecter l'image "combat.png"
            screenshot = ImageGrab.grab(bbox=capture_box)
            reference_image = get_resource_path("img/combat.png")
            print("Recherche de l'image de référence combat.png...")
            
            # Recherche dynamique dans le répertoire temporaire
            location = pyautogui.locateOnScreen(reference_image, confidence=0.8)

            if location:
                script_name = 'combat.py'
            else:
                script_name = 'treasure_1.py'

        # Obtenir le chemin du script sélectionné
        script_path = get_resource_path(script_name)

        # Vérification de l'existence du script et exécution
        if os.path.exists(script_path):
            print(f"Lancement du script : {script_name}")
            subprocess.run([sys.executable, script_path])  # Utilisation de sys.executable pour garantir la bonne version de Python
        else:
            print(f"Erreur : Le script {script_path} est introuvable.")

    except Exception as e:
        print(f"Erreur : {e}")


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
    
    # Spécifier l'emplacement de Brave (le chemin de l'exécutable)
    options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    
    # **Changer l'empreinte du navigateur** : Modifier l'user-agent pour simuler un autre navigateur
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # **Masquer les propriétés WebDriver** pour éviter la détection
    options.add_argument("--disable-blink-features=AutomationControlled")  # Masque l'indicateur WebDriver
    
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
        
        # Trouver la case à cocher
        checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.q-checkbox__inner.relative-position.non-selectable.q-checkbox__inner--falsy')))
        
        # Vérifier si la case est cochée. Si ce n'est pas le cas, cliquez pour la cocher.
        if 'q-checkbox__inner--falsy' in checkbox.get_attribute('class'):
            print("La case n'est pas cochée, on va la cocher.")
            checkbox.click()
        else:
            print("La case est déjà cochée.")
        
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

        # Utilisation de get_resource_path pour obtenir le bon chemin vers start_treasure.py
        start_treasure_path = get_resource_path('start_treasure.py')

        # Vérifier si le fichier start_treasure.py existe
        if os.path.exists(start_treasure_path):
            subprocess.Popen(["python", start_treasure_path])  # Lancer le script avec le chemin correct
        else:
            print(f"Erreur : Le fichier {start_treasure_path} est introuvable.")

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

    # Clic sur le bouton valider pour passer à l'étape suivante
    click(227, 327)
    close_browser()  # Fermer le navigateur
    time.sleep(2)
    detecter_image_et_lancer_script()

if __name__ == "__main__":
    main()