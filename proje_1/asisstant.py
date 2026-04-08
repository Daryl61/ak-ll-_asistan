import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("GEMİNİ_APİ_KEY")

if not api_key:
    raise ValueError("API key not found. Please set the GEMİNİ_APİ_KEY environment variable.")

url="https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"


header={
    "Content-Type":"application/json",
    "X-Goog-Api-Key":api_key
    }

def get_gemini_response(prompt:str)->str:
    payload={
        "contents":[
            {"parts":[
                {"text":prompt}
               ]           
            }
        ] 
    }

    response=requests.post(url,headers=header,json=payload)

    if response.status_code==200:
        try:
            result=response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"yanıt hatası: {e}"
    else:
        return f"API hatası: {response.status_code}:{response.text}"

def detect_intent(message: str) -> str:
    prompt=f"""
               kullanıcının aşşagıdaki cümlesini sınıflandır:

               Etiklerden sadece birini döndür:
               -not_ozet (eger notları özetlemesini istiyorsa)
               -etkinlik_goster (eger etkinlikleri görmek yada özet istiyorsa)
               -normal (diger her şey)

               Cümle: "{message}"
               Yalnızca etiket döndür : (örnek: not_ozet)


    """

    response=get_gemini_response(prompt)
    return response.strip().lower()



if __name__=="__main__":
    user_input=input("Kullanici Sorusu:")  
    yanit=get_gemini_response(user_input)
    print(f"asistan yaniti: {yanit}")   