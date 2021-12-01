from datetime import datetime, timedelta
import os, json, asyncio, sys
from telethon import events, Button
from telethon.sync import TelegramClient as TMPTelegramClient, TelegramClient
from telethon.errors import PhoneNumberFloodError, SessionPasswordNeededError
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateUsernameRequest, UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest

ADMIN = 1499446433
API_KEY = 19931841
API_HASH = "32f8e3cf6f8657f5aa44b0276bbba53d"
STRING_SESSION = ""
ADMINS = []
Getter = None
Number = None
arc = False
TempClient = None


def saveSS():
    global SSs
    with open("SSs.json", "w+") as f:
        json.dump(SSs, f)


def saveArchSS():
    global ArchSSs
    with open("ArchSSs.json", "w+") as f:
        json.dump(ArchSSs, f)

if os.path.exists("SSs.json"):
    with open("SSs.json", "r+") as f:
        SSs = json.load(f)
else:
    SSs = {}
    with open("SSs.json", "w+") as f:
        json.dump(SSs, f)

if os.path.exists("ArchSSs.json"):
    with open("ArchSSs.json", "r+") as f:
        ArchSSs = json.load(f)
else:
    ArchSSs = {}
    with open("ArchSSs.json", "w+") as f:
        json.dump(ArchSSs, f)

def varie():
    arc 

bot = TelegramClient("bot", API_KEY, API_HASH)

