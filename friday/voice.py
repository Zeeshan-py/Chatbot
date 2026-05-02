from __future__ import annotations

from typing import Any


class VoiceInterface:
    """Optional voice input/output wrapper."""

    def __init__(self) -> None:
        self._engine: Any = None
        self._recognizer: Any = None
        self.output_enabled = False
        self.available = False

        try:
            import pyttsx3
            import speech_recognition as sr

            self._engine = pyttsx3.init()
            self._recognizer = sr.Recognizer()
            self.available = True
        except Exception:
            self.available = False

    def enable_output(self, enabled: bool) -> str:
        if enabled and not self.available:
            return "Voice mode is unavailable because speech packages are not installed or initialized."
        self.output_enabled = enabled
        return "Voice output enabled." if enabled else "Voice output disabled."

    def speak(self, text: str) -> None:
        if not self.available or not self.output_enabled or not text.strip():
            return
        self._engine.say(text)
        self._engine.runAndWait()

    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 12) -> str:
        if not self.available:
            raise RuntimeError("Voice input is unavailable on this machine.")

        import speech_recognition as sr

        with sr.Microphone() as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self._recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )
        return self._recognizer.recognize_google(audio)

