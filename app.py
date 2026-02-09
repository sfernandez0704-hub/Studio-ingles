from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

temas = {
    "past simple": [
        {
            "ejemplo": "Example: I played with my friends yesterday / play",
            "frase": "She (____) for the exam yesterday. / study",
            "respuesta": "studied"
        },
        {
            "ejemplo": "Example: I worked with my father last night / work",
            "frase": "They (____) a movie last night. / watch",
            "respuesta": "watched"
        },
        {
            "ejemplo": "Example: I was tired yesterday / be",
            "frase": "I (____) very tired yesterday. / be",
            "respuesta": "was"
        }
    ],

    "present simple": [
        {
            "ejemplo": "Example: I study after school / study",
            "frase": "She (____) coffee every morning. / drink",
            "respuesta": "drinks"
        },
        {
            "ejemplo": "Example: He works for his family / work",
            "frase": "They (____) football on Sundays. / play",
            "respuesta": "play"
        }
    ],

    "present continuous": [
        {
            "ejemplo": "Example: I am playing football / play",
            "frase": "She (____) now. / study",
            "respuesta": "is studying"
        },
        {
            "ejemplo": "Example: He is reading a book / read",
            "frase": "They (____) TV at the moment. / watch",
            "respuesta": "are watching"
        }
    ],

    "future will": [
        {
            "ejemplo": "Example: I will play with you / play",
            "frase": "I (____) call you later. / call",
            "respuesta": "will"
        },
        {
            "ejemplo": "Example: He will study later",
            "frase": "She (____) help you tomorrow. / help",
            "respuesta": "will"
        }
    ],

    "going to": [
        {
            "ejemplo": "Example: She is going to study / go",
            "frase": "I am (____) travel next week. / go",
            "respuesta": "going to"
        },
        {
            "ejemplo": "Example: We are going to travel / go",
            "frase": "They are (____) buy a car. / buy",
            "respuesta": "going to"
        }
    ]
}

info_temas = """
📘 GRAMMAR GUIDE

🔹 Past Simple
Se usa para acciones terminadas en el pasado.
Ejemplo: I studied yesterday.

🔹 Present Simple
Se usa para rutinas y hábitos.
Ejemplo: She drinks coffee every morning.

🔹 Present Continuous
Se usa para acciones que están ocurriendo ahora.
Ejemplo: She is studying now.

🔹 Future Will
Se usa para decisiones espontáneas y promesas.
Ejemplo: I will call you later.

🔹 Going To
Se usa para planes ya decididos.
Ejemplo: I am going to travel next week.
"""

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/recibir", methods=["POST"])
def recibir():
    texto = request.json["texto"].strip().lower()

    if texto == "info":
        return jsonify({"respuesta": info_temas})
 

    if not hasattr(recibir, "tema"):
        recibir.tema = None
    if not hasattr(recibir, "indice"):
        recibir.indice = 0
    if not hasattr(recibir, "esperando_respuesta"):
        recibir.esperando_respuesta = False

    # === ELEGIR TEMA ===
    if texto in temas and not recibir.esperando_respuesta:
        recibir.tema = texto
        recibir.indice = 0
        recibir.esperando_respuesta = True

        pregunta_actual = temas[recibir.tema][recibir.indice]
        respuesta = (
            pregunta_actual.get("ejemplo", "") + "\n\n"
            + "Completa la frase:\n"
            + pregunta_actual["frase"]
        )

    # === RESPONDER ===
    elif recibir.esperando_respuesta:
        pregunta_actual = temas[recibir.tema][recibir.indice]

        if texto == pregunta_actual["respuesta"]:
            recibir.indice += 1

            if recibir.indice < len(temas[recibir.tema]):
                siguiente = temas[recibir.tema][recibir.indice]
                respuesta = (
                    "✅ Correcto!\n\n"
                    + siguiente.get("ejemplo", "") + "\n"
                    + "Completa la frase:\n"
                    + siguiente["frase"]
                )
            else:
                respuesta = "🎉 Excelente! Terminaste todas las preguntas."
                recibir.esperando_respuesta = False
                recibir.indice = 0
                recibir.tema = None
        else:
            respuesta = (
                "❌ Incorrecto. Try again.\n\n"
                + pregunta_actual.get("ejemplo", "") + "\n"
                + "Completa la frase:\n"
                + pregunta_actual["frase"]
            )

    # === TEXTO NO VÁLIDO ===
    else:
        respuesta = "Tema no válido. Opciones:\n" + ", ".join(temas.keys())

    return jsonify({"respuesta": respuesta})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



