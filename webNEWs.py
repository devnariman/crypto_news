from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from llama31_gguf import AIModel_Llm

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
                newss.append(result_html)
                print(i)
                
            except Exception as e:
                print(f"{i} feild for -->  {e}")

        self.driver.quit()
        llm = AIModel_Llm()
        llm.run_model()
        for i in reversed(range(len(newss))):
            try:
                res = llm.ask(newss[i])
                newss[i] = res
                print(f"Processed news item {i+1}/{len(newss)}")
            except Exception as e:
                print(f"Error processing news item {i+1}: {e}")
                del newss[i]


        with open("news_BTC.json", "w", encoding="utf-8") as f:
            json.dump(newss, f, ensure_ascii=False, indent=4)

        
        return newss


    def run_get(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.domain)
        time.sleep(0.7)
        try:
            li_el = self.search_element_css('#article > div > div')
            text = li_el.get_attribute("innerText").strip()
            self.driver.quit()
        except:
            try:
                li_el = self.search_element_css('#articleTitle')
                text = li_el.get_attribute("innerText").strip()
                self.driver.quit()
            except Exception as e:
                print(f"feild for -->  {e}")
                self.driver.quit()

        
        return text  


