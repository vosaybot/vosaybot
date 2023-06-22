from random import randint
from urllib.parse import quote

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.utils.decorators import check_user, delete_previous_messages
from bot.utils.text import mt
from models import voice_model
from settings import database, settings

# Один элемент списка: ["CATEGORY", "SUBCATEGORY", "EMOTION", "PERFORMER", "TITLE"]
donate_voices = [
    # fmt: off
    ["games", "hearthstoneblackmount", "answer", "Нефариан (рассказчик)", "Спасибо, хахаха, хоть на починку тратиться не придётся"],
    ["games", "warcraft3", "agreement", "Рыцарь", "Наконец то"],
    ["games", "warcraft3", "joy", "Гром", "Наконец то"],
    ["games", "hearthstoneblackmount", "answer", "Нефариан (рассказчик)", "Думаю, по такому случаю я придумаю для тебя новый титул"],
    ["games", "hearthstoneblackmount", "answer", "Малориак", "Ни что не пропадёт впустую"],
    ["games", "warcraft3", "answer", "Грант (бугай)", "Союзникам нужна наша помощь"],
    ["games", "warcraft3", "answer", "Рыцарь", "Скромность украшает, но оставляет голодным"],
    ["games", "warcraft3", "answer", "Говорящий с духами", "Да пребудет с тобой сила"],
    ["games", "warcraft3", "answer", "Могильщик", "Я жду"],
    ["games", "warcraft3", "answer", "Могильщик", "Ваш ход"],
    ["games", "warcraft3", "answer", "Друид Медведь", "Лучше бы дал поесть, лапа продукт не каллорийный"],
    ["games", "warcraft3", "answer", "Повелитель Ужаса", "Я голоден"],
    ["games", "warcraft3", "answer", "Грант (бугай)", "Нужно золото"],
    ["games", "warcraft3", "other", "Мясник", "Заплатил налоги и спи спокойно"],

    ["films", "loveandpigeons", "answer", "Надежда Кузякина", "Ну Людк, иди, неси сберкнижку"],
    ["films", "loveandpigeons", "answer", "Василий Кузякин", "А денежки то, бабай унес"],
    ["films", "twelve_chairs", "answer", "Мечников", "Утром деньги, вечером стулья, или вечером деньги, ночью стулья"],
    ["films", "twelve_chairs", "answer", "Остап Бендер", "Так и быть, 50 процентов, половина моя половина наша"],

    ["politicians", "alexeinavalny", "answer", "Алексей Навальный", "Да вы должны были заплатить в несколько разбольше"],
    ["politicians", "alexeinavalny", "answer", "Алексей Навальный", "Вы можете помочь мне деньгами, я не олигарх и без вас не обойдусь"],
    ["politicians", "alexeinavalny", "answer", "Алексей Навальный", "Вы проворачиваете главную корупционную схему своей жизни"],
    ["politicians", "alexeinavalny", "other", "Алексей Навальный", "700 миллионов долларов"],
    ["politicians", "alexeinavalny", "other", "Алексей Навальный", "3 миллиарда долларов США"],
    ["politicians", "alexeinavalny", "other", "Алексей Навальный", "Вот они сотни миллионов долларов, не заплаченные в российский бюджет"],
    ["politicians", "vladimirputin", "me", "Путин", "Все эти 8 лет я пахал как раб на галерах и делал это с полной отдачей сил"]
]


@check_user
@delete_previous_messages
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    random_voice = donate_voices[randint(0, len(donate_voices) - 1)]
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
        caption=mt.donate,
        parse_mode=ParseMode.MARKDOWN,
    )


__all__ = ["donate"]
