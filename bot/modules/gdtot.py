from bs4 import BeautifulSoup
from re import compile as re_compile
from requests import get as rget
from urllib.parse import urlparse, quote_plus
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher
from telegram.ext import CommandHandler


def search_gdtot(query):
    resp =  rget(f'https://gdbot.xyz/search?q={quote_plus(query)}')
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = soup.select("a[href*='https://gdbot.xyz/file']")
    info = [x.string for x in soup.find_all('span', string=re_compile(r'Size*'))]
    titles = [x.string for x in soup.find_all('a')[5:]]
    text, result = '', []
    for i, (title, inf, link) in enumerate(zip(titles, info, links), start=1):
        soup = BeautifulSoup(rget(link['href']).text, 'html.parser')
        text += f"{str(i).zfill(3)}. <a href='{link['href']}'>{str(title).strip()}</a>\n{inf}\n"
        for x in soup.select('a'):
            link = x['href']
            if 'gdbot.xyz' not in link:
                text += f"<a href='{link}'><b>{str(urlparse(link).hostname).upper()}</b></a> "
        text += '\n\n'
        result.append(text)
        text = ''
    return result


search_gdtot_handler = CommandHandler(command=BotCommands.GdtotCommand, gdtot,
                                    filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
                                    
dispatcher.add_handler(search_gdtot)
