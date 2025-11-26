# Comandos Rápidos


## 1. Entrenar el modelo
Ejecuta el entrenamiento del modelo de Rasa:

```bash
docker compose run --rm rasa train
```
## 2. Ejecutar el chatbot en modo interactivo
Una vez entrenado el modelo, puedes iniciar el contenedor y conversar con tu asistente:
```bash
docker compose run --rm rasa shell
```

## 3. Actualizar el docker compose

```bash
docker compose down
docker compose up -d --build
docker compose run --rm rasa action_server
```