@bot.on(events.NewMessage(incoming=True))
async def RaspaManager(e):
    global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, ADMINS
    if e.is_private:
        if e.chat_id == ADMIN or e.chat_id in ADMINS:
            if e.text == "/start":
                Getter, Number, TempClient = None, None, None
                if arc:
                    if varie():
                        await e.respond("**Benvenuto @diorxlatt nel tuo contenitore di account telegram\n\nUsa i bottoni sottostanti per capire come usarmi\n\n© Developer » @fsocietyUserBot**",
                                        buttons=[[Button.inline("👨🏼‍💻PANNELLO👨🏼‍💻", "voip")]])
                    else:
                        await e.respond("**Benvenuto @diorxlatt nel tuo contenitore di account telegram\n\nUsa i bottoni sottostanti per capire come usarmi\n\n© Developer » @fsocietyUserBot**",
                                        buttons=[[Button.inline("👨🏼‍💻PANNELLO👨🏼‍💻", "voip")]])
                else:
                    await e.respond("**Benvenuto @diorxlatt nel tuo contenitore di account telegram\n\nUsa i bottoni sottostanti per capire come usarmi\n\n© Developer » @fsocietyUserBot**",
                                    buttons=[[Button.inline("👨🏼‍💻PANNELLO👨🏼‍💻", "voip")]
                                    ])

            elif Getter != None:
                if Getter == 0:
                    Getter = None
                    if not e.text in SSs:
                        if not e.text in ArchSSs:
                            TempClient = TMPTelegramClient(StringSession(), API_KEY, API_HASH)
                            await TempClient.connect()
                            try:
                                await TempClient.send_code_request(phone=e.text, force_sms=False)
                                Number = e.text
                                Getter = 1
                                await e.respond("**⚠️ » Inserisci il codice di accesso**",
                                                buttons=[[Button.inline("❌ Annulla ❌", "voip")]])
                            except PhoneNumberFloodError:
                                await e.respond("**❌ » Troppi tentativi, prova un altro numero! [FloodWait]**",
                                                buttons=[[Button.inline("✨ Ritenta ✨", "addvoip")]])
                            except:
                                await e.respond("**❌ » Numero non valido**",
                                                buttons=[[Button.inline("✨ Ritenta ✨", "addvoip")]])
                        else:
                            await e.respond("**🔖 » Voip archiviato, riaggiungilo**",
                                            buttons=[[Button.inline("📁 Voip Archiviati", "arch")],
                                                     [Button.inline("✨ Ritenta ✨", "addvoip")]])
                    else:
                        await e.respond("**❌ » Voip già aggiunto**", buttons=[[Button.inline("✨ Ritenta ✨", "addvoip")]])
                elif Getter == 1:
                    try:
                        await TempClient.sign_in(phone=Number, code=e.text)
                        SSs[Number] = StringSession.save(TempClient.session)
                        Getter, Number = None, None
                        saveSS()
                        await e.respond("**✅ » Voip Aggiunto**",
                                        buttons=[[Button.inline("🔙 back 🔙", "voip")]])
                    except SessionPasswordNeededError:
                        Getter = 2
                        await e.respond("**🔑 » Inserisci La Password**",
                                        buttons=[[Button.inline("❌ Annulla ❌", "voip")]])
                    except:
                        Getter, Number = None, None
                        await e.respond("**❌ » Codice Errato**", buttons=[[Button.inline("✨ Ritenta ✨", "addvoip")]])
                elif Getter == 2:
                    try:
                        await TempClient.sign_in(phone=Number, password=e.text)
                        SSs[Number] = StringSession.save(TempClient.session)
                        Getter, Number = None, None
                        saveSS()
                        await e.respond("**✅ » Voip Aggiunto**",
                                        buttons=[[Button.inline("🔙 back 🔙", "voip")]])
                    except:
                        Getter, Number = None, None
                        await e.respond("**❌ » Password Errata**", buttons=[[Button.inline("✨ Ritenta ✨", "addvoip")]])
                elif Getter == 3:
                    Getter = None
                    if e.text in SSs:
                        await e.respond(f"**⚙️ » Gestione »** `{e.text}`", buttons=[
                            [Button.inline("📁 » FILE", "getSSS")],
                            [Button.inline("📁 » Archivia", "arch;" + e.text)],
                            [Button.inline("ℹ️ » Informazioni", "visualizza;" + e.text),
                             Button.inline("🔧 » Modifica / Ricevi codice", "setta;" + e.text)], [
                                Button.inline("➖ » Rimuovi", "del;" + e.text)], [Button.inline("🔙 back 🔙", "voip")]])
                    else:
                        await e.respond("**❌ » Voip Non Trovato**", buttons=[[Button.inline("✨ Ritenta ✨", "voips")]])
                elif Getter == 4:
                    Getter = None
                    if e.text in ArchSSs:
                        await e.respond(f"**🔧 » Gestione »** `{e.text}`", buttons=[
                            [Button.inline("🔄 » Riaggiungi", "add;" + e.text),
                             Button.inline("➖ » Rimuovi", "delarch;" + e.text)], [Button.inline("🔙 back 🔙", "voip")]])
                    else:
                        await e.respond("**❌ » Voip Non Trovato ❌**", buttons=[[Button.inline("✨ Ritenta ✨", "voips")]])
                elif Getter == 5:
                    Getter = None
                    await e.respond("**cc**")
                elif Getter == 6:
                    await e.respond("g")
                elif Getter == 9:
                    Getter = None
                    try:
                        await TempClient(UpdateUsernameRequest(e.text))
                        await e.respond("✅ » Username Impostato",
                                        buttons=[[Button.inline("🔙 back 🔙", "back")]])
                    except:
                        await e.respond("❌ » Username occupato o non valido!",
                                        buttons=[[Button.inline("🔙 back 🔙", "back")]])
                elif Getter == 10:
                    Getter = None
                    try:
                        path = await bot.download_media(e.media)
                        print(path)
                        await TempClient(UploadProfilePhotoRequest(
                            await TempClient.upload_file(path)
                        ))
                        await e.respond("✅ » Foto impostata",
                                        buttons=[[Button.inline("🔙 back 🔙", "back")]])
                    except Exception as e:
                        print(str(e))
                        await e.respond("❌ » Foto non impostata!\n__Formato non valido!__",
                                        buttons=[[Button.inline("🔙 back 🔙", "back")]])
                elif Getter == 12:
                    Getter = None
                    try:
                        await TempClient(UpdateProfileRequest(
                            first_name=e.text
                        ))
                        await e.respond("✅ » Nome impostato",
                                        buttons=[[Button.inline("🔙 back 🔙", "back")]])
                    except:
                        await e.respond("❌ » Nome non impostato",
                                        buttons=[[Button.inline("🔙 back 🔙", "back")]])
                elif Getter == 13:
                    Getter = None
                    try:
                        await TempClient(UpdateProfileRequest(
                            last_name=e.text
                        ))
                        await e.respond("✅ » Cognome impostato",
                                        buttons=[[Button.inline("🔙 back 🔙", "back")]])
                    except:
                        await e.respond("❌ » Cognome non impostato",
                                        buttons=[[Button.inline("🔙 back 🔙", "back")]])


