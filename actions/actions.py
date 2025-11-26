from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionEvaluarTriaje(Action):

    def name(self):
        return "action_evaluar_triaje"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        sintoma = tracker.get_slot("sintoma")

        if not sintoma:
            dispatcher.utter_message(text="No entendí el síntoma. ¿Puedes repetirlo?")
            return []

        # Clasificación simple de gravedad
        sintomas_graves = ["dificultad para respirar", "fiebre", "dolor de pecho"]
        sintomas_medios = ["fatiga", "náuseas", "vómitos", "diarrea", "dolor de cabeza"]
        sintomas_leves = ["congestión nasal", "tos", "dolor de garganta", "mareo", "escalofríos", "dolor abdominal", "pérdida del gusto", "pérdida del olfato"]

        sintoma_normalizado = sintoma.lower()

        if sintoma_normalizado in sintomas_graves:
            prioridad = "ALTA"
            recomendacion = "Atención inmediata. Llame a urgencias o acuda a un hospital."
        elif sintoma_normalizado in sintomas_medios:
            prioridad = "MEDIA"
            recomendacion = "Debe ser evaluado por un médico en las próximas horas."
        elif sintoma_normalizado in sintomas_leves:
            prioridad = "BAJA"
            recomendacion = "Reposo y observación. Consulte si empeora."
        else:
            prioridad = "DESCONOCIDA"
            recomendacion = "No puedo evaluar este síntoma, consulte con un médico."

        dispatcher.utter_message(
            text=f"Síntoma detectado: **{sintoma}**\n"
                 f"Prioridad: **{prioridad}**\n"
                 f"Recomendación: {recomendacion}"
        )

        return []
