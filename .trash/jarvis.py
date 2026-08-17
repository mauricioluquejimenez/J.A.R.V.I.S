from openai import OpenAI
import speech_recognition as sr
import pyttsx3

# Clave para la API de OpenAI
OPEN_AI_API_KEY = "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"

# Configuración del cliente de OpenAI y el modelo
client = OpenAI(api_key = OPEN_AI_API_KEY)
modelo = "gpt-4o"

# Configuración del reconocimiento de voz y mensajes
r = sr.Recognizer()
mensajes = []

# Función para convertir texto a voz mediante la biblioteca pyttsx3
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Función para grabar audio y convertirlo a texto
def record_text():
    while True:
        try:
            with sr.Microphone() as source:
                
                # Ajuste del ruido ambiental para mejorar la precisión del reconocimiento
                r.adjust_for_ambient_noise(source, duration = 0.5)
                print("Escuchando...")
                
                # Escucha el audio y lo convierte a texto
                audio = r.listen(source)
                texto = r.recognize_google(audio, language = 'es-ES')
                
                return texto
        
        except sr.RequestError as e:
            print(f"Error al conectar con el servicio de reconocimiento de voz: {e}")
            return "Error de conexión"
        
        except sr.UnknownValueError:
            print("No se entendió el audio, por favor intenta de nuevo.")

# Función para enviar mensajes a ChatGPT y recibir respuestas
def send_to_chatGPT(mensajes):
    respuesta = client.chat.completions.create(
        model = modelo,
        messages = mensajes,
        max_tokens = 150,
        temperature = 0.7
    )
    
    mensaje = respuesta.choices[0].message.content
    mensajes.append(respuesta.choices[0].message)
    return mensaje

# Bucle principal para grabar audio, enviar a ChatGPT y reproducir la respuesta
while True:
    #Grabar audio
    texto = record_text()
    
    # Convertir el texto en un prompt para ChatGPT
    mensajes.append({"role": "user", "content": texto})
    
    # Enviar mensaje a ChatGPT y guardar la respuesta
    respuesta = send_to_chatGPT(mensajes)
    
    # Reproducir la respuesta
    SpeakText(respuesta)
    
    print(respuesta, end = "\n")