@bot.on(events.CallbackQuery())
async def callbackQuery(e):
    global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, ADMINS
    if e.sender_id == ADMIN or e.sender_id in ADMINS:
        if e.data == b"back":
            Getter, Number, TempClient = None, None, None
            await e.edit("**Benvenuto @diorxlatt nel tuo contenitore di account telegram\n\nUsa i bottoni sottostanti per capire come usarmi\n\n© Developer » @fsocietyUserBot**", buttons=[[Button.inline("👨🏼‍💻PANNELLO👨🏼‍💻", "voip")]])
        elif e.data == b"getSSS":
                await e.respond("🗂 » File voip", file="SSs.json")
        elif e.data == b"voip":
            Getter, Number, TempClient = None, None, None
            await e.edit(f"**☔️PANNELLO BOT:☔️**\n\n**⚡️USA I TASTI QUA SOTTO⚡️**\n\n🎯**Numero di voip:** {SSs.__len__()}",
                         buttons=[[Button.inline("➕ » Aggiungi", "addvoip"), Button.inline("🔐 » Gestione", "voips")],
                                  [Button.inline("📁 » Archivio", "arch")], [Button.inline("🗂 » File", "getSSS")], [Button.inline("🔙 back 🔙", "back")]])
        elif e.data == b"addvoip":
            Getter = 0
            await e.edit("**☎️ » Inserisci il numero**",
                         buttons=[Button.inline("❌ Annulla ❌", "voip")])
        elif e.data == b"voips":
            if SSs.__len__() > 0:
                Getter = 3
                msg = "☎️ » Invia il numero del voip che vuoi gestire\n\n**📚 » LISTA VOIP**"
                for n in SSs:
                    msg += f"\n`{n}`"
                await e.edit(msg, buttons=[Button.inline("❌ Annulla ❌", "voip")])
            else:
                await e.edit("**❌ » Non hai aggiunto nessun voip **",
                             buttons=[[Button.inline("➕ » Aggiungi", "addvoip")], [Button.inline("🔙 back 🔙", "voip")]])
        elif e.data == b"arch":
            if ArchSSs.__len__() > 0:
                Getter = 4
                msg = f"📁 » Voip Archiviati » **{ArchSSs.__len__()}**\n\n__☎️ » Invia il numero del voip archiviato che vuoi gestire__\n\n**LISTA VOIP ARCHIVIATI**"
                for n in ArchSSs:
                    msg += f"\n`{n}`"
                await e.edit(msg, buttons=[Button.inline("❌ Annulla ❌", "voip")])
            else:
                await e.edit("**❌ » Non hai archiviato nessun voip**", buttons=[[Button.inline("🔙 back 🔙", "voip")]])
        else:
            st = e.data.decode().split(";")
            if st[0] == "setnome":
                if st[1] in SSs:
                    Getter = 12
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit("**🥀 » Inserisci il nome**\nNome attuale: " + me.first_name)
            elif st[0] == "setcognome":
                if st[1] in SSs:
                    Getter = 13
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit(
                        "**👑 » Inserisci il cognome**\nAttuale: " + str(me.last_name))
            elif st[0] == "getmsg":
                TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                await TempClient.connect()
                messages = await TempClient.get_messages(777000, limit=1)
                await e.client.send_message(e.sender_id, "**🚨 » MESSAGGIO D'ACCESSO RICEVUTO**\n\n"+ messages[0].message)
            elif st[0] == "setta":
                if st[1] in SSs:
                    await e.edit(
                        "**⚙️ » Impostazioni voip:** " + st[1] + "\n__🔙 » /start__",
                        buttons=[
                            [Button.inline("🌩 » Codice d'accesso", "getmsg;" + st[1])], [Button.inline("💠 » Imposta username", "setusername;" + st[1])],
                                 [Button.inline("🖼 » Imposta foto profilo", "setphoto;" + st[1])],
                                 [Button.inline("🥀 » Imposta nome", "setnome;" + st[1])],

                                 [Button.inline("👑 » Imposta cognome", "setcognome;" + st[1])]])
            elif st[0] == "visualizza":
                if st[1] in SSs:
                    try:
                        TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                        await TempClient.connect()
                        me = await TempClient.get_me()
                        path = await TempClient.download_profile_photo("me")
                        await bot.send_file(e.sender_id, path,
                                            caption="🌐 » Username: " + str(me.username) + "\n❇️ » Nome :" + me.first_name + "\n💠 » Cognome: " + str(
                                                me.last_name) + "\n🆔 » ID: " + str(
                                                me.id) + "\n🔙 » /start",
                                            buttons=[[Button.inline("🔧IMPOSTAZIONI VOIP🔧", "setta;" + st[1])]])

                    except Exception as e:
                        print(str(e))
            elif st[0] == "setusername":
                if st[1] in SSs:
                    Getter = 9
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit("**🌐 » Invia l'username da impostare**\n__☑️ » Attuale: " + me.username,
                                 buttons=[[Button.inline("🔙 back 🔙", "back")]])
            elif st[0] == "setphoto":
                if st[1] in SSs:
                    Getter = 10
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await TempClient.connect()
                    await e.edit("**🖼 » Invia la foto da impostare **",
                                 buttons=[[Button.inline("🔙 back 🔙", "voip")]])
            elif st[0] == "arch":
                if st[1] in SSs:
                    if not st[1] in ArchSSs:
                        ArchSSs[st[1]] = SSs[st[1]]
                        saveArchSS()
                    del (SSs[st[1]])
                    saveSS()
                    await e.edit("**✅ » Voip Archiviato Correttamente**",
                                 buttons=[[Button.inline("🔙 back 🔙", "voip")]])
                else:
                    await e.edit("**❌ » Voip Non Trovato**", buttons=[[Button.inline("🔙 back 🔙", "voip")]])
            elif st[0] == "add":
                if st[1] in ArchSSs:
                    SSs[st[1]] = ArchSSs[st[1]]
                    saveSS()
                    del (ArchSSs[st[1]])
                    saveArchSS()
                    await e.edit("**✅ » Voip Riaggiunto**",
                                 buttons=[[Button.inline("🔙 back 🔙", "voip")]])
                else:
                    await e.edit("**❌ » Voip Non Trovato**", buttons=[[Button.inline("🔙 back 🔙", "voip")]])
            elif st[0] == "del":
                if st[1] in SSs:
                    CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await CClient.connect()
                    try:
                        me = await CClient.get_me()
                        if me != None:
                            async with CClient as client:
                                await client.log_out()
                    except:
                        pass
                    del (SSs[st[1]])
                    saveSS()
                    await e.edit("**✅ » Voip Rimosso **", buttons=[[Button.inline("🔙 back 🔙", "voip")]])
                else:
                    await e.edit("**❌ » Voip Già Rimosso**", buttons=[[Button.inline("🔙 back 🔙", "voip")]])
            elif st[0] == "delarch":
                if st[1] in ArchSSs:
                    CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await CClient.connect()
                    try:
                        me = await CClient.get_me()
                        if me != None:
                            async with CClient as client:
                                await client.log_out()
                    except:
                        pass
                    del (ArchSSs[st[1]])
                    saveArchSS()
                    await e.edit("**✅ » Voip Rimosso Correttamente**", buttons=[[Button.inline("🔙 back 🔙", "voip")]])
                else:
                    await e.edit("**❌ » Voip Già Rimosso**", buttons=[[Button.inline("🔙 back 🔙", "voip")]])
            elif st[0] == "info":
                await e.answer(f"ℹ️ » L' errore è avvenuto nel seguente voip » {st[1]} ")


bot.start()

bot.run_until_disconnected()
