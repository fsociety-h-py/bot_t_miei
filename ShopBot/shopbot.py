# @@@@@@@@  @@@@@@  @@@@@@   @@@@@@@ @@@ @@@@@@@@ @@@@@@@ @@@ @@@
# @@!      !@@     @@!  @@@ !@@      @@! @@!        @@!   @@! !@@
# @!!!:!    !@@!!  @!@  !@! !@!      !!@ @!!!:!     @!!    !@!@! 
# !!:          !:! !!:  !!! :!!      !!: !!:        !!:     !!:  
#  :       ::.: :   : :. :   :: :: : :   : :: :::    :      .:   

#--------------- LIBRERIE ---------------#

import os
import datetime
import random
import sys
import shutil

from datetime import datetime
from telethon.sync import TelegramClient
from telethon import TelegramClient,events,sync,Button
from telethon import functions,types

#----------------------------------------#



#--------------- NOME SESSION, API ID, API HASH, START CLIENT ---------------#

bot = input("Inserisci un nome da applicare al file .session, se esiste hai già un file inserisci il nome del file già esistente (ESCLUSA l'estensione finale del file): ")
api_id = 11433512
api_hash = "608c12a75871c85cec3da8facbfb11cf"
client = TelegramClient(bot,api_id,api_hash)
client.start()

#----------------------------------------------------------------------------#



########## VARIABILI, TI VERRANNO RICHIESTE OGNI VOLTA ALL'AVVIO DEL FILE ##########

admin_id = int(input("Inserisci l'ID Telegram del proprietario del BOT che potrà utilizzare TUTTE le opzioni amministrative: "))
bot_name = input("Inserisci il nome dello SHOP BOT: ")
nome_operatore = input("Inserisci il nome operatore, ovvero il nome che comparirà agli utenti nelle comunicazioni via chat-live: ")
obbligo_canale = input('Vuoi obbligare gli utenti a iscriversi a un tuo canale prima di utilizzare il BOT? (S/N) ')
if obbligo_canale == "S" or obbligo_canale == "s":
    obbligo = True
    canale_obbligo = input("Inserisci l'username del tuo canale Telegram (inclusa la @): ")
    
elif obbligo_canale == "N" or obbligo_canale == "n":
    obbligo = False

############################################


#----------------------------------------------------------------


########## VARIABILE DATA & ORA ##########

now = datetime.now()
dataora = now.strftime("%d/%m/%Y %H:%M:%S")

##########################################


#----------------------------------------------------------------


#MESSAGGI IN ENTRATA---------------------------------------------#

