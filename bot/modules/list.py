from telegram.ext import CommandHandler
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage
from bot.helper.telegram_helper.filters import CustomFilters
import threading
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.mirror_utils.upload_utils.gdtot_helper import GDTOT

def list_drive(update, context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        LOGGER.info(f"Searching: {search}")
        reply = sendMessage('<b>🔎 Searching..... Please Wait!</b>', context.bot, update)
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        if button:
            editMessage(msg, reply, button)
        else:
            editMessage(f'<b>❌ No Result Found For</b> <code>{search}</code> 😎', reply, button)

    except IndexError:
        sendMessage('<b>📨 Send a Search Key Along With Command 🤒</b>', context.bot, update)


def gdtot(update, context):
    try:
        search = update.message.text.split(' ', 1)[1]
        search_list = search.split(' ')
        for glink in search_list:
            LOGGER.info(f"Extracting gdtot link: {glink}")
            button = None
            reply = sendMessage('<b>🔄 Getting Your GDTOT File Wait....</b>', context.bot, update)
            file_name, file_url = GDTOT().parse(url=glink)
            if file_name == 404:
                sendMessage(file_url, context.bot, update)
                return
            if file_url != 404:
                gdrive = GoogleDriveHelper(None)
                msg, button = gdrive.clone(file_url)
            if button:
                editMessage(msg, reply, button)
            else:
                editMessage(file_name, reply, button)
    except IndexError:
        sendMessage('<b>📨 Send Comment Along With Url 😐</b>', context.bot, update)
    except Exception as e:
        LOGGER.info(e)

list_handler = CommandHandler(BotCommands.ListCommand, list_drive, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
gdtot_handler = CommandHandler(BotCommands.GDTOTCommand, gdtot, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)



dispatcher.add_handler(list_handler)
dispatcher.add_handler(gdtot_handler)
