import streamlit as st
import speech_recognition as sr
import spacy
import language_tool_python
import textstat
import pyaudio
import parselmouth
from parselmouth.praat import call
import pandas as pd
# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please speak into the microphone...")
        recognizer.adjust_for_ambient_noise(source)
        audio_text = recognizer.listen(source)
        st.write("Recording complete, recognizing...")
    try:
        text = recognizer.recognize_google(audio_text)
        return text, audio_text
    except sr.UnknownValueError:
        return "Sorry, I did not understand the audio", None
    except sr.RequestError:
        return "Sorry, my speech service is down", None

# Function to analyze the text
def analyze_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tool = language_tool_python.LanguageTool('en-IN')
    matches = tool.check(text)

    # Metrics
    num_sentences = len(list(doc.sents))
    num_words = len(doc)
    num_complex_words = sum([1 for token in doc if len(token) > 6])
    num_mistakes = len(matches)
    flesch_score = textstat.flesch_reading_ease(text)

    # Calculations
    fluency_score = min(num_sentences + num_words / 10.0, 10)
    vocabulary_score = min(num_complex_words / num_words * 10, 10)
    grammar_score = min((num_words - num_mistakes) / num_words * 10, 10)
    coherence_score = min(sum([1 for sent in doc.sents if len(sent) > 5]) / num_sentences * 10, 10)
    readability_score = min(flesch_score / 10, 10)

    return {
        "fluency": fluency_score,
        "vocabulary": vocabulary_score,
        "grammar": grammar_score,
        "coherence": coherence_score,
        "readability": readability_score
    }

# Function to analyze audio for pronunciation and pace
def analyze_audio(audio_data):
    with open("temp.wav", "wb") as f:
        f.write(audio_data.get_wav_data())

    sound = parselmouth.Sound("temp.wav")
    pitch = call(sound, "To Pitch", 0.0, 75, 600)
    mean_pitch = call(pitch, "Get mean", 0, 0, "Hertz")

    intensity = call(sound, "To Intensity", 75, 0.0)
    mean_intensity = call(intensity, "Get mean", 0, 0, "dB")

    # Speech rate: Words per minute
    duration = sound.get_total_duration()
    recognizer = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    num_words = len(text.split())
    speech_rate = num_words / (duration / 60)

    return {
        "mean_pitch": mean_pitch,
        "mean_intensity": mean_intensity,
        "speech_rate": speech_rate
    }

# Function to provide feedback based on scores
def provide_feedback(scores):
    feedback = []
    for metric, score in scores.items():
        if score > 8:
            feedback.append(f"Excellent {metric} skills.")
        elif score > 6:
            feedback.append(f"Good {metric} skills.")
        elif score > 4:
            feedback.append(f"Average {metric} skills.")
        else:
            feedback.append(f"Needs improvement in {metric}.")
    return "\n".join(feedback)

if __name__ == "__main__":
    text, audio = speech_to_text()
    analysis_results = analyze_text(text)
    audio_results = analyze_audio(audio)
    combined_scores = {**analysis_results, **audio_results}
    rating = provide_feedback(combined_scores)
    