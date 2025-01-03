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
import sys

pyautogui.FAILSAFE = False

# Chemin vers Tesseract (modifiez si nécessaire)
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'

def get_resource_path(relative_path):
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Erreur lors de la récupération du chemin : {e}")
        return None

def detecter_image_et_lancer_script():
    # Capturer une zone de l'écran pour traitement
    zone = (15, 299, 83, 454)
    screenshot = pyautogui.screenshot(region=zone)
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Charger l'image de référence pour la correspondance
    template_path = get_resource_path("refereindice.png")
    if template_path is None:
        print("Erreur : le chemin de l'image de référence est invalide.")
        return
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Erreur : l'image de référence {template_path} n'a pas pu être chargée.")
        return
    print("L'image de référence a été chargée avec succès.")
    
    # Convertir l'image en niveaux de gris pour la correspondance
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    locations = np.where(result >= threshold)
    num_matches = len(locations[0])
    print(f"Nombre de correspondances détectées : {num_matches}")
    
    # Dessiner des rectangles autour des correspondances trouvées
    for pt in zip(*locations[::-1]):
        cv2.rectangle(image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)
    
    # Une fois toutes les correspondances effectuées, lancer le script approprié en fonction du nombre de correspondances
    if num_matches == 5:
        script_name = "treasure_6.py"
    elif num_matches == 4:
        script_name = "treasure_5.py"
    elif num_matches == 3:
        script_name = "treasure_4.py"
    elif num_matches == 2:
        script_name = "treasure_3.py"
    elif num_matches == 1:
        script_name = "treasure_2.py"
    else:
        print(f"Aucune action pour {num_matches} correspondances.")
        script_name = None

    # Si un script a été sélectionné
    if script_name:
        # Utiliser get_resource_path pour obtenir le chemin complet du script
        script_path = get_resource_path(script_name)

        # Vérifier si le fichier existe
        if script_path and os.path.exists(script_path):
            print(f"Correspondance trouvée, lancement de {script_name}...")
            # Lancer le script correspondant
            subprocess.run(["python", script_path])
        else:
            print(f"Erreur : Le fichier {script_name} est introuvable.")

def preprocess_image(image):
    grayscale_image = image.convert("L")
    threshold = 128
    binarized_image = grayscale_image.point(lambda p: p > threshold and 255)
    return binarized_image

def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()

def double_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(clicks=2, interval=0.25)

def capture_zone(left, top, right, bottom):
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    if left < 0 or top < 0 or right > screen_width or bottom > screen_height:
        print("Erreur : La zone dépasse les limites de l'écran.")
        return None
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    return screenshot

def get_text_from_image(image):
    image = preprocess_image(image)
    text = pytesseract.image_to_string(image, lang='eng')
    return text.strip()

def extract_coordinates(text):
    positions = []
    matches = re.findall(r'\[-?\d+, -?\d+\]', text)
    for match in matches:
        try:
            x, y = map(int, match)
            positions.append((x, y))
        except ValueError:
            continue
    return positions

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def find_closest_zaap(memory_coords, zaaps_dict):
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
    time.sleep(2)
    
    # Capture initiale de la zone
    first_zone_bbox = (95, 207, 170, 252)
    image = capture_zone(*first_zone_bbox)
    if image:
        text = get_text_from_image(image)
        clean_text = text.replace("[", "").replace("]", "").replace(" ", "")
        try:
            x, y = map(int, clean_text.split(","))
            memory_coords = (x, y)
        except ValueError:
            print("Erreur lors de la lecture des coordonnées.")
            return
        zaaps_dict = {"Château d'Amakna": (3, -5)}
        click(1821, 221)
        time.sleep(0.5)
        click(532, 380)
        closest_zaap = find_closest_zaap(memory_coords, zaaps_dict)
        if closest_zaap:
            zaap_name, _ = closest_zaap
            pyperclip.copy(zaap_name)
            pyautogui.hotkey("ctrl", "v")
            double_click(740, 420)
        else:
            print("Aucun Zaap trouvé.")
    detecter_image_et_lancer_script()

if __name__ == "__main__":
    main()
