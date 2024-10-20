import openai
import speech_recognition as sr
import pyttsx3
import traceback
import os
import webbrowser

# Initialize the speech engine
engine = pyttsx3.init()

# Set your OpenAI API key
openai.api_key = "openai api key"  # Replace with your actual API key

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"User said: {query}\n")
            return query
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return "None"
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return "None"
        except sr.RequestError as e:
            print(f"There was an issue connecting to the speech recognition service: {e}")
            return "None"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            return "None"

# Updated function to generate a response using the GPT-3.5-Turbo model
def generate_response(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    # Debugging: Print the messages sent to the API
    print("Sending the following messages to the API:")
    for message in messages:
        print(message)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()

    except openai.error.InvalidRequestError as e:
        print(f"Bad request: {e}")
    except openai.error.AuthenticationError as e:
        print(f"Authentication error: {e}")
    except openai.error.APIConnectionError as e:
        print(f"API connection error: {e}")
    except openai.error.OpenAIError as e:
        if "insufficient_quota" in str(e):
            print("Error: You have exceeded your usage limits. Please check your account.")
            return "I'm sorry, but I've exceeded my usage limits. Please check back later."
        else:
            print(f"OpenAI error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()

    return "I'm sorry, I couldn't process that."

# Function to open applications or websites
def open_application_or_website(command):
    if "open notepad" in command:
        os.system("notepad.exe")
        speak("Opening Notepad.")
    elif "open calculator" in command:
        os.system("calc.exe")
        speak("Opening Calculator.")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "open spotify" in command:
        os.system("C:\\Path\\To\\Spotify.exe")
        speak("Opening Spotify.")
    elif "open github" in command:
        webbrowser.open("https://www.github.com")
        speak("Opening GitHub.")
    else:
        speak("I'm not sure how to open that.")
        print("Friday: I'm not sure how to open that.")

# Main loop for the assistant
if __name__ == "__main__":
    speak("Hello, I am Friday. How can I assist you today?")

    while True:
        try:
            user_input = listen()

            if user_input.lower() in ["exit", "quit", "bye"]:
                speak("Goodbye!")
                break

            if user_input != "None" and user_input.lower().startswith("friday"):
                # Remove "Friday" from the command before processing it
                command = user_input.lower().replace("friday", "").strip()

                # Check if the command is to open an app or website
                if "open" in command:
                    open_application_or_website(command)
                else:
                    response = generate_response(command)
                    print(f"Friday: {response}")
                    speak(response)
            else:
                print("Waiting for the 'Friday' wake word.")

        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")
            traceback.print_exc()