from llama_cpp import Llama
import os

class lamma_llm():
    def __init__(self):
        self.MODEL_PATH = os.path.abspath("Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")
        self.llm = Llama(
            model_path=self.MODEL_PATH,
            n_ctx=4096,
            # n_ctx=2048,                                 # برای تست کوتاه، کانتکست کم
            n_gpu_layers=30,    # تعداد لایه‌هایی که روی GPU میرن (برای RTX 3060 شش‌گیگ خوبه)
            verbose=True        # نمایش لاگ برای اطمینان از GPU استفاده
        )


    def response(self , input):
        out = self.llm(
            input,
            max_tokens=750,
            temperature=0.7,
        )
        res = out["choices"][0]["text"].strip()
        # print("\nخروجی مدل:\n", out["choices"][0]["text"].strip())
        return res
    


# llm = lamma_llm()
# res = 
# llm.response(res)