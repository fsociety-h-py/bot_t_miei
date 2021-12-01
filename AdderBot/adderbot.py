

import os, json, asyncio, sys
from logging import basicConfig, getLogger, WARNING
from telethon import TelegramClient, events, Button
from telethon.sync import TelegramClient as TMPTelegramClient
from telethon.errors import FloodWaitError, PhoneNumberFloodError, SessionPasswordNeededError, UsersTooMuchError
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.sessions import StringSession
from importlib import import_module

basicConfig(format="%(asctime)s - [Bot] %(message)s", level=WARNING)
LOGS = getLogger(__name__)

ADMIN = 1499446433

API_KEY = "10063901"

API_HASH = "807d21e2810e6a36de88effa251f8e26"

STRING_SESSION = ""

Getter = None
Number = None
TempClient = None
Grab = None
inAdding = False
canAdd = True
AddedUsers = []

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
	

def saveSS():
	global SSs
	with open("SSs.json", "w+") as f:
		json.dump(SSs, f)
	

def saveArchSS():
	global ArchSSs
	with open("ArchSSs.json", "w+") as f:
		json.dump(ArchSSs, f)
	

async def addUsers(client, Users, group):
	global canAdd, AddedUsers
	AddedUsers = []
	for user in Users:
		if canAdd:
			AddedUsers.append(user)
			try:
				await client(InviteToChannelRequest(group, [user]))
				await asyncio.sleep(0.2)
			except:
				pass
		else:
			break
		
	

async def timeoutAdd(timeout):
	global canAdd
	await asyncio.sleep(timeout)
	canAdd = False

bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)

