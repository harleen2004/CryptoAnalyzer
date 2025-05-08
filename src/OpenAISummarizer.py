# src/OpenAISummarizer.py
import openai

class OpenAISummarizer:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def summarize(self, posts_text):
        combined = "\n".join(posts_text[:10])  # truncate for token safety
        prompt = f"Summarize the public sentiment from these Reddit posts about crypto:\n{combined}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error summarizing: {e}"
