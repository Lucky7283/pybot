from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import google.generativeai as genai
import re,os,telebot,requests,docx2pdf
import keys,t
from db import w
from functions import loads,user,hist
global file,chat,msg,userlist,historyuser

token,api_key=keys.__keys__()
bot=telebot.TeleBot(token)
genai.configure(api_key=api_key)

mod="gemini-2.0-flash-exp"

model = genai.GenerativeModel(model_name=mod)
userid=[]
may=sb=selectmodel=False


def sendtext(message,response): 
    response=t.f(response.text).strip('"').strip('\n')
    while response[-1]=='\n' or response[-1]=='"':
            response=response.strip('"').strip('\n').strip("\\")
    response=re.sub(r"^\s*\*", r"•", response, flags=re.MULTILINE)
    if len(response)>4096:
        i=0
        k=4096
        for i in range(len(response)//4096):
            txt=response[i:k]
            while txt[-1]!='.':
                k-=1
                txt=response[i:k]
            bot.send_message(message.chat.id,txt,parse_mode="HTML")
            i=k
        bot.send_message(message.chat.id,response[i:],parse_mode="HTML")
    else:
        bot.reply_to(message,response,parse_mode="HTML")


def errorformat(message,response):
    response=response.strip('"')  
    response=re.sub(r"\*\*\s*(.*?)\s*\*\*", r" \1 ", response,flags=re.DOTALL)
    response=re.sub(r"\*(\S.*?)\*(?!\w)", r"  \1  ", response)
    response=re.sub(r"^\s*\*", r"•", response, flags=re.MULTILINE)
    response=re.sub(r"\\n", "\n", response,flags=re.DOTALL)
    response = re.sub(r"^\s*```\n(.*?)\n\s*```$", r"\n\n\n \1 \n\n\n", response, flags=re.DOTALL | re.MULTILINE)
    bot.send_message(message.chat.id,f"{e}")
    if len(response)>4096:
        i=0
        k=4096
        for i in range(len(response)//4096):
            txt=response[i:k]
            while txt[-1]!='.':
                k-=1
                txt=response[i:k]
            bot.send_message(message.chat.id,txt)
            i=k
        bot.send_message(message.chat.id,response[i:])
    else:
        bot.reply_to(message,response)


@bot.message_handler(commands=["start"])
def start(message):
    global msg,bllist
    userlist=user()
    usr=f"{message.from_user.username}-{message.from_user.id}"

    if usr not in userlist:
        with open("data/userlist.csv", 'a', encoding="UTF-8") as d:
            d.write(f'{message.from_user.username};{message.from_user.first_name};{message.from_user.last_name};{message.from_user.id}\n')
    if message.from_user.id==1440683925:
        msg=message
        markup=InlineKeyboardMarkup(row_width=3)
        button1=InlineKeyboardButton("Userlist",callback_data="userlist")
        button2=InlineKeyboardButton("History",callback_data="history")
        button3=InlineKeyboardButton("Message",callback_data="message")
        button4=InlineKeyboardButton("Clear trash",callback_data="trash")
        markup.add(button1,button2,button3,button4)

        bot.send_message(text="select action",chat_id=message.chat.id,reply_markup=markup)
    else:
        w(message)
        bot.reply_to(message,"Hello I'm gemini ai bot")


    
@bot.message_handler(commands=["prompt"])
def promt(message):
    global may
    may=True
    with open(f"Prompts/{message.from_user.id}.txt",'r',encoding='UTF-8') as f:
        promt=f.read().strip()
        if promt:
            bot.send_message(message.chat.id,"Текущий промпт:\nCurrent prompt:")
            bot.send_message(message.chat.id,f"<b>{promt}</b>",parse_mode="HTML")
        else:
            bot.send_message(message.chat.id,"Промпт отсутствует\nPrompt is emty")
    bot.send_message(message.chat.id,"Введите новый промпт\nSend new prompt")

@bot.message_handler(commands=["clear"])
def clear(message):
    with open(f"data/{message.from_user.id}.txt","w",encoding="UTF-8") as f:
        f.write(" ")
    bot.send_message(message.chat.id,"История чата очищена\nChat history cleared")


@bot.message_handler(commands=["model"])
def md(message):
    selectmodel=True
    markup1=InlineKeyboardMarkup(row_width=1)
    button1=InlineKeyboardButton("gemini-2.0-flash",callback_data="gemini-2.0-flash")
    button2=InlineKeyboardButton("gemini\n2.0-pro-exp",callback_data="gemini-2.0-pro-exp")
    button3=InlineKeyboardButton("gemini\n2.0-flash-exp",callback_data="gemini-2.0-flash-exp")
    
    markup1.add(button1,button2,button3)
    bot.send_message(chat_id=message.chat.id,text="Выберите модель\nSelect model",reply_markup=markup1)
    
@bot.callback_query_handler(func=lambda call:True)
def allback(call):

    if call.data=="history":
        historyuser=hist()
        if len(historyuser)>4096:
            bot.send_document("1440683925", open("data/chathistory.csv", "r", encoding='utf-8'))
        else:
            bot.send_message(call.message.chat.id,historyuser)
    elif call.data=="userlist":
        userlist=user()
        bot.send_message(call.message.chat.id,"\n".join(userlist))
    elif call.data=="message":
        bot.send_message(call.message.chat.id,msg)
    elif call.data=="trash":
        for i in os.listdir("trash"):
            os.remove(f"trash/{i}")
        bot.send_message(call.message.chat.id,"Корзина очищена")
    elif call.data=="gemini-2.0-flash":
        mod="gemini-2.0-flash"
        bot.send_message(call.message.chat.id,"Модель изменена на gemini-2.0-flash")
    elif call.data=="gemini-2.0-pro-exp":
        mod="gemini-2.0-pro-exp"
        bot.send_message(call.message.chat.id,"Модель изменена на gemini-2.0-pro-exp")
    elif call.data=="gemini-2.0-flash-exp":
        mod="gemini-2.0-flash-exp"
        bot.send_message(call.message.chat.id,"Модель изменена на gemini-2.0-flash-exp")

try:
    @bot.message_handler(content_types=["text"])
    def text(message):
        global may,sb
        w(message)
        model,chat=loads(message=message,mod=mod)
        bot.send_chat_action(message.chat.id, "typing")
        if may:
            with open(f"Prompts/{message.from_user.id}.txt","r",encoding="UTF-8") as f:
                prompt=f.read().strip()
                if prompt:
                    bol=True
                else:
                    bol=False
            with open(f"Prompts/{message.from_user.id}.txt","w",encoding="UTF-8") as f:
                f.write(message.text)
            may=False
            if bol:
                bot.send_message(message.chat.id,"Промпт успешно обнавлен\nPrompt refresh succes")
            else:
                bot.send_message(message.chat.id,"Промпт успешно добавлен\nPrompt add succes")
            return
        try:
            question=message.text
            try:
                response = chat.send_message(question)
            except:
                chat=model.start_chat()
                response = chat.send_message(question)

            resp=response.text
            sendtext(message=message,response=response)       
        except Exception as e:
            errorformat(message,response=resp)
            print(f'error text:{e}')

        
        try:
            with open("data/"+str(message.from_user.id)+".txt","w",encoding="UTF-8") as f:
                txt=re.sub(r"\\(?!n)", "", f"{chat.history}")
                f.write(txt)
        except Exception as e:
            print(f"Ошибка текста: {e}")


    @bot.message_handler(content_types=['photo',])
    def photo(message):
        
        bot.send_chat_action(message.chat.id, "typing")
        w(message)
        model,chat=loads(message=message,mod=mod)
        try:
            fileid = message.photo[-1].file_id
            file_paz = bot.get_file(fileid).file_path
            fayl = bot.download_file(file_paz)
            filepaz = file_paz.split("/")[-1]

            with open(f"trash/{filepaz}", 'wb') as f:
                f.write(fayl)
            faylink = genai.upload_file(f"trash/{filepaz}")
            
            if message.caption:
                response = chat.send_message([faylink,  message.caption])
            else:
                response = chat.send_message([faylink,"что можешь сказать на счет фото"])
            resp=response.text
            response=t.f(response.text)
            while response[-1]=='\n' or response[-1]=='"':
                    response=response.strip('"').strip('\n').strip("\\")
            if len(response)>4096:
                i=0
                k=4096
                for i in range(len(response)//4096):
                    txt=response[i:k]
                    while txt[-1]!='.':
                        k-=1
                        txt=response[i:k]
                    bot.send_message(message.chat.id,txt,parse_mode="HTML")
                    i=k
                bot.send_message(message.chat.id,response[i:],parse_mode="HTML")
            else:
                bot.reply_to(message,response,parse_mode="HTML")

        except Exception as e:
            errorformat(message,response=resp)
            print(f'error photo:{e}')


        with open("data/"+str(message.from_user.id)+".txt","w",encoding="UTF-8") as f:
                txt=re.sub(r"\\(?!n)", "", f"{chat.history}")
                f.write(txt)

    @bot.message_handler(content_types=["audio","voice"])
    def audio(message):
        
        bot.send_chat_action(message.chat.id,"typing")
        w(message)
        model,chat=loads(message=message,mod=mod)
        try:
            if message.content_type=="audio":
                audioid=message.audio.file_id
                audiopaz=bot.get_file(audioid).file_path
                fayl=bot.download_file(audiopaz)
                paz = audiopaz.split("/")[-1]

            elif message.content_type=="voice":
                voiceid=message.voice.file_id
                voicepaz=bot.get_file(voiceid).file_path
                fayl=bot.download_file(voicepaz)
                paz = voicepaz.split("/")[-1]
            with open(f"trash/{paz}", 'wb') as f:
                f.write(fayl)
            faylink = genai.upload_file(f"trash/{paz}")

            if message.caption:
                response = chat.send_message([faylink,  message.caption] )
            elif message.content_type=="voice":
                response = chat.send_message([faylink,"послушай"])
            elif message.content_type=="audio":
                response = chat.send_message([faylink,"что можешь сказать на счет аудио"])
            resp=response.text
            response=sendtext(message=message,response=response)

        except Exception as e:
            errorformat(message,response=resp)
            print(f'error audio:{e}')

            
        with open("data/"+str(message.from_user.id)+".txt","w",encoding="UTF-8") as f:
                txt=re.sub(r"\\(?!n)", "", f"{chat.history}")
                f.write(txt)

    @bot.message_handler(content_types=["document"])
    def fayl(message):
        w(message)
        bot.send_chat_action(message.chat.id,"typing")
        model,chat=loads(message=message,mod=mod)
        try:
            fileid=message.document.file_id
            print(fileid)
            filepaz=bot.get_file(fileid)
            filepaz=filepaz.file_path.split("/")[-1]
            file=requests.get(bot.get_file_url(fileid)).content
            with open(f"trash/{filepaz}",'wb') as d:
                    d.write(file)
            if filepaz.count("doc")==1:
                docx2pdf.convert(input_path=f"trash/{filepaz}")
            else:            
                with open(f"trash/{filepaz}",'wb') as d:
                    d.write(file)
            faylink = genai.upload_file(f"trash/{filepaz.split('.')[0]}.pdf")
            if message.caption:
                response = chat.send_message([faylink, message.caption] )
            else:
                response = chat.send_message([faylink,"что можешь сказать на счет файла"])
            resp=response.text
            response=sendtext(message=message,response=response)

        except Exception as e:
            errorformat(message=message,response=resp)
            print(f'error document:{e}')

        with open("data/"+str(message.from_user.id)+".txt","w",encoding="UTF-8") as f:
                txt=re.sub(r"\\(?!n)", "", f"{chat.history}")
                f.write(txt)

    @bot.message_handler(content_types=["video","video_note"])
    def video(message):
        w(message)
        bot.send_chat_action(message.chat.id,"typing")
        model,chat=loads(message=message,mod=mod)
        try:
            if message.content_type=="video":
                file_link=bot.get_file_url(message.video.file_id)
                filepaz=bot.get_file(message.video.file_id).file_path.split('/')[-1]
                file=requests.get(file_link).content
            elif message.content_type=="video_note":
                
                file_link=bot.get_file_url(message.video_note.file_id)
                filepaz=bot.get_file(message.video_note.file_id).file_path.split('/')[-1]
                file=requests.get(file_link).content
            
            with open(f"trash/{filepaz}",'wb') as d:
                d.write(file)
            faylink = genai.upload_file(path=f"trash/{filepaz}")
            while requests.get(f"{faylink.uri}?key={api_key}").json()["state"]!="ACTIVE":
                continue
            if message.caption:
                response = chat.send_message([faylink, message.caption] )
            elif message.content_type=="video":
                response = chat.send_message([faylink,"что можешь сказать на счет видео"])
            elif message.content_type=="video_note":
                response = chat.send_message([faylink,"посмотри"])
            resp=response.text
            response=sendtext(message=message,response=response)

        except Exception as e:
            errorformat(message,response=resp)
            print(f'error video:{e}')
        with open("data/"+str(message.from_user.id)+".txt","w",encoding="UTF-8") as f:
                txt=re.sub(r"\\(?!n)", "", f"{chat.history}")
                f.write(txt)

except Exception as e:
    bot.send_message(1440683925,f"Произошла ошибка 1: {e}")

if __name__=="__main__":
    bot.polling(non_stop=True)