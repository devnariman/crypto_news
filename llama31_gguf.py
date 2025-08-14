

from typing import List, Dict, Any
from llama_cpp import Llama
import json
class AIModel_Llm:
    # --------------------------------------------
    # سازنده: دریافت حافظه‌ی سیستم (system memory) و آماده‌سازی پارامترها
    # --------------------------------------------
    def __init__(self,default_memory : bool = None,system_memory = None, model_path: str = "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"):
        self.MODEL_PATH = model_path

        # پارامترهای بارگذاری مدل
        self.LLAMA_KWARGS = {
            "n_ctx": 4096,       # طول کانتکست
            "n_gpu_layers": -1,  # تمام لایه‌ها روی GPU (در صورت موجود بودن)
            "n_threads": 12,     # نخ‌های CPU (در صورت اجرای CPU)
            "verbose": False,
            "seed": 50,
        }

        # پارامترهای تولید متن
        self.GENERATION_KWARGS = {
            "max_tokens": 512,
            "temperature": 0.6,
            "top_p": 0.95,
            "repeat_penalty": 1.08,
            "stop": ["</s>", "###", "User:", "Assistant:"],
        }

        self.llm = None

        if default_memory == True:
            system_memory = (
                "You are an assistant and your name is Gofi. ")
        else:
            None


        if system_memory == None:
            self.system_prompt = ""
            self.history: List[Dict[str, str]] = [
                {"role": "system", "content": self.system_prompt}
            ]
            self.load_last_history()
        else:
            self.system_prompt = system_memory.strip() if system_memory else "You are a helpful, concise assistant."
            self.history: List[Dict[str, str]] = [
                {"role": "system", "content": self.system_prompt}
            ]
            with open("system_prompt.json", "w", encoding="utf-8") as f:
                json.dump(self.history[0], f, ensure_ascii=False, indent=4)

        self.chat_loop_status = True

    # --------------------------------------------
    # بارگذاری/اجرای مدل
    # --------------------------------------------
    def run_model(self):
        if self.llm is None:
            print("Loading model...")
            self.llm = Llama(model_path=self.MODEL_PATH, **self.LLAMA_KWARGS)
            print("Model is ready.")
        else:
            print("Model already loaded.")

    # --------------------------------------------
    # فراخوانی ساده‌ی completion به‌صورت chat
    # --------------------------------------------
    def chat(self, messages: List[Dict[str, str]], **gen_kwargs: Any) -> str:
        args = {**self.GENERATION_KWARGS, **gen_kwargs}
        out = self.llm.create_chat_completion(messages=messages, **args)
        return out["choices"][0]["message"]["content"].strip()

    # --------------------------------------------
    # اضافه کردن متن جدید به حافظه‌ی سیستم و بازنویسی پیام system
    # --------------------------------------------
    def train_system(self, text: str):
        text = text.strip()
        if not text:
            return
        # محتوای جدید را به انتهای system memory اضافه می‌کنیم
       
        with open("system_prompt.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if "content" in data:
                self.system_prompt = data["content"]
        
        if self.system_prompt:
            self.system_prompt = f"{self.system_prompt}\n{text}"
        else:
            self.load_last_history()
            self.system_prompt = text
        # پیام system در تاریخچه را به‌روزرسانی می‌کنیم
        self.history[0] = {"role": "system", "content": self.system_prompt}
        with open("system_prompt.json", "w", encoding="utf-8") as f:
            json.dump(self.history[0], f, ensure_ascii=False, indent=4)

            
    def load_last_history(self):
        with open("system_prompt.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.history[0] = data
            except:
                self.history[0] = {"role": "system", "content": "You are an assistant and your name is Gofi."}
                with open("system_prompt.json", "w", encoding="utf-8") as f:
                    json.dump(self.history[0], f, ensure_ascii=False, indent=4)

    # --------------------------------------------
    # ریست کردن تاریخچه (system باقی می‌ماند)
    # --------------------------------------------
    def reset_history(self):
        self.history = [{"role": "system", "content": self.system_prompt}]

    # --------------------------------------------
    # اجرای یک دور پرسش-پاسخ: ورودی کاربر، خروجی مدل، به‌روزرسانی تاریخچه
    # --------------------------------------------
    def ask(self, user_text: str, **gen_kwargs: Any) -> str:
        user_text = user_text.strip()
        if not user_text:
            return ""
        self.history.append({"role": "user", "content": user_text})
        reply = self.chat(self.history, **gen_kwargs)
        self.history.append({"role": "assistant", "content": reply})
        return reply



    def delet_last_train(self):
        with open("system_prompt.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            data["content"] = data["content"].rsplit("\n", 1)[0]  # حذف آخرین خط
            print(data["content"])
            with open("system_prompt.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    # --------------------------------------------
    # حلقه‌ی چت مینیمال:
    # - اول پیام system ست است (قبلاً در history[0])
    # - سپس با کاربر وارد تعامل می‌شود
    # --------------------------------------------
    def chat_loop(self):
        if self.llm is None:
            self.run_model()

        print("Ready. Commands: ::exit | ::reset | ::train <text> | ::delet_last_train ")
        while self.chat_loop_status:
            try:
                user_inp = input("User: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nAssistant: Bye.")
                break

            # دستورات کنترلی
            if not user_inp:
                continue
            if user_inp == "::exit":
                print("Assistant: Bye.")
                break

            if user_inp == "::delet_last_train":
                self.delet_last_train()
                print("Assistant: Last training data deleted.")
                continue

            if user_inp == "::reset":
                self.reset_history()
                print("Assistant: Conversation memory cleared (system kept).")
                continue
            if user_inp.startswith("::train"):
                payload = user_inp[len("::train"):].strip()
                if payload:
                    self.train_system(payload)
                    print("Assistant: System memory updated.")
                else:
                    print("Assistant: Provide text after ::train")
                continue

            # پرسش عادی کاربر
            reply = self.ask(user_inp)
            print("Assistant:", reply)
