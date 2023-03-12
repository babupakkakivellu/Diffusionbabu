from bs4 import BeautifulSoup
from re import compile as re_compile
from requests import get as rget
from urllib.parse import urlparse, quote_plus
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage
from bot import dispatcher
from telegram.ext import CommandHandler


def search_gdtot(update, context):
    args = update.message.text.split(maxsplit=1)
    reply = update.message.reply_to_message
    if len(args) > 1 and not reply:
        query = args[1]
    elif reply and reply.text:
        query = reply.text.strip()
    else:
        sendMessage('Please provided movie title along with command or by reply with command!', context.bot, update.message)
        return
    soup = BeautifulSoup(rget(f'https://gdbot.xyz/search?q={quote_plus(query)}').text, 'html.parser')
    links = soup.select("a[href*='https://gdbot.xyz/file']")
    info = [x.string for x in soup.find_all('span', string=re_compile(r'Size*'))]
    titles = [x.string for x in soup.find_all('a')[5:]]
    text = ''
    for i, (title, inf, link) in enumerate(zip(titles, info, links), start=1):
        soup = BeautifulSoup(rget(link['href']).text, 'html.parser')
        text += f"{str(i).zfill(3)}. {str(title).strip()}\n{inf}\n"
        for x in soup.select('a'):
            link = x['href']
            if 'drivebot.fun' not in link:
                text += f"<a href='{link}'><b>{str(urlparse(link).hostname).upper()}</b></a> "
        text += '\n\n'
        sendMessage(text, context.bot, update.message)
        text = ""
dispatcher.add_handler(CommandHandler(BotCommands.GdtotCommand, search_gdtot, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user))
