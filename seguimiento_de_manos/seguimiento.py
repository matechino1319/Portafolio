import cv2
import mediapipe as mp
import os
import time
import subprocess 
import pyautogui 

# --- CONFIGURACIÓN DE MEDIAPIPE ---
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

PUNTAS_Y_NUDILLOS = {
    "INDICE": [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP],
    "MEDIO": [mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP],
    "ANULAR": [mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP],
    "MEÑIQUE": [mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP]
}

def is_finger_extended(landmarks, tip_id, pip_id):
    try:
        return landmarks.landmark[tip_id].y < landmarks.landmark[pip_id].y
    except:
        return False

def is_fist_closed(landmarks):
    for dedo in ["INDICE", "MEDIO", "ANULAR", "MEÑIQUE"]:
        tip_id, pip_id = PUNTAS_Y_NUDILLOS[dedo]
        if is_finger_extended(landmarks, tip_id, pip_id):
            return False 
    return True

def is_index_finger_only(landmarks):
    if not is_finger_extended(landmarks, PUNTAS_Y_NUDILLOS["INDICE"][0], PUNTAS_Y_NUDILLOS["INDICE"][1]):
        return False
    for dedo in ["MEDIO", "ANULAR", "MEÑIQUE"]:
        tip_id, pip_id = PUNTAS_Y_NUDILLOS[dedo]
        if is_finger_extended(landmarks, tip_id, pip_id):
            return False
    return True

def cerrar_chrome_totalmente():
    try:
        subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], check=True, capture_output=True)
        return True
    except:
        return False

def press_key_and_report(key, action_text, image):
    pyautogui.press(key)
    cv2.putText(image, action_text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
    return True

# --- BUCLE PRINCIPAL ---
cap = cv2.VideoCapture(0)
CHROME_ABIERTO = False
YOUTUBE_ABIERTO = False
ULTIMO_TIEMPO_ACCION = 0 
COOLDOWN_TIEMPO = 2 

URL_YOUTUBE = "https://www.youtube.com/watch?v=SMXU0yoggrk&list=RDSMXU0yoggrk&start_radio=1"
URL_CHROME = "https://www.google.com/" 

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success: continue

        image = cv2.flip(image, 1) # Espejo para que sea más natural
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        
        right_fist = False
        left_fist = False
        right_index = False
        left_index = False
        
        tiempo_actual = time.time()
        
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_type = handedness.classification[0].label 
                
                # Detectar estados por mano
                if hand_type == 'Right':
                    right_fist = is_fist_closed(hand_landmarks)
                    right_index = is_index_finger_only(hand_landmarks)
                else:
                    left_fist = is_fist_closed(hand_landmarks)
                    left_index = is_index_finger_only(hand_landmarks)
                
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # --- LÓGICA DE CONTROL ---
        if (tiempo_actual - ULTIMO_TIEMPO_ACCION) > COOLDOWN_TIEMPO:
            
            # 1. TOGGLE YOUTUBE: Ambos índices extendidos (Prioridad Absoluta)
            if right_index and left_index:
                if not YOUTUBE_ABIERTO:
                    os.system(f'start chrome "{URL_YOUTUBE}"')
                    YOUTUBE_ABIERTO = True
                    CHROME_ABIERTO = False # Resetear estado de Google simple
                    print(">>> YouTube Abierto")
                else:
                    cerrar_chrome_totalmente()
                    YOUTUBE_ABIERTO = False
                    print(">>> YouTube Cerrado")
                ULTIMO_TIEMPO_ACCION = tiempo_actual

            # 2. ACCIONES DENTRO DE YOUTUBE (Solo si YouTube está activo)
            elif YOUTUBE_ABIERTO:
                if right_fist and left_fist:
                    press_key_and_report('k', "PLAY/PAUSE", image)
                    ULTIMO_TIEMPO_ACCION = tiempo_actual
                elif right_fist:
                    press_key_and_report('l', "ADELANTAR 10s", image)
                    ULTIMO_TIEMPO_ACCION = tiempo_actual
                elif left_fist:
                    press_key_and_report('j', "RETRASAR 10s", image)
                    ULTIMO_TIEMPO_ACCION = tiempo_actual

            # 3. TOGGLE GOOGLE: Solo si YouTube está cerrado (Para evitar conflictos con adelantar/atrasar)
            elif not YOUTUBE_ABIERTO:
                if right_fist:
                    if not CHROME_ABIERTO:
                        os.system(f'start chrome "{URL_CHROME}"')
                        CHROME_ABIERTO = True
                    else:
                        cerrar_chrome_totalmente()
                        CHROME_ABIERTO = False
                    ULTIMO_TIEMPO_ACCION = tiempo_actual

        # --- Interfaz en pantalla ---
        color_yt = (0, 255, 0) if YOUTUBE_ABIERTO else (0, 0, 255)
        color_gg = (255, 0, 0) if CHROME_ABIERTO else (0, 0, 255)
        cv2.putText(image, f"YouTube (2 indices): {'SI' if YOUTUBE_ABIERTO else 'NO'}", (10, 30), 1, 1.5, color_yt, 2)
        cv2.putText(image, f"Google (1 punio): {'SI' if CHROME_ABIERTO else 'NO'}", (10, 70), 1, 1.5, color_gg, 2)

        cv2.imshow('Control Gestual Dual', image)
        if cv2.waitKey(5) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()