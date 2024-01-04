
import random
import requests
import telebot
from telebot import types
from khayyam import JalaliDate
import gtts
import qrcode

url = "https://hafez.p.rapidapi.com/fal"

headers = {
    "X-RapidAPI-Key": "09bad341bfmsha7a8753d2bd9417p1d122bjsncf03b722f3d1",
    "X-RapidAPI-Host": "hafez.p.rapidapi.com"
}

bot = telebot.TeleBot("6345852814:AAH7VxaXQpjCN2uQryPsNxYnljX-CFTtEdM") 
game_number = None  
flag=None
win=False

# commands
bot_keyboard = types.ReplyKeyboardMarkup(row_width=3)
key1 = types.KeyboardButton('/start')
key2 = types.KeyboardButton('/game')
key3=types.KeyboardButton('/fall')
key4 = types.KeyboardButton('/age')
key5 = types.KeyboardButton('/voice')
key6 = types.KeyboardButton('/max')
key7 = types.KeyboardButton('/argmax')
key8 = types.KeyboardButton('/qrcode')
key9 = types.KeyboardButton('/help')
bot_keyboard.add(key1, key2, key3, key4, key5, key6, key7, key8,key9)


# تابع ساخت کیبورد بازی
def create_game_keyboard():
    game_keyboard = types.ReplyKeyboardMarkup(row_width=1)
    new_game_key = types.KeyboardButton('/newgame')
    exit_key = types.KeyboardButton('/exit')
    game_keyboard.add(new_game_key, exit_key)
    return game_keyboard


bot=telebot.TeleBot("6345852814:AAH7VxaXQpjCN2uQryPsNxYnljX-CFTtEdM",parse_mode=None)

# decorator in Python
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global flag
    flag="start"
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    bot.reply_to(message," سلام به روی ماهت."+str(first_name+" "+last_name)+" 😘 خوش اومدی عزیزم.😍",reply_markup=bot_keyboard)

# ********************************************************************************#

@bot.message_handler(commands=['fall'])
def send_fall(message):
    global flag
    flag="fall"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        poem_text = response.json()["poem"]
        interpretation = response.json()["text"]
        full_text = f"شعر حافظ:\n\n{poem_text}\n\nتعبیر:\n\n{interpretation}"
        bot.send_message(message.chat.id, full_text)
    else:
        bot.send_message(message.chat.id, "متاسفانه نمی‌توان فال حافظ را دریافت کرد.")

# ********************************************************************************#

@bot.message_handler(commands=['game'])
def game(message):
    global flag
    global win
    flag="game"
    win=False
    global game_number
    game_number = random.randint(1, 100)
    bot.send_message(message.chat.id, "من به یک عدد بین 1 تا 100 فکر میکنم حدس بزن عدد من چیه. یادت باشه فقط 10 تا فرصت داری!!", reply_markup=create_game_keyboard())

@bot.message_handler(func=lambda message: message.text == '/newgame')
def new_game(message):
    global flag
    global win
    flag="game"
    win=False
    global game_number
    game_number = random.randint(1, 100)
    bot.send_message(message.chat.id, "یک بازی جدی شروع میکنیم! من به یک عدد بین 1 تا 100 فکر میکنم حدس بزن عدد من چیه!", reply_markup=create_game_keyboard())

@bot.message_handler(func=lambda message: message.text == '/exit')
def exit_game(message):
    global game_number
    game_number = None
    global win
    win=False
    bot.send_message(message.chat.id, "بازی کنسل شد، جنبه بازی نداری نیا اینجا دیگه 🤬", reply_markup=bot_keyboard)
    # reply_markup=types.ReplyKeyboardRemove()  ازین برای حذف کیبور استفاده کن

# ********************************************************************************#
@bot.message_handler(commands=['age'])
def calculate_age(message):
    global flag
    flag="age"
    bot.send_message(message.chat.id, "تاریخ تولد شمسی خود را به صورت 0000/00/00 وارد کنید", reply_markup=bot_keyboard)

# ********************************************************************************#
    
@bot.message_handler(commands=['voice'])
def send_voice(message):
    global flag
    flag="voice"
    bot.send_message(message.chat.id, ".لطفا متن مورد نظر خود را برای تبدیل به صوت وارد کنید.")

# ********************************************************************************#

@bot.message_handler(commands=['max'])
def find_max(message):
    global flag
    flag="max"
    bot.send_message(message.chat.id, "آرایه اعداد خود را وارد کنید تا بزرگترین آن ها را پیدا کنم.")
    bot.send_message(message.chat.id, "برای جدا کردن اعداد از , استفاده کنید.")

