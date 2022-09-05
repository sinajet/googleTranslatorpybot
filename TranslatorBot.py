import logging
from deep_translator import GoogleTranslator as ts
from TrbotToken import *
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters,CallbackQueryHandler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
#transdefs===================================================
t = ts()
langDict = t.get_supported_languages(as_dict=True)
langList = t.get_supported_languages()
frmPage=0
toPage=0
frm="auto"
to="en"
frmFull="detect Language"
toFull="english"
def tr(txt):
    global frm,to
    return ts(source=frm, target=to).translate(txt)
def exchngLang():
    global frm,to,frmFull,toFull
    a=frm
    frm=to
    to=a
    b=frmFull
    frmFull=toFull
    toFull=b
    
#keyboards==============================================
inLangKeyboard = []
inLangKeyboard1 = []
inLangKeyboard2 = []
counter=0
for i in range(2):
    for k in range(18):
        for j in range(3):
            inLangKeyboard= inLangKeyboard + [InlineKeyboardButton(langList[counter], callback_data=str(langList[counter]))]
            counter+=1
        inLangKeyboard1 +=  [inLangKeyboard]
        inLangKeyboard = []
    inLangKeyboard2 += [inLangKeyboard1]
    inLangKeyboard1 = []
inLangKeyboard2[1] += [[InlineKeyboardButton(langList[108], callback_data=str(langList[108]))]]
#btnDefs================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global frm,to
    startTxt="""
👉with this bot you can translate Your Text any language on this bot
🔎also it use google translate For translaiteing!
▶️for Start translating send /translator
😍more information about me with this Command: /aboutme
"""
    await update.message.reply_text(startTxt)