@bot.on(events.NewMessage(incoming=True))
async def RaspaManager(e):
	global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, Grab, inAdding, canAdd, AddedUsers
	if e.is_private and e.chat_id == ADMIN:
		if e.text == "/start":
			Getter, Number, TempClient = None, None, None
			await e.respond("**Benvenuto nell'adderbot creato dalla fsociety per te\n\n per utilizzzare il bot usa i pulsanti qui sotto**", buttons=[[Button.inline("🙈 Sessioni", "voip"), Button.inline("Proxy 🌐", "proxy")], [Button.inline("💣 Ruba", "grab"), Button.inline("Adder ➕", "add")], [Button.url("👨🏼‍💻 Developer 👨🏼‍💻", "https://t.me/fsocietyUserBot")]])
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
							await e.respond("**📨 Inserisci il Codice 📨**", buttons=[Button.inline("❌ Annulla ❌", "voip")])
						except PhoneNumberFloodError:
							await e.respond("**⚠️ **Errore:** Troppi tentativi! Prova più tardi o inserisci un altro numero.**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
						except:
							await e.respond("**❌ Numero non Valido ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
					else:
						await e.respond("**❌ VoIP Archiviato! Riaggiungilo. ❌**", buttons=[[Button.inline("🗂 VoIP Archiviati 🗂", "arch")], [Button.inline("🔄 Riprova 🔄", "addvoip")]])
				else:
					await e.respond("**❌ VoIP già Aggiunto. ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
			elif Getter == 1:
				try:
					await TempClient.sign_in(phone=Number, code=e.text)
					SSs[Number] = TempClient.session.save()
					Getter, Number = None, None
					saveSS()
					await e.respond("**✅ VoIP Aggiunto Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				except SessionPasswordNeededError:
					Getter = 2
					await e.respond("**🔑 Inserisci la Password (2FA) 🔑**", buttons=[Button.inline("❌ Annulla ❌", "voip")])
				except:
					Getter, Number = None, None
					await e.respond("**❌ Codice Errato ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
			elif Getter == 2:
				try:
					await TempClient.sign_in(phone=Number, password=e.text)
					SSs[Number] = TempClient.session.save()
					Getter, Number = None, None
					saveSS()
					await e.respond("**✅ VoIP Aggiunto Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				except:
					Getter, Number = None, None
					await e.respond("**❌ Password Errata ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
			elif Getter == 3:
				Getter = None
				if e.text in SSs:
					await e.respond(f"**⚙️ Pannello di Controllo del Numero »** `{e.text}`", buttons=[[Button.inline("🗂 Archivia", "arch;" + e.text), Button.inline("Rimuovi 🗑", "del;" + e.text)], [Button.inline("🔙 Indietro 🔙", "voip")]])
				else:
					await e.respond("**❌ VoIP non Trovato ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "voips")])
			elif Getter == 4:
				Getter = None
				if e.text in ArchSSs:
					await e.respond(f"**⚙️ Pannello di Controllo del Numero »** `{e.text}`", buttons=[[Button.inline("➕ Riaggiungi", "add;" + e.text), Button.inline("Rimuovi 🗑", "delarch;" + e.text)], [Button.inline("🔙 Indietro 🔙", "voip")]])
				else:
					await e.respond("**❌ VoIP non Trovato ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "voips")])
			elif Getter == 5:
				Getter == None
				if e.text != None and e.text != "":
					if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):
						if not " " in e.text:
							Grab = e.text
							await e.respond("**✅ Gruppo impostato Correttamente ✅**", buttons=[[Button.inline("➕ Adder ➕", "add")], [Button.inline("🔙 Indietro", "grab")]])
						else:
							await e.respond("**❌ Puoi inserire un solo Gruppo ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "setgrab")])
					else:
						await e.respond("**❌ Devi inserire un Link o una @ di un gruppo ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "setgrab")])
				else:
					await e.respond("**⚠️ Formato non Valido ⚠️**", buttons=[Button.inline("🔄 Riprova 🔄", "setgrab")])
			elif Getter == 6:
				Getter == None
				if e.text != None and e.text != "":
					if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):
						if not " " in e.text:
							inAdding = True
							canNotify = True
							banned = []
							Users = []
							msg = await e.respond("**✅ Adder in Corso ✅**", buttons=[Button.inline("❌ Interrompi", "stop")])
							for SS in SSs:
								isAlive = False
								CClient = TMPTelegramClient(StringSession(SSs[SS]), API_KEY, API_HASH)
								await CClient.connect()
								try:
									me = await CClient.get_me()
									if me == None:
										isAlive = False
									else:
										isAlive = True
								except:
									isAlive = False
								if isAlive:
									async with CClient as client:
										try:
											ent = await client.get_entity(Grab)
											try:
												await client(JoinChannelRequest(Grab))
											except:
												pass
											try:
												users = client.iter_participants(ent.id, aggressive=True)
												async for user in users:
													try:
														if not user.bot and not user.id in Users:
															Users.append(user.id)
													except:
														pass
											except:
												await msg.edit("**❌ Gruppo non Valido ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "grab")])
												canNotify = False
												break
										except FloodWaitError as err:
											await msg.edit(f"**⏳ Attendi {err.seconds} prima di Ri-Utilizzare il Bot ⏳**", buttons=[Button.inline("🔙 Indietro 🔙", "back")])
											canNotify = False
											break
										except:
											await msg.edit("**❌ Gruppo non Trovato ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "grab")])
											canNotify = False
											break
										try:
											ent2 = await client.get_entity(e.text)
											try:
												await client(JoinChannelRequest(e.text))
											except:
												pass
											canAdd = True
											await asyncio.gather(addUsers(client, Users, ent2.id), timeoutAdd(120))
											for user in AddedUsers:
												if user in Users:
													Users.remove(user)
										except:
											await msg.edit("**❌ Gruppo non Trovato ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "add")])
											canNotify = False
											break
								else:
									banned.append(SS)
									await e.respond(f"**⚠️ Attenzione »** __Il VoIP__ `{SS}` __potrebbe essere stato Bannato da Telegram o puoi averlo Disconnesso per Errore! Se l'hai Disconnesso per Errore Riaggiungilo.__")
							if banned.__len__() > 0:
								for n in banned:
									if n in SSs:
										del(SSs[n])
								saveSS()
							inAdding = False
							if canNotify:
								await msg.edit(f"**✅ Adder Completato con Successo ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "back")])
						else:
							await e.respond("**❌ Puoi inserire un solo Gruppo ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "add")])
					else:
						await e.respond("**❌ Devi inserire un Link o una @ di un gruppo ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "add")])
				else:
					await e.respond("**⚠️ Formato non Valido ⚠️**", buttons=[Button.inline("🔄 Riprova 🔄", "add")])
				
			
		
	

@bot.on(events.CallbackQuery())
async def callbackQuery(e):
	global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, Grab, inAdding
	if e.sender_id == ADMIN:
		if e.data == b"back":
			Getter, Number, TempClient = None, None, None
			await e.edit("**Benvenuto nell'adderbot creato dalla fsociety per te\n\n per utilizzzare il bot usa i pulsanti qui sotto**", buttons=[[Button.inline("🙈 Sessioni", "voip"), Button.inline("Proxy 🌐", "proxy")], [Button.inline("💣 Ruba", "grab"), Button.inline("Adder ➕", "add")], [Button.url("👨🏼‍💻 Developer 👨🏼‍💻", "https://t.me/fsocietyUserBot")]])
		elif e.data == b"stop":
			await e.edit("**✅ Adder Interrotto Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "back")])
			python = sys.executable
			os.execl(python, python, *sys.argv)
		elif inAdding:
			await e.answer("⚠️ **Avviso** » Questa Sezione è Bloccata durante l'Adder!", alert=True)
		elif e.data == b"voip":
			Getter, Number, TempClient = None, None, None
			await e.edit(f"__🙈 Sessioni Attive »__ **{SSs.__len__()}**", buttons=[[Button.inline("➕ Aggiungi", "addvoip"), Button.inline("Gestisci ⚙️", "voips")], [Button.inline("🗂 Archivio 🗂", "arch")], [Button.inline("🔙 Indietro 🔙", "back")]])
		elif e.data == b"addvoip":
			Getter = 0
			await e.edit("**➕ Stai creando una Nuova Sessione.**\nInvia ora il Numero della Sessione da aggiungere.", buttons=[Button.inline("❌ Annulla ❌", "voip")])
		elif e.data == b"voips":
			if SSs.__len__() > 0:
				Getter = 3
				msg = "**🙈 Invia ora il numero della Sessione che vuoi gestire.**\n"
				for n in SSs:
					msg += f"\n`{n}`"
				await e.edit(msg, buttons=[Button.inline("❌ Annulla ❌", "voip")])
			else:
				await e.edit("**❌ Non hai ancora aggiunto Sessioni. ❌**", buttons=[[Button.inline("➕ Aggiungi ➕", "addvoip")], [Button.inline("🔙 Indietro 🔙", "voip")]])
		elif e.data == b"arch":
			if ArchSSs.__len__() > 0:
				Getter = 4
				msg = f"**🗂 Sessioni Archiviate** » **{ArchSSs.__len__()}**\n\n__➕ Invia ora il Numero della Sessione Archiviata che vuoi Gestire.__\n"
				for n in ArchSSs:
					msg += f"\n`{n}`"
				await e.edit(msg, buttons=[Button.inline("❌ Annulla ❌", "voip")])
			else:
				await e.edit("**❌ Non hai Archiviato nessuna Sessione ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
		elif e.data == b"proxy":
			await e.answer("⚠️ » Prossimamente...", alert=True)
		elif e.data == b"grab":
			if Grab == None:
				await e.edit("**❌ Gruppo non Impostato ❌\n\nℹ️ Puoi impostarlo usando il Pulsante qua sotto!**", buttons=[[Button.inline("✍🏻 Imposta ✍🏻", "setgrab")], [Button.inline("🔙 Indietro 🔙", "back")]])
			else:
				await e.edit(f"**👥 Gruppo attualmente Impostato** » **{Grab}**", buttons=[[Button.inline("✍🏻 Modifica ✍🏻", "setgrab")], [Button.inline("🔙 Indietro 🔙", "back")]])
		elif e.data == b"setgrab":
			Getter = 5
			await e.edit("__💣 Invia il Link o la @ del Gruppo__ **da cui vuoi Rubare gli Utenti!**", buttons=[Button.inline("❌ Annulla ❌", "back")])
		elif e.data == b"add":
			if SSs.__len__() > 0:
				if Grab != None:
					Getter = 6
					await e.edit("__➕ Invia il Link o la @ del Gruppo__ **in cui vuoi Aggiungere gli Utenti!**", buttons=[Button.inline("❌ Annulla ❌", "back")])
				else:
					await e.edit("**❌ Impostare il Gruppo da cui Rubare gli Utenti ❌**", buttons=[[Button.inline("💣 Ruba 💣", "grab")], [Button.inline("🔙 Indietro 🔙", "back")]])
			else:
				await e.edit("**❌ Non hai ancora aggiunto Sessioni. ❌**", buttons=[[Button.inline("➕ Aggiungi ➕", "addvoip")], [Button.inline("🔙 Indietro 🔙", "back")]])
		else:
			st = e.data.decode().split(";")
			if st[0] == "arch":
				if st[1] in SSs:
					if not st[1] in ArchSSs:
						ArchSSs[st[1]] = SSs[st[1]]
						saveArchSS()
					del(SSs[st[1]])
					saveSS()
					await e.edit("**✅ Sessione archiviata Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				else:
					await e.edit("**❌ Sessione non Trovata ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
			elif st[0] == "add":
				if st[1] in ArchSSs:
					SSs[st[1]] = ArchSSs[st[1]]
					saveSS()
					del(ArchSSs[st[1]])
					saveArchSS()
					await e.edit("**✅ Sessione Ri-Aggiunta Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				else:
					await e.edit("**❌ Sessione non Trovata ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
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
					del(SSs[st[1]])
					saveSS()
					await e.edit("**✅ Sessione rimossa Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				else:
					await e.edit("**❌ Sessione già Rimossa ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
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
					del(ArchSSs[st[1]])
					saveArchSS()
					await e.edit("**✅ Sessione rimossa Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				else:
					await e.edit("**❌ Sessione già Rimossa ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				
			
		
	

LOGS.warning("L'Utente sta Avviando la Source...\n\nSource of fsociety")

bot.start()

LOGS.warning("Adder Bot avviato Correttamente!\n\nSource of fsociety")

bot.run_until_disconnected()