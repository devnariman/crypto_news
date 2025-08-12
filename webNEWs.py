from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from llama31_gguf import lamma_llm

class web_news():
    def __init__(self , domain):
        self.domain = domain


    def search_element_css(self , css_selector):
        element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        return element

    def run_BTC(self , number):
        self.driver = webdriver.Chrome()
        self.driver.get(self.domain)
        time.sleep(1)
        base = "#__next > div.md\\:relative.md\\:bg-white > div.relative.flex > div.md\\:grid-cols-\\[1fr_72px\\].md2\\:grid-cols-\\[1fr_420px\\].grid.flex-1.grid-cols-1.px-4.pt-5.font-sans-v2.text-\\[\\#232526\\].antialiased.transition-all.xl\\:container.sm\\:px-6.md\\:gap-6.md\\:px-7.md\\:pt-10.md2\\:gap-8.md2\\:px-8.xl\\:mx-auto.xl\\:gap-10.xl\\:px-10 > div.min-w-0 > div:nth-child(12) > div.hidden.md\\:block > ul > li:nth-child({i})"
        llm = lamma_llm()
        newss = []
        if number <= 2:
            number = 2

        if number >= 11:
            number = 11
        for i in range(1, number):
            try:
                selector = base.format(i=i)
                li_el = self.search_element_css(selector)
                a_tag = li_el.find_element(By.CSS_SELECTOR, "a[data-test='article-title-link']")
                Url =  a_tag.get_attribute("href")
                b2 = web_news(Url)
                result_html = b2.run_get()
                summary_prompt = """
                    Read all the provided content carefully.

                    GOAL
                    Produce a complete, non-truncated, well-structured digest of the news that captures only the most important points while adding brief clarifications where needed.

                    OUTPUT (English, plain text; no preface)
                    1) Executive Summary — 5–8 bullets
                    - One idea per bullet; crisp, factual, and non-repetitive.
                    2) Topic Buckets — group related items under short topic titles.
                    For each item:
                    - Headline (≤ 12 words)
                    - Summary (2–3 full sentences; no truncation)
                    - Key numbers/dates (if any)
                    - Named entities (people, companies, tickers)
                    - Why it matters (1 sentence)
                    - What to watch next (1 sentence, if applicable)
                    3) Highlights — Top 3 items overall with a one-sentence rationale each.

                    RULES
                    - Remove duplicates and trivialities; keep verifiable facts; no speculation.
                    - If something is unclear or missing, write “Unknown”.
                    - Keep formatting clean: headings with `==` and bullets with `-`; match the structure above.
                    - Do not cut explanations mid-sentence. Return a complete answer even if it is longer.
                    - Return only the sections above; no extra commentary or markdown beyond the specified markers.

                    FORMAT EXAMPLE
                    == Executive Summary ==
                    - ...
                    - ...

                    == Topic Buckets ==
                    1) <Topic name>
                    - Headline: ...
                    - Summary: ...
                    - Key numbers/dates: ...
                    - Named entities: ...
                    - Why it matters: ...
                    - What to watch next: ...

                    == Highlights ==
                    - <Item title> — <why it matters>
                    - <Item title> — <why it matters>
                    - <Item title> — <why it matters>
                    

                """

                last_res = result_html + "\n\n" + summary_prompt

                ai_res = llm.response(last_res)
                newss.append(ai_res)
                print(i)

            except:
                print('faild : ' , i)
                continue
        
        with open("news_BTC.json", "w", encoding="utf-8") as f:
            json.dump(newss, f, ensure_ascii=False, indent=4)

        self.driver.quit()
        return newss


    def run_get(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.domain)
        time.sleep(0.7)
        li_el = self.search_element_css('#article > div > div')
        text = li_el.get_attribute("innerText").strip()
        self.driver.quit()
        return text  