@client.on(events.NewMessage)
async def my_event_handler(e):
    ########## VARIABILI (NON MODIFICABILI) ##########
    
    client.parse_mode = 'html'
    sender = await e.get_sender()
    userpath = "utenti/" + str(sender.id) + "/"
    text = e.text.split(' ')
    
    file = open("admin/lista_admin", "r", encoding='utf-8')
    lista_admin = file.read()
    file.close()
    
    file = open("admin/lista_ban", "r", encoding='utf-8')
    lista_ban = file.read()
    file.close()
    
    ##################################################
    
    
    #----------------------------------------------------------------
    
    
    ########## SEZIONE ADMIN ##########
    
    if sender.id == admin_id or lista_admin.__contains__(str(sender.id)):
        file = open("admin/stato", "r", encoding='utf-8')
        admin_stato = file.read()
        file.close()
        
        
        if admin_stato.__contains__("nome_categoria"):
            file = open("admin/stato", "r", encoding='utf-8')
            categoria_selezionata_read = file.read().splitlines()
            file.close()
            
            categoria_selezionata = categoria_selezionata_read[0]
            
            os.rename("prodotti/" + categoria_selezionata, "prodotti/" + e.text)
            
            await e.respond("✅ OPERAZIONE COMPLETATA ✅",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_shop")]])
            
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
        
        
        
        
        elif admin_stato == "aggiungi_categoria":
            os.mkdir("prodotti/" + e.text)
            
            await e.respond("✅ Operazione eseguita correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_shop")]])
            
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
        
        
        
        
        elif admin_stato == "messaggio_globale":
            all_user = os.listdir("utenti/")
            all_user_count = len(all_user)
            i = -1
            
            await e.respond("🔄 <i>Attendi mentre invio il messaggio agli utenti...</i> 🔄")
            
            while i < all_user_count - 1:
                i = i + 1
                
                try:
                    await client.send_message(int(all_user[i]), e.text)
                
                except:
                    pass
                
            await e.respond("✅ Messaggio inviato correttamente a tutti gli utenti.",
                buttons=[[Button.inline("⬅️ INDIETRO", "Home_admin")]])
            
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
        
        
        
        
        elif admin_stato.__contains__("aggiungi_prodotto"):
            file = open("admin/stato", "r", encoding='utf-8')
            categoria_selezionata_read = file.read().splitlines()
            file.close()
            
            categoria_selezionata = categoria_selezionata_read[0]
            
            os.mkdir("prodotti/" + categoria_selezionata + "/" + e.text)
            path = "prodotti/" + categoria_selezionata + "/" + e.text + "/"
            
            file = open(path + "nome", "w", encoding='utf-8')
            file.write(e.text)
            file.close()
            
            file = open(path + "accounts", "w", encoding='utf-8')
            file.write("")
            file.close()
            
            file = open(path + "descrizione", "w", encoding='utf-8')
            file.write("NESSUNA DESCRIZIONE IMPOSTATA")
            file.close()
            
            file = open(path + "prezzo", "w", encoding='utf-8')
            file.write("0.00")
            file.close()
            
            file = open(path + "tipologia", "w", encoding='utf-8')
            file.write("account")
            file.close()
            
            await e.respond("✅ Operazione eseguita correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_shop")]])
            
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
        
        
        
        
        elif admin_stato == "aggiungi_file":
            nome_file = e.text
            await e.respond("✅ Ok il tuo file si chiamerà <b>" + nome_file + "</b>. Ora invia il file da uplodare nel database del BOT.",
                buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
            
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write(nome_file + "\naggiungi_file_upload")
            file.close()
        
        
        
        
        elif admin_stato.__contains__("aggiungi_file_upload"):
            file = open("admin/stato", "r")
            nome_file = file.read().splitlines()
            file.close()
            
            try:
                nome1 = nome_file[0].split('>')[1]
                nome2 = nome1.split('<')[0]
            except:
                nome2 = nome_file[0]
        
            if e.media:
                await e.download_media("files/" + nome2)
                
                await e.respond("✅ FILE UPLODATO CON SUCCESSO ✅",
                    buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            else:
                await e.respond("❌ INVIA UN FILE VALIDO ❌",
                    buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
        
        
        
        
        elif admin_stato == "rimuovi_file":
            nome_file = e.text
            
            try:
                nome1 = nome_file.split('>')[1]
                nome2 = nome1.split('<')[0]
            except:
                nome2 = nome_file
            
            try:
                os.remove("files/" + nome2)
            
                await e.respond("✅ FILE RIMOSSO CORRETTAMENTE ✅",
                        buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            except:
                await e.respond("❌ IL FILE SPECIFICATO NON ESISTE ❌",
                    buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
        
        
        
        
        elif admin_stato == "scarica_file":
            nome_file = e.text
            
            try:
                nome1 = nome_file.split('>')[1]
                nome2 = nome1.split('<')[0]
            except:
                nome2 = nome_file
            
            try:
                await client.send_file(admin_id, "files/" + nome2)
            
                await e.respond("✅ FILE INVIATO ✅",
                    buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            except:
                await e.respond("❌ Il file specifico non è presente nel database del BOT.",
                    buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
        
        
        
        
        elif admin_stato.__contains__("nome_prodotto"):
            file = open("admin/stato", "r", encoding='utf-8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "nome", "w", encoding='utf-8')
            file.truncate(0)
            file.write(e.text)
            file.close()
            
            file = open("admin/stato", "w", encoding='utf-8')
            file.write(e.text)
            file.close()
            
            os.rename(path, "prodotti/" + categoria_selezionata + "/" + e.text)
            
            file = open("admin/stato", "r", encoding='utf-8')
            stato_read = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf-8')
            file.truncate(0)
            file.write(categoria_selezionata + "\n" + stato_read.replace(prodotto_selezionato, e.text))
            file.close()
            
            
            await e.respond("✅ NOME MODIFICATO CORRETTAMENTE ✅",
                    buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
        
        
        
        
        elif admin_stato.__contains__("descrizione_prodotto"):
            file = open("admin/stato", "r", encoding='utf-8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "descrizione", "w", encoding='utf8')
            file.truncate(0)
            file.write(e.text)
            file.close()
            
            file = open("admin/stato", "r", encoding='utf-8')
            stato_read = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf-8')
            file.truncate(0)
            file.write(stato_read.replace(stato[2], "").strip('\n'))
            file.close()
            
            await e.respond("✅ DESCRIZIONE MODIFICATA CORRETTAMENTE ✅",
                buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
        
        
        
        
        elif admin_stato.__contains__("imposta_file"):
            file = open("admin/stato", "r", encoding='utf-8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            testo = e.text
            
            try:
                file_selezionato_try = testo.split('>')[1]
                file_selezionato = file_selezionato_try.split('<')[0]
            except:
                file_selezionato = testo
            
            try:
                file = open("files/" + file_selezionato, "r")
                file.close()
                
                file = open(path + "tipologia", "r", encoding='utf8')
                tipologia = file.read()
                file.close()
                
                file = open(path + "tipologia", "r", encoding='utf8')
                tipologia2 = file.read().splitlines()
                file.close()
                
                try:
                    check = tipologia2[1]
                    
                    file = open(path + "tipologia", "w", encoding='utf8')
                    file.truncate(0)
                    file.write(tipologia.replace(check, file_selezionato).strip("\n"))
                    file.close()
                
                except:
                    file = open(path + "tipologia", "w", encoding='utf8')
                    file.truncate(0)
                    file.write(tipologia + "\n" + file_selezionato)
                    file.close()
                
                await e.respond("✅ FILE IMPOSTATO CORRETTAMENTE ✅",
                    buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
                
                file = open("admin/stato", "r", encoding='utf-8')
                stato_read = file.read()
                file.close()
                
                file = open("admin/stato", "w", encoding='utf-8')
                file.truncate(0)
                file.write(stato_read.replace(stato[2], "").strip('\n'))
                file.close()
            
            except:
                await e.respond("❌ IL FILE SPECIFICATO NON ESISTE NEL DATABASE ❌",
                    buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
        
        
        
        
        elif admin_stato.__contains__("pannello_account"):
            file = open("admin/stato", "r", encoding='utf-8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "accounts", "r", encoding='utf-8')
            accounts = file.read()
            file.close()
            
            if accounts == "":
                file = open(path + "accounts", "w", encoding='utf-8')
                file.truncate(0)
                file.write(e.text)
                file.close()
            
            else:
                file = open(path + "accounts", "w", encoding='utf-8')
                file.truncate(0)
                file.write(accounts + "\n" + e.text)
                file.close()
            
            await e.respond("✅ ACCOUNT/S AGGIUNTO/I ALLA LISTA ✅",
                buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
            
            file = open("admin/stato", "r", encoding='utf-8')
            stato_read = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf-8')
            file.truncate(0)
            file.write(stato_read.replace(stato[2], "").strip('\n'))
            file.close()
        
        
        
        
        elif admin_stato.__contains__("rimuovi_account"):
            file = open("admin/stato", "r", encoding='utf-8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "accounts", "r", encoding='utf-8')
            accounts = file.read()
            file.close()
            
            file = open(path + "accounts", "w", encoding='utf-8')
            file.truncate(0)
            file.write(accounts.replace("\n" + e.text, "").strip("\n"))
            file.close()
            
            await e.respond("✅ ACCOUNT RIMOSSO DALLA LISTA ✅",
                buttons=[[Button.inline("⬅️ INDIETRO", "all_account_view")]])
            
            file = open("admin/stato", "r", encoding='utf-8')
            stato_read = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf-8')
            file.truncate(0)
            file.write(stato_read.replace(stato[2], "").strip('\n'))
            file.close()
        
        
        
        
        elif admin_stato.__contains__("prezzo_prodotto"):
            file = open("admin/stato", "r", encoding='utf-8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            try:
                if e.text.__contains__(","):
                    prezzo = float(e.text.replace(",", "."))
                
                else:
                    prezzo = float(e.text)
                
                file = open(path + "prezzo", "w")
                file.truncate(0)
                file.write(str(format(prezzo, ".2f")))
                file.close()
                
                await e.respond("✅ PREZZO AGGIORNATO CORRETTAMENTE ✅",
                    buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
                
                file = open("admin/stato", "r", encoding='utf-8')
                stato_read = file.read()
                file.close()
                
                file = open("admin/stato", "w", encoding='utf-8')
                file.truncate(0)
                file.write(stato_read.replace(stato[2], "").strip('\n'))
                file.close()
            
            except:
                await e.respond("❌ <b>ERRORE</b> ❌\n\nℹ️ Inserisci un prezzo valido, puoi inserire anche i centesimi.",
                    buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
        
        
        
        
        elif admin_stato == "get_info_user":
            try:
                id_user = int(e.text)
                path = "utenti/" + str(id_user) + "/"
                
                file = open(path + "saldo", "r", encoding='utf-8')
                saldo = file.read()
                file.close()
                
                file = open(path + "dataavvio", "r", encoding='utf-8')
                dataavvio = file.read()
                file.close()
                
                saldo_attuale = float(saldo)
                saldo_attuale_finale = str(format(saldo_attuale,".2f"))
                
                await e.respond("👤 <b>" + str(id_user) + "</b>\n\n💰 Saldo disponibile: " + saldo_attuale_finale.replace(".", ",") + " EUR\n🕖 Primo avvio del BOT: " + dataavvio,
                    buttons=[[Button.inline("🕖 CRONOLOGIA ORDINI 🕖", "get_cronologia_user" + " " + str(id_user))],
                        [Button.inline("⬅️ INDIETRO", "get_info_user")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            except:
                pass
        
        
        
        
        elif admin_stato == "add_saldo":
            try:
                id_user = int(text[0])
                
                if e.text.__contains__(","):
                    credito = float(text[1].replace(",", "."))
                
                else:
                    credito = float(text[1])
                
                path = "utenti/" + str(id_user) + "/"
                
                file = open(path + "saldo", "r", encoding='utf-8')
                saldo = file.read()
                file.close()
                
                saldo_attuale = float(saldo)
                
                calcolo = saldo_attuale + credito
                
                file = open(path + "saldo", "w", encoding='utf-8')
                file.truncate(0)
                file.write(str(format(calcolo, ".2f")))
                file.close()
                
                
                file = open(path + "cronologia", "r", encoding='utf-8')
                cronologia = file.read()
                file.close()
                
                credito_str = str(format(credito, ".2f"))
                
                file = open(path + "cronologia", "w", encoding='utf-8')
                file.truncate(0)
                file.write(cronologia + "\n\n\n🔄 RICARICA 🔄\n💳 Saldo: +" + credito_str.replace(".", ",") + " EUR\n🕑 Data & ora: " + dataora)
                file.close()
                
                await e.respond("✅ Saldo aggiunto correttamente (+" + credito_str.replace(".", ",") + " EUR) all'utente " + str(id_user),
                     buttons=[[Button.inline("⬅️ INDIETRO", "admin_utenti")]])
                
                await client.send_message(int(id_user), "🔄 RICARICA 🔄\nℹ️ Ti informiamo che il tuo saldo è stato ricaricato.\n\n💳 Saldo: +" + credito_str.replace(".", ",") + " EUR\n🕑 Data & ora: " + dataora,
                    buttons=[[Button.inline("🏠 Vai alla Home 🏠", "Homebuy")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            except:
                pass
        
        
        
        
        elif admin_stato == "rimuovi_saldo":
            try:
                id_user = int(text[0])
                
                if e.text.__contains__(","):
                    credito = float(text[1].replace(",", "."))
                
                else:
                    credito = float(text[1])
                
                path = "utenti/" + str(id_user) + "/"
                
                file = open(path + "saldo", "r", encoding='utf-8')
                saldo = file.read()
                file.close()
                
                saldo_attuale = float(saldo)
                
                calcolo = saldo_attuale - credito
                
                file = open(path + "saldo", "w", encoding='utf-8')
                file.truncate(0)
                file.write(str(format(calcolo, ".2f")))
                file.close()
                
                
                file = open(path + "cronologia", "r", encoding='utf-8')
                cronologia = file.read()
                file.close()
                
                credito_str = str(format(credito, ".2f"))
                
                file = open(path + "cronologia", "w", encoding='utf-8')
                file.truncate(0)
                file.write(cronologia + "\n\n\n❌ SALDO RIMOSSO ❌\n💳 Saldo: -" + credito_str.replace(".", ",") + " EUR\n🕑 Data & ora: " + dataora)
                file.close()
                
                await e.respond("✅ Saldo rimosso correttamente (-" + credito_str.replace(".", ",") + " EUR) all'utente " + str(id_user),
                     buttons=[[Button.inline("⬅️ INDIETRO", "admin_utenti")]])
                
                await client.send_message(int(id_user), "❌ SALDO RIMOSSO ❌\nℹ️ Ti informiamo che il tuo saldo è stato rimosso dall'amministratore del BOT.\n\n💳 Saldo: -" + credito_str.replace(".", ",") + " EUR\n🕑 Data & ora: " + dataora,
                    buttons=[[Button.inline("🏠 Vai alla Home 🏠", "Homebuy")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            except:
                pass
        
        
        
        
        elif admin_stato == "attiva_metodo_paypal":
            file = open("admin/pagamenti/paypal", "w", encoding='utf-8')
            file.truncate(0)
            file.write(e.text)
            file.close()
            
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
            
            await e.respond("✅ Metodo attivato e impostato correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "metodo_paypal")]])
        
        
        
        
        elif admin_stato == "attiva_metodo_bitcoin":
            file = open("admin/pagamenti/bitcoin", "w", encoding='utf-8')
            file.truncate(0)
            file.write(e.text)
            file.close()
            
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
            
            await e.respond("✅ Metodo attivato e impostato correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "metodo_bitcoin")]])
        
        
        
        
        elif admin_stato == "attiva_metodo_monero":
            file = open("admin/pagamenti/monero", "w", encoding='utf-8')
            file.truncate(0)
            file.write(e.text)
            file.close()
            
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
            
            await e.respond("✅ Metodo attivato e impostato correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "metodo_monero")]])
        
        
        
        
        elif admin_stato == "add_admin":
            try:
                id_utente = int(e.text)
                
                file = open("admin/lista_admin", "r", encoding='utf-8')
                admins = file.read()
                file.close()
                
                
                if admins == "":
                    file = open("admin/lista_admin", "w", encoding='utf-8')
                    file.truncate(0)
                    file.write(str(id_utente))
                    file.close()
                
                else:
                    file = open("admin/lista_admin", "w", encoding='utf-8')
                    file.truncate(0)
                    file.write(admins + "\n" + str(id_utente))
                    file.close()
                
                
                await e.respond("✅ Utente aggiunto correttamente admin.",
                    buttons=[[Button.inline("⬅️ INDIETRO", "lista_admin")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            except:
                pass
        
        
        
        
        elif admin_stato == "remove_admin":
            try:
                id_utente = int(e.text)
                utente = str(id_utente)
                
                file = open("admin/lista_admin", "r", encoding='utf-8')
                admins = file.read()
                file.close()
                
                
                file = open("admin/lista_admin", "w", encoding='utf-8')
                file.truncate(0)
                file.write(admins.replace(utente, ""))
                file.close()
                
                
                with open('admin/lista_admin') as reader, open('admin/lista_admin', 'r+', encoding='utf-8') as writer:
                  for line in reader:
                    if line.strip():
                      writer.write(line)
                  writer.truncate()
                
                
                await e.respond("✅ Utente rimosso correttamente dalla lista admin.",
                    buttons=[[Button.inline("⬅️ INDIETRO", "lista_admin")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            except:
                pass
        
        
        
        
        elif admin_stato == "modifica_tos":
            file = open("admin/tos", "w", encoding='utf-8')
            file.truncate(0)
            file.write(str(e.text))
            file.close()
            
            await e.respond("✅ TOS impostati correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_tos")]])
        
        
        
        
        elif admin_stato == "ban_user":
            try:
                file = open("admin/lista_ban", "r", encoding='utf-8')
                bannati = file.read()
                file.close()
                
                file = open("admin/lista_ban", "w", encoding='utf-8')
                file.truncate(0)
                file.write(bannati + "\n" + e.text)
                file.close()
                
                await e.respond("✅ Utente bannato correttamente.",
                    buttons=[[Button.inline("⬅️ INDIETRO", "admin_ban")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            except:
                pass
        
        
        
        
        elif admin_stato == "unban_user":
            try:
                file = open("admin/lista_ban", "r", encoding='utf-8')
                bannati = file.read()
                file.close()
                
                file = open("admin/lista_ban", "w", encoding='utf-8')
                file.truncate(0)
                file.write(bannati.replace(e.text, ""))
                file.close()
                
                with open('admin/lista_ban') as reader, open('admin/lista_ban', 'r+') as writer:
                  for line in reader:
                    if line.strip():
                      writer.write(line)
                  writer.truncate()
                
                await e.respond("✅ Utente sbannato correttamente.",
                    buttons=[[Button.inline("⬅️ INDIETRO", "admin_ban")]])
                
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
            
            except:
                pass
    
        
        
        
        elif e.text == "/start":
            await e.respond("👮 <b>PANNELLO ADMIN</b>👮\n\n👤 User: <b>" + sender.first_name + "</b>\n🆔 <b>" + str(sender.id) + "</b>.\n\n↪️ Naviga tra i menù tramite le opzioni sotto-stanti per gestire l'utenza e le opzioni amministrative.",
                buttons=[[Button.inline("👮 ADMIN 👮", "lista_admin"), Button.inline("👥 UTENTI 👥", "admin_utenti")],
                    [Button.inline("⛔ BAN ⛔", "admin_ban"), Button.inline("🛒 SHOP 🛒", "admin_shop")],
                    [Button.inline("📁 GESTIONE FILE 📁", "gestione_file"), Button.inline("💬 MESSAGGIO GLOBALE 💬", "messaggio_globale")],
                    [Button.inline("💳 METODI DI PAGAMENTO 💳", "metodi_pagamento"), Button.inline("🛡️ TOS 🛡️", "admin_tos")]])
        
        
        
        
        elif text[0] == "/mex":
            try:
                id_utente = text[1]
                
                messaggio1 = e.text.replace(text[0], "")
                messaggio2 = messaggio1.replace(text[1], "")
                
                messaggio = messaggio2.lstrip()
                
                await client.send_message(int(id_utente), nome_operatore + ": " + messaggio)
                
                await e.respond("✅ Messaggio inviato")
                
                file = open("admin/lista_admin", "r", encoding='utf8')
                admins = file.read().splitlines()
                file.close()
                
                admins_num = len(admins)
                i = -1
                
                if sender.id == admin_id:
                    pass
                
                else:
                    await client.send_message(int(admin_id), "👮 L'admin " + str(sender.id) + " ha inviato un messaggio a <a href='tg://user?id= " + id_utente + "'>l'utente</a> ID " + id_utente)
                
                while i < admins_num - 1:
                    i = i + 1
                    
                    if admins[i] == str(sender.id):
                        pass
                    
                    else:
                        await client.send_message(int(admins[i]), "👮 L'admin " + str(sender.id) + " ha inviato un messaggio a l'utente ID " + id_utente)
            
            except:
                pass
    
    ###################################
    
    
    #----------------------------------------------------------------#
    
    
    ########## SEZIONE UTENTE ##########
    
    else:
        
        if lista_ban.__contains__(str(sender.id)):
            await e.respond("⛔ <b>SEI STATO BANNATO</b> ⛔\n\nℹ️ Spiacenti, ma uno degli amministratori del BOT ha deciso di bannarti. Non potrai utilizzare il BOT e le sue funzioni ammenochè non verrai riammesso dallo staff.")
        
        else:
            try:
                file = open(userpath + "verifica")
                file.close()
            
            except:
                os.mkdir(userpath)
                
                file = open(userpath + "verifica", "w")
                file.write("")
                file.close()
                
                file = open(userpath + "saldo", "w")
                file.write("0.00")
                file.close()
                
                file = open(userpath + "dataavvio", "w")
                file.write(dataora)
                file.close()
                
                file = open(userpath + "cronologia", "w")
                file.write("")
                file.close()
                
                file = open(userpath + "stato", "w")
                file.write("")
                file.close()
            
            
            
            
            ###############
            if obbligo == True:
                try:
                    result = await client(functions.channels.GetParticipantRequest(
                    channel=canale_obbligo,
                    participant=int(sender.id)
                    ))
                
                except:
                    try:
                        canale_replace = canale_obbligo.replace("@", "")
                    except:
                        canale_replace = canale_obbligo
                    
                    await e.respond("⚠️ <b>ATTENZIONE</b> ⚠️\n\nℹ️ Per poter utilizzare il BOT devi essere iscritto a " + canale_obbligo + ". Iscriviti e successivamente premi sul pulsante 'AGGIORNA' sotto-stante.",
                        buttons=[[Button.url("✅ISCRIVITI✅", "https://t.me/" + canale_replace.lstrip())],
                            [Button.inline("🔄 AGGIORNA 🔄", "check_canale")]])
                    return
            
            
            file = open(userpath + "stato", "r", encoding='utf8')
            utente_stato = file.read()
            file.close()
            
            
            
            if utente_stato == "chatlive":
                if e.text == "/annulla":
                    file = open(userpath + "stato", "w")
                    file.truncate(0)
                    file.close()
                    
                    await e.respond("❌ CHAT-LIVE TERMINATA ❌",
                        buttons=[[Button.inline("⬅️ INDIETRO", "Home")]])
                
                else:
                    await client.send_message(int(admin_id), "👤 <a href='tg://user?id=" + str(sender.id) + "'>" + sender.first_name + "</a> ID <pre>" + str(sender.id) + "</pre> TI HA INVIATO QUESTO MESSAGGIO ⤵️\n\n<i>Digita /mex + id utente + il tuo messaggio per rispondere alla sua richiesta.</i>")
                    
                    result = await client(functions.messages.ForwardMessagesRequest(
                    from_peer='me',
                    id=[e.id],
                    to_peer=int(admin_id),
                    with_my_score=True ))
                    
                    file = open("admin/lista_admin", "r", encoding='utf-8')
                    lista_utenti = file.read().splitlines()
                    lista_utenti_num = len(lista_utenti)
                    file.close()
                    
                    i = -1
                    
                    while i < lista_utenti_num - 1:
                        i = i + 1
                        
                        await client.send_message(int(lista_utenti[i]), "👤 <a href='tg://user?id=" + str(sender.id) + "'>" + sender.first_name + "</a> ID <pre>" + str(sender.id) + "</pre> TI HA INVIATO QUESTO MESSAGGIO ⤵️\n\n<i>Digita /mex + id utente + il tuo messaggio per rispondere alla sua richiesta.</i>")
                        
                        result = await client(functions.messages.ForwardMessagesRequest(
                        from_peer='me',
                        id=[e.id],
                        to_peer=int(lista_utenti[i]),
                        with_my_score=True ))
                
                
                
                
            elif e.text == "/start":
                file = open(userpath + "dataavvio", "r")
                data_ora_avvio = file.read()
                file.close()

                file = open(userpath + "saldo", "r")
                saldo_read = file.read()
                file.close()
                
                saldo = float(saldo_read)
                
                await e.respond("<b> 👋🏻 Ciao " + sender.first_name + ".\n\n🤖 Questo è lo shop di @fsocietyUserBot\n\n💳 Saldo attuale: " + str(format(saldo, ".2f")) + "€</b>",
                    buttons=[[Button.inline("💰 Saldo", "wallet"), Button.inline("Shop 🛍", "shop")],
                    [Button.inline("💎 Tos", "tos"), Button.inline("Supporto ☎", "chatlive")]])


    ####################################
    
    
    #----------------------------------------------------------------
    
    
#CALLBACK BUTTON ---------------------------------------------#

@client.on(events.CallbackQuery())
async def CallbackQuery(e):
    ########## VARIABILI (NON MODIFICABILI) ##########
    
    client.parse_mode = 'html'
    sender = await e.get_sender()
    userpath = "utenti/" + str(sender.id) + "/"
    user_callback = int(e.original_update.user_id)
    data_str = e.data.decode('utf-8')
    data = data_str.split(' ')
    
    file = open("admin/lista_admin", "r", encoding='utf-8')
    lista_admin = file.read()
    file.close()
    
    file = open("admin/lista_ban", "r", encoding='utf-8')
    lista_ban = file.read()
    file.close()
    
    ##################################################
    
    
    #----------------------------------------------------------------
    
    
    ########## SEZIONE ADMIN ##########
    
    if user_callback == admin_id or lista_admin.__contains__(str(user_callback)):
        if e.data == b"Home_admin":
            await e.edit("👮 <b>PANNELLO ADMIN</b>👮\n\n👤 User: <b>" + sender.first_name + "</b>\n🆔 <b>" + str(sender.id) + "</b>.\n\n↪️ Naviga tra imenù tramite le opzioni sotto-stanti per gestire l'utenza e le opzioni amministrative.",
                buttons=[[Button.inline("👮 ADMIN 👮", "lista_admin"), Button.inline("👥 UTENTI 👥", "admin_utenti")],
                    [Button.inline("⛔ BAN ⛔", "admin_ban"), Button.inline("🛒 SHOP 🛒", "admin_shop")],
                    [Button.inline("📁 GESTIONE FILE 📁", "gestione_file"), Button.inline("💬 MESSAGGIO GLOBALE 💬", "messaggio_globale")],
                    [Button.inline("💳 METODI DI PAGAMENTO 💳", "metodi_pagamento"), Button.inline("🛡️ TOS 🛡️", "admin_tos")]])
        
        
        
        
        elif e.data == b"admin_ban":
            file = open("admin/lista_ban", "r", encoding='utf-8')
            bannati = file.read()
            file.close()
            
            if bannati == "":
                mex = "❌ NESSUN UTENTE BANNATO ❌"
            
            else:
                mex = bannati
            
            await e.edit("⛔ <b>BAN</b> ⛔\n\nℹ️ Di seguito sono riportati tutti gli ID degli utenti bannati:\n\n\n" + mex,
                buttons=[[Button.inline("⛔ BANNA UN UTENTE ⛔", "ban_user")],
                    [Button.inline("🔓 SBANNA UN UTENTE 🔓", "unban_user")],
                    [Button.inline("⬅️ INDIETRO", "Home_admin")]])
        
        
        
        
        elif e.data == b"ban_user":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("ban_user")
            file.close()
            
            await e.edit("⛔ <b>BANNA UN UTENTE</b> ⛔\n\nℹ️ Invia qui di seguito l'ID dell'utente da bannare da " + bot_name + ".",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_ban")]])
        
        
        
        
        elif e.data == b"unban_user":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("unban_user")
            file.close()
            
            await e.edit("🔓 <b>SBANNA UN UTENTE</b> 🔓\n\nℹ️ Invia qui di seguito l'ID dell'utente da sbannare da " + bot_name + ".",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_ban")]])
        
        
        
        
        elif e.data == b"admin_tos":
            file = open("admin/tos", "r", encoding='utf-8')
            tos = file.read()
            file.close()
            
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
            
            if tos == "":
                await e.edit("❌ TOS NON IMPOSTATO ❌",
                    buttons=[[Button.inline("✏️ MODIFICA ✏️", "modifica_tos")],
                        [Button.inline("⬅️ INDIETRO", "Home_admin")]])
            
            else:
                await e.edit(tos,
                    buttons=[[Button.inline("✏️ MODIFICA ✏️", "modifica_tos")],
                        [Button.inline("⬅️ INDIETRO", "Home_admin")]])
        
        
        
        
        elif e.data == b"modifica_tos":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("modifica_tos")
            file.close()
            
            await e.edit("ℹ️ Inoltra o scrivi, quindi invia qui di seguito il messaggio dei tuoi TOS (Termini di servizio). Puoi usare anche l'HTML per la formattazione del testo.",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_tos")]])
        
        
        
        
        elif e.data == b"lista_admin":
            if user_callback == admin_id:
                file = open("admin/stato", "w")
                file.truncate(0)
                file.close()
                
                file = open("admin/lista_admin", "r", encoding='utf8')
                admins = file.read()
                file.close()
                
                file = open("admin/lista_admin", "r", encoding='utf-8')
                admins = file.read()
                file.close()
                
                if admins == "":
                    await e.edit("👮 <b>LISTA ADMIN</b>👮\n\nℹ️ Di seguito sono riportati tutti gli admin da te approvati. Questi utenti hanno accesso alle opzioni amministrative.\n\n\n❌ NESSUN ADMIN AGGIUNTO ❌",
                        buttons=[[Button.inline("➕ AGGIUNGI ADMIN ➕", "add_admin"), Button.inline("➖ RIMUOVI ADMIN ➖", "remove_admin")],
                            [Button.inline("⬅️ INDIETRO", "Home_admin")]])
                
                else:
                    await e.edit("👮 <b>LISTA ADMIN</b>👮\n\nℹ️ Di seguito sono riportati tutti gli admin da te approvati. Questi utenti hanno accesso alle opzioni amministrative.\n\n\n" + admins,
                        buttons=[[Button.inline("➕ AGGIUNGI ADMIN ➕", "add_admin"), Button.inline("➖ RIMUOVI ADMIN ➖", "remove_admin")],
                            [Button.inline("⬅️ INDIETRO", "Home_admin")]])
            
            else:
                await e.answer("❌ ERRORE ❌\n\nℹ️ Solo il propietario del BOT può accedere a questa sezione.", alert=True)
        
        
        
        
        elif e.data == b"add_admin":
            if user_callback == admin_id:
                file = open("admin/stato", "w")
                file.truncate(0)
                file.write("add_admin")
                file.close()
                
                await e.edit("👮 <b>AGGIUNGI ADMIN</b>👮\n\nℹ️ Invia qui di seguito l'ID utente Telegram da aggiungere come admin di " + bot_name + ".",
                    buttons=[[Button.inline("⬅️ INDIETRO", "lista_admin")]])
            
            else:
                await e.answer("❌ ERRORE ❌\n\nℹ️ Solo il propietario del BOT può accedere a questa sezione.", alert=True)
        
        
        
        
        elif e.data == b"remove_admin":
            if user_callback == admin_id:
                file = open("admin/stato", "w")
                file.truncate(0)
                file.write("remove_admin")
                file.close()
                
                await e.edit("👮 <b>RIMUOVI ADMIN</b>👮\n\nℹ️ Invia qui di seguito l'ID utente Telegram da rimuovere dalla lista admin di " + bot_name + ".",
                    buttons=[[Button.inline("⬅️ INDIETRO", "lista_admin")]])
            
            else:
                await e.answer("❌ ERRORE ❌\n\nℹ️ Solo il propietario del BOT può accedere a questa sezione.", alert=True)
        
        
        
        
        elif e.data == b"metodi_pagamento":
            await e.edit("💳 <b>METODI DI PAGAMENTO</b> 💳\n\nℹ️ Premi sui pulsanti che riportano i metodi di pagamento, per attivarli o disattivarli e modificarli. Questi metodi sono utilizzati dagli utenti per ricaricare il saldo del BOT.",
                buttons=[[Button.inline("✅ PAYPAL ✅", "metodo_paypal")],
                    [Button.inline("🪙 BITCOIN (BTC)", "metodo_bitcoin"), Button.inline("🪙 MONERO (XMR)", "metodo_monero")],
                    [Button.inline("⬅️ INDIETRO", "Home_admin")]])
        
        
        
        
        elif e.data == b"metodo_paypal":
            file = open("admin/pagamenti/paypal", "r", encoding='utf-8')
            paypal_status = file.read()
            file.close()
            
            pulsanti = []
            
            if paypal_status == "Disabled":
                stato = "disabilitato e NON può essere utilizzato dagli utenti come metodo di ricarica del proprio saldo su " + bot_name + "."
                pulsanti.append([Button.inline("PAYPAL ❌", "attiva_metodo_paypal")])
            
            else:
                stato = "abilitato e può essere utilizzato dagli utenti come metodo di ricarica del proprio saldo su " + bot_name + "."
                pulsanti.append([Button.inline("PAYPAL ✅", "disattiva_metodo_paypal")])
            
            
            pulsanti.append([Button.inline("⬅️ INDIETRO", "metodi_pagamento")])
            
            await e.edit("💳 <b>METODO PAYPAL</b> 💳\n\nℹ️ Attualmente il metodo PayPal risulta <b>" + stato + "</b>",
                buttons=pulsanti)
        
        
        
        
        elif e.data == b"attiva_metodo_paypal":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("attiva_metodo_paypal")
            file.close()
            
            await e.edit("💳 <b>METODO PAYPAL</b> 💳\n\nℹ️ Invia di seguito una descrizione o un tutorial per l'utente di come effettuare il pagamento compreso il link, email o altro per farti pagare con questo metodo di pagamento.",
                buttons=[[Button.inline("⬅️ INDIETRO", "metodo_paypal")]])
        
        
        
        
        elif e.data == b"disattiva_metodo_paypal":
            file = open("admin/pagamenti/paypal", "w", encoding='utf-8')
            file.truncate(0)
            file.write("Disabled")
            file.close()
            
            await e.edit("✅ Metodo disabilitato correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "metodo_paypal")]])
        
        
        
        
        elif e.data == b"metodo_bitcoin":
            file = open("admin/pagamenti/bitcoin", "r", encoding='utf-8')
            bitcoin_status = file.read()
            file.close()
            
            pulsanti = []
            
            if bitcoin_status == "Disabled":
                stato = "disabilitato e NON può essere utilizzato dagli utenti come metodo di ricarica del proprio saldo su " + bot_name + "."
                pulsanti.append([Button.inline("BITCOIN ❌", "attiva_metodo_bitcoin")])
            
            else:
                stato = "abilitato e può essere utilizzato dagli utenti come metodo di ricarica del proprio saldo su " + bot_name + "."
                pulsanti.append([Button.inline("BITCOIN ✅", "disattiva_metodo_bitcoin")])
            
            
            pulsanti.append([Button.inline("⬅️ INDIETRO", "metodi_pagamento")])
            
            await e.edit("💳 <b>METODO BITCOIN (BTC)</b> 💳\n\nℹ️ Attualmente il metodo Bitcoin risulta <b>" + stato + "</b>",
                buttons=pulsanti)
        
        
        
        
        elif e.data == b"attiva_metodo_bitcoin":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("attiva_metodo_bitcoin")
            file.close()
            
            await e.edit("💳 <b>METODO BITCOIN (BTC)</b> 💳\n\nℹ️ Invia di seguito una descrizione o un tutorial per l'utente di come effettuare il pagamento compreso il wallet o altro per farti pagare con questo metodo di pagamento.",
                buttons=[[Button.inline("⬅️ INDIETRO", "metodo_bitcoin")]])
        
        
        
        
        elif e.data == b"disattiva_metodo_bitcoin":
            file = open("admin/pagamenti/bitcoin", "w", encoding='utf-8')
            file.truncate(0)
            file.write("Disabled")
            file.close()
            
            await e.edit("✅ Metodo disabilitato correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "metodo_bitcoin")]])
        
        
        
        
        elif e.data == b"metodo_monero":
            file = open("admin/pagamenti/monero", "r", encoding='utf-8')
            monero_status = file.read()
            file.close()
            
            pulsanti = []
            
            if monero_status == "Disabled":
                stato = "disabilitato e NON può essere utilizzato dagli utenti come metodo di ricarica del proprio saldo su " + bot_name + "."
                pulsanti.append([Button.inline("MONERO ❌", "attiva_metodo_monero")])
            
            else:
                stato = "abilitato e può essere utilizzato dagli utenti come metodo di ricarica del proprio saldo su " + bot_name + "."
                pulsanti.append([Button.inline("MONERO ✅", "disattiva_metodo_monero")])
            
            
            pulsanti.append([Button.inline("⬅️ INDIETRO", "metodi_pagamento")])
            
            await e.edit("💳 <b>METODO MONERO (XMR)</b> 💳\n\nℹ️ Attualmente il metodo Monero risulta <b>" + stato + "</b>",
                buttons=pulsanti)
        
        
        
        
        elif e.data == b"attiva_metodo_monero":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("attiva_metodo_monero")
            file.close()
            
            await e.edit("💳 <b>METODO MONERO (XMR)</b> 💳\n\nℹ️ Invia di seguito una descrizione o un tutorial per l'utente di come effettuare il pagamento compreso il wallet o altro per farti pagare con questo metodo di pagamento.",
                buttons=[[Button.inline("⬅️ INDIETRO", "metodo_bitcoin")]])
        
        
        
        
        elif e.data == b"disattiva_metodo_monero":
            file = open("admin/pagamenti/monero", "w", encoding='utf-8')
            file.truncate(0)
            file.write("Disabled")
            file.close()
            
            await e.edit("✅ Metodo disabilitato correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "metodo_monero")]])
        
        
        
        
        elif data[0] == "get_cronologia_user":
            id_user = data[1]
            path = "utenti/" + id_user + "/"
            
            file = open(path + "cronologia", "r", encoding='utf8')
            cronologia = file.read()
            file.close()
            
            if cronologia == "":
                await e.answer("❌ ERRORE ❌\n\nℹ️ L'utente " + id_user + " non ha effettuato nessun ordine.", alert=True)
            
            else:
                await e.respond(cronologia,
                    buttons=[[Button.inline("❌ CHIUDI ❌", "get_cronologia_user_close")]])
        
        
        
        
        elif e.data == b"get_cronologia_user_close":
            await e.delete()
        
        
        
        
        elif e.data == b"admin_utenti":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
            
            utenti = os.listdir("utenti/")
            utenti_num = len(utenti)
            i = -1
            mex = ""
            
            while i < utenti_num - 1:
                i = i + 1
                mex = mex + "\n↪️ " + utenti[i]
            
            await e.edit("👥 <b>LISTA UTENTI</b> 👥\nℹ️ Di seguito sono presenti tutti gli ID degli utenti che hanno avviato il BOT (TOT: " + str(utenti_num) + ").\n\n" + mex,
                buttons=[[Button.inline("➕ AGGIUNGI SALDO ➕", "add_saldo"), Button.inline("➖ RIMUOVI SALDO ➖", "rimuovi_saldo")],
                    [Button.inline("ℹ️ OTTIENI INFO USER ℹ️", "get_info_user")],
                    [Button.inline("⬅️ INDIETRO", "Home_admin")]])
        
        
        
        
        elif e.data == b"add_saldo":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("add_saldo")
            file.close()
            
            await e.edit("➕ <b>AGGIUNGI SALDO</b> ➕\nℹ️ Invia di seguito l'ID utente Telegram + il saldo da aggiungere.\n\n🗨 <i>Ad es. 1214002398 5,00</i>",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_utenti")]])
        
        
        
        
        elif e.data == b"rimuovi_saldo":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("rimuovi_saldo")
            file.close()
            
            await e.edit("➖ <b>RIMUOVI SALDO</b> ➖\nℹ️ Invia di seguito l'ID utente Telegram + il saldo da rimuovere.\n\n🗨 <i>Ad es. 1214002398 5,00</i>",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_utenti")]])
        
        
        
        
        elif e.data == b"get_info_user":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("get_info_user")
            file.close()
            
            await e.edit("👥 <b>OTTIENI INFO</b> 👥\nℹ️ Invia di seguito l'ID utente Telegram dalla quale ricavare tutte le informazioni sulla sua attività nel BOT.",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_utenti")]])
        
        
        
        
        elif e.data == b"messaggio_globale":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("messaggio_globale")
            file.close()
            
            await e.edit("💬 <b>MESSAGGIO GLOBALE</b> 💬\n\nℹ️ Invia qui di seguito il messaggio che verrà recapitato a tutti gli utenti che hanno avviato il BOT.",
                buttons=[[Button.inline("⬅️ INDIETRO", "Home_admin")]])
        
        
        
        
        elif e.data == b"admin_shop":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.close()
        
            categorie = os.listdir("prodotti/")
            categorie_num = len(categorie)
            i = -1
            pulsanti = [[Button.inline("➕ AGGIUNGI CATEGORIA ➕", "aggiungi_categoria")]]
            
            while i < categorie_num - 1:
                i = i + 1
                pulsanti.append([Button.inline(categorie[i], "categoria_selezionata" + categorie[i])])
            
            pulsanti.append([Button.inline("⬅️ INDIETRO", "Home_admin")])
            
            await e.edit("🛍 <b>CATEGORIE</b> 🛍\n\nℹ️ Seleziona o aggiungi una nuova categoria.",
                buttons=pulsanti)
        
        
        
        
        elif e.data.__contains__(b"categoria_selezionata"):
            data_callback = e.data.decode('utf-8')
            categoria_selezionata = data_callback.replace("categoria_selezionata", "")
            path = "prodotti/" + categoria_selezionata + "/"
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(categoria_selezionata)
            file.close()
            
            prodotti = os.listdir(path)
            prodotti_num = len(prodotti)
            i = -1
            pulsanti = [[Button.inline("➕ PRODOTTO ➕", "aggiungi_prodotto"), Button.inline("✏️ NOME CATEG. ✏️", "nome_categoria"), Button.inline("🗑 ELIMINA 🗑", "elimina_categoria")]]
            
            while i < prodotti_num - 1:
                i = i + 1
                pulsanti.append([Button.inline(prodotti[i], "prodotto_selezionato" + prodotti[i])])
            
            pulsanti.append([Button.inline("⬅️ INDIETRO", "admin_shop")])
            
            await e.edit("🛍 CATEGORIA SELEZIONATA: <b>" + categoria_selezionata + "</b>",
                buttons=pulsanti)
        
        
        
        
        elif e.data == b"nome_categoria":
            file = open("admin/stato", "r", encoding='utf8')
            categoria_selezionata = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(categoria_selezionata + "\nnome_categoria")
            file.close()
            
            await e.edit("✏️ MODIFICA NOME DELLA CATEGORIA " + categoria_selezionata + "\n\nℹ️ Invia qui di seguito il nuovo nome da applicare alla categoria selezionata.",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_shop")]])
        
        
        
        
        elif e.data == b"elimina_categoria":
            file = open("admin/stato", "r", encoding='utf8')
            categoria_selezionata = file.read()
            file.close()
            
            await e.edit("⚠️ STAI PER ELIMINARE LA CATEGORIA " + categoria_selezionata + "\n\nℹ️ Sei sicuro di voler eseguire questa azione? Ricordati che è irreversibile e perderai tutti i prodotti nella categoria.",
                buttons=[[Button.inline("✅ CONFERMA ✅", "elimina_categoria_yes"), Button.inline("❌ ANNULLA ❌", "admin_shop")]])
        
        
        
        
        elif e.data == b"elimina_categoria_yes":
            file = open("admin/stato", "r", encoding='utf8')
            categoria_selezionata = file.read()
            file.close()
            
            shutil.rmtree("prodotti/" + categoria_selezionata + "/")
            
            await e.edit("✅ Operazione eseguita correttamente.",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_shop")]])
        
        
        
        
        elif e.data == b"aggiungi_categoria":
            file = open("admin/stato", "w")
            file.truncate(0)
            file.write("aggiungi_categoria")
            file.close()
            
            await e.edit("✏️ Invia qui di seguito il nome della nuova categoria da inserire",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_shop")]])
        
        
        
        
        elif e.data == b"aggiungi_prodotto":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read()
            file.close()
            
            file = open("admin/stato", "r", encoding='utf8')
            categoria_selezionata = file.read().splitlines()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(stato + "\naggiungi_prodotto")
            file.close()
            
            await e.edit("✏️ Invia qui di seguito il nome del nuovo prodotto da inserire nella categoria <b>" + categoria_selezionata[0] + "</b>",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_shop")]])
        
        
        
        
        elif e.data.__contains__(b"prodotto_selezionato"):
            file = open("admin/stato", "r", encoding='utf8')
            categoria_selezionata = file.read()
            file.close()
            
            data_callback = e.data.decode('utf-8')
            prodotto_selezionato = data_callback.replace("prodotto_selezionato", "")
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(categoria_selezionata + "\n" + prodotto_selezionato)
            file.close()
            
            file = open(path + "nome", "r", encoding='utf8')
            nome = file.read()
            file.close()
            
            file = open(path + "descrizione", "r", encoding='utf8')
            descrizione = file.read()
            file.close()
            
            file = open(path + "prezzo", "r", encoding='utf8')
            prezzo = file.read()
            file.close()
            
            file = open(path + "tipologia", "r", encoding='utf8')
            tipologia = file.read().splitlines()
            file.close()
            
            if tipologia[0] == "file":
                button_type = [Button.inline("📁 IMPOSTA FILE 📁", "imposta_file")]
            
            elif tipologia[0] == "account":
                button_type = [Button.inline("👤 IMPOSTA ACCOUNTS 👤", "pannello_account")]
            
            await e.edit("🛒 Nome prodotto: <b>" + prodotto_selezionato + "</b>\n🏷 Tipologia: " + tipologia[0] + "\n💳 Prezzo: <b>" + prezzo.replace(".", ",") + " EUR</b>\n\n🔻 Descrizione: <b>" + descrizione + "</b>",
                buttons=[[Button.inline("✏️ NOME PRODOTTO ✏️", "nome_prodotto"), Button.inline("📜 DESC. PRODOTTO 📜", "descrizione_prodotto"), Button.inline("🗑 ELIMINA 🗑", "elimina_prodotto")],
                    [Button.inline("ℹ️ TIPOLOGIA ℹ️", "tipologia_prodotto"), Button.inline("💳 MODIFICA PREZZO 💳", "prezzo_prodotto")],
                    button_type,
                    [Button.inline("⬅️ INDIETRO", "admin_shop")]])
        
        
        
        
        elif e.data.__contains__(b"return_prodotto_scelto"):
            file = open("admin/stato", "r", encoding='utf8')
            reset = file.read()
            file.close()
            
            
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            
            try:
                check = stato[2]
                
                file = open("admin/stato", "w", encoding='utf8')
                file.truncate(0)
                file.write(reset.replace(stato[2], "").strip('\n'))
                file.close()
            
            except:
                pass
            
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "nome", "r", encoding='utf8')
            nome = file.read()
            file.close()
            
            file = open(path + "descrizione", "r", encoding='utf8')
            descrizione = file.read()
            file.close()
            
            file = open(path + "prezzo", "r", encoding='utf8')
            prezzo = file.read()
            file.close()
            
            file = open(path + "tipologia", "r", encoding='utf8')
            tipologia = file.read().splitlines()
            file.close()
            
            if tipologia[0] == "file":
                button_type = [Button.inline("📁 IMPOSTA FILE 📁", "imposta_file")]
            
            elif tipologia[0] == "account":
                button_type = [Button.inline("👤 IMPOSTA ACCOUNTS 👤", "pannello_account")]
            
            await e.edit("🛒 Nome prodotto: <b>" + prodotto_selezionato + "</b>\n🏷 Tipologia: " + tipologia[0] + "\n💳 Prezzo: <b>" + prezzo.replace(".", ",") + " EUR</b>\n\n🔻 Descrizione: <b>" + descrizione + "</b>",
                buttons=[[Button.inline("✏️ NOME PRODOTTO ✏️", "nome_prodotto"), Button.inline("📜 DESC. PRODOTTO 📜", "descrizione_prodotto"), Button.inline("🗑 ELIMINA 🗑", "elimina_prodotto")],
                    [Button.inline("ℹ️ TIPOLOGIA ℹ️", "tipologia_prodotto"), Button.inline("💳 MODIFICA PREZZO 💳", "prezzo_prodotto")],
                    button_type,
                    [Button.inline("⬅️ INDIETRO", "admin_shop")]])
        
        
        
        
        elif e.data == b"gestione_file":
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.close()
            
            all_file = os.listdir("files/")
            all_file_num = len(all_file)
            i = -1
            data = ""
            
            while i < all_file_num - 1:
                i = i + 1
                data = data + "\n- " + all_file[i]
            
            await e.edit("📁 DI SEGUITO SONO PRESENTI TUTTI I FILE NEL DATABASE:\n\nℹ️ Questi file vengono consegnati automaticamente all'acquisto del prodotto. Per impostare un file specifico a seconda del prodotto, recati nella pagina del prodotto che desideri.\n\n" + data,
                buttons=[[Button.inline("➕ AGGIUNGI FILE ➕", "aggiungi_file"), Button.inline("⬇️ SCARICA FILE ⬇️", "scarica_file"), Button.inline("➖ RIMUOVI FILE ➖", "rimuovi_file")],
                    [Button.inline("⬅️ INDIETRO", "Home_admin")]])
        
        
        
        
        elif e.data == b"scarica_file":
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write("scarica_file")
            file.close()
            
            await e.edit("ℹ️ Invia qui di seguito il nome del file da scaricare (compresa l'estensione).",
                buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
        
        
        
        
        elif e.data == b"aggiungi_file":
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write("aggiungi_file")
            file.close()
            
            await e.edit("ℹ️ Invia qui di seguito nome da dare al file che successivamente andrai ad uplodare nel database del BOT (compresa l'estensione finale). Nota che se inserisci un nome già esistente, il vecchio file verrà sostituito con questo nuovo.",
                buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
        
        
        
        
        elif e.data == b"rimuovi_file":
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write("rimuovi_file")
            file.close()
            
            await e.edit("ℹ️ Invia qui di seguito nome del file da rimuovere (compresa l'estensione finale).",
                buttons=[[Button.inline("⬅️ INDIETRO", "gestione_file")]])
        
        
        
        
        elif e.data == b"nome_prodotto":
            file = open("admin/stato", "r", encoding='utf-8')
            stato = file.read().splitlines()
            file.close()
            
            file = open("admin/stato", "r", encoding='utf-8')
            stato2 = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(stato2 + "\nnome_prodotto")
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            await e.edit("ℹ️ Invia qui di seguito il nuovo nome da applicare al prodotto <b>" + prodotto_selezionato + "</b>.",
                buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
        
        
        
        
        elif e.data == b"descrizione_prodotto":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            file = open("admin/stato", "r", encoding='utf8')
            stato2 = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(stato2 + "\ndescrizione_prodotto")
            file.close()
            
            await e.edit("ℹ️ Invia qui di seguito la nuova descrizione da applicare al prodotto <b>" + prodotto_selezionato + "</b>.",
                buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
        
        
        
        
        elif e.data == b"elimina_prodotto":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            await e.edit("⚠️ ELIMINA " + prodotto_selezionato + " ⚠️\n\nℹ️ Sei sicuro di voler eliminare il prodotto <b>" + prodotto_selezionato + "</b>? Nota che tutti le modifiche e progressi salvati verranno eliminati permanentemente. Questa azione è irreversibile.",
                buttons=[[Button.inline("✅ CONFERMA ✅", "elimina_prodotto_yes"), Button.inline("❌ ANNULLA ❌", "return_prodotto_scelto")]])
        
        
        
        
        elif e.data == b"elimina_prodotto_yes":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            shutil.rmtree(path)
            
            await e.edit("✅ OPERAZIONE ESEGUITA CORRETTAMENTE ✅",
                buttons=[[Button.inline("⬅️ INDIETRO", "admin_shop")]])
        
        
        
        
        elif e.data == b"tipologia_prodotto":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "tipologia", "r", encoding='utf8')
            tipologia = file.read().splitlines()
            file.close()
            
            if tipologia[0] == "account":
                pulsanti = [[Button.inline("FILE", "change_file"), Button.inline("ACCOUNT 🔘", "change_account")]]
            
            elif tipologia[0] == "file":
                pulsanti = [[Button.inline("FILE 🔘", "change_file"), Button.inline("ACCOUNT", "change_account")]]
            
            pulsanti.append([Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")])
            
            await e.edit("ℹ️ Visualizza o modifica la tipologia del prodotto <b>" + prodotto_selezionato + "</b>",
                buttons=pulsanti)
        
        
        
        
        elif e.data == b"change_account":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "tipologia", "w", encoding='utf8')
            file.truncate(0)
            file.write("account")
            file.close()
            
            await e.edit("✅ CATEGORIA PRODOTTO CAMBIATA ✅",
                buttons=[[Button.inline("⬅️ INDIETRO", "tipologia_prodotto")]])
        
        
        
        
        elif e.data == b"change_file":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "tipologia", "w", encoding='utf8')
            file.truncate(0)
            file.write("file")
            file.close()
            
            await e.edit("✅ CATEGORIA PRODOTTO CAMBIATA ✅",
                buttons=[[Button.inline("⬅️ INDIETRO", "tipologia_prodotto")]])
        
        
        
        
        elif e.data == b"imposta_file":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            
            file = open("admin/stato", "r", encoding='utf8')
            stato_read = file.read()
            file.close()
            
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(stato_read + "\nimposta_file")
            file.close()
            
            file = open(path + "tipologia", encoding='utf8')
            file_impostato = file.read().splitlines()
            file.close()
            
            try:
                file_sel = file_impostato[1]
            
            except:
                file_sel = "NESSUN FILE"
            
            await e.edit("📁 IMPOSTA FILE DA INVIARE AUTOMATICAMENTE DOPO L'ACQUISTO DEL PRODOTTO <b>" + prodotto_selezionato + "</b>.\n\nℹ️ Invia qui di seguito il nome del file che hai caricato precedentemente sul database del BOT. Se non ricordi il nome premi sul pulsante sotto-stante per visualizzare tutti i file nel database del BOT.\n\n<b>FILE ATTUALMENTE IMPOSTATO: </b>" + file_sel,
                buttons=[[Button.inline("👀 VISUALIZZA I FILES 👀", "all_file_view")],
                    [Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
        
        
        
        
        elif e.data == b"all_file_view":
            files = os.listdir("files/")
            files_num = len(files)
            i = -1
            mex = ""
            
            while i < files_num - 1:
                i = i + 1
                mex = mex + "\n- " + files[i]
            
            await e.edit("📁 TUTTI I FILE NEL DB: 📁\n\n" + mex,
                buttons=[[Button.inline("⬅️ INDIETRO", "imposta_file")]])
        
        
        
        
        elif e.data == b"pannello_account":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            file = open("admin/stato", "r", encoding='utf8')
            stato_read = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(stato_read + "\npannello_account")
            file.close()
            
            
            await e.edit("👤 <b>PANNELLO ACCOUNT</b> 👤\n\nℹ️ Invia qui di seguito uno o più account da aggiungere alla lista (andando a capo per ogni account). Lo script invierà automaticamente al cliente un account random dalla lista eliminandolo successivamente.",
                buttons=[[Button.inline("👀 VISUALIZZA LISTA 👀", "all_account_view")],
                    [Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
        
        
        
        
        elif e.data == b"all_account_view":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            file = open("admin/stato", "r", encoding='utf8')
            stato_read = file.read()
            file.close()
            
            try:
                check = stato[2]
                file = open("admin/stato", "w", encoding='utf8')
                file.truncate(0)
                file.write(stato_read.replace(stato[2], "").strip("\n"))
                file.close()
            
            except:
                pass
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "accounts", "r", encoding='utf-8')
            accounts = file.read()
            file.close()
            
            if accounts == "":
                await e.edit("👤 TUTTI GLI ACCOUNT IMPORTATI: 👤\n\n❌ NESSUN ACCOUNT IMPOSTATO ❌",
                    buttons=[[Button.inline("➖ RIMUOVI ACCOUNT ➖", "rimuovi_account"), Button.inline("❌ RESETTA LISTA ❌", "resetta_lista")],
                        [Button.inline("⬅️ INDIETRO", "pannello_account")]])
            
            else:
                await e.edit("👤 TUTTI GLI ACCOUNT IMPORTATI: 👤\n\n" + accounts,
                    buttons=[[Button.inline("➖ RIMUOVI ACCOUNT ➖", "rimuovi_account"), Button.inline("❌ RESETTA LISTA ❌", "resetta_lista")],
                        [Button.inline("⬅️ INDIETRO", "pannello_account")]])
        
        
        
        
        elif e.data == b"resetta_lista":
            await e.edit("⚠️ <b>CONFERMA ELIMINAZIONE</b> ⚠️\n\nℹ️ Sei sicuro di vorre eliminare tutta la lista degli account del prodotto? Questa azione è irreversibile.",
                buttons=[[Button.inline("✅ CONFERMA ✅", "resetta_lista_yes"), Button.inline("❌ ANNULLA ❌", "all_account_view")]])
        
        
        
        
        elif e.data == b"resetta_lista_yes":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "accounts", "w")
            file.truncate(0)
            file.close()
            
            await e.edit("✅ OPERAZIONE ESEGUITA CORRETTAMENTE ✅",
                buttons=[[Button.inline("⬅️ INDIETRO", "all_account_view")]])
        
        
        
        
        elif e.data == b"rimuovi_account":
            file = open("admin/stato", "r", encoding='utf8')
            stato_read = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(stato_read + "\nrimuovi_account")
            file.close()
            
            await e.edit("ℹ️ INVIA DI SEGUITO LA STRINGA DELL'ACCOUNT DA RIMUOVERE DALLA LISTA.",
                buttons=[[Button.inline("⬅️ INDIETRO", "all_account_view")]])
        
        
        
        
        elif e.data == b"prezzo_prodotto":
            file = open("admin/stato", "r", encoding='utf8')
            stato = file.read().splitlines()
            file.close()
            
            categoria_selezionata = stato[0]
            prodotto_selezionato = stato[1]
            
            path = "prodotti/" + categoria_selezionata + "/" + prodotto_selezionato + "/"
            
            file = open(path + "prezzo", "r")
            prezzo = file.read()
            file.close()
            
            file = open("admin/stato", "r", encoding='utf8')
            stato_read = file.read()
            file.close()
            
            file = open("admin/stato", "w", encoding='utf8')
            file.truncate(0)
            file.write(stato_read + "\nprezzo_prodotto")
            file.close()
            
            await e.edit("ℹ️ Invia di seguito il nuovo prezzo da modificare al prodotto <b>" + prodotto_selezionato + "</b>.\n\n<b>PREZZO ATTUALE: " + prezzo.replace(".", ",") + "</b> EUR.",
                buttons=[[Button.inline("⬅️ INDIETRO", "return_prodotto_scelto")]])
    
    ##################################
    
    
    #----------------------------------------------------------------#
    
    
    ########## SEZIONE UTENTE ##########
    
    else:
        if lista_ban.__contains__(str(user_callback)):
            await e.answer("⛔ SEI STATO BANNATO ⛔\n\nℹ️ Spiacenti, ma uno degli amministratori del BOT ha deciso di bannarti. Non potrai utilizzare il BOT e le sue funzioni ammenochè non verrai riammesso dallo staff.", alert=True)
        
        else:
            if obbligo == True:
                if e.data == b"check_canale":
                    try:
                        result = await client(functions.channels.GetParticipantRequest(
                        channel=canale_obbligo,
                        participant=int(sender.id)
                        ))
                        
                        await e.respond("✅ <b>SEI ISCRITTO</b> ✅\n\nℹ️ Grazie per esserti iscritto a " + canale_obbligo + ". Ora puoi utilizzare il bot",
                            buttons=[[Button.inline("🏠 Vai alla Home 🏠", "Home")]])
                    
                    except:
                        await e.answer("❌ ERRORE ❌\n\nℹ️ Non sei ancora iscritto al canale " + canale_obbligo + ". Iscriviti per poter utilizzare " + bot_name + ".", alert=True)
                        return
                
                try:
                    result = await client(functions.channels.GetParticipantRequest(
                    channel=canale_obbligo,
                    participant=int(sender.id)
                    ))
                
                except:
                    await e.answer("❌ ERRORE ❌\n\nℹ️ Devi essere iscritto a " + canale_obbligo + " per poter utilizzare " + bot_name + ".", alert=True)
                    return
            
            
            
            
            if e.data == b"Home":
                file = open(userpath + "dataavvio", "r")
                data_ora_avvio = file.read()
                file.close()

                file = open(userpath + "saldo", "r")
                saldo_read = file.read()
                file.close()
                
                saldo = float(saldo_read)
                
                await e.edit("<b> 👋🏻 Ciao " + sender.first_name + ".\n\n🤖 Questo è lo shop di @fsocietyUserBot\n\n💳 Saldo attuale: " + str(format(saldo, ".2f")) + "€</b>",
                    buttons=[[Button.inline("💰 Saldo", "wallet"), Button.inline("Shop 🛍", "shop")],
                    [Button.inline("💎 Tos", "tos"), Button.inline("Supporto ☎", "chatlive")]])
            
            
            
            
            elif e.data == b"tos":
                file = open("admin/tos", "r", encoding='utf-8')
                tos = file.read()
                file.close()
                
                if tos == "":
                    await e.edit("❌ NESSUN TOS IMPOSTATO ❌",
                        buttons=[[Button.inline("⬅️ INDIETRO", "Home")]])
                
                else:
                    await e.edit("⚠️ PROSEGUENDO CON UN ACQUISTO DA " + bot_name + " CONFERMI E DICHIARI AUTOMATICAMENTE DI AVER PRESO VISIONE ED <b>ACCETTATO</b> I TERMINI DI SERVIZIO SOTTO RIPORTATI:\n\n" + tos,
                        buttons=[[Button.inline("⬅️ INDIETRO", "Home")]])
            
            
            
            
            elif e.data == b"chatlive":
                file = open(userpath + "stato", "w")
                file.truncate(0)
                file.write("chatlive")
                file.close()
                
                await e.edit("💬 <b>CHAT LIVE</b> 💬\n\nℹ️ Qualsiasi messaggio che invierai da ora in poi verrà recapitato agli admin. Attendi un loro riscontro, riceverai un messaggio sulla messaggistica del BOT. Per chiudere la chat live utilizza il pulsante sotto stante o digita in qualunque momento il comando /annulla.",
                    buttons=[[Button.inline("❌ TERMINA CHAT ❌", "termina-chat")]])
            
            
            
            
            elif e.data == b"termina-chat":
                file = open(userpath + "stato", "w")
                file.truncate(0)
                file.close()
                
                await e.edit("❌ CHAT-LIVE TERMINATA ❌",
                    buttons=[[Button.inline("⬅️ INDIETRO", "Home")]])
            
            
            
            
            elif e.data == b"Homebuy":
                file = open(userpath + "dataavvio", "r")
                data_ora_avvio = file.read()
                file.close()

                file = open(userpath + "saldo", "r")
                saldo_read = file.read()
                file.close()
                
                saldo = float(saldo_read)
                
                await e.respond("<b> 👋🏻 Ciao " + sender.first_name + ".\n\n🤖 Questo è lo shop di @fsocietyUserBot\n\n💳 Saldo attuale: " + str(format(saldo, ".2f")) + "€</b>",
                    buttons=[[Button.inline("💰 Saldo", "wallet"), Button.inline("Shop 🛍", "shop")],
                    [Button.inline("💎 Tos", "tos"), Button.inline("Supporto ☎", "chatlive")]])
            
            
            
            
            
            elif e.data == b"wallet":
                file = open(userpath + "saldo", "r")
                saldo_read = file.read()
                file.close()
                
                saldo = float(saldo_read)
                
                await e.edit("💰 <b>WALLET</b> 💰\n\nℹ️ Qui di seguito sono presenti tutte le opzioni del tuo saldo e di tutte le tue transazioni.\n\n\n💳 Saldo attuale: <b>" + str(format(saldo, ".2f")) + " EUR</b>.",
                    buttons=[[Button.inline("➕ RICARICA SALDO ➕", "ricarica_saldo")], 
                    [Button.inline("🕓 CRONOLOGIA TRANSAZIONI 🕓", "cronologia_transazioni")],
                        [Button.inline("⬅️ INDIETRO", "Home")]])
            
            
            
            
            elif e.data == b"ricarica_saldo":
                pulsanti = []
                
                file = open("admin/pagamenti/paypal", "r", encoding='utf8')
                paypal = file.read()
                file.close()
                
                file = open("admin/pagamenti/bitcoin", "r", encoding='utf8')
                bitcoin = file.read()
                file.close()
                
                file = open("admin/pagamenti/monero", "r", encoding='utf8')
                monero = file.read()
                file.close()
                
                if paypal == "Disabled":
                    pass
                
                else:
                    pulsanti.append([Button.inline("✅ PAYPAL ✅", "ricarica_paypal")])
                
                
                if bitcoin == "Disabled":
                    pass
                
                else:
                    pulsanti.append([Button.inline("🪙 BITCOIN (BTC) 🪙", "ricarica_bitcoin")])
                
                
                if monero == "Disabled":
                    pass
                
                else:
                    pulsanti.append([Button.inline("🪙 MONERO (XMR) 🪙", "ricarica_monero")])
                
                pulsanti.append([Button.inline("⬅️ INDIETRO", "wallet")])
                
                await e.edit("🔄 <b>RICARICA IL SALDO</b>🔄\n\nℹ️ Seleziona prima di tutto che metodo di pagamento intendi usare per ricaricare il saldo del BOT <b>" + bot_name + "</b>.",
                    buttons=pulsanti)
            
            
            
            
            elif e.data == b"ricarica_paypal":
                file = open("admin/pagamenti/paypal", "r", encoding='utf-8')
                desc = file.read()
                file.close()
                
                await e.edit("🔄 <b>RICARICA CON PAYPAL</b>🔄\n\nℹ️ " + desc,
                    buttons=[[Button.inline("⬅️ INDIETRO", "ricarica_saldo")]])
            
            
            
            
            elif e.data == b"ricarica_bitcoin":
                file = open("admin/pagamenti/bitcoin", "r", encoding='utf-8')
                desc = file.read()
                file.close()
                
                await e.edit("🔄 <b>RICARICA CON BITCOIN (BTC)</b>🔄\n\nℹ️ " + desc,
                    buttons=[[Button.inline("⬅️ INDIETRO", "ricarica_saldo")]])
            
            
            
            
            elif e.data == b"ricarica_monero":
                file = open("admin/pagamenti/monero", "r", encoding='utf-8')
                desc = file.read()
                file.close()
                
                await e.edit("🔄 <b>RICARICA CON MONERO (XMR)</b>🔄\n\nℹ️ " + desc,
                    buttons=[[Button.inline("⬅️ INDIETRO", "ricarica_saldo")]])
            
            
            
            
            elif data[0] == "pagamento_effettuato":
                metodo = data[1]
                
                if metodo == "paypal":
                    mex = "PayPal"
                
                elif metodo == "bitcoin":
                    mex = "Bitcoin (BTC)"
                
                elif metodo == "monero":
                    mex = "Monero (XMR)"
                
                await client.send_message(int(admin_id), "✅ UN UTENTE HA CONFERMATO UN PAGAMENTO ✅\n\nℹ️ L'utente <a href='tg://user?id=" + str(sender.id) + "'>" + sender.first_name + "</a> (" + str(sender.id) + ") ha confermato di aver ricaricato e quindi pagato con il metodo di pagamento <b>" + mex + "</b>.\nControlla se ha effettuato il pagamento e ricarica la cifra che ti ha inviato.")
                
                file = open("admin/lista_admin", "r", encoding='utf8')
                admins = file.read().splitlines()
                admins_num = len(admins)
                file.close()
                i = - 1
                
                while i < admins_num - 1:
                    i = i + 1
                    await client.send_message(int(admins[i]), "✅ UN UTENTE HA CONFERMATO UN PAGAMENTO ✅\n\nℹ️ L'utente <a href='tg://user?id=" + str(sender.id) + "'>" + sender.first_name + "</a> (" + str(sender.id) + ") ha confermato di aver ricaricato e quindi pagato con il metodo di pagamento <b>" + mex + "</b>.\nControlla se ha effettuato il pagamento e ricarica la cifra che ti ha inviato.")
                
                
                await e.edit("✅ <b>RICHIESTA RICEVUTA</b> ✅\n\nℹ️ Abbiamo ricevuto la tua richiesta di ricarica del saldo. Attendi, un nostro staff controllerà il tuo pagamento se risulterà valido riceverai un riscontro sulla messaggistica del BOT.",
                    buttons=[[Button.inline("✅ CONFERMA ✅", "Home")]])
            
            
            
            
            elif e.data == b"cronologia_transazioni":
                file = open(userpath + "cronologia", "r", encoding='utf8')
                cronologia = file.read()
                file.close()
                
                if cronologia == "":
                    await e.answer("❌ ERRORE ❌\n\nℹ️ Non hai effettuato nessuna transazione.", alert=True)
                
                else:
                    await e.edit(cronologia,
                        buttons=[[Button.inline("⬅️ INDIETRO", "wallet")]])
            
            
            
            
            elif e.data == b"shop":
                categorie = os.listdir("prodotti/")
                
                if categorie == []:
                    await e.edit("❌ <b>ERRORE</b> ❌\n\nℹ️ Attualmente non è disponibile nessuna categoria.",
                        buttons=[[Button.inline("⬅️ INDIETRO", "Home")]])
                
                else:
                    num_categorie = len(categorie)
                    i = -1
                    pulsanti = []
                    
                    while i < num_categorie - 1:
                        i = i + 1
                        pulsanti.append([Button.inline(categorie[i], "categoria_selezionata" + categorie[i])])
                    
                    pulsanti.append([Button.inline("⬅️ INDIETRO", "Home")])
                    await e.edit("🛒 <b>CATEGORIE</b> 🛒\n\nℹ️ Scegli una categoria tramite i pulsanti sotto-stanti.",
                        buttons=pulsanti)
            
            
            
            
            elif e.data.__contains__(b"categoria_selezionata"):
                data_callback = e.data.decode('utf-8')
                categoria_selezionata_replace = str(data_callback)
                categoria_selezionata = categoria_selezionata_replace.replace("categoria_selezionata", "")
                
                path = "prodotti/" + categoria_selezionata + "/"
                
                prodotti = os.listdir(path)
                
                if prodotti == []:
                    await e.edit("❌ <b>ERRORE</b> ❌\n\nℹ️ Attualmente non è disponibile nessun prodotto per questa categoria.",
                        buttons=[[Button.inline("⬅️ INDIETRO", "Home")]])
                
                else:
                    num_prodotti = len(prodotti)
                    i = -1
                    pulsanti = []
                    
                    while i < num_prodotti - 1:
                        i = i + 1
                        try:
                            adici = os.listdir(path + prodotti[i] + "/")
                            pulsanti.append([Button.inline(prodotti[i], "prodotto_selezionato" + prodotti[i])])
                        
                        except:
                            pass
                    
                    file = open(userpath + "stato", "w", encoding='utf-8')
                    file.truncate(0)
                    file.write(categoria_selezionata)
                    file.close()
                    
                    pulsanti.append([Button.inline("⬅️ INDIETRO", "shop")])
                    await e.edit("🛒 <b>TUTTI I PRODOTTI</b> 🛒\n <i>🔸 Categoria: " + categoria_selezionata + "</i>\n\nℹ️ Scegli un prodotto tramite i pulsanti sotto-stanti e procedi successivamente con l'acquisto.",
                        buttons=pulsanti)
            
            
            
            
            elif e.data.__contains__(b"prodotto_selezionato"):
                data_callback = e.data.decode('utf-8')
                prodotto_selezionato_replace = str(data_callback)
                prodotto_selezionato = prodotto_selezionato_replace.replace("prodotto_selezionato", "")
                
                file = open(userpath + "stato", "r", encoding='utf8')
                categoria = file.read()
                file.close()
                
                path = "prodotti/" + categoria + "/" + prodotto_selezionato + "/"
                
                file = open(path + "nome", "r", encoding='utf8')
                nome = file.read()
                file.close()
                
                file = open(path + "descrizione", "r", encoding='utf8')
                descrizione = file.read()
                file.close()
                
                file = open(path + "prezzo", "r", encoding='utf8')
                prezzo = file.read()
                file.close()
                
                file = open(path + "tipologia", "r", encoding='utf8')
                tipologia = file.read()
                file.close()
                
                file = open(userpath + "stato", "w", encoding='utf8')
                file.truncate(0)
                file.write(nome + "\n" + descrizione + "\n" + prezzo + "\n" + tipologia + "\n" + path)
                file.close()
                
                await e.edit("🛒 Nome prodotto: <b>" + nome + "</b>\n\nℹ️ " + descrizione + "\n\n💰 Prezzo: <b>" + prezzo.replace(".", ",") + " EUR</b>.",
                    buttons=[[Button.inline("💳 ACQUISTA 💳", "conferma_acquisto")],
                        [Button.inline("⬅️ INDIETRO", "shop")]])
            
            
            
            
            elif e.data == b"conferma_acquisto":
                file = open(userpath + "stato", "r", encoding='utf8')
                stato = file.read().splitlines()
                file.close()
                
                await e.edit("✅ <b>CONFERMA ACQUISTO</b> ✅\n\nℹ️ Sei sicuro di voler acquistare <b>" + stato[0] + "</b> a <b>" + stato[2].replace(".", ",") + " EUR</b>?",
                    buttons=[[Button.inline("✅ CONFERMA ✅", "acquisto_confermato"), Button.inline("❌ ANNULLA ❌", "shop")]])
            
            
            
            
            elif e.data == b"acquisto_confermato":
                file = open(userpath + "saldo", "r")
                saldo_read = file.read()
                file.close()
                
                saldo = float(saldo_read)
                
                file = open(userpath + "stato", "r", encoding='utf8')
                stato = file.read().splitlines()
                file.close()
                
                prezzo = float(stato[2])
                
                if(saldo < prezzo):
                    await e.edit("❌ <b>ERRORE</b>❌\n\nℹ️ Fondi non sufficenti per completare la transazione. Ricarica il saldo prima di acquistare il prodotto.",
                        buttons=[[Button.inline("⬅️ INDIETRO", "shop")]])
                
                elif(saldo >= prezzo):
                    calcolo_finale = saldo - prezzo
                    
                    file = open(userpath + "saldo", "w")
                    file.truncate(0)
                    file.write(str(calcolo_finale))
                    file.close()
                    
                    file = open(userpath + "cronologia", "r", encoding='utf8')
                    cronologia = file.read()
                    file.close()
                    
                    file = open(userpath + "cronologia", "w", encoding='utf8')
                    file.truncate(0)
                    file.write(cronologia + "\n\n\n🛒 ACQUISTO 🛒\n🛍 Prodotto: " + stato[0] + "\n💳 Prezzo: -" + stato[2].replace(".", ",") + " EUR\n🕐 Data & ora: " + dataora)
                    file.close()
                    
                    try:
                        path = stato[5]
                    
                    except:
                        path = stato[4]
                    
                    file = open(path + "tipologia", "r", encoding='utf8')
                    tipologia = file.read().splitlines()
                    file.close()
                    
                    await e.delete()
                    
                    if tipologia[0] == "file":
                        try:
                            file_send = "files/" + tipologia[1]
                            
                            await client.send_file(int(sender.id), file_send)
                            
                            await e.respond("🎉 <b>ACQUISTO COMPLETATO</b>🎉\n\n👍 Grazie del tuo acquisto. Il file acquistato lo trovi al di sopra di questo messaggio.",
                                buttons=[[Button.inline("🏠 Torna alla Home", "Home")]])
                            

                        except:
                            await e.respond("🎉 <b>ACQUISTO COMPLETATO</b>🎉\n\n👍 Grazie del tuo acquisto. Il propietario dello SHOP BOT non ha impostato nessun invio automatico dopo l'acquisto del prodotto. Contattalo in chat per sapere come ricevere il prodotto acquistato nel caso si trattasse di una cosa non voluta.",
                                buttons=[[Button.inline("🏠 Torna alla Home", "Homebuy")]])
                    
                    elif tipologia[0] == "account":
                        try:
                            file = open(path + "accounts", "r", encoding='utf8')
                            line_count = -1
                            for line in file:
                                if line != "\n":
                                    line_count += 1
                            file.close()
                            
                            numero_rnd = random.randint(0,line_count)
                            
                            
                            file = open(path + "accounts", "r", encoding='utf8')
                            accounts = file.read().splitlines()
                            file.close()
                            
                            
                            file = open(path + "accounts", "r", encoding='utf8')
                            accounts_rpl = file.read()
                            file.close()
                            
                            selezionato = accounts[numero_rnd]
                            
                            replace_acc = accounts_rpl.replace(selezionato, "").strip('\n')
                            
                            if line_count <= 1:
                                file = open(path + "accounts", "w", encoding='utf8')
                                file.truncate(0)
                                file.close()
                            
                            else:
                                file = open(path + "accounts", "w", encoding='utf8')
                                file.truncate(0)
                                file.write(replace_acc)
                                file.close()
                            
                            
                            await e.respond("🎉 <b>ACQUISTO COMPLETATO</b>🎉\n\n👍 Grazie del tuo acquisto, ecco il tuo account:\n\n<pre>" + accounts[numero_rnd] + "</pre>",
                                buttons=[[Button.inline("🏠 Torna alla Home", "Homebuy")]])
                        
                        except:
                            await e.respond("🎉 <b>ACQUISTO COMPLETATO</b>🎉\n\n👍 Grazie del tuo acquisto. Il propietario dello SHOP BOT non ha impostato nessun invio automatico dopo l'acquisto del prodotto. Contattalo in chat per sapere come ricevere il prodotto acquistato nel caso si trattasse di una cosa non voluta.",
                                buttons=[[Button.inline("🏠 Torna alla Home", "Homebuy")]])
                    
                    
                    file = open("admin/lista_admin", "r", encoding='utf8')
                    admins = file.read().splitlines()
                    admins_num = len(admins)
                    file.close()
                    i = - 1
                    
                    await client.send_message(int(admin_id), "🛒 ACQUISTO 🛒\n\n👤 L'utente <a href='tg://user?id=" + str(sender.id) + "'>" + sender.first_name + "</a> (" + str(sender.id) + ") ha effettuato un acquisto.\n\n🛍 Prodotto: " + stato[0] + "\n💳 Prezzo: -" + stato[2].replace(".", ",") + " EUR\n🕐 Data & ora: " + dataora)
                    
                    while i < admins_num - 1:
                        i = i + 1
                        await client.send_message(int(admins[i]), "🛒 ACQUISTO 🛒\n\n👤 L'utente <a href='tg://user?id=" + str(sender.id) + "'>" + sender.first_name + "</a> (" + str(sender.id) + ") ha effettuato un acquisto.\n\n🛍 Prodotto: " + stato[0] + "\n💳 Prezzo: -" + stato[2].replace(".", ",") + " EUR\n🕐 Data & ora: " + dataora)
    
    ####################################
    
    
    
    
    

client.run_until_disconnected()