from PIL import ImageGrab, Image
import pytesseract
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

pyautogui.FAILSAFE = False

# Chemin vers Tesseract (modifiez si nécessaire)
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'

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

    # Logique pour lancer les scripts en fonction du nombre de correspondances
    if num_matches == 5:
        print("5 correspondances détectées, lancement de step6_treasure...")
        subprocess.run(["python", "treasure_6.py"])  # Remplace par ton script exact
    elif num_matches == 4:
        print("4 correspondances détectées, lancement de step5_treasure...")
        subprocess.run(["python", "treasure_5.py"])  # Remplace par ton script exact
    elif num_matches == 3:
        print("3 correspondances détectées, lancement de step4_treasure...")
        subprocess.run(["python", "treasure_4.py"])  # Remplace par ton script exact
    elif num_matches == 2:
        print("2 correspondances détectées, lancement de 3step_treasure...")
        subprocess.run(["python", "treasure_3.py"])  # Remplace par ton script exact
    elif num_matches == 1:
        print("1 correspondances détectées, lancement de step2_treasure...")
        subprocess.run(["python", "treasure_2.py"])  # Remplace par ton script exact
    else:
        print(f"Aucune action pour {num_matches} correspondances.")

# Fonction de pré-traitement de l'image (conversion en noir et blanc)
def preprocess_image(image):
    """Effectue un pré-traitement de l'image en la convertissant en noir et blanc."""
    grayscale_image = image.convert("L")
    threshold = 128  # Seuil de binarisation
    binarized_image = grayscale_image.point(lambda p: p > threshold and 255)
    return binarized_image

def click(x, y):
    """Simule un clic à une position donnée."""
    print(f"Clic aux coordonnées : ({x}, {y})")
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()

def double_click(x, y):
    """Simule un double clic à une position donnée."""
    print(f"Double clic aux coordonnées : ({x}, {y})")
    pyautogui.moveTo(x, y)
    pyautogui.click(clicks=2, interval=0.25)

def capture_zone(left, top, right, bottom):
    """Capture une zone spécifique de l'écran."""
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    if left < 0 or top < 0 or right > screen_width or bottom > screen_height:
        print("Erreur : La zone dépasse les limites de l'écran.")
        return None
    
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    return screenshot

def get_text_from_image(image):
    """Utilise l'OCR pour extraire du texte d'une image."""
    image = preprocess_image(image)
    text = pytesseract.image_to_string(image, lang='eng')
    return text.strip()

def extract_coordinates(text):
    """Extrait les coordonnées sous forme de (x, y) à partir du texte OCR."""
    positions = []
    matches = re.findall(r'\[(-?\d+),(-?\d+)\]', text)
    for match in matches:
        try:
            x, y = map(int, match)
            positions.append((x, y))
        except ValueError:
            continue
    return positions

def manhattan_distance(pos1, pos2):
    """Calcule la distance de Manhattan entre deux points (x1, y1) et (x2, y2)."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def find_closest_zaap(memory_coords, zaaps_dict):
    """Trouve le Zaap le plus proche à partir du dictionnaire des Zaaps."""
    closest_zaap = None
    min_distance = float('inf')

    for zaap_name, zaap_coords in zaaps_dict.items():
        distance = manhattan_distance(memory_coords, zaap_coords)
        if distance < min_distance:
            min_distance = distance
            closest_zaap = (zaap_name, zaap_coords)

    return closest_zaap

def main():
    print("Démarrage du script.")
    time.sleep(2)  # Pause avant de capturer la première zone

    # Capture de la première zone pour récupérer la position initiale
    first_zone_bbox = (95, 207, 170, 252)
    print(f"Capture de la première zone : {first_zone_bbox}")
    image = capture_zone(*first_zone_bbox)

    if image:
        text = get_text_from_image(image)
        print(f"Texte extrait : {text}")

        try:
            clean_text = text.replace("[", "").replace("]", "").replace(" ", "")
            x, y = map(int, clean_text.split(","))
            memory_coords = (x, y)
            print(f"Coordonnées mémorisées : {memory_coords}")
        except ValueError:
            print("Erreur lors de la lecture des coordonnées.")
            return

        # Dictionnaire des Zaaps avec leurs coordonnées dans le jeu
        zaaps_dict = {
            "Château d'Amakna": (3, -5),
            "Port de Madrestam": (7, -4),
            "Cité d'Astrub": (5, -18),
            "Sufokia": (13, 26),
            "Immaculé": (-31, -56),
            "La Cuirasse": (-26, 37),
            "Foire du Trool": (-11, -36),
            "Massif de Cania": (-13, -28),
            "Village d'Amakna": (-2, 0),
        }

        # Premier clic (si besoin)
        click(1821, 221)
        print("Premier clic effectué.")

        # Attente avant le deuxième clic
        time.sleep(0.5)
        click(532, 380)
        print("Deuxième clic effectué.")
        # Recherche du Zaap le plus proche
        closest_zaap = find_closest_zaap(memory_coords, zaaps_dict)

        if closest_zaap:
            zaap_name, zaap_coords = closest_zaap
            print(f"Zaap le plus proche trouvé : {zaap_name} à {zaap_coords}")

            # Copier dynamiquement le nom du Zaap dans le presse-papiers
            pyperclip.copy(zaap_name)
            pyautogui.hotkey("ctrl", "v")  # Coller le texte
            print(f"Nom du Zaap écrit : {zaap_name}")

            # Double clic pour valider
            double_click(740, 420)
            print(f"Double clic effectué pour valider.")
        else:
            print("Aucun Zaap trouvé ou problème dans la détection.")
    else:
        print("Erreur lors de la capture de la première zone.")

    detecter_image_et_lancer_script()
if __name__ == "__main__":
    main()
