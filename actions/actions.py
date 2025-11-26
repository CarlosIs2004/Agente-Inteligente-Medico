from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os

class ActionTriajeCompleto(Action):

    def name(self) -> str:
        return "action_triaje_completo"

    def run(self, dispatcher, tracker, domain):

        # Ruta del archivo sintomas.txt
        acciones_dir = os.path.dirname(__file__)
        sintomas_path = os.path.join(acciones_dir, "sintomas.txt")

        # Verificar si existe
        if not os.path.exists(sintomas_path):
            dispatcher.utter_message(text="No hay síntomas registrados.")
            return []

        # Leer síntomas
        with open(sintomas_path, "r", encoding="utf-8") as f:
            sintomas_lista = [s.strip() for s in f.readlines() if s.strip()]

        if not sintomas_lista:
            dispatcher.utter_message(text="No se ha registrado ningún síntoma.")
            return []

        # Listas referencia
        sintomas_graves = ["dificultad para respirar", "fiebre", "dolor de pecho"]
        sintomas_medios = ["fatiga", "náuseas", "vómitos", "diarrea", "dolor de cabeza"]
        sintomas_leves = [
            "congestión nasal", "tos", "dolor de garganta", "mareo",
            "escalofríos", "dolor abdominal", "pérdida del gusto", "pérdida del olfato"
        ]

        # Contadores
        total_graves = 0
        total_medios = 0
        total_leves = 0

        for sintoma in sintomas_lista:
            sin = sintoma.lower()

            if sin in sintomas_graves:
                total_graves += 1
            elif sin in sintomas_medios:
                total_medios += 1
            elif sin in sintomas_leves:
                total_leves += 1

        # --- Evaluación final global ---
        if total_graves > 0:
            prioridad = "ALTA"
            recomendacion = "Atención inmediata. Se recomienda ser atendido de forma inmediata."
        elif total_medios > 0:
            prioridad = "MEDIA"
            recomendacion = "Atención media. Se debe consultar con un médico en las próximas horas."
        else:
            prioridad = "BAJA"
            recomendacion = "Reposo y observación. Mantente atento a cualquier cambio."

        # Construcción del reporte final
        reporte = (
            "**Evaluación médica completa según tus síntomas:**\n\n"
            f"Síntomas reportados: {', '.join(sintomas_lista)}\n\n"
            f"Prioridad del caso: **{prioridad}**\n"
            f"Recomendación: {recomendacion}\n"
        )

        dispatcher.utter_message(text=reporte)

        # Limpiar archivo después del triaje
        with open(sintomas_path, "w", encoding="utf-8") as f:
            f.write("")

        return []


class ActionGuardarSintoma(Action):

    def name(self) -> str:
        return "action_guardar_sintoma"

    def run(self, dispatcher, tracker, domain):
        sintoma = tracker.get_slot("sintoma")

        # Guardar en archivo dentro de la carpeta de acciones (montada en el host)
        acciones_dir = os.path.dirname(__file__)
        sintomas_path = os.path.join(acciones_dir, "sintomas.txt")
        with open(sintomas_path, "a", encoding="utf-8") as f:
            f.write(f"{sintoma}\n")

        # La respuesta al usuario está gestionada por la plantilla `utter_register_sintoma`
        # para evitar mensajes duplicados. Esta acción sólo guarda el síntoma.
        return []
