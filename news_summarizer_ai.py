import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from gtts import gTTS
import io
import pygame.mixer


def news_infos(url): 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    news_list =[]

 
    headlines= soup.find_all('div', class_='col-12 col-lg-4 d-xl-flex d-lg-flex')

    for headline in headlines[:5]  #You can set how many news you want to see (limit is 21) 
        news = {}
        news['headline'] = headline.text.strip()
        news['link'] = headline.find('a')['href']
        news['content'] = news_contents(news['link'])
        news_list.append(news)
       
    return news_list

def news_contents(links):        #getting contents of each news
    response = requests.get(links)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('div', class_='content-text')
    if content:
        content=content.text.strip()
    else:                           # if Image-based news or news that cannot be summarized, content is none
        content='None'

    return content

def summarizer(inputs):

    genai.configure(api_key='YOUR_APİ_KEY')          #gemini api key


    summaries=[]
    for each_news in inputs:
        try:
            model = genai.GenerativeModel('gemini-pro')
            if each_news != None:
                response = model.generate_content(f"Lütfen bu haberi 3 cümlede özetle:\n{each_news}\n\nÖzet:")
                summary=response.text
                summaries.append(summary)
            else:
                summary='Image-based news or news that cannot be summarized'
                summaries.append(summary)
           
        except Exception as e:
            print(f'error is {str(e)}')
            return None
    return summaries



def read_text(text):   #text to speech 
    tts = gTTS(text=text, lang='tr' ) 
    audio_data = io.BytesIO()
 
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_data)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

url = 'URL OF  THE NEWS SİTE'

new_news = news_infos(url)
inputs=[news['content'] for news in new_news]
outputs=summarizer(inputs)



for news, result in zip(new_news, outputs): #printing results
    print()
    print(f'Headline: {news["headline"]}')
    read_text(news["headline"])              
    print(f'Summary: {result}')
    read_text(result)
    print(f"Link:'{news['link']}")
    print()






