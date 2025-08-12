from deep_translator import GoogleTranslator
import time

class traslator():
    def __init__(self):
        self.fa2en = GoogleTranslator(source="fa", target="en")
        self.en2fa = GoogleTranslator(source="en", target="fa")

    def fa_to_en(self, persion_text):
        """ترجمه فارسی به انگلیسی با قطع‌بندی متن‌های بلند"""
        return self._translate_chunked(persion_text, self.fa2en)

    def en_to_fa(self, persion_text):
        """ترجمه انگلیسی به فارسی با قطع‌بندی متن‌های بلند"""
        return self._translate_chunked(persion_text, self.en2fa)

    def _translate_chunked(self, text: str, translator, chunk_size=3500, retries=2, pause=0.8):
        """ترجمه chunk شده با ریترا‌ی و فالبک"""
        if not text:
            return ""
        out = []
        i = 0
        n = len(text)
        while i < n:
            chunk = text[i:i+chunk_size]
            for attempt in range(retries + 1):
                try:
                    translated_chunk = translator.translate(chunk) or ""
                    out.append(translated_chunk)
                    break
                except Exception as e:
                    if attempt == retries:
                        out.append(chunk)  # fallback
                    else:
                        time.sleep(pause)
                        continue
            i += chunk_size
        return " ".join(out)
