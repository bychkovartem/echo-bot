from aiogram import Router
from aiogram.types import Message

router = Router()

# Обработчик ВСЕХ сообщений
@router.message()
async def echo_all(message: Message):
    try:
        # Текстовые сообщения (включая Markdown/HTML)
        if message.text:
            await message.answer(
                text=message.text
            )

        # Фото (с подписью или без)
        elif message.photo:
            await message.answer_photo(
                photo=message.photo[-1].file_id,
                caption=message.caption
            )

        # Видео
        elif message.video:
            await message.answer_video(
                video=message.video.file_id,
                caption=message.caption
            )

        # Стикеры
        elif message.sticker:
            await message.answer_sticker(
                sticker=message.sticker.file_id
            )

        # Голосовые сообщения
        elif message.voice:
            await message.answer_voice(
                voice=message.voice.file_id,
                caption=message.caption
            )

        # Аудио (музыка)
        elif message.audio:
            await message.answer_audio(
                audio=message.audio.file_id,
                caption=message.caption
            )

        # Документы (PDF, ZIP и др.)
        elif message.document:
            await message.answer_document(
                document=message.document.file_id,
                caption=message.caption
            )

        # GIF-анимации
        elif message.animation:
            await message.answer_animation(
                animation=message.animation.file_id,
                caption=message.caption
            )

        # Контакты
        elif message.contact:
            await message.answer_contact(
                phone_number=message.contact.phone_number,
                first_name=message.contact.first_name,
                last_name=message.contact.last_name,
                vcard=message.contact.vcard
            )

        # Геолокация
        elif message.location:
            await message.answer_location(
                latitude=message.location.latitude,
                longitude=message.location.longitude
            )

        # Опросы (Quiz/Poll)
        elif message.poll:
            await message.answer_poll(
                question=message.poll.question,
                options=[option.text for option in message.poll.options],
                is_anonymous=message.poll.is_anonymous,
                type=message.poll.type,
                allows_multiple_answers=message.poll.allows_multiple_answers,
                correct_option_id=message.poll.correct_option_id if message.poll.type == "quiz" else None,
                explanation=message.poll.explanation if message.poll.type == "quiz" else None,
                explanation_entities=message.poll.explanation_entities if message.poll.type == "quiz" else None,
                open_period=message.poll.open_period,
                close_date=message.poll.close_date
            )

        # Кубик (🎲, 🎯, 🏀 и др.)
        elif message.dice:
            await message.answer_dice(
                emoji=message.dice.emoji
            )

        # Данные из WebApp (если бот поддерживает WebApp)
        elif message.web_app_data:
            await message.answer(
                text=f"📲 WebApp Data:\n{message.web_app_data.data}"
            )

        # Места (Venue)
        elif message.venue:
            await message.answer_venue(
                latitude=message.venue.location.latitude,
                longitude=message.venue.location.longitude,
                title=message.venue.title,
                address=message.venue.address,
                foursquare_id=message.venue.foursquare_id,
                foursquare_type=message.venue.foursquare_type,
                google_place_id=message.venue.google_place_id,
                google_place_type=message.venue.google_place_type
            )

        # Если тип не распознан
        else:
            await message.answer("❌ Не могу повторить этот тип сообщения.")

    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")