# ********************************************************************************#

@bot.message_handler(commands=['argmax'])
def find_argmax(message):
    global flag
    flag="argmax"
    bot.send_message(message.chat.id, "آرایه اعداد خود را وارد کنید تا اندیس بزرگترین آن ها را پیدا کنم.")
    bot.send_message(message.chat.id, "برای جدا کردن اعداد از , استفاده کنید.")

# ********************************************************************************#

@bot.message_handler(commands=['qrcode'])
def generate_qrcode(message):
    global flag
    flag="qrcode"
    bot.send_message(message.chat.id, "لطفا رشته مورد نظر خود را وارد کنید.")

# ********************************************************************************#

@bot.message_handler(commands=['help'])
def display_help(message):
    send_help_message(message)  

# ********************************************************************************#

@bot.message_handler(func=lambda message: True)
def handle_guess(message):
    if flag=="game":
        global game_number
        global win
        win=False
        count=1
        try:
            if count<=10 and win==False:
                guess = int(message.text)
                if guess < game_number:
                    bot.reply_to(message, "برو بالاتر ☝")
                elif guess > game_number:
                    bot.reply_to(message, "برو پایین تر 👇")
                else:
                    bot.reply_to(message, "تبریک میگم درست حدس زدی ")
                    bot.send_message(message,"🥳")
                    game_number = None
                    win=True
                count+=1
            elif win==True:
                bot.send_message(message.chat.id, "میخوای دوباره بازی کنیم؟", reply_markup=create_game_keyboard())
                
            else:
                win=False
                bot.reply_to(message, f"متاسفم اما باختی عدد من {game_number} بود.")
                bot.send_message(message.chat.id, "میخوای دوباره بازی کنیم؟", reply_markup=create_game_keyboard())
        except ValueError:
            bot.reply_to(message, "این بازی حدص عدده، باید عدد وارد کنی . این چیه آخه! 😠 ")
            
    
    elif flag=="age":
        try:
            birthday = (message.text)
            birth_year, birth_month, birth_day = map(int, birthday.split('/'))

            today = JalaliDate.today()
        
            age = today.year - birth_year - 1 if (today.month, today.day) < (birth_month, birth_day) else today.year - birth_year
            month = today.month - birth_month if today.month >= birth_month else 12 - birth_month + today.month
            day = today.day - birth_day if today.day >= birth_day else JalaliDate(today.year, today.month - 1, today.day).days_in_month - birth_day + today.day
            
            bot.send_message(message.chat.id,f"سن شما برابر {age} سال و {month} ماه و {day} روز است." )

        except ValueError:
            bot.send_message(message.chat.id,"ورودی نامعتبر. لطفاً تاریخ تولد را به درستی وارد کنید.")

    elif flag=="voice":
        text = (message.text) 
        x = gtts.gTTS(text, lang="en", slow=False)
        x.save("output.mp3") 
            
        audio_file = open("output.mp3", "rb")
        bot.send_voice(message.chat.id, audio_file)
        audio_file.close()
    
    elif flag=="max":      
        text = (message.text) 
        numbers = text.split(',')
        numbers = [int(num.strip()) for num in numbers]
        max_value = max(numbers)
        bot.send_message(message.chat.id, f"بزرگترین عدد: {max_value}")
 
    elif flag=="argmax":
        text=(message.text)
        numbers = text.split(',')
        numbers = [int(num.strip()) for num in numbers]
        max_index = numbers.index(max(numbers))
        bot.send_message(message.chat.id, f"اندیس بزرگترین عدد: {max_index}")
    
    elif flag=="qrcode":
        text=(message.text)
        img_QR = qrcode.make(text)
        img_QR.save("MyQrCode.png")

        qr_file=open("MyQrCode.png","rb")
        bot.send_photo(message.chat.id, qr_file)     
 
    else:
        ...

# ********************************************************************************#
def send_help_message(message):
    help_text = '''لیست دستورات:
    /start - شروع کار با بات
    /fall - دریافت فال حافظ
    /game - بازی حدس عدد
    /age - محاسبه سن شمسی
    /voice - ارسال پیام به صورت صوتی
    /max - یافتن بزرگترین عدد در آرایه
    /argmax - یافتن اندیس بزرگترین عدد در آرایه
    /qrcode - تولید کد QR از یک رشته
    /help - نمایش این راهنما'''

    bot.send_message(message.chat.id, help_text)

bot.infinity_polling()