async def translateTelDef(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global frm,to,frmFull,toFull
    trnsltkeyboard = [
    [
        InlineKeyboardButton(frmFull.capitalize(), callback_data="f1"),
        InlineKeyboardButton(toFull.capitalize(), callback_data="t1"),
    ],
    [
        InlineKeyboardButton("🔁", callback_data="<=>")
    ]
    ]
    reply_markup = InlineKeyboardMarkup(trnsltkeyboard)
    await update.message.reply_text(f"You can Change your Language by pushing buttons😉\nSend your Text for translating😍\nfrom👉{frmFull.capitalize()}               to👉{toFull.capitalize()}", reply_markup=reply_markup)
    
    
    
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global frm,to,frmFull,toFull,frmPage,toPage
    q=update.callback_query
    if frmFull!="detect Language" and q.data=="<=>":
        exchngLang()
        trnsltkeyboard = [
    [
        InlineKeyboardButton(frmFull.capitalize(), callback_data="f1"),
        InlineKeyboardButton(toFull.capitalize(), callback_data="t1"),
    ],
    [
        InlineKeyboardButton("🔁", callback_data="<=>")
    ]
    ]
        reply_markup = InlineKeyboardMarkup(trnsltkeyboard)
        await q.edit_message_text(f"You can Change your Language by pushing buttons😉\nSend your Text for translating😍\nfrom👉{frmFull.capitalize()}               to👉{toFull.capitalize()}", reply_markup=reply_markup)
    elif frmFull=="detect Language" and q.data=="<=>":
        trnsltkeyboard = [
        [
            InlineKeyboardButton(frmFull.capitalize(), callback_data="f1"),
            InlineKeyboardButton(toFull.capitalize(), callback_data="t1"),
        ],
        [
            InlineKeyboardButton("🔁", callback_data="<=>")
        ]
        ]
        try:
            reply_markup = InlineKeyboardMarkup(trnsltkeyboard)
            await q.edit_message_text(f"You can Change your Language by pushing buttons😉\nSend your Text for translating😍\nWe cant translate to a Detect Language😐\nfrom👉{frmFull.capitalize()}               to👉{toFull.capitalize()}", reply_markup=reply_markup)
        except:
            pass
#mainKyeboard================================================================
    elif q.data=="mainKeyboard":
        frmPage=0
        toPage=0
        trnsltkeyboard = [
    [
        InlineKeyboardButton(frmFull.capitalize(), callback_data="f1"),
        InlineKeyboardButton(toFull.capitalize(), callback_data="t1"),
    ],
    [
        InlineKeyboardButton("🔁", callback_data="<=>")
    ]
    ]
        reply_markup = InlineKeyboardMarkup(trnsltkeyboard)
        await q.edit_message_text(f"You can Change your Language by pushing buttons😉\nSend your Text for translating😍\nfrom👉{frmFull.capitalize()}               to👉{toFull.capitalize()}", reply_markup=reply_markup)
#keyboardsCommands=============================================================

    elif q.data=="f1":
        frmPage=1
        LangKeyboard = [[InlineKeyboardButton("Back to Translation", callback_data="mainKeyboard")],[InlineKeyboardButton("Detect Language", callback_data="auto")]] + inLangKeyboard2[0] + [[InlineKeyboardButton("➡️", callback_data="f2")]]
        reply_markup = InlineKeyboardMarkup(LangKeyboard)
        await q.edit_message_text(f"Select a Language🔎!\nTranslate from: {frmFull.capitalize()}", reply_markup=reply_markup)
    elif q.data=="f2":
        frmPage=1
        LangKeyboard = inLangKeyboard2[1] + [[InlineKeyboardButton("⬅️", callback_data="f1")]]
        reply_markup = InlineKeyboardMarkup(LangKeyboard)
        await q.edit_message_text(f"Select a Language🔎!\nTranslate from: {frmFull.capitalize()}", reply_markup=reply_markup)
    elif q.data=="t1":
        toPage=1
        LangKeyboard = [[InlineKeyboardButton("Back to Translation", callback_data="mainKeyboard")]] + inLangKeyboard2[0] + [[InlineKeyboardButton("➡️", callback_data="t2")]]
        reply_markup = InlineKeyboardMarkup(LangKeyboard)
        await q.edit_message_text(f"Select a Language🔎!\nTranslate to: {toFull.capitalize()}", reply_markup=reply_markup)
    elif q.data=="t2":
        toPage=1
        LangKeyboard = inLangKeyboard2[1] + [[InlineKeyboardButton("⬅️", callback_data="t1")]]
        reply_markup = InlineKeyboardMarkup(LangKeyboard)
        await q.edit_message_text(f"Select a Language🔎!\nTranslate to: {toFull.capitalize()}", reply_markup=reply_markup)
    else:
        if frmPage==1:
            if q.data != toPage:
                frm=langDict[q.data]
                frmFull=q.data
                frmPage=0
                trnsltkeyboard = [
                [
                    InlineKeyboardButton(frmFull.capitalize(), callback_data="f1"),
                    InlineKeyboardButton(toFull.capitalize(), callback_data="t1"),
                ],
                [
                    InlineKeyboardButton("🔁", callback_data="<=>")
                ]
                ]  
                reply_markup = InlineKeyboardMarkup(trnsltkeyboard)
                await q.edit_message_text(f"You can Change your Language by pushing buttons😉\nSend your Text for translating😍\nfrom👉{frmFull.capitalize()}               to👉{toFull.capitalize()}", reply_markup=reply_markup)
            else:
                LangKeyboard = [[InlineKeyboardButton("Back to Translation", callback_data="mainKeyboard")],[InlineKeyboardButton("Detect Language", callback_data="auto")]] + inLangKeyboard2[0] + [[InlineKeyboardButton("➡️", callback_data="f2")]]
                reply_markup = InlineKeyboardMarkup(LangKeyboard)
                await q.edit_message_text(f"Select a Language🔎!\nCant translate Between same Languages🤷‍♂️\nTranslate from: {frmFull.capitalize()}", reply_markup=reply_markup)
        elif toPage==1:
            if q.data != frmFull:
                to=langDict[q.data]
                toFull=q.data
                toPage=0
                trnsltkeyboard = [
                [
                    InlineKeyboardButton(frmFull.capitalize(), callback_data="f1"),
                    InlineKeyboardButton(toFull.capitalize(), callback_data="t1"),
                ],
                [
                    InlineKeyboardButton("🔁", callback_data="<=>")
                ]
                ]  
                reply_markup = InlineKeyboardMarkup(trnsltkeyboard)
                await q.edit_message_text(f"You can Change your Language by pushing buttons😉\nSend your Text for translating😍\nfrom👉{frmFull.capitalize()}               to👉{toFull.capitalize()}", reply_markup=reply_markup)
            else:
                LangKeyboard = [[InlineKeyboardButton("Back to Translation", callback_data="mainKeyboard")],[InlineKeyboardButton("Detect Language", callback_data="auto")]] + inLangKeyboard2[0] + [[InlineKeyboardButton("➡️", callback_data="t2")]]
                reply_markup = InlineKeyboardMarkup(LangKeyboard)
                await q.edit_message_text(f"Select a Language🔎!\nCant translate Between same Languages🤷‍♂️\nTranslate from: {frmFull.capitalize()}", reply_markup=reply_markup)

async def trTXT(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(tr(update.message.text))
  
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton('Telegram Channel!', url='https://t.me/sinajet')],
        [InlineKeyboardButton('YouTube Channel!', url='https://www.youtube.com/c/SinaJet')],
        [InlineKeyboardButton('Bot Source On my Github!', url='https://github.com/sinajet/googleTranslatorpybot')]
    ]
    reply_markup = InlineKeyboardMarkup (keyboard)
    await update.message.reply_text("Hi, My name is Sina!\nYou can Follow me on these Social Media Sites!!", reply_markup=reply_markup)  
#mainDef================================================
def main()-> None:
    app = Application.builder().token(tkn()).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aboutme", about))
    app.add_handler(CommandHandler("translator", translateTelDef))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT,trTXT))
    app.run_polling()
if __name__ == "__main__":
    main()