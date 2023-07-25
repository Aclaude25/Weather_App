#%%writefile app.py
import streamlit as st
import requests
import speech_recognition as sr
from gtts import gTTS
# from IPython.display import Audio
from io import BytesIO

# Fonction pour générer la synthèse vocale et jouer l'audio
def text_to_speech(text):
    tts = gTTS(text, lang="fr")
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    return audio_stream


def transcribe_speech():
    # Initialisation
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        st.info("Je vous écoute...")
        # Stockage de la parole dans la variable audio_text
        audio_text = r.listen(source)
        st.info("Transcryption en cours...")

        try:
            text = r.recognize_google(audio_text)
            return text
        except sr.UnknownValueError:
            return "Désolé, je n'ai pas compris votre discours."
        except sr.RequestError:
            return "Désolé, il y a eu un problème avec le service de reconnaissance vocale."

def bot_response(nom_ville):
  """
    Cette fonction prend le nom d'un ville et renvoie un tuple contenant la température, la vitesse du vent et le taux d'humidité actuelle de cette ville.

    Args:
        nom_ville (str): Nom d'une ville

    Returns:
        tuple: température en °C, vitesse en m/s, taux d'humidité en %
  """
  api_key = "e07b4825969e591497152aa44223274d"
  base_url = "http://api.openweathermap.org/data/2.5/weather?"
  units = "metrics" # "metric" pour des unités en Celsius, "imperial" pour Fahrenheit, ou "standard" pour Kelvin

  complete_url = f"{base_url}q={nom_ville}&units={units}&appid={api_key}"

  response = requests.get(complete_url)
  weather_data = response.json()

  if weather_data["cod"] == 200:  # Vérifier si la requête a réussi (code 200)
      temperature = weather_data["main"]["temp"] # °C
      wind_speed = weather_data["wind"]["speed"] # m/s
      humidity = weather_data["main"]["humidity"] # %
      return (temperature, wind_speed, humidity)
  else:
      return "Echec"


# Étape 1: Message de bienvenue et introduction au chatbot
st.title("Application de prévision météorologique avec Chatbot")
st.write("Bienvenue ! Je suis un chatbot météo. Entrez le nom de la ville pour obtenir la météo.")

# Entrée de l'utilisateur
user_input = st.chat_input("Abidjan")

# Historique des conversations
chat_history = []

if user_input:
  st.write(f'User# {user_input}')
  response = bot_response(user_input)
  #st.write(response)
  chat_history.append({"user_message": user_input, "bot_message": bot_response})
  temperature = response[0]
  wind_speed = response[1]
  humidity = response[2]
  vocal_response = f"""Voici les données méteorologiques de la ville de {user_input}.
                      La température est de {temperature}dégré celsius, La vitesse du vent est de {wind_speed} mètres par seconde
                      et le taux d'humidité est de {humidity}%"""
  # Réponse écrite
  if response != "Echec":
    audio_stream = text_to_speech(vocal_response)
    st.write(f'Données Météorologiques de la ville de {user_input}')
    st.write(f'Température : {temperature}°C')
    st.write(f'Vitesse du vent : {wind_speed}m/s')
    st.write(f'Taux d\'humidité : {humidity}%')
    st.audio(audio_stream, format="audio/mpeg", start_time=0)

  else:
    st.write("Une erreur est survenue. Vérifiez le nom de votre ville svp !!!")

# Enregistrement audio
if st.button("Début de l'enregistrement"):
  text_vocal = transcribe_speech()
  st.write("Chatbot@root:~$ ", text_vocal)
  response = bot_response(text_vocal)
  #st.write(response)
  chat_history.append({"user_message": user_input, "bot_message": bot_response})
  temperature = response[0]
  wind_speed = response[1]
  humidity = response[2]
  vocal_response = f"""Voici les données méteorologiques de la ville de {text_vocal}.
                      La température est de {temperature}dégré celsius, La vitesse du vent est de {wind_speed} mètres par seconde
                      et le taux d'humidité est de {humidity}%"""
  # Réponse écrite
  if response != "Echec":
    audio_stream = text_to_speech(vocal_response)
    st.write(f'Données Météorologiques de la ville de {text_vocal}')
    st.write(f'Température : {temperature}°C')
    st.write(f'Vitesse du vent : {wind_speed}m/s')
    st.write(f'Taux d\'humidité : {humidity}%')
    st.audio(audio_stream, format="audio/mpeg", start_time=0)

  else:
    st.write("Une erreur est survenue. Vérifiez le nom de votre ville svp !!!")

# Bouton effacer l'historique des réponses
if st.button("Effacer l'historique"):
    chat_history.clear()
