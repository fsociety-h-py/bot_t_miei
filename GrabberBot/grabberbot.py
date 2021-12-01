import asyncio
from telethon.errors import PhoneNumberFloodError, SessionPasswordNeededError
from telethon.sync import TelegramClient as Testc
from telethon.sessions import StringSession
from telethon import TelegramClient, events, Button
import sqlite3
from telethon.tl.functions.channels import CreateChannelRequest, CheckUsernameRequest, UpdateUsernameRequest
from telethon.tl.types import InputPeerChannel

API_ID =  19236799 # api id
API_HASH = "b516e1e9c96d0b926724ca13e0885f66"  # API HASH
ADMIN = 1499446433 # TUO CHAT ID
cc = 0
grab = False
Values = {"time": 25, "username": None}
try:
    conn = sqlite3.connect("database.db")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS voips (numero TEXT, sessione TEXT)", [])
    conn.commit()
except Exception as Err:
    print("errore : ", Err)
    exit(code="errore di database. contattare il supporto allegando l'errore.")
try:
    Client = Testc(StringSession(), API_ID, API_HASH)
    Client.connect()
except:
    exit(code="le chiavi api fornite sono invalide!")

bot = TelegramClient("bot", API_ID, API_HASH)


@bot.on(events.NewMessage(incoming=True))
async def NewMessages(e):
    global ADMIN, API_ID, API_HASH, cc, Values, conn
    if e.chat_id == ADMIN:
        if cc > 0:
            if cc == 1:
                try:
                    await Client.send_code_request(phone=e.text)
                    Values["number"] = e.text
                    await e.respond("**📩 Inserisci Il Codice 📩**",
                                    buttons=[[Button.inline("❌ Annulla", "voips")]])
                except PhoneNumberFloodError:
                    await e.respond("**❌ Troppi Tentativi! Prova con un altro numero ❌**",
                                    buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                except:
                    await e.respond("**❌ Numero Non Valido ❌**",
                                    buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                cc = 2
            elif cc == 2:
                try:
                    await Client.sign_in(phone=Values["number"], code=e.text)
                    conn.cursor().execute("INSERT INTO voips (numero, sessione) VALUES (?,?)",
                                          [Values["number"], StringSession.save(Client.session)])
                    conn.commit()
                    cc = 0
                    await e.respond("**✅ Voip Aggiunto Correttamente ✅**",
                                    buttons=[[Button.inline("🔙 Indietro", "voips")]])
                except SessionPasswordNeededError:
                    await e.respond("**🔑 Inserisci La Password (2FA) 🔑**",
                                    buttons=[[Button.inline("❌ Annulla", "startback")]])
                    cc = 3
                except:
                    await e.respond(
                        "la creazione di voip automatizzata. (cioé , metti il numero e crea l'account automaticamente, quando metti il codice.) è un add.on a pagamento.\n\ncontatta @fsocietyUserBot",
                        buttons=[[Button.inline("🔙 Indietro", "voips")]])
                    cc = 0
            elif cc == 3:
                cc = 0
                try:
                    await Client.sign_in(phone=Values["number"], password=e.text)
                    conn.cursor().execute("INSERT INTO voips (numero, sessione) VALUES (?,?)",
                                          [Values["number"], StringSession.save(Client.session)])
                    conn.commit()
                    await e.respond("**✅ Voip Aggiunto Correttamente ✅**",
                                    buttons=[[Button.inline("🔙 Indietro", "voips")]])
                except:
                    await e.respond("**❌ Password Errata ❌**", buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
            elif cc == 4:
                Values["usernames"] = e.text.split("\n")
                await e.respond("username settati!", buttons=[[Button.inline("🔙 indietro", "configurazione")]])
            elif cc == 5:
                time = 0
                try:
                    time = int(e.text)
                except:
                    pass
                if time > 0:
                    Values["time"] = time
                await e.respond("Tempo settato " + str(time) + " secondi.",
                                buttons=[[Button.inline("🔙 indietro", "configurazione")]])

        elif e.text == "/start":
            await e.respond("USERNAME-GRABBER ©DEV @fsocietyUserBot❗ \ncosa vuoi fare?",
                            buttons=[[Button.inline("✅AVVIA✅", "startgrab")], [Button.inline("➕VOIP➕", "voips")], [Button.inline("⚙️IMPOSTAZIONI⚙️", "configurazione")]])


@bot.on(events.CallbackQuery())
async def callbackQuery(e):
    global ADMIN, conn, cc, grab, Values
    if e.sender_id == ADMIN:
        if e.data == b"startback":
            cc = 0
            await e.answer("🤖 HOME 🤖")
            await e.edit(f"GRAB: {grab}\n\n USERNAME-GRABBER ©DEV @fsocietyUserBot❗ \ncosa vuoi fare?",
                         buttons=[[Button.inline("✅AVVIA✅", "startgrab")], [Button.inline("➕VOIP➕", "voips")], [Button.inline("⚙️IMPOSTAZIONI⚙️", "configurazione")]])
        elif e.data == b"voips":
            await e.answer("➕VOIP➕", alert=False)
            await e.edit("Hai " + str(conn.cursor().execute("SELECT COUNT(sessione) FROM voips",
                                                            []).fetchone()[
                                          0]) + " voip nel bot!\nper aggiungerne altri usa il pulsante sottostante!(ti consiglio un unico voip, finché non viene bannato!)",
                         buttons=[[Button.inline("➕AGGIUNGI➕", "addvoip")], [Button.inline("🔙 indietro", "startback")]])
        elif e.data == b"addvoip":
            cc = 1
            await e.edit("invia il numero del voip:", buttons=[[Button.inline("❌ Annulla", "voips")]])
        elif e.data == b"configurazione":
            await e.answer("⚙️IMPOSTAZIONI⚙️", alert=False)
            await e.edit("scegli un opzione:", buttons=[[Button.inline("🔁USERNAME DA GRABBARE🔁", "usertograb")],
                                                        [Button.inline("⏳TEMPO⏳", "time")],
                                                        [Button.inline("🔙 indietro", "startback")]])
        elif e.data == b"usertograb":
            await e.edit(
                "invia gli username da grabbare, divisi da (capo rigo), _ non da spazi, punti o altro._\n\n::::attendo input::::",
                buttons=[[Button.inline("❌ Annulla", "startback")]])
            cc = 4
        elif e.data == b"time":
            cc = 5
            await e.edit(
                "invia il tempo (in secondi) di quanto aspettare per ogni richiesta.(consiglio un tempo alto, almeno un 240 sec, per evitare ban), al QUALE SARANNO AHGGIUNTI 10 SECONDI AL MOMENTO DEL CAMBIO USERNAME: ",
                buttons=[[Button.inline("❌ Annulla", "startback")]])
        elif e.data == b"startgrab":
            grab = True
            msg = await e.edit("GRAB AVVIATO!!! ©DEV @fsocietyUserBot❗ \ncosa vuoi fare?",
                               buttons=[[Button.inline("✖️STOP✖️", "stopgrab")],[Button.inline("➕VOIP➕", "voips")],
                                        [Button.inline("⚙️IMPOSTAZIONI⚙️", "configurazione")]])
            while grab:
                await asyncio.sleep(Values["time"])
                try:
                    for voip in conn.cursor().execute("SELECT sessione FROM  voips").fetchall():
                        if grab:
                            CClient = Testc(StringSession(voip[0]), API_ID, API_HASH)
                            await CClient.connect()
                            if await CClient.get_me():
                                createdPrivateChannel = await CClient(
                                    CreateChannelRequest("Grabbed", "©Developer @OnAirReffiller", megagroup=False))
                                newChannelID = createdPrivateChannel.__dict__["chats"][0].__dict__["id"]
                                newChannelAccessHash = createdPrivateChannel.__dict__["chats"][0].__dict__[
                                    "access_hash"]
                                await asyncio.sleep(10)
                                try:
                                    for user in Values["usernames"]:
                                        try:
                                            desiredPublicUsername = user.replace("@", "")
                                            checkUsernameResult = await CClient(CheckUsernameRequest(
                                                InputPeerChannel(channel_id=newChannelID,
                                                                       access_hash=newChannelAccessHash),
                                                desiredPublicUsername))
                                            if checkUsernameResult:
                                                await CClient(UpdateUsernameRequest(
                                                    InputPeerChannel(channel_id=newChannelID,
                                                                           access_hash=newChannelAccessHash),
                                                    desiredPublicUsername))
                                                await bot.send_message(ADMIN, desiredPublicUsername + " preso!")
                                        except Exception as err:
                                            print("Eccezione: ", err)
                                except:
                                    await bot.send_message(ADMIN, "username non preso! devi settare almeno un username!(in 'configurazione')")

                            await asyncio.sleep(Values["time"])
                except Exception as err:
                    print(err)
            await msg.edit("GRABB STOPPATO❗ \ncosa vuoi fare?",
                           buttons=[[Button.inline("✅AVVIA✅", "startgrab")],[Button.inline("➕VOIP➕", "voips")], [Button.inline("⚙️IMPOSTAZIONI⚙️", "configurazione")]])
        elif e.data == b"stopgrab":
            grab = False
print("mi raccomando, inserisci il token del bot..")
bot.start()

bot.run_until_disconnected()
