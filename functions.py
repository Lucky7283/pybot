import time,re,csv,keys


def history(file):
    parts="parts"
    text="text"
    role="role"
    strn=[]
    try:
        with open(f"data/{file}.txt",'r',encoding='utf-8') as f:
            r=f.read()
            if r==[]:
                return
            r=re.split("parts",r)
        i=0
        say=len(r)
        while i<say:
            if "file_data {" in r[i]:
                match = re.search(r"mime_type:\s*(\S+)", r[i])
                txt_type=match[1]
                match = re.search(r"file_uri:\s*(\S+)",r[i] )
                url=match[1]
                url=re.sub(r'"',"",url)
                txt_type=re.sub(r'"',"",txt_type)
                url=url.strip()
                txt=re.search(r"text:\s*(.+)", r[i+1])[1]
                rl="user"
                a={'role': rl,'parts':[{'file_data' :{'mime_type': txt_type,'file_uri':url }},{'text':txt}]}
                i=i+2
                strn.append(a)
            else:
                txt=re.search(r"text:\s*(.+)",r[i])
                rl=re.search(r'role:\s*(.+)',r[i])
                i=i+1
                if rl!=None and txt!=None:
                    rl=rl[1]
                    txt=txt[1]
                    if 'model'in rl:
                        rl="model"
                    else:
                        rl="user"
                else:
                    continue
                a={role: rl, parts: [{text: txt}]}
                strn.append(a)
        return strn
    except Exception as e:
        print(f'Error as a:{e}')
        return strn



def loads(message,mod):
    import google.generativeai as genai

    genai.configure(api_key=keys.__keys__())
    try:
        with open(f"Prompts/{message.from_user.id}.txt","r",encoding="UTF-8") as f:
            prompt=f.read().strip()
    except:
        prompt=None
    if prompt:
        model = genai.GenerativeModel(model_name=mod,system_instruction=prompt)
    else:
        print("Промт не обнаружен")
        model = genai.GenerativeModel(model_name=mod)
    histor=history(message.from_user.id)
    if histor!=' ':
        chat=model.start_chat(history=histor)
    else:
        print("История не обнаружена")
        chat=model.start_chat()
    return model,chat

def w(message,tm):
    with open("data/chathistory.csv", "a", encoding="UTF-8") as f:
        if message.from_user.username:
            f.write(f"{message.from_user.username};{message.text};{message.content_type};{message.date};{tm} \n")
        else:
            f.write(f"{message.from_user.id};{message.text};{message.content_type};{message.date};{tm} \n")



def times():
    day=time.strftime("%d")
    month=time.strftime("%m")
    year=time.strftime("%Y")
    hour=time.strftime("%H")
    minute=time.strftime("%M")
    second=time.strftime("%S")
    return f"{year}-{month}-{day} {hour}:{minute}:{second}"
def hist():
    with open("data/chathistory.csv", "r", encoding="UTF-8") as f:
        historyuser=f.read()
    return historyuser
def user():
    users=[]
    with open("data/userlist.csv", "r") as f:
            userlist=csv.DictReader(f,delimiter=";")
            for i in userlist:
                users.append(i["USERNAME"]+"-"+i["ID"])
    return users



def image():
    from google import genai as genai2
    from google.genai import types
    client = genai2.Client(api_key=keys.__key__)

    contents = ('Hi, can you create a 3d rendered image of a pig '
                'with wings and a top hat flying over a happy '
                'futuristic scifi city with lots of greenery?')

    response = client.models.generate_content(
        model="models/gemini-2.0-flash-exp",
        contents=contents,
        config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
    )

    with open("a.png",'wb') as f:
        f.write(response.candidates[0].content.parts[-1].inline_data.data)