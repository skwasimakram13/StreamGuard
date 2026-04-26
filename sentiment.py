from google import genai
import logging
import asyncio

logger = logging.getLogger(__name__)

class SentimentEngine:
    def __init__(self):
        self.api_key = ""
        self.is_ready = False
        self.model = None

    def configure(self, api_key: str):
        """Configures the Gemini API client."""
        if not api_key:
            self.is_ready = False
            return
            
        try:
            self.client = genai.Client(api_key=api_key)
            self.api_key = api_key
            self.is_ready = True
            logger.info("Gemini Sentiment Engine configured successfully.")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            self.is_ready = False

    async def analyze_vibe(self, messages: list[str]) -> str:
        """
        Analyzes a batch of chat messages and returns a single emoji representing the vibe.
        Expected return values: 🔥 (Hyped), 💖 (Happy), 😡 (Angry), ❓ (Confused), 💬 (Neutral)
        """
        if not self.is_ready or not messages:
            return "💬"
            
        try:
            prompt = (
                "You are an AI analyzing the 'vibe' of a YouTube live stream chat.\n"
                "Read the following batch of recent chat messages and determine the overall sentiment.\n"
                "Respond ONLY with a SINGLE emoji that best represents the current vibe.\n"
                "Choose from: 🔥 (Hyped/Excited), 💖 (Happy/Positive), 😡 (Angry/Negative), ❓ (Confused), 💬 (Neutral/Random).\n\n"
                "Chat Messages:\n"
            )
            for msg in messages:
                prompt += f"- {msg}\n"
                
            def run_gen():
                return self.client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
            
            response = await asyncio.get_event_loop().run_in_executor(
                None, run_gen
            )
            
            result = response.text.strip()
            # Fallback if the AI returns text instead of an emoji
            if any(e in result for e in ["🔥", "💖", "😡", "❓", "💬"]):
                for e in ["🔥", "💖", "😡", "❓", "💬"]:
                    if e in result:
                        return e
            return "💬"
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return "💬"
