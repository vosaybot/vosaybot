from random import randint
from urllib.parse import quote

from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.decorators import check_user, delete_previous_messages
from bot.utils.text import mt
from models import voice_model
from settings import database, settings

# Один элемент списка: ["CATEGORY", "SUBCATEGORY", "EMOTION", "PERFORMER", "TITLE"]
welcome_voices = [
    # fmt: off
    ["other", "mems", "greetings", "Дмитрий Goblin Пучков", "Я вас категорически приветствую"],
    
    ["games", "hearthstoneblackmount", "greetings", "Корен Худовар", "Эй, народ, смотрите ка, хаха, у нас гость"],
    ["games", "warcraft3", "greetings", "Повелитель Ужаса", "Приветствую"],
    ["games", "hearthstoneblackmount", "greetings", "Лорд Виктор Нефарий", "Добро пожаловать в мою резиденцию, герой"],
    ["games", "warcraft3", "greetings", "Гоблин торговец", "Здравствуй"],
    
    ["politicians", "vladimirputin", "greetings", "Путин", "Здравствуйте"],
    
    ["films", "loveandpigeons", "greetings", "Надежда Кузякина", "Ты ли, чё ли"],
    ["films", "loveandpigeons", "greetings", "Надежда Кузякина", "Это откудова это к нам такого красивого дяденьку замело. Иль чё забыл, сказать пришёл"],
    ["films", "brother", "greetings", "Продавщица", "О, где ж вы были"],
    ["films", "brother", "greetings", "Данила Багров", "Здрасте"]
]


@check_user
@delete_previous_messages
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    random_voice = welcome_voices[randint(0, len(welcome_voices) - 1)]
    voice = await database.fetch_one(
        voice_model.select()
        .with_only_columns(voice_model.c.path)
        .where(
            voice_model.c.category == random_voice[0],
            voice_model.c.subcategory == random_voice[1],
            voice_model.c.emotion == random_voice[2],
            voice_model.c.performer == random_voice[3],
            voice_model.c.title == random_voice[4],
        )
    )
    await update.message.reply_voice(
        voice=f"{settings.voice_url_path}/{quote(voice.path)}",
        caption=mt.start,
        quote=False,
    )


__all__ = ["start"]
