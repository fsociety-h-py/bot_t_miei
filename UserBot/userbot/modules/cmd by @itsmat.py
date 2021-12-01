############################################################
#cmds by @itsmat
############################################################

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.events import register
from userbot import bot
from time import sleep

@register(outgoing=True, pattern="^.sg(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("Rispondi al messaggio di un utente")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("Rispondi al messaggio di un utente")
       return
    chat = "@SangMataInfo_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("Rispondi al messaggio di un utente non di un bot")
       return
    await event.edit("Processo...")
    async with bot.conversation(chat, exclusive=False) as conv:
          response = None
          try:
              msg = await reply_message.forward_to(chat)
              response = await conv.get_response(message=msg, timeout=5)
          except YouBlockedUserError: 
              await event.edit(f"Sblocca {chat} e riprova")
              return
          except Exception as e:
              print(e.__class__)

          if not response:
              await event.edit("Bot probabilmente offline")
          elif response.text.startswith("Forward"):
             await event.edit("Errore, le impostazioni privacy dell'utente non permettono di visualizzare la sua cronologia nomi/username")
          else: 
             await event.edit(response.text)
          sleep(1)
          await bot.send_read_acknowledge(chat, max_id=(response.id+3))
          await conv.cancel_all()

############################################################

from asyncio import sleep
from userbot.events import register

@register(outgoing=True, pattern=r"\.kickme$")
async def kickme(leave):
    """Comando per autokickarti by @itsmat"""
    await leave.edit("Io vado via👋")
    await leave.client.kick_participant(leave.chat_id, 'me')

############################################################

from telethon.tl.types import ChannelParticipantsAdmins
from userbot.events import register

@register(outgoing=True, pattern="all( (.*)|$)")
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    mentions = input_str or "@all"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 100):
        mentions += f"[............all............](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()

############################################################

from userbot.events import register

@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ chatid. """
    if not chat.text[0].isalpha() and chat.text[0] not in ("/", "#", "@", "!"):
        await chat.edit("Chat ID: `" + str(chat.chat_id) + "`")


#######################################

from telethon.tl import functions
from telethon import events, types
import asyncio

from asyncio import sleep
from os import remove
from telethon import events
from telethon.tl import functions, types
from platform import python_version, uname
from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (PeerChannel, ChannelParticipantsAdmins,
                               ChatAdminRights, ChatBannedRights,
                               MessageEntityMentionName, MessageMediaPhoto,
                               ChannelParticipantsBots)

from userbot import bot
from userbot.events import register


@register(outgoing=True, pattern=r"\.create (s|g|c)(?: |$)(.*)")
async def telegraphs(grop):
    """Utilizza .create per creare un gruppo o canale"""
    if grop.text[0].isalpha() or grop.text[0] in ("/", "#", "@", "!"):
        return
    if grop.fwd_from:
        return
    type_of_group = grop.pattern_match.group(1)
    group_name = grop.pattern_match.group(2)
    if type_of_group == "s":
        try:
            result = await grop.client(functions.messages.CreateChatRequest(  # pylint:disable=E0602
                users=["@GroupHelpBot"],
                title=group_name
            ))
            created_chat_id = result.chats[0].id
            result = await grop.client(functions.messages.ExportChatInviteRequest(
                peer=created_chat_id,
            ))
            await grop.edit("Il gruppo {0} è stato creato. Premi [{0}]({1}) per entrare".format(group_name, result.link))
        except Exception as e:  # pylint:disable=C0103,W0703
            await grop.edit(str(e))
    elif type_of_group in ("g", "c"):
        try:
            r = await grop.client(functions.channels.CreateChannelRequest(  # pylint:disable=E0602
                title=group_name,
                about="Welcome",
                megagroup=not bool(type_of_group == "c")
            ))
            created_chat_id = r.chats[0].id
            result = await grop.client(functions.messages.ExportChatInviteRequest(
                peer=created_chat_id,
            ))
            await grop.edit("Il tuo gruppo/canale {0} è stato creato. Premi [{0}]({1}) per entrare".format(group_name, result.link))
        except Exception as e:  # pylint:disable=C0103,W0703
            await grop.edit(str(e))