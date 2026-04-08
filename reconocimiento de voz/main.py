import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

translator = Translator()

# 📂 Diccionario de palabras por nivel
words_by_level = {
    "facil": ["gato", "perro", "manzana", "leche", "sol"],
    "medio": ["banano", "escuela", "amigo", "ventana", "amarillo"],
    "dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}

puntos = 0
errores = 0

print("🎮 BIENVENIDO AL JUEGO DE TRADUCCIÓN 🎮")
print("📚 Niveles disponibles: facil, medio, dificil")

nivel = input("👉 Elige un nivel: ").lower()

if nivel not in words_by_level:
    print("❌ Nivel no válido")
    exit()

while True:
    duration = 5
    sample_rate = 44100

    palabra = random.choice(words_by_level[nivel])

    print("🧠 Traduce esta palabra al INGLÉS:")
    print("👉", palabra)

    # Traducción correcta
    traduccion = translator.translate(palabra, dest="en")
    texto = traduccion.text
    correcta = texto.lower()    
    print("🎤 Habla ahora...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()
    wav.write("output.wav", sample_rate, recording)

    print("⏳ Grabación completa, reconociendo...")

    recognizer = sr.Recognizer()

    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        recognized = recognizer.recognize_google(audio, language="en-US")
        recognized = recognized.lower()

        print("🗣️ Dijiste:", recognized)
        print("📖 Respuesta correcta:", correcta)

        if correcta in recognized:
            puntos += 1
            print("✅ ¡Correcto! +1 punto 🎉")
        else:
            errores += 1
            print("❌ Incorrecto 😢")

        print("⭐ Puntos:", puntos)
        print("💔 Errores:", errores, "/ 3")

    except sr.UnknownValueError:
        errores += 1
        print("😵 No se entendió tu voz.")
    except sr.RequestError as e:
        print("⚠️ Error del servicio:", e)

    # 🛑 Fin del juego
    if errores >= 3:
        print("💀 GAME OVER 💀")
        print("🏆 Puntos finales:", puntos)
        break

    repetir = input("🔁 ¿Quieres seguir jugando? (si/no): ")
    if repetir.lower() != "si":
        print("🏁 Juego finalizado")
        print("🏆 Puntos finales:", puntos)
        break