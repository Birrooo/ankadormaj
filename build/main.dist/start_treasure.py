import ctypes
import time
import win32gui
import win32con
import keyboard
import pyautogui
import subprocess  # Pour lancer des scripts

# Reste des fonctions pour l'automatisation du clic
def find_dofus_window():
    """Trouve la fenêtre Dofus qui contient 'Release' dans son titre"""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Release" in title:  # Identifier la fenêtre Dofus par son titre
                windows.append(hwnd)
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if not windows:
        raise Exception("Fenêtre Dofus non trouvée")
    
    return windows[0]  # Retourne le handle de la première fenêtre trouvée

def set_foreground_window(hwnd):
    """Met la fenêtre Dofus au premier plan"""
    win32gui.SetForegroundWindow(hwnd)
    print("Fenêtre Dofus mise au premier plan.")

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

def double_click(x, y):
    """Simule un double-clic à la position spécifiée"""
    click(x, y)  # Premier clic
    time.sleep(0.1)  # Petit délai entre les deux clics
    click(x, y)  # Deuxième clic
    print(f"Double-clic effectué aux coordonnées : {x}, {y}")

def check_ctrl_key():
    """Vérifie si CTRL est maintenu pendant 5 secondes pour arrêter le programme"""
    start_time = time.time()
    
    while True:
        if keyboard.is_pressed('ctrl'):
            print("\nTouche CTRL détectée. Maintenir pendant 5 secondes pour arrêter...")
            
            # Vérifie si CTRL est maintenu pendant 5 secondes
            while keyboard.is_pressed('ctrl') and time.time() - start_time < 5:
                remaining = 5 - (time.time() - start_time)
                print(f"\rTemps restant: {remaining:.1f} secondes", end='')
                time.sleep(0.1)
            
            # Si la touche a été maintenue pendant 5 secondes, on arrête le programme
            if time.time() - start_time >= 5:
                print("\nArrêt du programme...")
                break
        time.sleep(0.1)

def write_text(text):
    """Simule la saisie d'un texte"""
    pyautogui.write(text)
    print(f"Texte '{text}' écrit dans la fenêtre Dofus")

def main():
    print("Démarrage du programme de clic automatique pour Dofus")
    print("Maintenez CTRL pendant 5 secondes pour arrêter le programme")
    
    try:
        # Trouver la fenêtre Dofus
        hwnd = find_dofus_window()

        # Mettre la fenêtre Dofus au premier plan
        set_foreground_window(hwnd)
        
        # Attendre un peu pour être sûr que la fenêtre est en premier plan
        time.sleep(1)

        # Commencer les clics et autres actions automatisées
        click(1821, 221)
        time.sleep(0.5)
        click(532, 380)
        time.sleep(0.5)
        write_text("champs de cania")
        time.sleep(0.5)
        double_click(740, 420)
        time.sleep(1.5)
        click(1766, 445)
        time.sleep(3)
        click(1766, 445)
        time.sleep(4)
        click(1004, 509)
        time.sleep(3)
        click(1454, 455)
        time.sleep(4)
        click(1041, 466)
        time.sleep(1)
        click(1074, 509)
        time.sleep(6)
        click(327, 834)
        time.sleep(5)
        click(545, 833)
        time.sleep(3)

        # Une fois tous les clics terminés, lancer le script zaap.py
        print("Tous les clics terminés, lancement de go_zaap.py...")
        subprocess.run(["python", "go_zaap.py"])

    except Exception as e:
        print(f"Erreur : {e}")
    
    # Attendre l'arrêt du programme si CTRL est maintenu
    check_ctrl_key()
    
    print("Programme arrêté avec succès")

if __name__ == "__main__":
    main()
