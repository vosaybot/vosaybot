from urllib.parse import quote

from sqlalchemy import or_
from telegram import InlineQueryResultAudio, Update
from telegram.constants import InlineQueryLimit
from telegram.ext import ContextTypes

from bot.utils import check_user
from models import user_model, user_voice_model, voice_model
from settings import database, settings


@check_user
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    offset = 0 if not update.inline_query.offset else int(update.inline_query.offset)
    voices = (
        voice_model.select()
        .with_only_columns(
            voice_model.c.uuid, voice_model.c.title, voice_model.c.path, voice_model.c.performer
        )
        .limit(InlineQueryLimit.RESULTS)
        .offset(offset * InlineQueryLimit.RESULTS)
        .order_by(voice_model.c.created_at)
    )

    if text_search := update.inline_query.query:
        if text_search == "my":
            user_uuid_subq = (
                user_model.select()
                .with_only_columns(user_model.c.uuid)
                .where(user_model.c.telegram_id == update.effective_user.id)
                .scalar_subquery()
            )
            voices = voices.join(
                user_voice_model, voice_model.c.uuid == user_voice_model.c.voice_uuid, isouter=True
            ).where(user_voice_model.c.user_uuid == user_uuid_subq)
        else:
            voices = voices.where(
                or_(
                    voice_model.c.title.ilike(f"%{text_search}%"),
                    voice_model.c.performer.ilike(f"%{text_search}%"),
                )
            )

    await update.inline_query.answer(
        [
            InlineQueryResultAudio(
                id=voice["uuid"],
                title=voice["title"],
                audio_url=f"{settings.voice_url}/{settings.telegram_token}/assets/{quote(voice['path'])}",
                performer=voice["performer"],
            )
            for voice in await database.fetch_all(voices)
        ],
        cache_time=10,
        is_personal=True,
        connect_timeout=10,
        next_offset=offset + 1,
    )


__all__ = ["search"]
