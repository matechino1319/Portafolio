import requests
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import calendar
from collections import defaultdict

API_KEY = "LEYXF4Q6Z4E3Y2BLQT9RQ9ATL"

ubicacion = "San Rafael, Mendoza Province, Argentina"

CURRENT_YEAR = datetime.now().year
YEAR_RANGE = list(range(2010, CURRENT_YEAR + 1))

meses_a_numeros = {
    "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
    "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}

def mostrar_grafico():
    """Función que se ejecuta al presionar el botón."""
    mes_str = combo_meses.get()
    year_str = combo_anios.get()
    
    if mes_str not in meses_a_numeros:
        mensaje_label.config(text="Por favor, selecciona un mes válido.", foreground="red")
        return
        
    try:
        YEAR = int(year_str)
    except ValueError:
        mensaje_label.config(text="Por favor, selecciona un año válido.", foreground="red")
        return

    mes_num = meses_a_numeros[mes_str]
    mensaje_label.config(text=f"Buscando datos meteorológicos para {mes_str} de {YEAR} en San Rafael...", foreground="blue")
    alerta_granizo_label.config(text="") 
    
    root.update()

    try:
        start_date = datetime(YEAR, mes_num, 1).strftime("%Y-%m-%d")
        _, ultimo_dia = calendar.monthrange(YEAR, mes_num)
        end_date = datetime(YEAR, mes_num, ultimo_dia).strftime("%Y-%m-%d")
        
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{ubicacion}/{start_date}/{end_date}?unitGroup=metric&key={API_KEY}&include=days&elements=precip,humidity,preciptype,precipprob"

        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        lluvia_por_dia = []
        humedad_por_dia = []
        prob_lluvia_por_dia = []
        dias_del_mes = []
        dias_con_granizo = {}

        if "days" in data:
            for i, dia in enumerate(data["days"]):
                lluvia_diaria = dia.get("precip", 0)
                humedad_diaria = dia.get("humidity", 0)
                probabilidad_diaria = dia.get("precipprob", 0)
                preciptype_diario = dia.get("preciptype", [])

                lluvia_por_dia.append(lluvia_diaria)
                humedad_por_dia.append(humedad_diaria)
                prob_lluvia_por_dia.append(probabilidad_diaria)
                dias_del_mes.append(i + 1)
    
                if isinstance(preciptype_diario, str):
                    if 'hail' in preciptype_diario:
                        dias_con_granizo[str(i + 1)] = probabilidad_diaria
                elif isinstance(preciptype_diario, list):
                    if 'hail' in preciptype_diario:
                        dias_con_granizo[str(i + 1)] = probabilidad_diaria
        
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color_lluvia = 'tab:blue'
        ax1.set_xlabel("Día del mes", fontsize=12, color='gray')
        ax1.set_ylabel("Lluvia (mm)", fontsize=12, color=color_lluvia)
        ax1.plot(dias_del_mes, lluvia_por_dia, marker='o', linestyle='-', color=color_lluvia, label='Lluvia')
        ax1.tick_params(axis='y', labelcolor=color_lluvia)
        ax1.set_ylim(bottom=0)
        ax1.fill_between(dias_del_mes, lluvia_por_dia, color=color_lluvia, alpha=0.3)

        ax2 = ax1.twinx()
        color_humedad = 'tab:orange'
        ax2.set_ylabel("Humedad (%)", fontsize=12, color=color_humedad)
        ax2.plot(dias_del_mes, humedad_por_dia, marker='s', linestyle='--', color=color_humedad, label='Humedad')
        ax2.tick_params(axis='y', labelcolor=color_humedad)
        ax2.set_ylim(0, 100)
        
        fig.suptitle(f"Lluvia y Humedad diaria en San Rafael ({mes_str} de {YEAR})", fontsize=16, color='darkblue')
        fig.legend(loc="upper left", bbox_to_anchor=(0.15, 0.9))

        ax1.set_xticks(dias_del_mes)
        ax1.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

        total_lluvia_mes = sum(lluvia_por_dia)
        if dias_con_granizo:
            dias_str = ", ".join([f"{d} ({p}%)" for d, p in dias_con_granizo.items()])
            alerta_granizo_label.config(text=f"¡ALERTA! Granizo pronosticado para los días: {dias_str}.", foreground="red")
        
        if total_lluvia_mes > 0:
            mensaje_label.config(text=f"La lluvia total en {mes_str} de {YEAR} fue de {total_lluvia_mes:.2f} mm. "
                                        f"Probabilidad de lluvia promedio del mes: {sum(prob_lluvia_por_dia) / len(prob_lluvia_por_dia):.1f}%.", foreground="green")
        else:
            mensaje_label.config(text=f"No se registró lluvia en {mes_str} de {YEAR}.", foreground="orange")

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            mensaje_label.config(text="Error 401: Clave de API inválida. Revisa tu clave.", foreground="red")
        else:
            mensaje_label.config(text=f"Error de HTTP: {err}", foreground="red")
    except requests.exceptions.RequestException as err:
        mensaje_label.config(text=f"Error de conexión: {err}", foreground="red")
    except Exception as e:
        mensaje_label.config(text=f"Ocurrió un error inesperado: {e}", foreground="red")
root = tk.Tk()
root.title(f"Pronóstico Agrícola - San Rafael")
root.geometry("800x600")
root.resizable(False, False)

frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

label_instrucciones = ttk.Label(frame, text="Selecciona el mes y año:", font=("Arial", 12))
label_instrucciones.pack(pady=10)

combo_frame = ttk.Frame(frame)
combo_frame.pack()

label_anios = ttk.Label(combo_frame, text="Año:")
label_anios.pack(side="left", padx=(0, 5))
combo_anios = ttk.Combobox(combo_frame, values=YEAR_RANGE, state="readonly", width=8)
combo_anios.pack(side="left", padx=(0, 15))
combo_anios.set(CURRENT_YEAR)

label_meses = ttk.Label(combo_frame, text="Mes:")
label_meses.pack(side="left", padx=(0, 5))
combo_meses = ttk.Combobox(combo_frame, values=list(meses_a_numeros.keys()), state="readonly", width=12)
combo_meses.pack(side="left")
combo_meses.set("Enero")

boton_graficar = ttk.Button(frame, text="Mostrar Gráfico", command=mostrar_grafico)
boton_graficar.pack(pady=15)

alerta_granizo_label = ttk.Label(frame, text="", font=("Arial", 10, "bold"))
alerta_granizo_label.pack(pady=5)

mensaje_label = ttk.Label(frame, text="", font=("Arial", 10))
mensaje_label.pack(pady=5)

root.mainloop()