import json
import os
import re
from asyncio import sleep
from datetime import datetime, time
from random import randint
from shutil import rmtree
from sqlite3 import connect
from urllib.parse import quote

import phonenumbers
import wikipedia
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from babel.numbers import format_decimal as babel_format_decimal
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from emoji import is_emoji
from faker import Faker
from gtts import gTTS
from pyfiglet import Figlet
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.enums.chat_action import ChatAction
from pyrogram.errors import BadRequest, FloodWait, Forbidden
from pyrogram.types import (
    Animation,
    Audio,
    BotCommand,
    CallbackQuery,
    Chat,
    Contact,
    Dice,
    Document,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Location,
    Message,
    Photo,
    Poll,
    Sticker,
    User,
    Venue,
    Video,
    VideoNote,
    Voice,
)
from pyshorteners import Shortener
from qrcode import make as qrcode_make
from ua_alarm import Client as UkraineAlertApiClient
from urlextract import URLExtract

from Additions.Borysfen_DB_V97 import (
    Any_Map,
    Buttons_Map,
    DB_Map,
    Dict_Map,
    Markup_Map,
    Text_Map,
    TG_Emoji_Map,
)
from Additions.maze_game import MAZE_COLS, MAZE_ROWS, get_map_cell, get_map_str
from Additions.virustotal import VirusTotal

# from icecream import ic
load_dotenv()

# ruff: noqa: E501, E722

try:
    PREFIX = str(os.environ["PREFIX_FOR_COMMANDS"])
except KeyError:
    print(
        f"{Dict_Map.COLORS['RED']}Create and fill .env file{Dict_Map.COLORS['WHITE']}"
    )
    exit()

# Create the Text_Map.CONFIG_DIR directory if it doesn't exist
os.makedirs(Text_Map.CONFIG_DIR, exist_ok=True)

# Set the language for Wikipedia to Ukrainian
wikipedia.set_lang("uk")

maze_maps = {}

fake = Faker("en_US")

school_day = "default"

# Create a VirusTotal object using the API key
virus_total = VirusTotal(os.environ["VIRUS_TOTAL_API_KEY"], os.environ["MONGO_DB_URL"])


def create_database(database_path: str):
    """
    Creates the database tables if they don't exist.

    Parameters:
    - database_path (str): The path to the database file.

    Note:
    - This function assumes the existence of the `Text_Map` dictionary, which contains the column names for the 'users' and 'messages' tables.
    """
    with connect(database_path) as conn:
        cursor = conn.cursor()

        def column_and_datatype(dct: dict) -> str:
            """
            Generate a string representation of column names and their corresponding data types.

            Args:
                dct (dict): A dictionary containing column names as keys and data types as values.

            Returns:
                str: A string representation of column names and their corresponding data types.
            """
            return ", ".join(
                [f"{column} {datatype}" for column, datatype in dct.items()]
            )

        # Create the 'users' table if it doesn't exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users ?",
            column_and_datatype(DB_Map.USER_COLUMNS),
        )

        # Create the 'messages' table if it doesn't exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS messages ?",
            column_and_datatype(DB_Map.MESSAGE_COLUMNS),
        )

        # Create the 'alert_users' table if it doesn't exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS alert_users (ID INTEGER PRIMARY KEY)"
        )

        # Commit the changes
        conn.commit()


app = Client(
    f"{Text_Map.CONFIG_DIR}/{os.environ['CLIENT_NAME']}",
    api_id=os.environ["TELEGRAM_API_ID"],
    api_hash=os.environ["TELEGRAM_API_HASH"],
    system_version=os.environ["CLIENT_NAME"],
    device_model=os.environ["CLIENT_NAME"],
    lang_code=os.environ["LANG_CODE"],
    parse_mode=ParseMode.HTML,
)

BOT_COMMANDS = [
    BotCommand(os.environ["START"], f"{TG_Emoji_Map.HOUSE} Меню"),
    BotCommand(os.environ["SEARCH_TEACHER"], f"{TG_Emoji_Map.MAG_RIGHT} Пошук вчителя"),
    BotCommand(os.environ["INFO"], f"{TG_Emoji_Map.INFORMATION_SOURCE} Інформація"),
    BotCommand(os.environ["ASK"], f"{TG_Emoji_Map.TELEPHONE_RECEIVER} Запитайка"),
    BotCommand(os.environ["DATA_SEARCH"], f"{TG_Emoji_Map.MAG_RIGHT} Пошук в базі"),
    BotCommand(os.environ["ADD_INFO"], f"{TG_Emoji_Map.PENCIL} Додати інформацію"),
    BotCommand(
        os.environ["ME"],
        f"{TG_Emoji_Map.BUST_IN_SILHOUETTE} Інформація про мене",
    ),
    BotCommand(os.environ["HELP"], f"{TG_Emoji_Map.QUESTION} Умовні знаки"),
    BotCommand(
        os.environ["SEND"],
        f"{TG_Emoji_Map.SPEECH_BALLOON} Надіслати повідомлення",
    ),
    BotCommand(os.environ["NOW_IS"], f"{TG_Emoji_Map.CLOCK} Годинник"),
    BotCommand(os.environ["WIKI"], f"{TG_Emoji_Map.BOOKS} Вікіпедія"),
    BotCommand(
        os.environ["QR"],
        f"{TG_Emoji_Map.BLACK_SQUARE_BUTTON} Створити або зчитати QR",
    ),
    BotCommand(os.environ["WEATHER"], f"{TG_Emoji_Map.WHITE_SUN_SMALL_CLOUD} Погода"),
    BotCommand(
        os.environ["TEXT_2_SPEECH"],
        f"{TG_Emoji_Map.PENCIL} Текст -> Голос {TG_Emoji_Map.SPEAKING_HEAD}",
    ),
    BotCommand(
        os.environ["UPLOAD"],
        f"{TG_Emoji_Map.OUTBOX_TRAY} Завантажити повідомлення до бота",
    ),
    BotCommand(os.environ["MAZE"], f"{TG_Emoji_Map.RED_CIRCLE} Гра лабіринт"),
    BotCommand(
        os.environ["PASSWORD_GENERATOR"], f"{TG_Emoji_Map.KEY} Генератор паролю"
    ),
    BotCommand(
        os.environ["VIRUSTOTAL"],
        f"{TG_Emoji_Map.CORONAVIRUS} Перевірити на віруси",
    ),
    BotCommand(
        os.environ["ALERT"], f"{TG_Emoji_Map.LOUD_SOUND} Сповіщення про тривогу"
    ),
    BotCommand(
        os.environ["URL_SHORTENER"],
        f"{TG_Emoji_Map.LINK} Скорочення URL-адреси",
    ),
]


# BotCommand(os.environ["START"], ""),


def bold_text(text: str) -> str:
    """
    Wraps the input text in HTML bold tags.

    Parameters:
        - text (str): The input text to be wrapped.

    Returns:
        - str: The input text wrapped in HTML bold tags.
    """
    return f"<b>{str(text)}</b>"


def change_layout(text: str) -> str:
    """
    This function converts the layout of the provided text from English to Ukrainian using a predefined mapping.

    Parameters:
    - text (str): The text to convert the layout.

    Returns:
    - str: The converted text with the layout changed.
    """
    return "".join(Dict_Map.LAYOUT_EN_2_UA.get(char.lower(), char) for char in text)


@app.on_message(
    filters.command(
        commands=[
            os.environ["START"],
            change_layout(os.environ["START"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def start(
    client: Client,
    message: Message,
    callback: CallbackQuery = None,
    file_not_found: bool = False,
):
    """
    Handle the start command or callback to initiate the conversation with the bot.

    Parameters:
        - client (Client): The Telegram client object.
        - message (Message): The message object representing the start command.
        - callback (CallbackQuery): The callback query object if the start command was triggered by a callback.
        - file_not_found (bool): Flag indicating if the file was not found. Default is False.

    Raises:
        - BadRequest: If there is a bad request during the execution.
        - Exception: If any other error occurs during the execution.

    Note:
        - The function retrieves user information using the `get_tg_info` function.
        - The function checks if the user is registered or not and determines the appropriate reply markup.
        - The function sends the start message to the chat with the corresponding reply markup.
    """
    try:
        # Get the user ID
        user_id = get_tg_info(message, callback)

        # Check if the user is registered or not and determine the reply markup
        if not (is_me(user_id) or await get_info(user_id)):
            reply_markup = Markup_Map.START_NOT_REGISTERED
        else:
            # Check if the command is to get a file and call the corresponding function
            if (
                not (callback or file_not_found)
                and len(message.command) == 2
                and len(message.command[1]) == 40
            ):
                await get_message(client, message)
                return

            reply_markup = (
                Markup_Map.START_WITH_CLASS_INFORMATION
                if (await get_info(user_id, DB_Map.CLASSROOM)).isdigit()
                else Markup_Map.START
            )

        private_chat = is_private_chat(message, callback)

        if not private_chat:
            reply_markup.inline_keyboard.append([Buttons_Map.DELETE_FULL])

        # Set the start message text
        text = bold_text(
            f'{TG_Emoji_Map.WAVE} {get_greeting()}! Я – бот помічник Ліцею "Борисфен" \n\n{Text_Map.SELECT_ITEM}'
        )

        if callback:
            # Edit the message with the start message
            await callback.message.edit_text(text, reply_markup=reply_markup)
        else:
            # Send a new message with the start message
            await client.send_message(
                message.chat.id,
                text,
                reply_to_message_id=message.id,
                reply_markup=reply_markup,
            )

        if not private_chat:
            reply_markup.inline_keyboard.pop(-1)

    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            callback=callback,
            markup=Markup_Map.DELETE,
            badrequest=True,
        )
    except Exception as error:
        await send_exception(
            client=client,
            message=message,
            error=error,
            markup=Markup_Map.DELETE,
            callback=callback,
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["SEARCH_TEACHER"],
            change_layout(os.environ["SEARCH_TEACHER"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def search_teacher(
    client: Client, message: Message, callback: CallbackQuery = None
):
    """
    This function handles the search_teacher command or callback to search for people.

    Parameters:
    - client (Client): The Telegram client object.
    - message (Message): The message object representing the search_teacher command.
    - callback (CallbackQuery): The callback query object if the search_teacher command was triggered by a callback.

    Raises:
    - IndexError: If there is an index error during the execution.
    - FloodWait: If there is a flood wait time during the execution.
    - BadRequest: If there is a bad request during the execution.
    - Exception: If any other error occurs during the execution.
    """
    try:
        user_id = get_tg_info(message, callback)

        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        if callback:
            text = (
                callback.message.reply_to_message.text
                or callback.message.reply_to_message.caption
            )
            command = os.environ["SEARCH_TEACHER"]
        else:
            command = message.command[0]
            text = message.text or message.caption

        name = split_command(text.lower(), command)

        matching_persons = [key for key in Dict_Map.PEOPLE_MAP if name in key.lower()]

        if not matching_persons:
            raise Exception(Text_Map.NO_RESULTS)

        if callback and callback.data.startswith("search_page_"):
            page = int(callback.data.split("search_page_", 1)[1])
        else:
            page = 1

        start_index = (page - 1) * Any_Map.RESULTS_PER_PAGE
        end_index = start_index + Any_Map.RESULTS_PER_PAGE
        matching_persons_page = matching_persons[start_index:end_index]

        if len(matching_persons) == 1:
            text = bold_text(
                "\n\n".join(
                    f"{k} {v}"
                    for k, v in Dict_Map.PEOPLE_MAP[matching_persons[0]].items()
                )
            )

            reply_markup = (
                Markup_Map.SEARCH_TEACHER_NUMBER
                if has_number(text)
                else Markup_Map.DELETE_FULL
            )

            if callback:
                await callback.message.edit_text(
                    text=text, reply_markup=reply_markup, disable_web_page_preview=True
                )
            else:
                await client.send_message(
                    message.chat.id,
                    text=text,
                    reply_markup=reply_markup,
                    reply_to_message_id=message.id,
                    disable_web_page_preview=True,
                )
        else:
            reply_markup = InlineKeyboardMarkup(
                sorted(
                    [
                        [InlineKeyboardButton(text=person, callback_data=f"{person}_s")]
                        for person in matching_persons_page
                    ],
                    key=lambda x: x[0].text.lower(),
                )
            )

            pagination_buttons = []

            if page > 2:
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=TG_Emoji_Map.REWIND, callback_data="search_page_1"
                    )
                )

            if page > 1:
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=TG_Emoji_Map.ARROW_BACKWARD,
                        callback_data=f"search_page_{page - 1}",
                    )
                )

                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=str(page), callback_data=f"page_counter_{page}"
                    )
                )

            if end_index < len(matching_persons):
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=TG_Emoji_Map.ARROW_FORWARD,
                        callback_data=f"search_page_{page + 1}",
                    )
                )

            if (
                len(matching_persons) - end_index > 1
                and len(matching_persons) - end_index > Any_Map.RESULTS_PER_PAGE
            ):
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=TG_Emoji_Map.FAST_FORWARD,
                        callback_data=f"search_page_{len(matching_persons) // Any_Map.RESULTS_PER_PAGE + 1}",
                    )
                )

            reply_markup.inline_keyboard.append(pagination_buttons)
            reply_markup.inline_keyboard.append([Buttons_Map.DELETE_FULL])

            text = bold_text(
                f"Кількість збігів: {len(matching_persons)}\n\n{Text_Map.SELECT_ITEM}"
            )

            if callback:
                await callback.message.edit_text(text, reply_markup=reply_markup)
            else:
                await client.send_message(
                    message.chat.id,
                    text,
                    reply_to_message_id=message.id,
                    reply_markup=reply_markup,
                )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except IndexError:
        await send_exception(
            client=client,
            message=message,
            error=f"{os.environ['SEARCH_TEACHER']} {Dict_Map.ERRORS['IndexError']['SEARCH_TEACHER']}",
            callback=callback,
            index_error=True,
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            floodwait=True,
            badrequest=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error=Text_Map.NO_RESULTS,
            callback=callback,
            badrequest=True,
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["INFO"],
            change_layout(os.environ["INFO"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def info(client: Client, message: Message):
    """
    Retrieves and displays information about a user, chat, or forwarded message.

    Parameters:
        - client (Client): The Telegram client object.
        - message (Message): The message containing the request for information.

    Note:
        - The function retrieves information based on the type of message received:
            - If the message is a reply to another message, it retrieves information about the replied message.
            - If the message contains a valid user ID or username, it retrieves information about the user.
            - If the message contains a valid chat ID or username, it retrieves information about the chat.
            - If no specific target is identified, it retrieves information about the sender of the message.
        - The function displays the retrieved information in a formatted text message.
        - It supports different types of messages, such as contacts, forwarded messages, forwarded from chats, and regular messages.
    """
    try:
        user_id = get_tg_info(message)

        # Check if the user has permission to access the requested information
        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        # Define a constant for displaying "no results" text
        user = True
        file = (
            message.reply_to_message.document
            if message.reply_to_message
            else message.document
        )

        if message.reply_to_message:
            reply_msg = message.reply_to_message
            # Information about a replied message
            if reply_msg.contact:
                msg = reply_msg.contact
                info = {
                    TG_Emoji_Map.BUST_IN_SILHOUETTE: f"{msg.first_name} {msg.last_name or ''}",
                    TG_Emoji_Map.ID: msg.user_id or Text_Map.NO_RESULTS2,
                    **info_phone(msg),
                }
            elif reply_msg.poll:
                # Handling information retrieval for a replied poll message
                msg = reply_msg.poll
                info = {
                    TG_Emoji_Map.QUESTION: msg.question,
                    TG_Emoji_Map.SPEAKING_HEAD: format_int_number(
                        msg.total_voter_count
                    ),
                    TG_Emoji_Map.WHITE_CHECK_MARK: (
                        msg.options[msg.correct_option_id].text
                    )
                    if msg.correct_option_id
                    else Text_Map.NO_RESULTS2,
                    TG_Emoji_Map.PAGE_FACING_UP: msg.explanation
                    or Text_Map.NO_RESULTS2,
                }
            elif reply_msg.forward_from:
                # Handling information retrieval for a message forwarded from a user
                msg = reply_msg.forward_from
                info = {
                    **info_simple_user(msg),
                    **info_forward_date(reply_msg),
                }
            elif reply_msg.forward_from_chat:
                # Handling information retrieval for a message forwarded from a chat
                msg = reply_msg.forward_from_chat
                info = {
                    **info_title(msg),
                    **info_id(msg),
                    **info_username(msg),
                    **info_chat_type(msg),
                    TG_Emoji_Map.COP: reply_msg.forward_signature
                    or Text_Map.NO_RESULTS2,
                    TG_Emoji_Map.EYE: format_int_number(reply_msg.views)
                    if reply_msg.views
                    else Text_Map.NO_RESULTS2,
                }
            elif reply_msg.forward_sender_name:
                # Handling information retrieval for a message forwarded with a hidden sender name
                info = {
                    TG_Emoji_Map.BUST_IN_SILHOUETTE: reply_msg.forward_sender_name,
                    **info_forward_date(reply_msg),
                }
            else:
                # Handling information retrieval for a regular user message
                info = info_simple_user(reply_msg.from_user)
        else:
            try:
                text = message.text or message.caption
                id = replace_tme(split_command(text.lower(), message.command[0]))

                if not (is_user_id(id) or is_group_id(id)):
                    if not (is_username(id)):
                        raise BadRequest

                if user:
                    # Information about a user
                    try:
                        user = await client.get_users(id)
                        info = info_simple_user(user)
                    except (BadRequest, IndexError):
                        user = False

                if not user:
                    # Information about a chat
                    chat = await client.get_chat(id)
                    info = {
                        **info_title(chat),
                        **info_id(chat),
                        **info_username(chat),
                        **info_chat_type(chat),
                        TG_Emoji_Map.BUSTS_IN_SILHOUETTE: format_int_number(
                            chat.members_count
                        )
                        if chat.members_count
                        else Text_Map.NO_RESULTS2,
                        f"{TG_Emoji_Map.PAGE_FACING_UP} {chat.description or Text_Map.NO_RESULTS2}": Text_Map.FAKE_VOID,
                    }

            except IndexError:
                # Information about the sender of the message
                info = info_simple_user(message.from_user)

        if file:
            # Define a function to convert a given size in bytes to a human-readable format
            def convert_bytes(size):
                """
                Converts a given size in bytes to a human-readable format.

                Args:
                    size (float): The size in bytes.

                Returns:
                    str: The human-readable format of the size.
                """
                # Define the units for size
                units = ["bytes", "KB", "MB", "GB", "TB"]

                # Iterate through the units and divide size by 1024 until size is less than 1024
                for unit in units:
                    if size < 1024.0:
                        return "%3.1f %s" % (size, unit)
                    size /= 1024.0

                # Return the size in the last unit
                return size

            # Update the 'info' dictionary with the file information
            info.update(
                {
                    TG_Emoji_Map.PAGE_FACING_UP: file.file_name,
                    TG_Emoji_Map.PACKAGE: convert_bytes(file.file_size),
                    TG_Emoji_Map.CALENDAR_SPIRAL: file.date.strftime(
                        "%d.%m.%Y %H:%M:%S"
                    ),
                }
            )

        # Send the formatted information to the chat
        await client.send_message(
            message.chat.id,
            text=bold_text(
                "\n\n".join(f"{k} <code>{v}</code>" for k, v in info.items())
            ),
            reply_markup=Markup_Map.DELETE_FULL,
            reply_to_message_id=message.id,
        )

    except PermissionError:
        await send_exception(client=client, message=message, permissionerror=True)
    except BadRequest:
        await send_exception(client=client, message=message, error=Text_Map.NO_RESULTS)
    except Exception as error:
        await send_exception(client=client, message=message, error=error)


@app.on_message(
    filters.command(
        commands=[os.environ["ASK"], change_layout(os.environ["ASK"])],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def ask(client: Client, message: Message):
    """
    Asks a question by forwarding the message or its associated file to the specified chat.

    Parameters:
        - client (Client): The Telegram client object.
        - message (Message): The message containing the question.

    Raises:
        - IndexError: If there is an index error during the execution.
        - ValueError: If there is a value error during the execution.
        - Exception: If any other error occurs during the execution.

    Note:
        - The function forwards the message or its associated file to the specified chat as a question.
        - It extracts the question text from the message and includes it in the forwarded message.
        - If the message is a reply to another message, it includes the original message text as well.
        - If the user is not an admin, the function sends a notification to the admin about the received question.
        - The function supports various types of files and media, such as photos, videos, audios, documents, contacts, locations, voices, dice, animations, venues, stickers, and video notes.
    """
    try:
        # Get user information
        user_id = get_tg_info(message)
        user_role = await get_info(user_id)
        user_is_me = is_me(user_id)

        msg_to_forward = message.reply_to_message or message

        file = has_file(msg_to_forward)

        text = msg_to_forward.caption or msg_to_forward.text
        text = text.html if text else ""

        command = message.command[0]

        if message.reply_to_message:
            # Include the original message text as part of the question
            send_text = bold_text(text)
        else:
            try:
                send_text = bold_text(split_command(text, command))

            except IndexError:
                if not file:
                    raise IndexError
                send_text = ""

        if not (user_is_me or user_role == DB_Map.ADMIN):
            # Notify admin about the received question
            if not message.from_user.is_bot:
                info = info_simple_user(message.from_user)
                t_id = os.environ["YOUR_TELEGRAM_ACCOUNT_ID"]
                who_is_text = bold_text(
                    "Вам надійшло повідомлення від:\n\n"
                    + ("\n\n".join(f"{k} <code>{v}</code>" for k, v in info.items()))
                )
        else:
            # Forward the message to the specified chat
            s_text = message.caption or message.text
            s_text = split_command(s_text.html, command)
            message_parts = s_text.split(" ", 1)

            t_id = message_parts[0]
            if not (is_user_id(t_id) or is_group_id(t_id)):
                t_id = await username2id(t_id)

            if not message.reply_to_message:
                try:
                    send_text = bold_text(message_parts[1])
                except IndexError:
                    if not file:
                        raise IndexError
                    send_text = ""

            who_is_text = bold_text("Вам надійшло повідомлення від Адміністрації")

        if not file:
            # Send the text message
            forwarded_msg = await client.send_message(
                chat_id=t_id,
                disable_web_page_preview=True,
                text=send_text,
                reply_markup=msg_to_forward.reply_markup,
            )
        else:
            # Forward the file message
            forwarded_msg = await forwards_cover(
                client=client,
                msg_to_forward=msg_to_forward,
                file=file,
                t_id=t_id,
                reply_markup=msg_to_forward.reply_markup,
                send_text=(
                    send_text if not message.reply_to_message.media_group_id else ""
                )
                if message.reply_to_message
                else send_text,
            )

        # Send a notification message to the admin or the target chat
        await client.send_message(
            chat_id=t_id,
            text=who_is_text,
            reply_markup=Markup_Map.DELETE_FULL,
            reply_to_message_id=forwarded_msg.id,
        )

        # Send a confirmation message to the current chat
        await client.send_message(
            chat_id=message.chat.id,
            text=Text_Map.WAIT_FOR_RESPONSE,
            reply_markup=Markup_Map.DELETE_FULL,
            reply_to_message_id=message.id,
        )

    except PermissionError:
        await send_exception(client=client, message=message, permissionerror=True)
    except (IndexError, ValueError):
        await send_exception(
            error=f"{os.environ['ASK']} {Dict_Map.ERRORS['IndexError']['ASK']['admin' if user_is_me or user_role == DB_Map.ADMIN else 'user']}",
            client=client,
            message=message,
            index_error=True,
        )
    except Exception as error:
        await send_exception(client=client, message=message, error=error)


@app.on_message(
    filters.command(
        commands=[
            os.environ["DATA_SEARCH"],
            change_layout(os.environ["DATA_SEARCH"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def data_search(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Handles the data search functionality.

    Parameters:
    - client (Client): The Telegram client object.
    - message (Message): The message object that triggered the search.
    - callback (CallbackQuery, optional): The callback query object, if the search is performed from a callback.

    Notes:
    - The function handles both direct messages and callbacks.
    - The search function is based on an SQLite database.
    - The search can be performed on different columns of the database.
    - Pagination is used to display the search results.
    - The function requires various constants like `Dict_Map.FILES['database']`, `Text_Map`, `Buttons_Map`, and `Markup_Map`.
    """
    try:
        user_id = get_tg_info(message, callback)
        user_role = await get_info(user_id)
        user_is_me = is_me(user_id)

        # Check if the user has sufficient rights to perform the search
        if not user_is_me and not user_role or user_role == DB_Map.STUDENT:
            raise PermissionError()

        # If it's not a callback, send a message to select a column for search

        if not await check_private_chat(client, message, callback):
            return

        if not callback:
            await client.send_message(
                message.chat.id,
                Text_Map.SELECT_ITEM,
                reply_markup=Markup_Map.SELECT_COLUMN,
                reply_to_message_id=message.id,
            )
            return

        search_text = back_column = None
        page = 1

        # Handle different callback actions
        match callback.data:
            case "data_search_main":
                await callback.message.edit_text(
                    Text_Map.SELECT_ITEM, reply_markup=Markup_Map.SELECT_COLUMN
                )
                return

            case data if Text_Map.DATA_SEARCH_SEP in data:
                # Pagination callback
                callback_parts = callback.data.split(Text_Map.DATA_SEARCH_SEP)
                search_column = callback_parts[0]
                page = int(callback_parts[1])
                search_text = callback_parts[2] if len(callback_parts) == 3 else None

            case data if data == f"search_column_{DB_Map.ROLE}":
                # Special case for admin role selection
                if user_role == DB_Map.ADMIN:
                    reply_markup = Markup_Map.SELECT_COLUMN_ROLE_ADMIN
                else:
                    reply_markup = Markup_Map.SELECT_COLUMN_ROLE_NOT_ADMIN
                await callback.message.edit_text(
                    Text_Map.SELECT_ITEM, reply_markup=reply_markup
                )
                return

            case data if data == f"search_column_{DB_Map.CLASSROOM}":
                # Special case for classroom selection
                await callback.message.edit_text(
                    Text_Map.SELECT_ITEM,
                    reply_markup=Markup_Map.SELECT_COLUMN_CLASSROOM,
                )
                return

            case data if data.startswith("search_column_"):
                # Column selection callback
                search_column = callback.data.split("search_column_", 1)[1]
            case data if "db_s" in data:
                # Database search callback
                callback_parts = callback.data.split("db_s")
                search_text = callback_parts[0]
                search_column = callback_parts[1]
            case data if "db_r" in data:
                # Database result callback
                callback_parts = callback.data.split("db_r")
                search_text = callback_parts[0]
                back_column = callback_parts[1]
                search_column = DB_Map.ID

            case data if "del_r" in data:
                """
                Delete result
    
                Notes:
                - The "del_r" callback data format: "<search_text>del_r<answer>"
                - The "del_r" callback is used to delete a specific result based on the search text and answer.
                - If the answer is "?", it will prompt the user to confirm the deletion.
                - If the answer is "yes", it will delete the result from the database.
                """
                callback_parts = callback.data.split("del_r")
                search_text = callback_parts[0]
                answer = callback_parts[1]

                if answer == "?":
                    # Prompt the user to confirm the deletion
                    await callback.message.edit_text(
                        bold_text("Ви впевнені?"),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text=Text_Map.YES,
                                        callback_data=f"{search_text}del_ryes",
                                    ),
                                    InlineKeyboardButton(
                                        text=f"{TG_Emoji_Map.X} Ні",
                                        callback_data="data_search_main",
                                    ),
                                ],
                                Buttons_Map.DATA_SEARCH_MAIN,
                            ]
                        ),
                    )

                elif answer == "yes":
                    # Perform the deletion from the database
                    with connect(Dict_Map.FILES["database"]) as conn:
                        cursor = conn.cursor()

                        query = f"DELETE FROM users WHERE {DB_Map.ID} = ?"
                        cursor.execute(query, (search_text,))
                        conn.commit()

                    # Send a confirmation message to the user and update the view
                    await callback.answer(Text_Map.DATA_UPDATED)
                    await callback.message.edit_text(
                        Text_Map.SELECT_ITEM, reply_markup=Markup_Map.SELECT_COLUMN
                    )

                return

        # If search text is not provided, extract it from the replied message
        if not search_text:
            text = (
                callback.message.reply_to_message.text
                or callback.message.reply_to_message.caption
            )

            if has_emoji(text):
                raise Exception(Text_Map.NO_EMOJI)

            search_text = split_command(text.lower(), os.environ["DATA_SEARCH"])

        if search_column == DB_Map.NAME and len(search_text) > 1:
            search_text = search_text[1:]

        # Perform the search in the SQLite database
        with connect(Dict_Map.FILES["database"]) as conn:
            cursor = conn.cursor()

            if search_column == DB_Map.PHONE_NUMBER:
                query = f"SELECT * FROM users WHERE REPLACE(lower({search_column}), ' ', '') LIKE REPLACE(lower(?), ' ', '')"
            else:
                query = (
                    f"SELECT * FROM users WHERE lower({search_column}) LIKE lower(?)"
                )

            cursor.execute(
                query,
                (
                    f"%{replace_tme(search_text) if search_column == DB_Map.USERNAME else search_text}%",
                ),
            )

            fetched_rows = cursor.fetchall()

        # Convert the fetched rows into dictionaries
        matching_results = []
        for row in fetched_rows:
            row_dict = dict(
                zip([description[0] for description in cursor.description], row)
            )
            if not row_dict[DB_Map.ID] == user_id:
                if user_is_me or (
                    row_dict[DB_Map.ROLE] == DB_Map.ADMIN and user_role == DB_Map.ADMIN
                ):
                    matching_results.append(row_dict)
                elif row_dict[DB_Map.ROLE] != DB_Map.ADMIN:
                    matching_results.append(row_dict)

        # Handle no matching results
        if not matching_results:
            raise BadRequest

        # Process the search results
        if not back_column:
            back_column = search_column

        if len(matching_results) == 1:
            # Show detailed information if only one match is found
            result = matching_results[0]
            text = "\n\n".join(f"{k} <code>{v}</code>" for k, v in result.items())

            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=Text_Map.BACK,
                            callback_data=f"search_column_{back_column}",
                        )
                    ],
                    Buttons_Map.DATA_SEARCH_MAIN,
                ]
            )

            if has_number(text):
                reply_markup.inline_keyboard[0].insert(0, Buttons_Map.GET_NUMBER)

            if not bad_intentions(result[DB_Map.ROLE], user_role, user_is_me):
                reply_markup.inline_keyboard.insert(
                    1,
                    [
                        InlineKeyboardButton(
                            text=f"{TG_Emoji_Map.X} Видалити",
                            callback_data=f"{result[DB_Map.ID]}del_r?",
                        )
                    ],
                )

            await callback.message.edit_text(
                text=bold_text(text), reply_markup=reply_markup
            )
        else:
            # Paginate the search results
            start_index = (page - 1) * Any_Map.RESULTS_PER_PAGE
            end_index = start_index + Any_Map.RESULTS_PER_PAGE
            matching_persons_page = matching_results[start_index:end_index]

            reply_markup = InlineKeyboardMarkup(
                sorted(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"{row[DB_Map.NAME]} {(DB_Map.CLASSROOM + row[DB_Map.CLASSROOM] if not row[DB_Map.CLASSROOM] == '' else '') if not search_column == DB_Map.CLASSROOM else ''}",
                                callback_data=f"{row[DB_Map.ID]}db_r{back_column}",
                            )
                        ]
                        for row in matching_persons_page
                    ],
                    key=lambda x: x[0].text.lower(),
                )
            )

            pagination_buttons = []

            if back_column not in [DB_Map.ROLE, DB_Map.CLASSROOM]:
                if page > 2:
                    pagination_buttons.append(
                        InlineKeyboardButton(
                            text=TG_Emoji_Map.REWIND,
                            callback_data=f"{search_column}{Text_Map.DATA_SEARCH_SEP}1",
                        )
                    )

                if page > 1:
                    pagination_buttons.append(
                        InlineKeyboardButton(
                            text=TG_Emoji_Map.ARROW_BACKWARD,
                            callback_data=f"{search_column}{Text_Map.DATA_SEARCH_SEP}{page - 1}",
                        )
                    )

                    pagination_buttons.append(
                        InlineKeyboardButton(
                            text=str(page), callback_data=f"page_counter_{page}"
                        )
                    )

                if end_index < len(matching_results):
                    pagination_buttons.append(
                        InlineKeyboardButton(
                            text=TG_Emoji_Map.ARROW_FORWARD,
                            callback_data=f"{search_column}{Text_Map.DATA_SEARCH_SEP}{page + 1}{Text_Map.DATA_SEARCH_SEP}{search_text}",
                        )
                    )
            else:
                if page > 2:
                    pagination_buttons.append(
                        InlineKeyboardButton(
                            text=TG_Emoji_Map.REWIND,
                            callback_data=f"{search_column}{Text_Map.DATA_SEARCH_SEP}1{Text_Map.DATA_SEARCH_SEP}{search_text}",
                        )
                    )

                if page > 1:
                    pagination_buttons.append(
                        InlineKeyboardButton(
                            text=TG_Emoji_Map.ARROW_BACKWARD,
                            callback_data=f"{search_column}{Text_Map.DATA_SEARCH_SEP}{page - 1}{Text_Map.DATA_SEARCH_SEP}{search_text}",
                        )
                    )

                    pagination_buttons.append(
                        InlineKeyboardButton(
                            text=str(page), callback_data=f"page_counter_{page}"
                        )
                    )

                if end_index < len(matching_results):
                    pagination_buttons.append(
                        InlineKeyboardButton(
                            text=TG_Emoji_Map.ARROW_FORWARD,
                            callback_data=f"{search_column}{Text_Map.DATA_SEARCH_SEP}{page + 1}{Text_Map.DATA_SEARCH_SEP}{search_text}",
                        )
                    )

            reply_markup.inline_keyboard.append(pagination_buttons)
            if back_column in [DB_Map.ROLE, DB_Map.CLASSROOM]:
                reply_markup.inline_keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=Text_Map.BACK,
                            callback_data=f"search_column_{back_column}",
                        )
                    ]
                )

            reply_markup.inline_keyboard.append(Buttons_Map.DATA_SEARCH_MAIN)

            await callback.message.edit_text(
                bold_text(
                    f"Кількість збігів: {len(matching_results)}\n\n{Text_Map.SELECT_ITEM}"
                ),
                reply_markup=reply_markup,
            )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except IndexError:
        await send_exception(
            client=client,
            message=message,
            error=f"{os.environ['DATA_SEARCH']} {Dict_Map.ERRORS['IndexError']['DATA_SEARCH']}",
            callback=callback,
            index_error=True,
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            floodwait=True,
            badrequest=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error=Text_Map.NO_RESULTS,
            callback=callback,
            badrequest=True,
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["ADD_INFO"],
            change_layout(os.environ["ADD_INFO"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def add_info(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Handle adding and editing user information in the database.

    Args:
        client (Client): The Telegram client instance.
        message (Message): The message that triggered the command.
        callback (CallbackQuery, optional): The callback query (if the function is called from an inline keyboard callback). Defaults to None.

    Raises:
        Exception: Raised for various errors, such as not having enough rights or invalid input data.

    Returns:
        None
    """
    try:
        # Fetch user_id and user_username from the message or callback
        user_id, user_username = get_tg_info(message, callback, username=True)

        # Get the role of the user executing the command
        user_role = await get_info(user_id, check_agreement=True)
        user_is_me = is_me(user_id)

        # Check if the user has sufficient rights to perform the action
        if not (user_is_me or user_role):
            raise PermissionError()

        if not await check_private_chat(client, message, callback):
            return

        # Determine the appropriate reply markup based on the user's role
        if user_role == DB_Map.STUDENT:
            edit_reply_markup = Markup_Map.ADD_INFO_COLUMN_STUDENT
        else:
            edit_reply_markup = Markup_Map.ADD_INFO_COLUMN_TEACHER

        # If it's not a callback, send a message to select an action
        if not callback:
            await client.send_message(
                user_id,
                Text_Map.SELECT_ITEM,
                reply_markup=edit_reply_markup,
                reply_to_message_id=message.id,
            )
            return

        text = (
            callback.message.reply_to_message.text
            or callback.message.reply_to_message.caption
        )
        text = text.lower()

        # Check if the message contains any emojis (which should not be present)
        if has_emoji(text):
            raise Exception(Text_Map.NO_EMOJI)

        command = os.environ["ADD_INFO"]

        # Handle different callback actions
        if callback.data == "add_info_main":
            await callback.message.edit_text(
                Text_Map.SELECT_ITEM, reply_markup=edit_reply_markup
            )
            return

        elif callback.data in [
            f"add_role_{DB_Map.ADMIN}",
            f"add_role_{DB_Map.STAFF}",
            f"add_role_{DB_Map.TEACHER}",
            f"add_role_{DB_Map.STUDENT}",
        ]:
            # Handle adding a new role to a user
            id, *name = split_command(text, command).split(" ", maxsplit=1)

            username = ""
            if not is_user_id(id):
                username = replace_tme(id)
                id = await username2id(username)

            role = callback.data[len("add_role_") :]

            t_user_role = await get_info(id)
            if t_user_role and t_user_role == str(role):
                raise Exception(Text_Map.IT_IS_IN_BASE.format(DB_Map.ROLE))

            if bad_intentions(t_user_role, user_role, user_is_me):
                raise PermissionError()

            time = datetime.today().strftime("%d.%m.%Y %H:%M:%S")

            with connect(Dict_Map.FILES["database"]) as conn:
                cursor = conn.cursor()

                query = f"SELECT * FROM users WHERE {DB_Map.ID} = ?"
                cursor.execute(query, (id,))
                result = cursor.fetchone()

                if result:
                    # User already exists, update the information
                    update_query = f"UPDATE users SET {DB_Map.ROLE} = ?, {DB_Map.ADDER_ID} = ?, {DB_Map.DATE} = ? WHERE {DB_Map.ID} = ?"
                    cursor.execute(update_query, (role, user_id, time, id))
                else:
                    # User doesn't exist, insert a new row
                    insert_query = f"INSERT INTO users ({DB_Map.NAME}, {DB_Map.ID}, {DB_Map.ROLE}, {DB_Map.USERNAME}, {DB_Map.ADDER_ID}, {DB_Map.DATE}) VALUES (?, ?, ?, ?, ?, ?)"
                    cursor.execute(
                        insert_query,
                        (" ".join(name).title(), id, role, username, user_id, time),
                    )

                conn.commit()

            await callback.message.edit_text(
                Text_Map.SELECT_ITEM, reply_markup=edit_reply_markup
            )
            await callback.answer(Text_Map.DATA_UPDATED)

        elif callback.data.startswith("add_classroom_"):
            # Handle adding a new classroom to a user
            try:
                id, *rubbish = split_command(text, command).split(" ", maxsplit=1)
            except IndexError:
                await send_exception(
                    client=client,
                    message=message,
                    error=f"{os.environ['ADD_INFO']} {Dict_Map.ERRORS['IndexError']['ADD_INFO']['id']}",
                    callback=callback,
                    index_error=True,
                )
                return

            if not is_user_id(id):
                id = await username2id(id)

            t_user_role = await get_info(id)

            if bad_intentions(t_user_role, user_role, user_is_me):
                raise PermissionError()

            classroom = callback.data[len("add_classroom_") :]

            with connect(Dict_Map.FILES["database"]) as conn:
                cursor = conn.cursor()

                query = f"SELECT * FROM users WHERE {DB_Map.ID} = ?"
                cursor.execute(query, (id,))
                result = cursor.fetchone()

                if result:
                    if result[3] == classroom:
                        raise Exception(Text_Map.IT_IS_IN_BASE.format(DB_Map.CLASSROOM))

                    update_query = (
                        f"UPDATE users SET {DB_Map.CLASSROOM} = ? WHERE {DB_Map.ID} = ?"
                    )
                    cursor.execute(update_query, (classroom, id))
                    conn.commit()
                else:
                    raise Exception(Text_Map.IT_IS_IN_BASE.format("користувач"))

            await callback.message.edit_text(
                Text_Map.SELECT_ITEM, reply_markup=edit_reply_markup
            )
            await callback.answer(Text_Map.DATA_UPDATED)

        elif callback.data.startswith("edit_column_"):
            # Handle editing a specific column ({DB_Map.NAME}, {DB_Map.MAIL_ADDRESS}, {DB_Map.PHONE_NUMBER}, {DB_Map.USERNAME}, {DB_Map.ROLE})
            if callback.data.endswith(DB_Map.MAIL_ADDRESS):
                try:
                    add_text = split_command(text, command)

                    if not bool(
                        re.fullmatch(
                            r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                            add_text,
                        )
                    ):
                        raise IndexError

                except IndexError:
                    await send_exception(
                        client=client,
                        message=message,
                        error=f"{os.environ['ADD_INFO']} {Dict_Map.ERRORS['IndexError']['ADD_INFO'][DB_Map.MAIL_ADDRESS]}",
                        callback=callback,
                        index_error=True,
                    )
                    return

                if await get_info(user_id, DB_Map.MAIL_ADDRESS) == add_text:
                    raise Exception(Text_Map.IT_IS_IN_BASE.format(DB_Map.MAIL_ADDRESS))

                with connect(Dict_Map.FILES["database"]) as conn:
                    cursor = conn.cursor()

                    query = f"SELECT * FROM users WHERE {DB_Map.ID} = ?"
                    cursor.execute(query, (user_id,))
                    result = cursor.fetchone()

                    if result:
                        update_query = f"UPDATE users SET {DB_Map.MAIL_ADDRESS} = ? WHERE {DB_Map.ID} = ?"
                        cursor.execute(update_query, (add_text, user_id))
                        conn.commit()
                    else:
                        raise Exception(Text_Map.IT_IS_IN_BASE.format("користувач"))

                await callback.answer(Text_Map.DATA_UPDATED)

            elif callback.data.endswith(DB_Map.NAME):
                try:
                    id, *name = split_command(text, command).split(" ", maxsplit=1)
                    name = name[0].title()

                    if not is_user_id(id):
                        id = await username2id(id)

                    if bad_intentions(await get_info(id), user_role, user_is_me):
                        raise PermissionError()

                    if await get_info(id, DB_Map.NAME) == name:
                        raise Exception(Text_Map.IT_IS_IN_BASE.format(DB_Map.NAME))

                    with connect(Dict_Map.FILES["database"]) as conn:
                        cursor = conn.cursor()

                        query = f"SELECT * FROM users WHERE {DB_Map.ID} = ?"
                        cursor.execute(query, (id,))
                        result = cursor.fetchone()

                        if result:
                            update_query = f"UPDATE users SET {DB_Map.NAME} = ? WHERE {DB_Map.ID} = ?"
                            cursor.execute(update_query, (name, id))
                            conn.commit()
                        else:
                            raise Exception(Text_Map.IT_IS_IN_BASE.format("користувач"))

                    await callback.answer(Text_Map.DATA_UPDATED)

                except IndexError:
                    await send_exception(
                        client=client,
                        message=message,
                        error=f"{os.environ['ADD_INFO']} {Dict_Map.ERRORS['IndexError']['ADD_INFO'][DB_Map.NAME]}",
                        callback=callback,
                        index_error=True,
                    )
                    return

            elif callback.data.endswith(DB_Map.PHONE_NUMBER):
                # Request contact number from the user
                if clean_html_tags(Text_Map.SELECT_ITEM) not in callback.message.text:
                    await callback.message.edit_text(
                        Text_Map.SELECT_ITEM, reply_markup=edit_reply_markup
                    )

                await client.send_message(
                    message.chat.id,
                    bold_text(Text_Map.CLICK_ON_THE_BUTTON),
                    reply_markup=Markup_Map.REQUEST_CONTACT,
                )
                await callback.answer(Text_Map.CLICK_ON_THE_BUTTON)

            elif callback.data.endswith(DB_Map.USERNAME):
                # Handle adding a username (@username) to a user
                if not user_username:
                    raise Exception(f"У вас немає username ({DB_Map.USERNAME})")

                if await get_info(user_id, DB_Map.USERNAME) == user_username:
                    raise Exception(Text_Map.IT_IS_IN_BASE.format(DB_Map.USERNAME))

                with connect(Dict_Map.FILES["database"]) as conn:
                    cursor = conn.cursor()

                    query = f"SELECT * FROM users WHERE {DB_Map.ID} = ?"
                    cursor.execute(query, (user_id,))
                    result = cursor.fetchone()

                    if result:
                        update_query = f"UPDATE users SET {DB_Map.USERNAME} = ? WHERE {DB_Map.ID} = ?"
                        cursor.execute(update_query, (user_username, user_id))
                        conn.commit()
                    else:
                        raise Exception(Text_Map.IT_IS_IN_BASE.format("користувач"))

                await callback.answer(Text_Map.DATA_UPDATED)

            elif callback.data.endswith(DB_Map.ROLE):
                # Handle changing user role
                if user_role == DB_Map.ADMIN or is_me(user_id):
                    reply_markup = Markup_Map.ADD_ROLE_ADMIN
                elif user_role == DB_Map.STAFF:
                    reply_markup = Markup_Map.ADD_ROLE_STAFF
                elif user_role == DB_Map.TEACHER:
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [Buttons_Map.ADD_ROLE_STUDENT],
                            Buttons_Map.ADD_INFO_MAIN,
                        ]
                    )
                else:
                    raise PermissionError()

                id, *name = split_command(text, command).split(" ", maxsplit=1)

                if not is_user_id(id):
                    await username2id(id)

                await callback.message.edit_text(
                    Text_Map.SELECT_ITEM, reply_markup=reply_markup
                )

            elif callback.data.endswith(DB_Map.CLASSROOM):
                # Handle selecting a classroom for a user
                try:
                    id, *rubbish = split_command(text, command).split(" ", maxsplit=1)

                except IndexError:
                    await send_exception(
                        client=client,
                        message=message,
                        error=f"{os.environ['ADD_INFO']} {Dict_Map.ERRORS['IndexError']['ADD_INFO']['id']}",
                        callback=callback,
                        index_error=True,
                    )
                    return

                if not is_user_id(id):
                    id = await username2id(id)

                if not await get_info(id):
                    raise Exception(Text_Map.IT_IS_IN_BASE.format("користувач"))

                await callback.message.edit_text(
                    Text_Map.SELECT_ITEM, reply_markup=Markup_Map.CLASSROOMS
                )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except (IndexError, AttributeError):
        await send_exception(
            client=client,
            message=message,
            error=f"{os.environ['ADD_INFO']} {Dict_Map.ERRORS['IndexError']['ADD_INFO']['id_and_text']}",
            callback=callback,
            index_error=True,
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            floodwait=True,
            badrequest=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error=Text_Map.NO_RESULTS,
            callback=callback,
            badrequest=True,
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(filters.contact & filters.private)
async def edit_column_number(client: Client, message: Message):
    """
    Edits a column number in a CSV file based on user input.

    Parameters:
        client (Client): An instance of the Client class representing the Telegram client.
        message (Message): The Telegram message object that triggered the function.

    Raises:
        Exception: If the user is not authorized or if an error occurs during execution.
    """
    try:
        from icecream import ic

        ic(message)
        # Retrieve user_id using the get_tg_info function
        user_id = get_tg_info(message)

        # Retrieve user_role using the get_info function
        user_role = await get_info(user_id)

        # Check if the user is authorized (me) or has a valid user_role
        if is_me(user_id) or user_role:
            # Check if the contact message is from the same user
            if message.contact.user_id and str(message.contact.user_id) == str(user_id):
                # Delete the original message that triggered the function
                await message.delete()

                # Check if the message is a reply to another message and delete the replied message
                if message.reply_to_message:
                    await client.delete_messages(
                        message.chat.id, message_ids=message.reply_to_message.id
                    )

                # Format the phone number provided in the contact message
                formatted_number = format_phone_number(
                    message.contact.phone_number
                    if message.contact.phone_number.startswith("+")
                    else "+" + message.contact.phone_number
                )
                old_number = await get_info(user_id, DB_Map.PHONE_NUMBER)

                # Check if the user already has a stored phone number and if the formatted number matches the existing one
                if old_number and old_number == formatted_number:
                    raise Exception(Text_Map.IT_IS_IN_BASE.format(DB_Map.PHONE_NUMBER))

                # Open the CSV file in read mode and create a CSV reader object
                with connect(Dict_Map.FILES["database"]) as conn:
                    cursor = conn.cursor()

                    query = f"SELECT * FROM users WHERE {DB_Map.ID} = ?"
                    cursor.execute(query, (user_id,))
                    result = cursor.fetchone()

                    if result:
                        update_query = f"UPDATE users SET {DB_Map.PHONE_NUMBER} = ? WHERE {DB_Map.ID} = ?"
                        cursor.execute(update_query, (formatted_number, user_id))
                        conn.commit()
                    else:
                        raise Exception(Text_Map.IT_IS_IN_BASE.format("користувач"))

                # Send a success message to the chat indicating that the data has been updated
                await client.send_message(
                    message.chat.id,
                    bold_text(Text_Map.DATA_UPDATED),
                    reply_markup=Markup_Map.DELETE,
                )

    except Exception as error:
        await send_exception(client=client, message=message, error=error)


@app.on_message(
    filters.command(
        commands=[os.environ["ME"], change_layout(os.environ["ME"])],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def me(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Retrieves user information from an SQLite database and sends it as a message.

    Parameters:
        client (Client): An instance of the Client class representing the Telegram client.
        message (Message): The Telegram message object that triggered the function.
        callback (CallbackQuery, optional): The callback query object, if the function was triggered by a callback. Defaults to None.

    Raises:
        BadRequest: If there is a bad request in handling the callback.
        Exception: If an error occurs during execution.
    """
    try:
        # Retrieve user_id using the get_tg_info function
        user_id = get_tg_info(message, callback)

        # Check user permissions
        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        # Connect to the SQLite database
        with connect(Dict_Map.FILES["database"]) as conn:
            cursor = conn.cursor()

            # Retrieve matching results from the users table based on user_id
            query = f"SELECT * FROM users WHERE {DB_Map.ID} = ?"
            cursor.execute(query, (user_id,))
            matching_results = cursor.fetchall()

        # If no matching results were found, raise an exception
        if not matching_results:
            raise Exception(Text_Map.IT_IS_IN_BASE.format("Вас"))

        # Get the column names from the cursor description
        column_names = [description[0] for description in cursor.description]

        # Format the user information into a text message
        text = bold_text(
            "\n\n".join(
                f"{k} <code>{v}</code>"
                for k, v in zip(column_names, matching_results[0])
            )
        )

        # Prepare the reply markup for the message
        reply_markup = Markup_Map.ME_NUMBER if has_number(text) else Markup_Map.ME

        # Check if the function was triggered by a callback query or a regular message
        if callback:
            # Edit the existing message with the updated user information
            await callback.message.edit_text(
                text=text, reply_markup=reply_markup, disable_web_page_preview=True
            )
        else:
            # Send a new message with the user information
            await client.send_message(
                message.chat.id,
                text=text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                reply_to_message_id=message.id,
            )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except BadRequest:
        await send_exception(
            client=client, message=message, callback=callback, badrequest=True
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["HELP"],
            change_layout(os.environ["HELP"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def help(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Provides help information to the user.

    Parameters:
        client (Client): An instance of the Client class representing the Telegram client.
        message (Message): The Telegram message object that triggered the function.
        callback (CallbackQuery, optional): The callback query object, if the function was triggered by a callback. Defaults to None.

    Raises:
        Exception: If the user doesn't have sufficient rights or if an error occurs during execution.
        FloodWait: If there is a flood wait time imposed by Telegram.
        BadRequest: If there is a bad request, such as a reversed point.
    """
    try:
        # Retrieve user_id using the get_tg_info function
        user_id = get_tg_info(message, callback)

        # Check if the user is authorized (me) or has a valid user_id
        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        if callback:
            # Extract the symbol from the callback data
            symbol = callback.data[-1]
            # Generate the help text for the symbol
            symbol_text = Dict_Map.SYMBOLS_HELP.get(symbol)
            if symbol_text:
                text = bold_text(f"{symbol} {symbol_text}\n\n{Text_Map.SELECT_ITEM}")
                # Edit the existing message with the updated help text
                await callback.message.edit_text(
                    text=text,
                    reply_markup=callback.message.reply_markup,
                    disable_web_page_preview=True,
                )
            else:
                await callback.answer(text=Text_Map.NO_RESULTS)

        else:
            # Send a new message with the general help text and available options
            await client.send_message(
                message.chat.id,
                bold_text(
                    f"{TG_Emoji_Map.QUESTION} {Dict_Map.SYMBOLS_HELP[Text_Map.HELP_TEXT]}\n\n{Text_Map.SELECT_ITEM}"
                ),
                reply_to_message_id=message.id,
                reply_markup=InlineKeyboardMarkup(
                    Buttons_Map.SYMBOLS_HELP + [[Buttons_Map.DELETE_FULL]]
                ),
                disable_web_page_preview=True,
            )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            floodwait=True,
            badrequest=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error=Text_Map.REVERSED_POINT,
            callback=callback,
            badrequest=True,
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["SEND"],
            change_layout(os.environ["SEND"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def send(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Send messages to users based on various criteria.

    Parameters:
        - client (Client): The Telegram client object.
        - message (Message): The message object representing the command or initial message.
        - callback (CallbackQuery): The callback query object if the function is triggered by a callback.

    Raises:
        - Exception: If there is an error during the execution.

    Note:
        - The function retrieves user information using the `get_tg_info` function.
        - The function checks user privileges and determines the appropriate reply markup.
        - The function performs searches in the users database based on the specified criteria.
        - The function supports pagination for displaying multiple matching results.
        - The function allows sending messages to individual users or all users matching the search criteria.
    """
    try:
        # Get user information
        user_id = get_tg_info(message, callback)
        user_role, user_classroom = await get_info(
            user_id, (DB_Map.ROLE, DB_Map.CLASSROOM)
        )
        user_is_me = is_me(user_id)

        # Check user privileges
        if not (user_is_me or user_role):
            raise PermissionError()

        if not callback:
            text = message.caption or message.text
            text = text.html if text else ""
            command = message.command[0]

            try:
                bold_text(split_command(text, command))

            except IndexError:
                if not has_file(message):
                    raise IndexError

            await client.send_message(
                message.chat.id,
                Text_Map.SELECT_ITEM,
                reply_markup=Markup_Map.SEND_COLUMN_ROLE,
                reply_to_message_id=message.id,
            )
            return

        search_text = None
        page = 1

        if callback.data == f"send_column_{DB_Map.ROLE}":
            # Edit message to show the main menu
            await callback.message.edit_text(
                Text_Map.SELECT_ITEM, reply_markup=Markup_Map.SEND_COLUMN_ROLE
            )
            return
        elif f"_{TG_Emoji_Map.PAGE_FACING_UP}_" in callback.data:
            callback_parts = callback.data.split(f"_{TG_Emoji_Map.PAGE_FACING_UP}_")
            search_column = callback_parts[0]
            page = int(callback_parts[1])
            search_text = callback_parts[2]
        elif callback.data == f"send_column_{DB_Map.CLASSROOM}":
            if not user_classroom or user_role != DB_Map.STUDENT:
                await callback.message.edit_text(
                    Text_Map.SELECT_ITEM, reply_markup=Markup_Map.SEND_COLUMN_CLASSROOM
                )
                return
            search_text = user_classroom
            search_column = DB_Map.CLASSROOM
        elif "se_s" in callback.data:
            # se_s - DataBase search
            callback_parts = callback.data.split("se_s")
            search_text = callback_parts[0]
            search_column = callback_parts[1]

        # Connect to the SQLite database
        with connect(Dict_Map.FILES["database"]) as conn:
            cursor = conn.cursor()

            # Perform the search in the users database
            query = f"SELECT * FROM users WHERE lower({search_column}) LIKE lower(?)"
            cursor.execute(query, (f"%{search_text}%",))

            fetched_rows = cursor.fetchall()

            # Convert the fetched rows into dictionaries
            rows = []
            for row in fetched_rows:
                row_dict = dict(
                    zip([description[0] for description in cursor.description], row)
                )
                rows.append(row_dict)

        matching_results = []
        for row in rows:
            if not row[DB_Map.ID] == user_id:
                if (
                    search_column == DB_Map.CLASSROOM
                    and not row[DB_Map.ROLE] == DB_Map.STUDENT
                ):
                    continue
                if row[DB_Map.ROLE] == DB_Map.ADMIN and user_role == DB_Map.ADMIN:
                    matching_results.append(row)
                elif row[DB_Map.ROLE] != DB_Map.ADMIN:
                    matching_results.append(row)

        if not matching_results:
            raise BadRequest

        if len(matching_results) == 1 or page == -1:
            # Handle single result or sending to all
            reply_message = callback.message.reply_to_message

            file = has_file(reply_message)

            text = reply_message.caption or reply_message.text
            text = text.html if text else ""
            command = os.environ["SEND"]

            try:
                send_text = bold_text(split_command(text, command))

            except IndexError:
                if not file:
                    raise IndexError

                send_text = ""

            if not bad_intentions(
                user_role,
                str(matching_results[0][DB_Map.ROLE]),
                is_me(matching_results[0][DB_Map.ROLE]),
            ):
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"{TG_Emoji_Map.QUESTION} Хто це",
                                callback_data=f"who_is_this{user_id}",
                            ),
                            Buttons_Map.DELETE,
                        ]
                    ]
                )
            else:
                reply_markup = Markup_Map.DELETE_FULL

            text = bold_text(
                f"Вам надійшло повідомлення від {await get_info(user_id, DB_Map.NAME)} {DB_Map.CLASSROOM + user_classroom if not user_classroom == '' else ''}\n\n{send_text}"
            )

            bad_results = []
            good_results = []

            for result in matching_results:
                t_id = result[DB_Map.ID]
                t_info = f"{result[DB_Map.NAME]}{DB_Map.CLASSROOM + result[DB_Map.CLASSROOM] if not str(result[DB_Map.CLASSROOM]) == '' else ''}"
                try:
                    if not file:
                        await client.send_message(
                            chat_id=t_id,
                            reply_markup=reply_markup,
                            disable_web_page_preview=True,
                            text=text,
                        )
                    else:
                        forwarded_msg = await forwards_cover(
                            client=client,
                            msg_to_forward=reply_message,
                            file=file,
                            t_id=t_id,
                            reply_markup=reply_markup,
                            send_text=send_text
                            if reply_message.media_group_id
                            else text,
                        )

                        if reply_message.media_group_id:
                            await client.send_message(
                                chat_id=t_id,
                                reply_markup=reply_markup,
                                text=bold_text(text.split("\n\n")[0]),
                                reply_to_message_id=forwarded_msg[0].id,
                            )
                    good_results.append(t_info)

                except BadRequest:
                    bad_results.append(t_info)
                    continue

            await callback.message.edit_text(
                text=bold_text(
                    (
                        (
                            f"{Text_Map.WAIT_FOR_RESPONSE} від "
                            + ", ".join(f"{k}" for k in good_results)
                        )
                        if good_results
                        else ""
                    )
                    + ("\n" if good_results and bad_results else "")
                    + (
                        (
                            f"\n{Text_Map.SENDING_FAILED} до "
                            + ", ".join(f"{k}" for k in bad_results)
                        )
                        if bad_results
                        else ""
                    )
                    + f"\n\nВи можете відправити повідомлення ще комусь, для цього натисніть на кнопку {Text_Map.MAIN}"
                ),
                reply_markup=InlineKeyboardMarkup([Buttons_Map.SEND_MAIN]),
            )

        else:
            # Handle pagination and multiple results
            start_index = (page - 1) * Any_Map.RESULTS_PER_PAGE
            end_index = start_index + Any_Map.RESULTS_PER_PAGE
            matching_persons_page = matching_results[start_index:end_index]

            reply_markup = InlineKeyboardMarkup(
                sorted(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"{row[DB_Map.NAME]} {DB_Map.CLASSROOM + row[DB_Map.CLASSROOM] if not row[DB_Map.CLASSROOM] == '' else ''}",
                                callback_data=f"{row[DB_Map.ID]}se_s{DB_Map.ID}",
                            )
                        ]
                        for row in matching_persons_page
                    ],
                    key=lambda x: x[0].text.lower(),
                )
            )

            pagination_buttons = []

            if page > 2:
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=TG_Emoji_Map.REWIND,
                        callback_data=f"{search_column}_{TG_Emoji_Map.PAGE_FACING_UP}_1_{TG_Emoji_Map.PAGE_FACING_UP}_{search_text}",
                    )
                )

            if page > 1:
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=TG_Emoji_Map.ARROW_BACKWARD,
                        callback_data=f"{search_column}_{TG_Emoji_Map.PAGE_FACING_UP}_{page - 1}_{TG_Emoji_Map.PAGE_FACING_UP}_{search_text}",
                    )
                )

                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=str(page), callback_data=f"page_counter_{page}"
                    )
                )

            if end_index < len(matching_results):
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text=TG_Emoji_Map.ARROW_FORWARD,
                        callback_data=f"{search_column}_{TG_Emoji_Map.PAGE_FACING_UP}_{page + 1}_{TG_Emoji_Map.PAGE_FACING_UP}_{search_text}",
                    )
                )

            reply_markup.inline_keyboard.append(pagination_buttons)

            if not bad_intentions(search_text, user_role, user_is_me):
                reply_markup.inline_keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=f"{TG_Emoji_Map.BUSTS_IN_SILHOUETTE} Надіслати всім",
                            callback_data=f"{search_column}_{TG_Emoji_Map.PAGE_FACING_UP}_-1_{TG_Emoji_Map.PAGE_FACING_UP}_{search_text}",
                        )
                    ]
                )

            reply_markup.inline_keyboard.append(Buttons_Map.SEND_MAIN)

            await callback.message.edit_text(
                bold_text(
                    f"Кількість збігів: {len(matching_results)}\n\n{Text_Map.SELECT_ITEM}"
                ),
                reply_markup=reply_markup,
            )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except IndexError:
        await send_exception(
            client=client,
            message=message,
            error=f"{os.environ['SEND']} {Dict_Map.ERRORS['IndexError']['SEND']}",
            callback=callback,
            index_error=True,
        )
    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error=f"{Text_Map.SENDING_FAILED} {TG_Emoji_Map.CONFUSED}",
            callback=callback,
            badrequest=True,
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["NOW_IS"],
            change_layout(os.environ["NOW_IS"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def now_is(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Retrieves and sends the current date, time, and day of the week along with the user's current lesson information (if available).

    Parameters:
        client (Client): An instance of the Client class representing the Telegram client.
        message (Message): The Telegram message object that triggered the function.
        callback (CallbackQuery, optional): The Telegram callback query object, if the function is triggered from a callback. Default is None.

    Raises:
        FloodWait: If there is a flood wait time imposed by the Telegram API.
        BadRequest: If there is a bad request error while sending the message.
        Exception: If an error occurs during execution.

    Note:
        - The function retrieves the current date, time, and day of the week and displays it in a formatted text message.
        - If the user has provided a classroom ('user_classroom' is not default), the function also attempts to determine the user's current lesson information.
        - The function checks if it is a weekday (Monday to Friday) and the current time is between 9:00 and 14:30. If so, it tries to determine the current lesson based on the provided lesson times.
        - If it is a lesson time, the function displays the lesson number, time range, and the subject. If it is a recess, the recess time is displayed.
        - If the user's current lesson information is not available, the function displays a default message.
        - If the function is triggered from a callback query, the message is edited with the updated information. Otherwise, a new message is sent.
    """
    try:
        user_id = get_tg_info(message, callback)
        user_is_me = is_me(user_id)
        user_role, user_classroom = await get_info(
            user_id, (DB_Map.ROLE, DB_Map.CLASSROOM)
        )

        if not (user_is_me or user_role):
            raise PermissionError()

        # Get the current date and time
        today = datetime.today()

        reply_markup: InlineKeyboardMarkup = Markup_Map.NOW_IS
        # Define the current date, time, and day of the week
        now_is = {
            TG_Emoji_Map.CALENDAR_SPIRAL: f"{today.strftime('%d.%m.%Y')}",
            TG_Emoji_Map.ALARM_CLOCK: f"{today.strftime('%H:%M:')}{(int(today.strftime('%S')) // 10) * 10:02d}",
            TG_Emoji_Map.DATE: f"{Dict_Map.DAYS_OF_WEEK_MAP.get(today.strftime('%A'))}",
        }

        text = "\n\n".join(f"{k} <code>{v}</code>" for k, v in now_is.items())
        current_time = today.time()

        if len(reply_markup.inline_keyboard) == 3:
            reply_markup.inline_keyboard.pop(0)

        if user_classroom:
            lesson_num = Text_Map.CHILL
            # Check if it is a weekday (Monday to Friday) and the current time is between 9:00 and 14:30, excluding holidays
            if is_school_day(today, today.year) and is_school_time(current_time):
                if Buttons_Map.GET_TIMETABLE not in reply_markup.inline_keyboard[-2]:
                    reply_markup.inline_keyboard[-2].insert(
                        0, Buttons_Map.GET_TIMETABLE
                    )

                # Assign lesson time based on the current time
                lesson_time = ""

                # Iterate over the lesson times and find the current lesson number and time
                for num, (start_time, end_time) in Dict_Map.LESSON_TIMES.items():
                    if start_time <= current_time <= end_time:
                        lesson_num = num
                        lesson_time = format_lesson_time(start_time, end_time)
                        break

                if lesson_num == Text_Map.CHILL:
                    # If the current time is during the recess, update the text and find the next lesson time
                    text += f"\n\n{Text_Map.RECESS}"
                    for num, (start_time, end_time) in Dict_Map.LESSON_TIMES.items():
                        if start_time > current_time:
                            lesson_num = num
                            lesson_time = format_lesson_time(start_time, end_time)
                            text += recess_time(start_time, current_time, today.date())
                            break

                if not lesson_num == Text_Map.CHILL:
                    # If it is a lesson time, retrieve the lesson information based on the user's classroom and current day
                    lesson = (
                        Dict_Map.TIMETABLE_MAP.get(user_classroom, {})
                        .get(now_is[TG_Emoji_Map.DATE], {})
                        .get(lesson_num, Text_Map.RECESS)
                    )

                    if not lesson == Text_Map.RECESS:
                        book_info = Dict_Map.CLASS_BOOKS.get(user_classroom, {}).get(
                            lesson, ""
                        )

                        # Check if a book_info was found
                        if book_info:
                            if isinstance(book_info, list):
                                # If the link info is a list
                                link = find_link_in_list(book_info)
                            elif isinstance(book_info, tuple):
                                # If the link info is a tuple
                                link = find_link_in_list(book_info[0])
                        else:
                            link = f"https://www.google.com/search?q={quote(f'{lesson} {user_classroom} клас')}"

                        # If it is not a recess, add the lesson information to the text
                        text += f"\n\n{num_to_emoji(lesson_num)}) {lesson_time}{recess_time(end_time, current_time, today.date())}\n\n<a href='{link}'>{lesson}</a>\n\n"
                        lesson_info = Dict_Map.SUBJECTS.get(lesson)

                        def add_lesson_link(name: str) -> str:
                            """
                            Retrieves the lesson link from the Dict_Map dictionary based on the given name.

                            Args:
                                name (str): The name of the lesson.

                            Returns:
                                str: An HTML link with the retrieved link and the name.
                            """

                            # Retrieve the lesson link from the Dict_Map dictionary
                            link_info = Dict_Map.LESSON_LINKS.get(
                                user_classroom, {}
                            ).get(lesson, "")

                            # Check if a link was found
                            if link_info:
                                if isinstance(link_info, list):
                                    # If the link info is a list, find the link in the list if the name is present
                                    link = (
                                        find_link_in_list(link_info)
                                        if name in link_info
                                        else ""
                                    )
                                elif isinstance(link_info, tuple):
                                    # If the link info is a tuple, find the link in the tuple if the name is present
                                    info_list: list | None = next(
                                        (lst for lst in link_info if name in lst), None
                                    )
                                    link = (
                                        find_link_in_list(info_list)
                                        if info_list
                                        else ""
                                    )
                            else:
                                link = ""

                            # Create an HTML link with the retrieved link and the name
                            return f"<a href='{link}'>{TG_Emoji_Map.BUST_IN_SILHOUETTE} {name}</a>"

                        if isinstance(lesson_info, list):
                            text += "\n\n".join(
                                add_lesson_link(
                                    person.get(TG_Emoji_Map.BUST_IN_SILHOUETTE)
                                )
                                for person in lesson_info
                            )
                        elif isinstance(lesson_info, dict):
                            text += add_lesson_link(
                                lesson_info.get(TG_Emoji_Map.BUST_IN_SILHOUETTE)
                            )
                    else:
                        # If it is a recess, add the recess information to the text
                        text += f"\n\n{num_to_emoji(lesson_num)}) {lesson} {lesson_time}{recess_time(end_time, current_time, today.date())}"
                else:
                    # If it is not a lesson time or recess, update the text with the default value
                    text += f"\n\n{lesson_num}"
            else:
                if is_school_day(tomorrow_day(today), today.year):
                    if (
                        Buttons_Map.GET_TIMETABLE
                        not in reply_markup.inline_keyboard[-2]
                    ):
                        reply_markup.inline_keyboard[-2].insert(
                            0, Buttons_Map.GET_TIMETABLE
                        )

                # If it is not a weekday or the current time is outside the lesson time range, update the text with the default value
                text += f"\n\n{lesson_num}"

        # Make the text bold
        text = bold_text(text)

        if is_school_time(current_time) and (
            user_is_me or user_role in [DB_Map.ADMIN, DB_Map.STAFF]
        ):
            # Define the school_day_list and add appropriate buttons to the reply markup
            school_day_list: list = Buttons_Map.SCHOOL_DAY.copy()

            if school_day == "default":
                school_day_list.pop(2)
            elif school_day:
                school_day_list.pop(1)
            elif not school_day:
                school_day_list.pop(0)

            if school_day_list not in reply_markup.inline_keyboard:
                reply_markup.inline_keyboard.insert(0, school_day_list)

        if callback:
            # Edit the message with the current date, time, and day of the week
            await callback.message.edit_text(
                text=text, reply_markup=reply_markup, disable_web_page_preview=True
            )
        else:
            # Send a new message with the current date, time, and day of the week
            await client.send_message(
                message.chat.id,
                text=text,
                reply_markup=reply_markup,
                reply_to_message_id=message.id,
                disable_web_page_preview=True,
            )

        if Buttons_Map.GET_TIMETABLE in reply_markup.inline_keyboard[-2]:
            reply_markup.inline_keyboard[-2].pop(0)

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            floodwait=True,
            badrequest=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client, message=message, callback=callback, badrequest=True
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["WIKI"],
            change_layout(os.environ["WIKI"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def wiki(client: Client, message: Message):
    """
    Search for a summary of a given topic on Wikipedia and send it as a message.

    Args:
        client (Client): The Telethon client instance.
        message (Message): The message that triggered the search.

    Raises:
        PermissionError: If the user does not have the permission to access the search feature.
        IndexError: If an IndexError occurs during the search.
    """
    try:
        # Get the user ID from the message
        user_id = get_tg_info(message)

        # Check if the user is the bot owner or has permission to access the search feature
        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        # Get the command (e.g., "/wiki") from the message
        command = message.command[0]

        # Extract the text after the command to use as the search query
        text = message.text or message.caption
        text = text.lower()
        # Remove the command and any mention of the bot's username from the search query
        text = bold_text(wikipedia.summary(split_command(text, command), 7))

        # Send a message with the retrieved summary
        await client.send_message(
            message.chat.id,
            text=text,
            reply_markup=Markup_Map.DELETE_FULL,
            reply_to_message_id=message.id,
            disable_web_page_preview=True,
        )

    except PermissionError:
        await send_exception(client=client, message=message, permissionerror=True)
    except (IndexError, AttributeError):
        await send_exception(
            client=client,
            message=message,
            error=f"{os.environ['WIKI']} {Dict_Map.ERRORS['IndexError']['WIKI']}",
            index_error=True,
        )
    except Exception as error:
        if "does not match any pages." in str(error):
            error = Text_Map.NO_RESULTS
        await send_exception(
            client=client,
            message=message,
            error=str(error).replace("may refer to", "може відноситися до", 1),
        )


async def who_is_this(client: Client, message: Message, callback: CallbackQuery):
    """
    Retrieves and sends information about a user based on their ID.

    Parameters:
        client (Client): An instance of the Client class representing the Telegram client.
        message (Message): The Telegram message object that triggered the function.
        callback (CallbackQuery): The Telegram callback query object.

    Raises:
        FloodWait: If there is a flood wait time imposed by the Telegram API.
        BadRequest: If there is a bad request error while sending the message.
        Exception: If an error occurs during execution.
    """
    try:
        # Get the user ID from the callback query
        user_id = get_tg_info(message, callback)

        # Check user role and permissions
        user_role = await get_info(user_id)

        # If the user is not the bot itself and is not an admin or student, raise a BadRequest
        if not is_me(user_id) and not user_role or user_role == DB_Map.STUDENT:
            raise BadRequest

        with connect(Dict_Map.FILES["database"]) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM users WHERE {DB_Map.ID} = ?"
            cursor.execute(query, (callback.data[len("who_is_this") :],))

            # Get the row dictionary from the database query result
            row_dict = dict(
                zip(
                    [description[0] for description in cursor.description],
                    cursor.fetchone(),
                )
            )

            matching_results = []
            # If the user is the bot owner or an admin, show all matching results
            if is_me(user_id) or (
                user_role == DB_Map.ADMIN and row_dict[DB_Map.ROLE] == DB_Map.ADMIN
            ):
                matching_results.append(row_dict)
            # If the user is not an admin, only show non-admin results
            elif row_dict[DB_Map.ROLE] != DB_Map.ADMIN:
                matching_results.append(row_dict)

        # If no matching results found, raise a BadRequest
        if not matching_results:
            raise BadRequest

        # Answer the callback with the user information in an alert
        await callback.answer(
            text="\n\n".join(f"{k} {v}" for k, v in matching_results[0].items()),
            show_alert=True,
        )

    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            floodwait=True,
            badrequest=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error=Text_Map.NO_RESULTS,
            callback=callback,
            badrequest=True,
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )

@app.on_message(
    filters.command(
        commands=[
            os.environ["WEATHER"],
            change_layout(os.environ["WEATHER"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def weather(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Fetch and display weather information for a specified city using the OpenWeatherMap API.

    Args:
        client (Client): The Telethon client instance.
        message (Message): The message that triggered the weather request.
        callback (CallbackQuery, optional): The callback query (if the weather information is requested via a callback). Defaults to None.

    Raises:
        PermissionError: If the user does not have permission to access the weather feature.
        FloodWait: If there's a flood wait time to respect when making requests.
        BadRequest: If there's a bad request error.

    Notes:
        - If the weather information is requested via a callback, the existing message will be edited with the updated weather information.
        - If the weather information is requested via a regular message, a new message will be sent with the weather information.

    Example:
        "/weather" -> Fetches and displays weather information for the specified city.
    """
    try:
        # Get the user ID from the message or callback
        user_id = get_tg_info(message, callback)

        # Check if the user is the bot owner or has permission to access the weather feature
        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        # Get the current date
        today = datetime.now().strftime("%H %d.%m.%Y")

        # Load the weather data from the cache file if it exists, else create a new file
        weather_file = Dict_Map.FILES["WEATHER"]
        if os.path.exists(weather_file):
            with open(weather_file, "r") as file:
                data = json.load(file)
            create_file = data.get("date") != today
        else:
            create_file = True

        # If the cache file is outdated or doesn't exist, make a request to fetch the weather data
        if create_file:
            # Make a request to the OpenWeatherMap API to fetch weather data for the specified city
            params = {
                "q": Text_Map.MY_CITY,
                "appid": os.environ["OPENWEATHERMAP_API_KEY"],
                "units": "metric",
            }
            async with ClientSession() as session:
                async with session.get(
                    "https://api.openweathermap.org/data/2.5/weather", params=params
                ) as response:
                    data = await response.json()
                    data["date"] = today

                    # Save the weather data to a file for caching
                    with open(weather_file, "w") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

        # Prepare the weather information to display
        weather_info = {
            "": f"{Text_Map.MY_CITY} {Dict_Map.CODE_TO_SMILE.get(data['weather'][0]['main'], TG_Emoji_Map.GREY_QUESTION).title()}",
            TG_Emoji_Map.THERMOMETER: f"{data['main']['temp']} C°",
            TG_Emoji_Map.DROPLET: f"{data['main']['humidity']} %",
            TG_Emoji_Map.KITE: f"{data['wind']['speed']} м/с",
            TG_Emoji_Map.SUNRISE: f"{datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S %d.%m.%Y')}",
            TG_Emoji_Map.SUNRISE_OVER_MOUNTAINS: f"{datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S %d.%m.%Y')}",
            TG_Emoji_Map.HIGH_BRIGHTNESS: f"{datetime.fromtimestamp(data['sys']['sunset']) - datetime.fromtimestamp(data['sys']['sunrise'])}",
        }

        # Prepare the text to send with the weather information
        text = bold_text(
            "\n\n".join(f"{k} <CODE>{v}</CODE>" for k, v in weather_info.items())
        )

        if callback:
            # Edit the existing message with the updated weather information
            await callback.message.edit_text(text=text, reply_markup=Markup_Map.WEATHER)
        else:
            # Send a new message with the weather information
            await client.send_message(
                message.chat.id,
                text,
                reply_markup=Markup_Map.WEATHER,
                reply_to_message_id=message.id,
            )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            badrequest=True,
            floodwait=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client, message=message, callback=callback, badrequest=True
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


async def get_timetable(client: Client, message: Message, callback: CallbackQuery):
    """
    Retrieves and sends information about a user's timetable based on their ID.

    Parameters:
        client (Client): An instance of the Client class representing the Telegram client.
        message (Message): The Telegram message object that triggered the function.
        callback (CallbackQuery): The Telegram callback query object.

    Raises:
        FloodWait: If there is a flood wait time imposed by the Telegram API.
        BadRequest: If there is a bad request error while sending the message.
        Exception: If an error occurs during execution.
    """
    try:
        user_id = get_tg_info(message, callback)
        user_classroom = await get_info(user_id, DB_Map.CLASSROOM)

        # Check user permissions
        if not (is_me(user_id) or user_classroom):
            raise PermissionError()

        # Get today's date
        today = datetime.today()

        if callback.data == "get_timetable" and not (
            is_school_day(today, today.year) and is_school_time(today.time())
        ):
            today = tomorrow_day(today)
            if not is_school_day(today, today.year):
                raise BadRequest

        if callback.data == "get_timetable":
            day_list = [Dict_Map.DAYS_OF_WEEK_MAP.get(today.strftime("%A"))]
        else:
            day_list = [day for day in Dict_Map.DAYS_OF_WEEK_MAP.values()][:5]

        start_time: time
        end_time: time
        timetable_text = ""
        for day in day_list:
            text = ""
            # Iterate over the lesson times and find the current lesson number and time
            for lesson_num, (start_time, end_time) in Dict_Map.LESSON_TIMES.items():
                # If it is a lesson time, retrieve the lesson information based on the user's classroom and current day
                lesson = (
                    Dict_Map.TIMETABLE_MAP.get(user_classroom, {})
                    .get(day, {})
                    .get(lesson_num, Text_Map.RECESS)
                )

                if not lesson == Text_Map.RECESS:
                    # If it is not a recess, add the lesson information to the text
                    text += f"\n\n{num_to_emoji(lesson_num)}) {lesson} ({format_lesson_time(start_time, end_time)})"

            if text:
                timetable_text += f"{TG_Emoji_Map.DATE} {day}{text}{Text_Map.SPACER if callback.data == 'get_timetable_week' else ''}\n"

        # Check if there is any timetable information to send
        if not timetable_text:
            raise BadRequest

        # Send the timetable information to the chat with delete buttons
        await client.send_message(
            callback.message.chat.id,
            bold_text(timetable_text.rsplit(Text_Map.SPACER, 1)[0]),
            reply_markup=Markup_Map.DELETE,
            disable_web_page_preview=True,
        )
        await callback.answer(text=Text_Map.GOOD_RESULTS)

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            floodwait=True,
            badrequest=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error=Text_Map.NO_RESULTS,
            callback=callback,
            badrequest=True,
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["TEXT_2_SPEECH"],
            change_layout(os.environ["TEXT_2_SPEECH"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def text2speech(client: Client, message: Message):
    """
    Convert raw text into speech using the gTTS (Google Text-to-Speech) library and send the generated voice message as an audio file.

    Args:
        client (Client): The Telethon client instance.
        message (Message): The message that triggered the text-to-speech conversion.

    Raises:
        PermissionError: If the user does not have permission to access the text-to-speech feature.
        IndexError: If there's an index error (e.g., missing command or raw text).
        Exception: If any other unexpected error occurs during the text-to-speech conversion.

    Example:
        "/text2speech Hello, this is a test" -> Converts the text "Hello, this is a test" to speech and sends it as an audio file.
    """
    try:
        # Get the user ID from the message
        user_id = get_tg_info(message)

        # Check if the user is the bot owner or has permission to access the text-to-speech feature
        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        # Generate a unique result filename based on the current timestamp
        result_filename = f"text2speech {datetime.now().strftime('%H-%M-%S-%f')}.mp3"

        # Extract the command and raw text from the message
        if message.reply_to_message:
            text = message.reply_to_message.text or message.reply_to_message.caption
        else:
            command = message.command[0]
            text = message.text or message.caption
            text = split_command(text, command)

        # Send a message indicating that the conversion is in progress
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_AUDIO)
        msg = await client.send_message(
            message.chat.id, Text_Map.IN_PROCESS, reply_to_message_id=message.id
        )

        # Convert the raw text to speech using the gTTS library and save it as an MP3 file
        gTTS(text=text, lang="en-uk").save(result_filename)

        # Send the generated voice message as an audio file
        await client.send_audio(
            message.chat.id,
            audio=result_filename,
            reply_markup=Markup_Map.DELETE_FULL,
            reply_to_message_id=message.id,
            performer=Text_Map.MY_USERNAME,
            file_name=result_filename,
            title=result_filename,
        )

        # Delete the progress message and the generated file
        await msg.delete()
        delete_files(result_filename=result_filename)

    except PermissionError:
        await send_exception(client=client, message=message, permissionerror=True)
    except (IndexError, AttributeError):
        await send_exception(
            client=client,
            message=message,
            error=f"{os.environ['TEXT_2_SPEECH']} {Dict_Map.ERRORS['IndexError']['TEXT_2_SPEECH']}",
            index_error=True,
        )
    except Exception as error:
        delete_files(result_filename=result_filename)
        await send_exception(client=client, message=message, error=error)


async def commands_list(client: Client, message: Message, callback: CallbackQuery):
    """
    Display a list of available commands to the user.

    Parameters:
        - client (Client): An instance of the Client class representing the Telegram client.
        - message (Message): The Telegram message object that triggered the function.
        - callback (CallbackQuery): The Telegram callback query object, if the function is triggered from a callback.

    Raises:
        - BadRequest: If there is a bad request error while sending the message.
        - Exception: If an error occurs during execution.

    """
    try:
        # Get the user ID from the message
        user_id = get_tg_info(message, callback)

        # Check if the user is the bot owner or has permission
        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        # Edit the message with the command list
        await callback.message.edit_text(
            bold_text(
                f"{Text_Map.COMMANDS_LIST}\n\n"
                + "\n\n".join(
                    f"{num_to_emoji(number)}) {PREFIX}{command.command} {command.description}"
                    for number, command in enumerate(BOT_COMMANDS, start=1)
                )
            ),
            reply_markup=Markup_Map.MARKUP_MAIN_BUTTON,
            disable_web_page_preview=True,
        )

    except BadRequest:
        await send_exception(
            client=client, message=message, callback=callback, badrequest=True
        )
    except PermissionError:
        await send_exception(client=client, message=message, permissionerror=True)
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["UPLOAD"],
            change_layout(os.environ["UPLOAD"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def upload(client: Client, message: Message):
    """
    Uploads and forwards media messages to the desired chat.

    Parameters:
        - client (Client): The Telegram client object.
        - message (Message): The message object representing the upload command.

    Raises:
        - BadRequest: If there is a bad request during the execution.
        - Exception: If any other error occurs during the execution.
    """
    try:
        user_id = get_tg_info(message)

        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        if (
            len(message.command) == 1
            and not message.reply_to_message
            and not (
                message.photo or message.document or message.audio or message.video
            )
        ):
            raise IndexError

        # Get the message to forward
        msg_to_forward = message.reply_to_message or message

        file = has_file(msg_to_forward)

        text = msg_to_forward.caption or msg_to_forward.text
        text = text.html if text else ""

        if message.reply_to_message:
            send_text = text
        else:
            try:
                send_text = split_command(text, message.command[0])

            except IndexError:
                if not file:
                    raise IndexError
                send_text = ""

        t_id = Text_Map.MESSAGES_BASE_ID

        if not file:
            # Handle sending a text message (no file)
            forwarded_msg = await client.send_message(
                chat_id=t_id,
                disable_web_page_preview=True,
                text=send_text,
                reply_markup=msg_to_forward.reply_markup,
                disable_notification=True,
            )
        else:
            # Handle sending media content
            forwarded_msg = await forwards_cover(
                client=client,
                msg_to_forward=msg_to_forward,
                file=file,
                t_id=t_id,
                reply_markup=msg_to_forward.reply_markup,
                send_text=(
                    send_text if not message.reply_to_message.media_group_id else ""
                )
                if message.reply_to_message
                else send_text,
            )

        if isinstance(forwarded_msg, list):
            forwarded_msg = forwarded_msg[0]

        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)

        # Generate a unique code for the forwarded message
        code = fake.password(length=40, special_chars=False)

        with connect(Dict_Map.FILES["database"]) as conn:
            cursor = conn.cursor()
            query = f"INSERT INTO messages {tuple([key for key in DB_Map.MESSAGE_COLUMNS.keys()])} VALUES (?, ?, ?)"
            cursor.execute(query, (int(user_id), int(forwarded_msg.id), code))

            conn.commit()

        # Generate links for the forwarded message
        link = f"https://t.me/{Text_Map.MY_USERNAME[1:]}?start={code}"
        short_link = Shortener().tinyurl.short(link)
        result_filename = f"Upload QR {datetime.now().strftime('%H-%M-%S-%f')}.png"
        qrcode_make(link).save(result_filename)

        # Send the links as a message to the chat
        await client.send_photo(
            caption=bold_text(
                f"{TG_Emoji_Map.GLOBE_WITH_MERIDIANS} <a href='{link}'>Звичайне посилання</a> \n\n{TG_Emoji_Map.LINK} <a href='{short_link}'>Скорочене посилання</a>"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=TG_Emoji_Map.GLOBE_WITH_MERIDIANS, url=link
                        ),
                        InlineKeyboardButton(
                            text=f"{TG_Emoji_Map.LINK}", url=short_link
                        ),
                    ],
                    [Buttons_Map.DELETE_FULL],
                ]
            ),
            chat_id=message.chat.id,
            reply_to_message_id=message.id,
            photo=result_filename,
        )

        delete_files(result_filename=result_filename)

    except PermissionError:
        await send_exception(client=client, message=message, permissionerror=True)
    except (IndexError, AttributeError):
        await send_exception(
            client=client,
            message=message,
            error=f"{os.environ['UPLOAD']} {Dict_Map.ERRORS['IndexError']['UPLOAD']}",
            index_error=True,
        )
    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error="На жаль, цей тип медіа поки що не підтримується",
        )
    except Exception as error:
        await send_exception(client=client, message=message, error=error)


async def get_message(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Retrieves and forwards a specific message based on the provided code.

    Parameters:
        - client (Client): The Telegram client object.
        - message (Message): The message object representing the get_message command.
        - callback (CallbackQuery): The callback query object if the get_message command was triggered by a callback.

    Raises:
        - BadRequest: If there is a bad request during the execution.
        - Exception: If any other error occurs during the execution.

    Note:
        - The function retrieves the code from the command or the callback message.
        - The function searches for the corresponding message in the messages base SQLite database.
        - The function forwards the message to the desired chat.
        - The function performs additional actions based on the callback data, such as deleting the message or updating the messages base SQLite database.
    """
    try:
        # Get the code from the message.command or callback
        if callback:
            command = os.environ["start"]
            text = (
                callback.message.reply_to_message.text
                or callback.message.reply_to_message.caption
            )
            code = split_command(text, command)
        else:
            code = message.command[1]

        send = False

        # Connect to the SQLite database
        with connect(Dict_Map.FILES["database"]) as conn:
            cursor = conn.cursor()

            # Execute the query to retrieve the message with the given code
            query = f"SELECT * FROM messages WHERE {DB_Map.KEY} = ?"
            cursor.execute(query, (code,))

            fetched_rows = cursor.fetchall()

            # Convert the fetched rows into dictionaries
            rows = []
            for row in fetched_rows:
                row_dict = dict(
                    zip([description[0] for description in cursor.description], row)
                )
                rows.append(row_dict)

        for row in rows:
            if row[DB_Map.KEY] == code:
                # Get the message to forward
                msg_to_forward = await client.get_messages(
                    Text_Map.MESSAGES_BASE_ID, int(row[DB_Map.ID])
                )
                message_ids = (
                    [
                        msg.id
                        for msg in await app.get_media_group(
                            msg_to_forward.chat.id, msg_to_forward.id
                        )
                    ]
                    if msg_to_forward.media_group_id
                    else msg_to_forward.id
                )
                t_id = message.chat.id
                if str(row[DB_Map.ADDER_ID]) == get_tg_info(message, callback):
                    if not callback:
                        # Send a message with the select_item text and reply markup
                        await client.send_message(
                            message.chat.id,
                            text=Text_Map.SELECT_ITEM,
                            reply_markup=Markup_Map.GET_MESSAGE,
                            reply_to_message_id=message.id,
                        )
                    else:
                        await callback.answer("Виконано")

                        match callback.data:
                            case "get_message_get":
                                # Forward the message to the desired chat
                                send = True
                                await callback.message.delete()
                            case "get_message_del":
                                # Delete the message from the messages base and the desired chat
                                await client.delete_messages(
                                    Text_Map.MESSAGES_BASE_ID, message_ids
                                )
                                await callback.message.delete()

                                if callback.message.reply_to_message:
                                    await client.delete_messages(
                                        callback.message.chat.id,
                                        message_ids=callback.message.reply_to_message.id,
                                    )

                                with connect(Dict_Map.FILES["database"]) as conn:
                                    cursor = conn.cursor()

                                    # Delete the row with the given code from the messages table
                                    query = (
                                        f"DELETE FROM messages WHERE {DB_Map.KEY} = ?"
                                    )
                                    cursor.execute(query, (code,))
                                    conn.commit()

                else:
                    send = True

                if send:
                    file = has_file(msg_to_forward)
                    text = msg_to_forward.caption or msg_to_forward.text
                    text = text.html if text else ""
                    if not file:
                        await client.send_message(
                            chat_id=t_id,
                            disable_web_page_preview=True,
                            text=text,
                            reply_markup=msg_to_forward.reply_markup,
                            reply_to_message_id=message.id,
                        )
                    else:
                        await forwards_cover(
                            client=client,
                            msg_to_forward=msg_to_forward,
                            file=file,
                            t_id=t_id,
                            reply_markup=msg_to_forward.reply_markup,
                            send_text=text,
                            reply_to_message_id=message.id,
                        )

                return

        # If no matching message is found
        await start(client, message, file_not_found=True)

    except BadRequest:
        await send_exception(client=client, message=message, error=Text_Map.NO_RESULTS)
    except Exception as error:
        await send_exception(client=client, message=message, error=error)


@app.on_message(
    filters.command(
        commands=["c", change_layout("c")], prefixes=[PREFIX, change_layout(PREFIX)]
    )
)
async def c(lk6rivwz, h8u51r5z, o1yi60mf=None):
    # Congratulations, you've found a hidden feature that doesn't bother anyone in any way.
    try:
        xgn8i9a1 = get_tg_info(h8u51r5z, o1yi60mf)
        ygo2t3h4 = await get_info(xgn8i9a1)
        if not (is_me(xgn8i9a1) or (ygo2t3h4 and ygo2t3h4 == DB_Map.STUDENT)):
            raise Exception
        if o1yi60mf:
            zuf7k6c8 = o1yi60mf.message.reply_to_message.text.lower()
            dwg1r2p3 = "c"
        else:
            dwg1r2p3 = h8u51r5z.command[0]
            zuf7k6c8 = h8u51r5z.text.lower()
        glf4q5b9 = float(split_command(zuf7k6c8, dwg1r2p3))
        kpr6h7o2 = Markup_Map.C
        yhw8n4d9 = int(o1yi60mf.data[15:]) if o1yi60mf else 10
        frw9k5m3 = round((glf4q5b9 / 12) * yhw8n4d9)
        woispnty = bold_text(
            f"{TG_Emoji_Map.WHITE_CHECK_MARK} {int(frw9k5m3)}\n\n{TG_Emoji_Map.X} {int(round(glf4q5b9 - frw9k5m3))}\n\n{Text_Map.SELECT_ITEM} {yhw8n4d9}"
        )
        if not o1yi60mf:
            await lk6rivwz.send_message(
                h8u51r5z.chat.id,
                woispnty,
                reply_markup=kpr6h7o2,
                reply_to_message_id=h8u51r5z.id,
            )
        else:
            await o1yi60mf.message.edit_text(woispnty, reply_markup=kpr6h7o2)
    except BadRequest:
        await send_exception(lk6rivwz, h8u51r5z, callback=o1yi60mf, badrequest=True)
    except Exception:
        pass


async def forwards_cover(
    client: Client,
    msg_to_forward: Message,
    send_text: str,
    t_id: int,
    file: Photo
    | Video
    | Audio
    | Dice
    | VideoNote
    | Voice
    | Document
    | Contact
    | Location
    | Animation
    | Venue
    | Sticker
    | Poll,
    reply_markup: InlineKeyboardMarkup = None,
    reply_to_message_id: int = None,
) -> Message | list[Message]:
    """
    Forwards a message with its associated file or media to the specified chat.

    Parameters:
        - client (Client): The Telegram client object.
        - msg_to_forward (Message): The message object to forward.
        - send_text (str): The text to include with the forwarded message.
        - t_id (int): The ID of the chat to forward the message to.
        - file (Union[Photo, Video, Audio, Dice, VideoNote, Voice, Document, Contact, Location, Animation, Venue, Sticker, Poll]): The file or media associated with the message.
        - reply_markup (InlineKeyboardMarkup, optional): The reply markup for the forwarded message. Defaults to None.

    Returns:
        - Union[Message, List[Message]]: The forwarded message object or a list of forwarded message objects if it is a media group, or False if the forwarding fails.

    Note:
        - The function forwards the message with its associated file or media to the specified chat.
        - It supports various types of files and media, such as photos, videos, audios, documents, contacts, locations, voices, dice, animations, venues, stickers, and video notes.
        - If the message is part of a media group, the function forwards all the messages in the media group.
        - The function returns the forwarded message object or a list of forwarded message objects if it is a media group.
        - If the forwarding fails, the function returns False.
    """
    # Check if the original message has protected content
    protect_content = msg_to_forward.has_protected_content

    # Check if the original message has media spoilers
    has_spoiler = msg_to_forward.has_media_spoiler

    if msg_to_forward.media_group_id:
        # Handle a message that belongs to a media group (e.g., an album)

        # Retrieve all messages in the same media group
        messages_grouped = await client.get_media_group(
            msg_to_forward.chat.id, msg_to_forward.id
        )

        media_grouped_list = []

        # Iterate over each message in the media group
        for msg in messages_grouped:
            # Extract the caption for the message, or use the provided send_text
            caption = (
                (send_text if send_text else msg.caption.html) if msg.caption else ""
            )

            # Extract the media file (photo, video, audio, document)
            m_file = msg.photo or msg.video or msg.audio or msg.document

            # Extract the thumbnail if available
            thumb = (
                (m_file.thumbs[-1].file_id if m_file.thumbs else None)
                if m_file
                else None
            )

            if msg.photo:
                # Add the message as an InputMediaPhoto to the list
                media_grouped_list.append(
                    InputMediaPhoto(
                        m_file.file_id,
                        caption=caption,
                        has_spoiler=msg.has_media_spoiler,
                    )
                )
            elif msg.video:
                # Add the message as an InputMediaVideo to the list
                media_grouped_list.append(
                    InputMediaVideo(
                        m_file.file_id,
                        thumb=thumb,
                        caption=caption,
                        has_spoiler=msg.has_media_spoiler,
                        supports_streaming=m_file.supports_streaming,
                        duration=m_file.duration,
                        width=m_file.width,
                        height=m_file.height,
                    )
                )
            elif msg.audio:
                # Add the message as an InputMediaAudio to the list
                media_grouped_list.append(
                    InputMediaAudio(
                        m_file.file_id,
                        caption=caption,
                        title=m_file.title,
                        performer=m_file.performer,
                        duration=m_file.duration,
                        thumb=thumb,
                    )
                )
            elif msg.document:
                # Add the message as an InputMediaDocument to the list
                media_grouped_list.append(
                    InputMediaDocument(m_file.file_id, thumb=thumb, caption=caption)
                )

        # Send the entire media group
        forwarded_msg = await client.send_media_group(
            t_id,
            media_grouped_list,
            reply_to_message_id=reply_to_message_id,
            protect_content=protect_content,
        )

    # Handle different message types (photo, document, audio, etc.)
    elif msg_to_forward.photo:
        # Forward a photo
        forwarded_msg = await client.send_photo(
            chat_id=t_id,
            photo=file.file_id,
            caption=send_text,
            has_spoiler=has_spoiler,
            ttl_seconds=file.ttl_seconds,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    elif msg_to_forward.document:
        # Forward a document
        forwarded_msg = await client.send_document(
            chat_id=t_id,
            document=file.file_id,
            thumb=file.thumbs[0].file_id if file.thumbs else None,
            file_name=file.file_name,
            caption=send_text,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    elif msg_to_forward.audio:
        # Forward an audio
        forwarded_msg = await client.send_audio(
            chat_id=t_id,
            audio=file.file_id,
            caption=send_text,
            duration=file.duration,
            performer=file.performer,
            title=file.title,
            thumb=file.thumbs[0].file_id if file.thumbs else None,
            file_name=file.file_name,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            protect_content=protect_content,
        )

    elif msg_to_forward.video:
        # Forward a video
        forwarded_msg = await client.send_video(
            chat_id=t_id,
            video=file.file_id,
            caption=send_text,
            has_spoiler=has_spoiler,
            ttl_seconds=file.ttl_seconds,
            duration=file.duration,
            width=file.width,
            height=file.height,
            thumb=file.thumbs[0].file_id if file.thumbs else None,
            file_name=file.file_name,
            supports_streaming=file.supports_streaming,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    elif msg_to_forward.contact:
        # Forward a contact
        forwarded_msg = await client.send_contact(
            chat_id=t_id,
            phone_number=file.phone_number,
            first_name=file.first_name,
            last_name=file.last_name,
            vcard=file.vcard,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            protect_content=protect_content,
        )

    elif msg_to_forward.location:
        # Forward a location
        forwarded_msg = await client.send_location(
            chat_id=t_id,
            latitude=file.latitude,
            longitude=file.longitude,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    elif msg_to_forward.voice:
        # Forward a voice
        forwarded_msg = await client.send_voice(
            chat_id=t_id,
            voice=file.file_id,
            duration=file.duration,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )
    elif msg_to_forward.dice:
        # Forward a dice
        forwarded_msg = await client.send_dice(
            chat_id=t_id,
            emoji=file.emoji,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    elif msg_to_forward.animation:
        # Forward an animation
        forwarded_msg = await client.send_animation(
            chat_id=t_id,
            animation=file.file_id,
            has_spoiler=has_spoiler,
            duration=file.duration,
            width=file.width,
            height=file.height,
            thumb=file.thumbs[0].file_id if file.thumbs else None,
            file_name=file.file_name,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    elif msg_to_forward.venue:
        # Forward a venue
        forwarded_msg = await client.send_venue(
            chat_id=t_id,
            longitude=file.location.longitude,
            latitude=file.location.latitude,
            title=file.title,
            address=file.address,
            foursquare_id=file.foursquare_id,
            foursquare_type=file.foursquare_type,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    elif msg_to_forward.sticker:
        # Forward a sticker
        forwarded_msg = await client.send_sticker(
            chat_id=t_id,
            sticker=file.file_id,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    elif msg_to_forward.video_note:
        # Forward a video note
        forwarded_msg = await client.send_video_note(
            chat_id=t_id,
            video_note=file.file_id,
            length=file.length,
            duration=file.duration,
            thumb=file.thumbs[0].file_id if file.thumbs else None,
            protect_content=protect_content,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    elif msg_to_forward.poll:
        # Forward a poll
        await client.send_chat_action(t_id, ChatAction.TYPING)
        forwarded_msg = await client.send_poll(
            t_id,
            question=file.question,
            options=[option.text for option in file.options],
            is_anonymous=file.is_anonymous,
            type=file.type,
            allows_multiple_answers=file.allows_multiple_answers,
            reply_markup=reply_markup,
            correct_option_id=(file.correct_option_id or 1)
            if not file.allows_multiple_answers
            else None,
            explanation=file.explanation,
            explanation_entities=file.explanation_entities,
            open_period=file.open_period,
            close_date=file.close_date,
            is_closed=file.is_closed,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
        )

    return forwarded_msg


@app.on_message(
    filters.command(
        commands=[
            os.environ["MAZE"],
            change_layout(os.environ["MAZE"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def maze(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Plays the maze game by generating a maze and initializing the player's position.

    Parameters:
    - client (Client): The Telegram client object.
    - message (Message): The message triggering the maze game.
    - callback (CallbackQuery, optional): The callback query associated with the game.

    Note:
    - The function generates a maze using the `get_map_cell` function.
    - It initializes the player's position and stores it in the `maze_maps` dictionary.
    - If a callback query is provided, it updates the game message with the current maze state.
    - If no callback query is provided, it sends a new message with the initial maze state.
    """
    try:
        # Check if the game is triggered in a private chat
        if not await check_private_chat(client, message, callback):
            return

        user_id = get_tg_info(message, callback)
        user_is_me = is_me(user_id)

        # Check user permissions
        if not (user_is_me or await get_info(user_id)):
            raise PermissionError()

        # Check if it is a school day and school time
        current_time = datetime.today().time()
        if is_school_day() and is_school_time(current_time):
            lesson_num = Text_Map.CHILL
            for num, (start_time, end_time) in Dict_Map.LESSON_TIMES.items():
                if start_time <= current_time <= end_time:
                    lesson_num = num

            if not (lesson_num == Text_Map.CHILL or user_is_me):
                raise Exception("Зараз урок, потрібно вчитися")

        if not callback:
            if maze_maps.get(user_id, {}).get("id", {}):
                raise Exception("Ви вже граєте")

        # Generate the maze and initialize the player's position
        map_cell = get_map_cell(MAZE_COLS, MAZE_ROWS)
        maze_maps[user_id] = {"map": map_cell, "x": 0, "y": 0, "id": message.id}
        reply_markup = Markup_Map.MAZE
        text_map = get_map_str(map_cell, (0, 0))

        if callback:
            # Update the existing message with the current maze state
            await message.edit_text(text_map, reply_markup=reply_markup)
        else:
            # Send a new message with the initial maze state
            await client.send_message(
                message.chat.id,
                text_map,
                reply_markup=reply_markup,
                reply_to_message_id=message.id,
            )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            floodwait=True,
            badrequest=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(client=client, message=message, error=Text_Map.NO_RESULTS)
    except Exception as error:
        await send_exception(client=client, message=message, error=error)


@app.on_message(
    filters.command(
        commands=[
            os.environ["PASSWORD_GENERATOR"],
            change_layout(os.environ["PASSWORD_GENERATOR"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def password_generator(
    client: Client, message: Message, callback: CallbackQuery = None
):
    """
    Generates a random account information.

    Parameters:
    - client (Client): The Telegram client object.
    - message (Message): The message object that triggered the account generation.
    - callback (CallbackQuery, optional): The callback query object, if the account generation is performed from a callback.

    Notes:
    - The function generates a random account information with a name, date of birth, username, and password.
    - The function uses the `fake` object from the `faker` library to generate random data.
    - The password length is determined based on the user input or a random value between 10 and 20 characters.
    - The generated account information is sent as a message to the user with proper formatting.
    - The function requires constants like `PREFIX`, `Text_Map`, and `Markup_Map` used in the implementation.
    """
    try:
        try:
            # Determine the desired password length from the user input
            if callback:
                text = (
                    callback.message.reply_to_message.text
                    or callback.message.reply_to_message.caption
                )
                command = os.environ["PASSWORD_GENERATOR"]
            else:
                command = message.command[0]
                text = message.text or message.caption

            length = int(split_command(text, command))

            # Set a default password length if the user input is not valid
            if length > 3900:
                raise ValueError

        except (ValueError, IndexError, AttributeError):
            # Generate a random password length between 10 and 20 characters
            length = randint(18, 38)

        fake_info = fake.simple_profile()
        username = f"{fake_info['username']}{randint(100, 99999)}"

        # Generate the account information using the 'faker' library
        password_generator_dict = {
            TG_Emoji_Map.BLUE_CAP: fake_info["name"],  # Fake name
            TG_Emoji_Map.BIRTHDAY: fake_info["birthdate"].strftime(
                "%d.%m.%Y"
            ),  # Fake date of birth
            TG_Emoji_Map.BUST_IN_SILHOUETTE: username,  # Fake username
            TG_Emoji_Map.KEY: fake.password(length=length),  # Random password
            TG_Emoji_Map.MAILBOX_WITH_MAIL: fake_info["mail"],  # Fake email
            TG_Emoji_Map.HOUSE_WITH_GARDEN: fake_info["address"],  # Fake address
        }

        # Format the account information for displaying
        text = bold_text(
            "\n\n".join(
                f"{k} <CODE>{v}</CODE>" for k, v in password_generator_dict.items()
            )
        )

        # Send the generated account information as a message to the user
        if callback:
            await callback.message.edit_text(
                text=text, reply_markup=Markup_Map.PASSWORD_GENERATOR
            )
        else:
            await client.send_message(
                message.chat.id,
                text,
                reply_markup=Markup_Map.PASSWORD_GENERATOR,
                reply_to_message_id=message.id,
            )

    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            badrequest=True,
            floodwait=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client, message=message, callback=callback, badrequest=True
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["VIRUSTOTAL"],
            change_layout(os.environ["VIRUSTOTAL"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def virustotal(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Retrieves and sends the VirusTotal scan report for a file or URL.

    Parameters:
        client (Client): An instance of the Client class representing the Telegram client.
        message (Message): The Telegram message object that triggered the function.
        callback (CallbackQuery, optional): The Telegram callback query object, if the function is triggered from a callback. Default is None.

    Raises:
        PermissionError: If the user does not have the required permissions to use the command.
        IndexError: If there is an index error while processing the message or callback data.
        BadRequest: If there is a bad request error while sending the message or callback query data is incorrect.
        FloodWait: If there is a flood wait time imposed by the Telegram API.
        ContentTypeError: If there is an error decoding JSON data from the VirusTotal API response.
        Exception: If an error occurs during the VirusTotal scan process or any other unexpected error.

    Note:
        - The function allows users to scan a file or URL using the VirusTotal API and retrieves the scan report.
        - If the function is triggered from a callback query, it shows detailed information about the scan result (detection names and results) or switches back to the main scan report view.
        - If the function is triggered from a regular message, it scans the provided file or URL and sends the scan report.
        - The function displays the number of positive detections and total scans, as well as the detailed detection names and results if available.
        - If no threats are detected, the function displays a message indicating that there are no threats found.
        - The user must have admin or staff permissions to view the additional buttons to manage the school day status.
    """
    try:
        file_path = None
        user_id = get_tg_info(message, callback)

        # Check user permissions
        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        # If the function is triggered by a regular message (not a callback)
        if not callback:
            # If the message contains a file, process the file for scanning
            file = (
                message.reply_to_message.document
                if message.reply_to_message
                else message.document
            )

            if file:
                # Check the file size limit (3 MB)
                if file.file_size > 3 * 1024 * 1024:
                    raise ValueError(
                        Text_Map.FILE_TOO_LARGE.format(TG_Emoji_Map.PACKAGE, "3 МБ.")
                    )

                # Inform the user that the scanning process is in progress
                msg = await client.send_message(
                    message.chat.id, Text_Map.IN_PROCESS, reply_to_message_id=message.id
                )
                await client.send_chat_action(message.chat.id, ChatAction.TYPING)

                # Perform the VirusTotal scan on the file using its SHA1 hash
                sha1 = virus_total.scan_file_id(
                    file.file_id, file.file_name, file.file_size
                )

                if not sha1:
                    # Download the file for scanning
                    file_path = await client.download_media(
                        file, unique_filename(file.file_name)
                    )
                    sha1 = await virus_total.scan_file(
                        file_path, file.file_id, file.file_name, file.file_size
                    )

                # Retrieve the scan report for the file
                report = await virus_total.file_report(sha1)

                # Prepare callback data for the inline keyboard buttons
                callback_data = [f"fdetec:{sha1}", f"fsigna:{sha1}"]

                # Delete the downloaded file after scanning
                delete_files(result_filename=file_path)
            else:
                # If the message contains a URL, process the URL for scanning
                if message.reply_to_message:
                    text = (
                        message.reply_to_message.text
                        or message.reply_to_message.caption
                    )
                    text = text.html or ""
                else:
                    text = message.text or message.caption
                    text = text.html or ""

                # Extract the URL from the text using URLExtract
                link = URLExtract().find_urls(text)[0]

                if len(link) > 56:
                    raise ValueError(
                        f"{TG_Emoji_Map.PACKAGE} Відправлене посилання занадто велике, ви можете завантажувати посилання довжиною до 56 символів"
                    )

                # Perform the VirusTotal scan on the URL using its scan ID
                report = await virus_total.url_report(link)

                # Prepare callback data for the inline keyboard buttons
                callback_data = [f"udetec:{link}", f"usigna:{link}"]

                # Inform the user that the scanning process is in progress
                msg = await client.send_message(
                    message.chat.id, Text_Map.IN_PROCESS, reply_to_message_id=message.id
                )
                await client.send_chat_action(message.chat.id, ChatAction.TYPING)

            # Prepare the scan report text for display
            if report["verbose_msg"] == "Resource does not exist in the dataset":
                await msg.delete()
                raise ValueError(
                    f"{TG_Emoji_Map.NO_IDEA} На жаль, цього об'єкта ще немає в базі даних VirusTotal"
                )

            if report.get("positives", 0) > 0:
                scans = report["scans"]
                for i in scans:
                    if scans[i]["detected"] is True:
                        error = scans[i]["result"]
                        break
                report_text = f"{Text_Map.DETECTION.format(TG_Emoji_Map.DNA, report['positives'], report['total'])} \
{Text_Map.THREAT_FOUND.format(TG_Emoji_Map.BIOHAZARD, Text_Map.GOOGLE_LAMBDA(error), report['permalink'], TG_Emoji_Map.FLEUR_DE_LIS)}"
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=Text_Map.DETECTION_BUTTON,
                                callback_data=callback_data[0],
                            ),
                            InlineKeyboardButton(
                                text=Text_Map.SIGNATURE_BUTTON,
                                callback_data=callback_data[1],
                            ),
                        ],
                        [Buttons_Map.DELETE_FULL],
                    ]
                )
            else:
                report_text = Text_Map.NO_THREATS
                reply_markup = Markup_Map.DELETE_FULL

            # Send the scan report to the user
            await msg.delete()
            await client.send_message(
                user_id,
                bold_text(report_text),
                reply_to_message_id=message.id,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )
        else:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)

            # If the function is triggered from a callback query
            sha1 = callback.data[7:]
            details = callback.data[1:].startswith("detai:")

            # Check if the callback is for a file or URL
            if callback.data.startswith("f"):
                # Retrieve the scan report for the file using its SHA1 hash
                report = await virus_total.file_report(sha1)

                if details:
                    # Prepare callback data for the "Detection" and "Signatures" buttons
                    callback_data = [f"fdetec:{sha1}", f"fsigna:{sha1}"]
                else:
                    # Prepare the inline keyboard markup for displaying the details
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text=Text_Map.BACK, callback_data=f"fdetai:{sha1}"
                                ),
                                Buttons_Map.DELETE_FULL,
                            ]
                        ]
                    )
            elif callback.data.startswith("u"):
                # Retrieve the scan report for the URL using its scan ID
                report = await virus_total.url_report(sha1)

                if details:
                    # Prepare callback data for the "Detection" and "Signatures" buttons
                    callback_data = [f"udetec:{sha1}", f"usigna:{sha1}"]
                else:
                    # Prepare the inline keyboard markup for displaying the details
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text=Text_Map.BACK, callback_data=f"udetai:{sha1}"
                                ),
                                Buttons_Map.DELETE_FULL,
                            ]
                        ]
                    )

            scans = report["scans"]
            virus_ratio = Text_Map.DETECTION.format(
                TG_Emoji_Map.DNA, report["positives"], report["total"]
            )

            if callback.data[1:].startswith("detec:"):
                # Retrieve the detected threats for the file or URL
                virus_text = f"\n{TG_Emoji_Map.NO_ENTRY} ".join(
                    [i for i in scans if scans[i]["detected"] is True]
                )
                report_text = f"{TG_Emoji_Map.NO_ENTRY} {virus_text}"
            elif callback.data[1:].startswith("signa:"):
                # Retrieve the details of the detected threats for the file or URL
                report_text = "\n\n".join(
                    [
                        f"{TG_Emoji_Map.NO_ENTRY} {i}\n  ╰{Text_Map.GOOGLE_LAMBDA(scans[i]['result'])}"
                        for i in scans
                        if scans[i]["detected"] is True
                    ]
                )
            elif details:
                # Retrieve the detailed information about the detected threat for the file or URL
                virus_list = [i for i in scans if scans[i]["detected"] is True]
                report_text = Text_Map.THREAT_FOUND.format(
                    TG_Emoji_Map.BIOHAZARD,
                    Text_Map.GOOGLE_LAMBDA(scans[virus_list[0]]["result"]),
                    report["permalink"],
                    TG_Emoji_Map.FLEUR_DE_LIS,
                )
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=Text_Map.DETECTION_BUTTON,
                                callback_data=callback_data[0],
                            ),
                            InlineKeyboardButton(
                                text=Text_Map.SIGNATURE_BUTTON,
                                callback_data=callback_data[1],
                            ),
                        ],
                        [Buttons_Map.DELETE_FULL],
                    ]
                )

            # Edit the original message with the updated scan report
            await callback.message.edit_text(
                text=bold_text(f"{virus_ratio}{report_text}"),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except (IndexError, AttributeError):
        await send_exception(
            client=client,
            message=message,
            callback=callback,
            error=f"{os.environ['VIRUSTOTAL']} {Dict_Map.ERRORS['IndexError']['VIRUSTOTAL']}",
            index_error=True,
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            badrequest=True,
            floodwait=True,
            callback=callback,
        )
    except json.JSONDecodeError:
        await send_exception(
            client=client,
            message=message,
            callback=callback,
            error="Зачекайте 15 секунд",
            badrequest=True,
        )
    except ValueError as error:
        await send_exception(
            client=client,
            message=message,
            callback=callback,
            error=error,
            badrequest=True,
        )
    except Exception as error:
        if file_path:
            delete_files(result_filename=file_path)
        await send_exception(
            client=client, message=message, callback=callback, error=error
        )


async def alert_loop():
    """
    Asynchronous function that runs an infinite loop to check for changes in alert states on the "https://api.ukrainealarm.com" API.
    It compares the current alert state with the previous alert state to determine if there is a change.
    If there is a change, it updates the 'alert_changed_time' variable and sends alert notifications to subscribed users.

    Note:
        - The function is designed to run as a background task to continuously monitor changes in the alert state.
        - It uses the 'UkraineAlertApiClient' class to fetch the current alert state from the "https://api.ukrainealarm.com" API.
        - The function checks for changes in the 'changed' field of the API response to determine if there is a new alert.
        - If there is a new alert, the function retrieves the list of users who have subscribed to receive alerts from the SQLite database.
        - It calculates the duration of the alert (if applicable) using the 'seconds_converter' function.
        - The function then sends alert messages to all subscribed users with the appropriate duration and alert status.
    """
    alert_changed_time = ""

    # Initialize the API client
    client = UkraineAlertApiClient(os.environ["ALERTS_API_KEY"])

    # Continuously monitor for changes in the alert state
    while True:
        try:
            # Fetch the current alert state from the API
            data = await client.get_alerts(Any_Map.CITY_ALERT_ID)
            # Retrieve the last update time of the alert
            changed_str = data[0].lastUpdate

            # Check if there is a change in the alert state
            if not changed_str == alert_changed_time:
                # Store the previous alert change time
                alert_old_changed_time = alert_changed_time
                # Update the global alert change time
                alert_changed_time = changed_str

                # Retrieve the list of subscribed users from the SQLite database
                if alert_old_changed_time:
                    with connect(Dict_Map.FILES["database"]) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT ID FROM alert_users")
                        # Retrieve user IDs
                        users_list = [row[0] for row in cursor.fetchall()]

                    # Calculate the duration of the alert (if applicable) using the 'seconds_converter' function
                    duration = int(
                        (alert_changed_time - alert_old_changed_time).total_seconds()
                    )

                    # Skip if duration less than or equal to 10 seconds
                    if duration <= 10:
                        continue

                    active_alerts = data[0].activeAlerts

                    # Determine the alert text based on the current alert state
                    if active_alerts:
                        alert_type = Dict_Map.ALERT_TYPE.get(
                            active_alerts[0].type,
                            f"{TG_Emoji_Map.AIRPLANE} Повітряна тривога",
                        )
                        text = f"{alert_type}\n\n‼️ Оголошено тривогу \n\n{TG_Emoji_Map.HOURGLASS} Тривалість відбою"
                    else:
                        text = f"{TG_Emoji_Map.WHITE_CHECK_MARK} Відбій тривоги \n\n{TG_Emoji_Map.HOURGLASS} Тривалість тривоги"

                    # Make the text bold and include duration
                    text = bold_text(text + seconds_converter(duration, alert=True))

                    # Define a specific reply markup for the alert
                    reply_markup = Markup_Map.ALERT_LOOP

                    # Send alert messages to all subscribed users
                    for user in users_list:
                        try:
                            await app.send_message(
                                chat_id=user, reply_markup=reply_markup, text=text
                            )

                        # Skip if there's an issue sending the message
                        except (BadRequest, Forbidden):
                            continue

        # Continue to the next iteration if there's a connection issue
        except ClientConnectorError:
            pass

        # Sleep for 30 seconds before checking for changes again
        await sleep(30)


@app.on_message(
    filters.command(
        commands=[
            os.environ["ALERT"],
            change_layout(os.environ["ALERT"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def alert(client: Client, message: Message, callback: CallbackQuery = None):
    """
    Asynchronous function that allows users to subscribe or unsubscribe from receiving alert notifications.

    Parameters:
        - client (Client): An instance of the Client class representing the Telegram client.
        - message (Message): The Telegram message object that triggered the function.
        - callback (CallbackQuery, optional): The Telegram callback query object, if the function is triggered from a callback. Default is None.

    Raises:
        - PermissionError: If the user does not have the required permissions to use the command.
        - BadRequest: If there is a bad request error while sending the message.
        - FloodWait: If there is a flood wait time imposed by the Telegram API.
        - Exception: If an error occurs during execution.

    Note:
        - The function allows users to enable or disable alert notifications through the use of inline keyboards in a private chat.
        - Users can subscribe to receive alert notifications by clicking on the f"{TG_Emoji_Map.BELL} Вкл." button in the inline keyboard.
        - Users can unsubscribe from receiving alert notifications by clicking on the f"{TG_Emoji_Map.NO_BELL} Викл." button in the inline keyboard.
        - The function checks the user's subscription status in the SQLite database and updates it accordingly when the user clicks on the buttons.
    """
    try:
        user_id = int(get_tg_info(message, callback))

        # Check if the user has the required permissions to use the command
        if not (is_me(str(user_id)) or await get_info(str(user_id))):
            raise PermissionError()

        # Check if the function is triggered in a private chat
        if not await check_private_chat(client, message, callback):
            return

        # Define the inline keyboard markup with the "Enable" or "Disable" button based on the user's subscription status
        with connect(Dict_Map.FILES["database"]) as conn:
            cursor = conn.cursor()

            if callback:
                # Handle the user's callback data to update the subscription status
                match callback.data:
                    case "alert_on":
                        query = "INSERT INTO alert_users (ID) VALUES (?)"
                        switch_text = "вимкнути"
                        reply_markup = Markup_Map.ALERT_OFF
                    case "alert_off":
                        query = "DELETE FROM alert_users WHERE ID = ?"
                        switch_text = "увімкнути"
                        reply_markup = Markup_Map.ALERT_ON

                cursor.execute(query, (user_id,))
                conn.commit()

            else:
                query = "SELECT * FROM alert_users WHERE ID = ?"
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                if result:
                    switch_text = "вимкнути"
                    reply_markup = Markup_Map.ALERT_OFF
                else:
                    switch_text = "увімкнути"
                    reply_markup = Markup_Map.ALERT_ON

        # Send the inline keyboard to the user to subscribe or unsubscribe from alerts
        text = bold_text(
            f"{TG_Emoji_Map.POINT_DOWN} За допомогою кнопки нижче ви можете {switch_text} сповіщення про повітряну тривогу"
        )
        if callback:
            await callback.message.edit_text(text, reply_markup=reply_markup)
        else:
            await client.send_message(
                user_id, text, reply_markup=reply_markup, reply_to_message_id=message.id
            )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            badrequest=True,
            floodwait=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client, message=message, callback=callback, badrequest=True
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_message(
    filters.command(
        commands=[
            os.environ["URL_SHORTENER"],
            change_layout(os.environ["URL_SHORTENER"]),
        ],
        prefixes=[PREFIX, change_layout(PREFIX)],
    )
)
async def url_shortener(client: Client, message: Message):
    """
    Shortens the URL found in the given message and provides short URL options.

    Parameters:
        - client (Client): The Telegram client used to interact with the Telegram API.
        - message (Message): The incoming message containing the URL to be shortened.

    Raises:
        - PermissionError: If the user does not have the required permissions to use the command.
        - IndexError: If the URL is not found in the message.
        - ValueError: If there is an issue with URL extraction or shortening.

    Note:
        - The function uses the URLExtract library to find the URL in the message text.
        - It provides three options for shortening the URL using different URL shortening services (TinyURL, is.gd, and dagd).
        - The short URL options are displayed with corresponding numeric codes as inline keyboard buttons.
        - If the user clicks on one of the buttons, they will be redirected to the corresponding short URL.
        - If the user clicks on the "Delete" button, the bot will delete the message with the short URL options.
    """
    try:
        user_id = get_tg_info(message)

        # Check user permissions
        if not (is_me(user_id) or await get_info(user_id)):
            raise PermissionError()

        # Extract the URL from the message
        if message.reply_to_message:
            text = message.reply_to_message.text or message.reply_to_message.caption
            text = text.html or ""
        else:
            text = message.text or message.caption
            text = text.html or ""

        # Extract the first URL found in the text using URLExtract library
        long_url = URLExtract().find_urls(text)[0]

        # Shorten the URL using three different URL shortening services
        url_shortener = {
            num_to_emoji(i): link
            for i, link in enumerate(
                [
                    Shortener().tinyurl.short(long_url),
                    Shortener().isgd.short(long_url),
                    Shortener().dagd.short(long_url),
                ],
                start=1,
            )
        }.items()

        # Send the short URL options to the chat with inline keyboard buttons
        await client.send_message(
            message.chat.id,
            reply_to_message_id=message.id,
            text=bold_text(
                "\n\n".join(f"{k}) <CODE>{v}</CODE>" for k, v in url_shortener)
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text=k, url=v) for k, v in url_shortener],
                    [Buttons_Map.DELETE_FULL],
                ]
            ),
        )

    except PermissionError:
        await send_exception(client=client, message=message, permissionerror=True)
    except (IndexError, AttributeError):
        await send_exception(
            client=client,
            message=message,
            error=f"{os.environ['URL_SHORTENER']} {Dict_Map.ERRORS['IndexError']['URL_SHORTENER']}",
            index_error=True,
        )
    except ValueError as error:
        await send_exception(
            client=client, message=message, error=error, badrequest=True
        )
    except Exception as error:
        await send_exception(client=client, message=message, error=error)


async def personal_data_agreement(
    client: Client, message: Message, callback: CallbackQuery
):
    """
    Handle personal data agreement for a user.

    Args:
        client (Client): The Telegram client.
        message (Message): The message object.
        callback (CallbackQuery): The callback query object.
    """
    try:
        # Retrieve user_id using the get_tg_info function
        user_id = get_tg_info(message, callback)

        # Retrieve personal_data_agreement status for the user from the database
        personal_data_agree = await get_info(user_id, DB_Map.PERSONAL_DATA_AGREEMENT)

        # Check if the user is authorized (me) or has a valid user_id
        if not (is_me(user_id) or await get_info(user_id, DB_Map.NAME)):
            raise PermissionError()

        # Handle callback data
        match callback.data:
            case "Personal_Data_Agree":
                if personal_data_agree == DB_Map.AGREED:
                    await callback.message.delete()
                else:
                    # Connect to the SQLite database
                    with connect(Dict_Map.FILES["database"]) as conn:
                        # Create a cursor object to execute SQL commands
                        cursor = conn.cursor()

                        # Update the personal_data_agreement status for the user in the database
                        update_query = f"UPDATE users SET {DB_Map.PERSONAL_DATA_AGREEMENT} = ? WHERE {DB_Map.ID} = ?"
                        cursor.execute(update_query, (DB_Map.AGREED, user_id))
                        conn.commit()

                        # Send a response to the callback query indicating that the data has been updated
                        await callback.answer(Text_Map.DATA_UPDATED)
                        await callback.message.delete()

            case "Personal_Data_Agreement":
                # Show full personal data agreement text
                reply_markup = callback.message.reply_markup
                reply_markup.inline_keyboard[0].pop(1)
                await callback.message.edit_text(
                    text=Text_Map.PERSONAL_DATA_AGREEMENT,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True,
                )

    except PermissionError:
        await send_exception(
            client=client, message=message, callback=callback, permissionerror=True
        )
    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=message,
            error=time_to_wait.value,
            floodwait=True,
            badrequest=True,
            callback=callback,
        )
    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error=Text_Map.REVERSED_POINT,
            callback=callback,
            badrequest=True,
        )
    except Exception as error:
        await send_exception(
            client=client, message=message, error=error, callback=callback
        )


@app.on_callback_query()
async def callback_buttons(client: Client, callback: CallbackQuery):
    """
    Process various callback data received from inline keyboards and call corresponding functions to handle them.

    Args:
        client (Client): The Telethon client instance.
        callback (CallbackQuery): The callback query received from the inline keyboard.

    Raises:
        FloodWait: If the bot is being flooded with requests and needs to wait before processing more.
        BadRequest: If the received callback data is not valid.
        Forbidden: If the bot doesn't have enough rights to perform the requested action.
        Exception: For any other unexpected error.
    """
    try:
        match callback.data:
            case "start_main":
                await start(client, callback.message, callback)

            case "contact_information":
                await callback.message.edit_text(
                    bold_text(
                        "\n\n".join(
                            f"{k}  <CODE>{v}</CODE>"
                            for k, v in Dict_Map.CONTACT_INFORMATION.items()
                        )
                    ),
                    reply_markup=Markup_Map.CONTACT_INFORMATION,
                )

            case "commands_list":
                await commands_list(client, callback.message, callback)

            case "delete_bot_message":
                await callback.message.delete()

            case "delete_full_message":
                await delete_full_message(client, callback.message)

            case "lessons":
                await callback.message.edit_text(
                    Text_Map.SELECT_ITEM, reply_markup=Markup_Map.LESSONS
                )

            case subject if subject in Dict_Map.SUBJECTS:
                lesson_info = Dict_Map.SUBJECTS.get(subject)
                if isinstance(lesson_info, list):
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text=person.get(TG_Emoji_Map.BUST_IN_SILHOUETTE),
                                    callback_data=f"{subject}_teacher{i}",
                                )
                            ]
                            for i, person in enumerate(lesson_info)
                        ]
                        + [Buttons_Map.BACK_LESSONS]
                    )
                    await callback.message.edit_text(
                        Text_Map.SELECT_ITEM, reply_markup=reply_markup
                    )
                elif isinstance(lesson_info, dict):
                    text = f"{subject}\n\n"
                    text += "\n\n".join([f"{k} {v}" for k, v in lesson_info.items()])

                    reply_markup = (
                        Markup_Map.BACK_LESSONS_NUMBER
                        if has_number(text)
                        else Markup_Map.BACK_LESSONS
                    )

                    await callback.message.edit_text(
                        bold_text(text),
                        reply_markup=reply_markup,
                        disable_web_page_preview=True,
                    )
                else:
                    await callback.answer(text=Text_Map.NO_RESULTS)

            case teacher_info if "_teacher" in teacher_info:
                callback_parts = teacher_info.split("_teacher")
                lesson = callback_parts[0]
                lesson_info = Dict_Map.SUBJECTS.get(lesson)
                if lesson_info:
                    try:
                        selected_person = lesson_info[int(callback_parts[1])]

                        text = f"{lesson}\n\n"
                        text += "\n\n".join(
                            [f"{k} {v}" for k, v in selected_person.items()]
                        )

                        reply_markup = (
                            Markup_Map.BACK_LESSONS_NUMBER
                            if has_number(text)
                            else Markup_Map.BACK_LESSONS
                        )

                        await callback.message.edit_text(
                            bold_text(text),
                            reply_markup=reply_markup,
                            disable_web_page_preview=True,
                        )

                    except IndexError:
                        await callback.answer(text=Text_Map.NO_RESULTS)
                else:
                    await callback.answer(text=Text_Map.NO_RESULTS)

            case data if data.endswith("_s"):
                teacher_name = data[:-2]
                if teacher_name in Dict_Map.PEOPLE_MAP:
                    teacher_info = Dict_Map.PEOPLE_MAP[teacher_name]
                    text = "\n\n".join([f"{k} {v}" for k, v in teacher_info.items()])
                    reply_markup = (
                        Markup_Map.BACK_SEARCH_AGAIN_NUMBER
                        if has_number(text)
                        else Markup_Map.BACK_SEARCH_AGAIN
                    )

                    await callback.message.edit_text(
                        bold_text(text),
                        reply_markup=reply_markup,
                        disable_web_page_preview=True,
                    )
                else:
                    raise Exception(Text_Map.NO_RESULTS)

            case data if data == "search_again" or data.startswith("search_page_"):
                await search_teacher(client, callback.message, callback)

            case data if data.startswith("page_counter_"):
                await callback.answer(
                    text=f"Cторінка {data.split('page_counter_', 1)[1]}"
                )

            case "get_number":
                text = callback.message.text or callback.message.caption

                def extract_info(pattern: str) -> str:
                    """
                    Extracts information from text using a regular expression pattern.

                    Args:
                        pattern (str): The regular expression pattern for extracting information from text.

                    Returns:
                        str: Extracted information if found, an empty string otherwise.

                    Description:
                        This function utilizes a regular expression pattern to search for information within a given text.
                        It returns the captured group (group 1) if the pattern matches, otherwise, it returns an empty string.
                    """
                    # Search for information using the provided regular expression pattern
                    info = re.search(pattern, text)

                    # Return the captured group (group 1) if the pattern matches, otherwise, return an empty string
                    return info.group(1) if info else ""

                first_name = extract_info(
                    rf"{TG_Emoji_Map.BUST_IN_SILHOUETTE} (.+?)\n\n"
                )
                subject = extract_info(
                    rf"(.*?)\n\n{TG_Emoji_Map.BUST_IN_SILHOUETTE} (.+?)"
                )
                number = extract_info(rf"{TG_Emoji_Map.TELEPHONE_RECEIVER} ([\d\s+-]+)")

                if first_name and number:
                    await client.send_contact(
                        callback.message.chat.id,
                        first_name=first_name,
                        last_name=subject,
                        phone_number=number,
                        reply_markup=Markup_Map.DELETE,
                    )
                    await callback.answer(text=Text_Map.GOOD_RESULTS)
                else:
                    await callback.answer(text=Text_Map.NO_RESULTS)

            case data if any(
                text in data
                for text in [
                    Text_Map.DATA_SEARCH_SEP,
                    "search_column_",
                    "db_s",
                    "db_r",
                    "del_r",
                ]
            ) or data.endswith("_c") or data == "data_search_main":
                await data_search(client, callback.message, callback)

            case data if data in [
                f"add_role_{DB_Map.ADMIN}",
                f"add_role_{DB_Map.STAFF}",
                f"add_role_{DB_Map.TEACHER}",
                f"add_role_{DB_Map.STUDENT}",
                "add_info_main",
            ] or data.startswith(("edit_column_", "add_classroom_")):
                await add_info(client, callback.message, callback)

            case data if data.startswith("symbols_help_"):
                await help(client, callback.message, callback)

            case data if data.startswith(Text_Map.HELP_TEXT):
                back = data[len(Text_Map.HELP_TEXT) :]
                reply_markup = InlineKeyboardMarkup(
                    Buttons_Map.SYMBOLS_HELP
                    + [
                        [
                            InlineKeyboardButton(
                                text=Text_Map.MAIN, callback_data=back
                            ),
                            Buttons_Map.DELETE_FULL,
                        ]
                    ]
                )

                await callback.message.edit_text(
                    text=bold_text(
                        f"{TG_Emoji_Map.QUESTION} {Dict_Map.SYMBOLS_HELP[Text_Map.HELP_TEXT]}\n\n{Text_Map.SELECT_ITEM}"
                    ),
                    reply_markup=reply_markup,
                    disable_web_page_preview=True,
                )

            case "me_again":
                await me(client, callback.message, callback)

            case "now_is_again":
                await now_is(client, callback.message, callback)

            case data if any(
                text in data for text in [f"_{TG_Emoji_Map.PAGE_FACING_UP}_", "se_s"]
            ) or data.startswith("send_column_"):
                await send(client, callback.message, callback)

            case data if data.startswith("who_is_this"):
                await who_is_this(client, callback.message, callback)

            case "weather_again":
                await weather(client, callback.message, callback)

            case "get_timetable" | "get_timetable_week":
                await get_timetable(client, callback.message, callback)

            case "class_books_list":
                text = generate_list(
                    user_classroom=await get_info(
                        get_tg_info(callback), DB_Map.CLASSROOM
                    ),
                    dictionary=Dict_Map.CLASS_BOOKS,
                )

                if text:
                    await callback.message.edit_text(
                        bold_text(f"{Text_Map.BOOKS}\n\n{text}"),
                        reply_markup=Markup_Map.MARKUP_MAIN_BUTTON,
                        disable_web_page_preview=True,
                    )
                else:
                    await send_exception(
                        client=client,
                        message=callback.message,
                        error=Text_Map.NO_RESULTS,
                        callback=callback,
                        badrequest=True,
                    )

            case "get_message_get" | "get_message_del":
                await get_message(client, callback.message.reply_to_message, callback)

            case data if data.startswith("MV5yNR9N0BKvheO"):
                await c(client, callback.message, callback)

            case "maze_left" | "maze_right" | "maze_up" | "maze_down":
                try:
                    user_data = maze_maps[get_tg_info(callback=callback)]
                    new_x, new_y = user_data["x"], user_data["y"]

                    match callback.data:
                        case "maze_left":
                            new_x -= 1
                        case "maze_right":
                            new_x += 1
                        case "maze_up":
                            new_y -= 1
                        case "maze_down":
                            new_y += 1

                    if (
                        new_x < 0
                        or new_x > 2 * MAZE_COLS - 2
                        or new_y < 0
                        or new_y > MAZE_ROWS * 2 - 2
                    ):
                        raise ValueError
                    if user_data["map"][new_x + new_y * (MAZE_COLS * 2 - 1)]:
                        raise ValueError

                    user_data["x"], user_data["y"] = new_x, new_y

                    if new_x == MAZE_COLS * 2 - 2 and new_y == MAZE_ROWS * 2 - 2:
                        await callback.answer(
                            text=f"Вы виграли {TG_Emoji_Map.THUMBSUP}", show_alert=True
                        )
                        raise KeyError

                except ValueError:
                    await callback.answer(
                        text="Ви вдарилися об стінку ☹️", show_alert=True
                    )
                    return
                except KeyError:
                    await maze(client, callback.message, callback)
                    return

                await callback.message.edit_text(
                    text=get_map_str(user_data["map"], (new_x, new_y)),
                    reply_markup=Markup_Map.MAZE,
                )

            case "password_generator":
                await password_generator(client, callback.message, callback)

            case "school_day_true" | "school_day_false" | "school_day_default":
                global school_day
                id = callback.from_user.id
                if bad_intentions(DB_Map.STAFF, await get_info(id), is_me(id)):
                    raise PermissionError()

                match data:
                    case "school_day_true":
                        school_day = True
                    case "school_day_false":
                        school_day = False
                    case "school_day_default":
                        school_day = "default"

                await now_is(client, callback.message, callback)
                await callback.answer(Text_Map.DATA_UPDATED)

            case data if data[1:].startswith(("detec:", "signa:", "detai:")):
                await virustotal(client, callback.message, callback)

            case "alert_on" | "alert_off":
                await alert(client, callback.message, callback)

            case "maze_delete":
                maze_maps.pop(get_tg_info(callback=callback))
                await delete_full_message(client, callback.message)

            case "lesson_links_list":
                text = generate_list(
                    user_classroom=await get_info(
                        get_tg_info(callback), DB_Map.CLASSROOM
                    ),
                    dictionary=Dict_Map.LESSON_LINKS,
                )

                if text:
                    await callback.message.edit_text(
                        bold_text(f"{TG_Emoji_Map.LINK} Посилання \n\n{text}"),
                        reply_markup=Markup_Map.MARKUP_MAIN_BUTTON,
                        disable_web_page_preview=True,
                    )
                else:
                    await send_exception(
                        client=client,
                        message=callback.message,
                        error=Text_Map.NO_RESULTS,
                        callback=callback,
                        badrequest=True,
                    )

            case "Personal_Data_Agree" | "Personal_Data_Agreement":
                await personal_data_agreement(client, callback.message, callback)

            case _:
                raise KeyError(callback.data)

    except FloodWait as time_to_wait:
        await send_exception(
            client=client,
            message=callback.message,
            error=time_to_wait.value,
            badrequest=True,
            floodwait=True,
            callback=callback,
        )
    except PermissionError:
        await send_exception(
            client=client,
            message=callback.message,
            callback=callback,
            permissionerror=True,
        )
    except BadRequest:
        await send_exception(
            client=client, message=callback.message, callback=callback, badrequest=True
        )
    except Forbidden:
        await send_exception(
            client=client,
            message=callback.message,
            callback=callback,
            error=f"Мені не вистачає прав для виконання цієї дії {TG_Emoji_Map.CONFUSED}",
        )
    except KeyError as error:
        await send_exception(
            client=client,
            message=callback.message,
            error=error,
            callback=callback,
            to_me=True,
        )
    except Exception as error:
        await send_exception(
            client=client, message=callback.message, error=error, callback=callback
        )


def seconds_converter(seconds: int, recess: bool = False, alert: bool = False) -> str:
    """
    Converts a given number of seconds into a human-readable format representing years, months, days, hours, minutes, and seconds.

    Parameters:
        - seconds (int): The number of seconds to convert.
        - recess (bool, optional): If True, the converted time is represented as the remaining time. If False (default), the converted time is represented as the elapsed time.
        - alert (bool, optional): If True, an alert message is included in the output. This parameter is useful to indicate that the conversion is ongoing or to display an alert message. Default is False.

    Returns:
        - str: A human-readable representation of the converted time.

    Raises:
        - Exception: If an error occurs during the conversion process.

    Note:
        - The function uses approximate conversions based on the following factors:
            - 1 month = 30 days
            - 1 year = 12 months
        - If 'recess' is True, the function represents the converted time as remaining time, otherwise as elapsed time.
        - If 'ALERT' is True, the function includes an alert message at the beginning of the output.

    Example:
        seconds_converter(3666)  # Returns "Зачекайте 1 годину, 1 хвилину, 6 секунд"
    """
    try:
        # If recess is True, round the seconds up to the nearest multiple of 10
        if recess:
            seconds = int((seconds // 10) * 10) + 10

        # If seconds is less than or equal to 0, return an error message
        if seconds <= 0:
            return f"{TG_Emoji_Map.NO_IDEA} Я не можу вести відлік від {seconds}"

        # Initialize an empty list to store the time parts
        time_parts = []

        # Define the time units and their corresponding seconds
        time_units = [
            ("років", 31104000),  # 60 * 60 * 24 * 30 * 12
            ("місяців", 2592000),  # 60 * 60 * 24 * 30
            ("днів", 604800),  # 60 * 60 * 24 * 7
            ("годин", 3600),  # 60 * 60
            ("хвилин", 60),
            ("секунд", 1),
        ]

        # Loop through the time units in descending order
        for unit_name, unit_seconds in time_units:
            # If the remaining seconds is greater than or equal to the current unit, calculate the unit value and update the remaining seconds
            if seconds >= unit_seconds:
                unit_value, seconds = divmod(seconds, unit_seconds)
                time_parts.append(f"{unit_value} {unit_name}")

        # Construct the output string based on the recess and alert parameters
        return f"{', залишилося' if recess else 'Зачекайте' if not alert else ''} {' : '.join(time_parts) if recess else ', '.join(time_parts)}"

    except Exception as error:
        return str(error)


async def send_exception(
    client: Client,
    message: Message,
    error: Exception = None,
    markup: InlineKeyboardMarkup = Markup_Map.DELETE_FULL,
    callback: CallbackQuery = None,
    badrequest: bool = False,
    index_error: bool = False,
    floodwait: bool = False,
    to_me: bool = False,
    permissionerror: bool = False,
) -> None:
    """
    Send error messages to users or the bot owner.

    Parameters:
        client (Client): The Telethon client instance.
        message (Message): The original message that triggered the exception.
        error (Exception, optional): The exception or error to handle and send. Defaults to None.
        markup (InlineKeyboardMarkup, optional): The inline keyboard markup to include in the error message. Defaults to Markup_Map.DELETE_FULL.
        callback (CallbackQuery, optional): The callback query if the error is associated with a callback. Defaults to None.
        badrequest (bool, optional): A flag indicating if the error is due to a bad request. Defaults to False.
        index_error (bool, optional): A flag indicating if the error is an IndexError. Defaults to False.
        floodwait (bool, optional): A flag indicating if the error is a FloodWait error. Defaults to False.
        to_me (bool, optional): A flag indicating if the error message should be sent to the bot owner. Defaults to False.
        permissionerror (bool, optional): A flag indicating if the error is due to insufficient permissions. Defaults to False.
    """
    try:
        if floodwait:
            # Convert flood wait time to a human-readable format
            error = seconds_converter(int(error))
        elif permissionerror:
            # Set the error message for insufficient permissions
            error = Dict_Map.ERRORS["PermissionError"]

        if badrequest and not error:
            # Set a default error message for bad request
            error = Text_Map.NO_CHANGES

        mono_error = f"{TG_Emoji_Map.X} <code>{error}</code>"

        if to_me:
            msg = callback or message
            user_info = "\n\n".join(
                f"{k} <code>{v}</code>"
                for k, v in info_simple_user(msg.from_user).items()
            )
            # Send the exception message to the bot owner
            await client.send_message(
                os.environ["YOUR_TELEGRAM_ACCOUNT_ID"],
                bold_text(
                    f"{mono_error}\n\n{message.text}{Text_Map.SPACER}{user_info}"
                ),
                reply_markup=markup,
                disable_web_page_preview=True,
            )
            return

        if badrequest:
            # Handle bad request error
            if callback:
                if len(error) > 20 and error != Text_Map.NO_CHANGES:
                    await callback.message.edit_text(
                        mono_error, reply_markup=callback.message.reply_markup
                    )
                else:
                    await callback.answer(show_alert=True, text=error)
            else:
                await client.send_message(
                    message.chat.id,
                    bold_text(error),
                    reply_markup=markup,
                    disable_web_page_preview=True,
                    reply_to_message_id=message.id,
                )
        else:
            if not index_error:
                # Handle other exceptions
                if callback:
                    await callback.answer(show_alert=True, text=error)
                else:
                    await client.send_message(
                        message.chat.id,
                        mono_error,
                        reply_markup=markup,
                        disable_web_page_preview=True,
                        reply_to_message_id=message.id,
                    )
            else:
                # Handle IndexError
                if callback:
                    await callback.message.edit_text(
                        bold_text(
                            f"{TG_Emoji_Map.X} {Dict_Map.ERRORS['IndexError']['try']}<code>{PREFIX}{error}"
                        ),
                        reply_markup=callback.message.reply_markup,
                    )
                else:
                    await client.send_message(
                        message.chat.id,
                        bold_text(
                            f"{TG_Emoji_Map.X} {Dict_Map.ERRORS['IndexError']['try']}<code>{PREFIX}{error}"
                        ),
                        reply_markup=markup,
                        disable_web_page_preview=True,
                        reply_to_message_id=message.id,
                    )

    except BadRequest:
        await send_exception(
            client=client,
            message=message,
            error=Text_Map.REVERSED_POINT,
            callback=callback,
            badrequest=True,
        )
    except AttributeError:
        await send_exception(
            client=client,
            message=message,
            error=error.__str__(),
            markup=markup,
            callback=callback,
            badrequest=badrequest,
            index_error=index_error,
            floodwait=floodwait,
            permissionerror=permissionerror,
            to_me=to_me,
        )
    except Exception as error:
        await send_exception(client=client, message=message, error=error, to_me=True)


def format_phone_number(number: str) -> str:
    """
    This function takes a phone number in string format and returns the formatted international version of the number using the `phonenumbers` library.

    Parameters:
    - number (str): The phone number to format.

    Returns:
    - str: The formatted international version of the phone number.
    """
    return phonenumbers.format_number(
        phonenumbers.parse(number, "ID"), phonenumbers.PhoneNumberFormat.INTERNATIONAL
    )


async def get_info(
    id: str, search_column: str | tuple = DB_Map.ROLE, check_agreement: str = False
) -> str | tuple | None:
    """
    Retrieves information from the SQLite database based on the provided ID and search parameters.

    Args:
        id (str): The identifier used to retrieve information from the database.
        search_column (str | tuple, optional): The column(s) to search in the database. Defaults to DB_Map.ROLE.
        check_agreement (str, optional): Specifies whether an agreement check is required. Defaults to False.

    Returns:
        str | tuple | None: Retrieved information from the database, or None if no information is found.
    """
    # Connect to the SQLite database
    with connect(Dict_Map.FILES["database"]) as conn:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # Determine if the agreement check is required
        if check_agreement:
            check_agreement = (DB_Map.ROLE in search_column) if not is_me(id) else False

        # Determine if the search column is a tuple
        search_is_tuple = isinstance(search_column, tuple)

        # Construct the SQL query to select the specified column(s) based on the provided ID
        if search_is_tuple:
            columns = ", ".join(search_column)
            if check_agreement:
                # Include the personal data agreement column in the query
                query = f"SELECT {columns}, {DB_Map.PERSONAL_DATA_AGREEMENT} FROM users WHERE {DB_Map.ID} = ?"
            else:
                query = f"SELECT {columns} FROM users WHERE {DB_Map.ID} = ?"
        else:
            if check_agreement:
                # Include the personal data agreement column in the query
                query = f"SELECT {search_column}, {DB_Map.PERSONAL_DATA_AGREEMENT} FROM users WHERE {DB_Map.ID} = ?"
            else:
                query = f"SELECT {search_column} FROM users WHERE {DB_Map.ID} = ?"

        # Execute the query with the provided ID as a parameter
        cursor.execute(query, (id,))

        # Fetch the first result from the query
        result = cursor.fetchone()

        if result:
            # Extract the user information from the result if it exists
            if check_agreement:
                # If the personal data agreement column is included in the query, check the agreement status
                if result[-1] != DB_Map.AGREED:
                    # If the agreement status is not "Agreed", set the result to None or a tuple of None values
                    result = (None,) * len(search_column) if search_is_tuple else None
                    # Send a message to the user about the personal data agreement
                    await app.send_message(
                        id,
                        Text_Map.PERSONAL_DATA_AGREEMENT_SHORT,
                        reply_markup=Markup_Map.PERSONAL_DATA_AGREEMENT,
                    )
                else:
                    # If the agreement status is "Agreed", extract the user information without the agreement column
                    result = result[:-1]

            if result and len(result) == 1:
                # If the result contains only one value, extract it as a single value
                result = result[0]

        else:
            result = (None,) * len(search_column) if search_is_tuple else None

    # Return the retrieved user information
    return result


def is_me(id: str | int) -> bool:
    """
    This function checks if the provided ID matches the Telegram account ID configured in the `os.environ` file.

    Parameters:
    - id (str): The ID to compare with the configured Telegram account ID.

    Returns:
    - bool: True if the ID matches the configured Telegram account ID, otherwise False.
    """
    return str(id) == os.environ["YOUR_TELEGRAM_ACCOUNT_ID"]


def clean_html_tags(text: str) -> str:
    """
    Removes HTML tags from a given text.

    Parameters:
    - text (str): The text to clean.

    Returns:
    - str: The cleaned text with HTML tags removed.
    """
    return re.sub(
        r"</?code>|</?b>|</?u>|</?i>|</?s>|</?pre>|</?spoiler>|</?a>|</?a(?:\s+href=[\"'][^\"']+['\"])?\s*>",
        "",
        text,
    )


async def username2id(username: str) -> str | None:
    """
    Retrieves the ID of a user based on their username.

    Parameters:
        - username (str): The username of the user.

    Returns:
        - str or None: The ID of the user if found, otherwise None.

    Raises:
        - Exception: If the username is not found.
    """
    try:
        # Replace any special characters in the username with their URL-encoded equivalents
        username = replace_tme(username)

        # Check if the username is valid
        if not is_username(username):
            raise BadRequest

        # Get the user object based on the username
        tmp_user = await app.get_users(username)

        # Return the ID of the user as a string
        return str(tmp_user.id)

    except BadRequest:
        # If the username is not found, raise an exception with an appropriate error message
        raise Exception(Text_Map.USERNAME_NOT_FOUND.format(username))


def get_tg_info(
    message: Message = None, callback: CallbackQuery = None, username: bool = False
) -> str | tuple:
    """
    Retrieve Telegram user information from a Message object or a CallbackQuery object.

    Parameters:
    - message (Message): The Message object containing user information.
    - callback (CallbackQuery, optional): The CallbackQuery object containing user information. Default is None.
    - username (bool, optional): If True, includes the username in the returned value. Default is False.

    Returns:
    - str or tuple: The user ID if username is False, or a tuple of user ID and username if username is True.
    """
    # Check if callback exists, if not use message
    user = callback or message
    user = user.from_user

    # Get the user ID as a string
    user_id = str(user.id)

    # Get the username as a string, if it exists, otherwise use an empty string
    user_username = str(user.username) if user.username else ""

    # Return the user ID if username is False, otherwise return a tuple of user ID and username
    return (user_id, user_username) if username else user_id


def has_emoji(text: str) -> bool:
    """
    This function checks if the provided text contains any emoji characters.

    Parameters:
    - text (str): The text to check for emoji characters.

    Returns:
    - bool: True if the text contains at least one emoji character, otherwise False.
    """
    return any(is_emoji(char) for char in text)


def is_user_id(id: str | int) -> str | None:
    """
    Check if the provided string or integer is a valid user ID consisting of 9 to 10 digits.

    Parameters:
    - id (str | int): The string or integer to check for a valid user ID.

    Returns:
    - str or None: The valid user ID if the input is a valid user ID, otherwise None.
    """
    return re.match(r"^\d{9,10}$", str(id))


def has_number(text: str) -> str | None:
    """
    This function searches for a phone number in the provided text and returns it if found.

    Parameters:
    - text (str): The text to search for a phone number.

    Returns:
    - str or None: The found phone number if it exists, otherwise None.
    """
    return (
        number_match := re.search(
            rf"{TG_Emoji_Map.TELEPHONE_RECEIVER} ([\d\s+-]+)", clean_html_tags(text)
        )
    ) and number_match.group(1).strip()


def is_username(username: str) -> str | None:
    """
    This function checks if the provided string is a valid Telegram username.

    Parameters:
    - username (str): The string to check for username validity.

    Returns:
    - str or None: The provided username if it is valid, otherwise None.
    """
    return re.match(r"^[a-zA-Z0-9_@]{1,32}$", username)


def get_greeting() -> str:
    """
    Returns a greeting based on the current time of day.

    Returns:
        str: The appropriate greeting.
    """
    # Find the appropriate greeting based on the current hour
    return next(
        (
            message
            for time_range, message in Dict_Map.GREETINGS.items()
            if datetime.now().time().hour in time_range
        ),
        "Доброї ночі",
    )


def delete_files(directory: str = "downloads", result_filename: str = None):
    """
    Deletes files in a specified directory or a single file.

    Parameters:
        - directory (str, optional): The directory path where the files are located. Default is "downloads".
        - result_filename (str, optional): The path of a specific file to delete. If provided, only this file will be deleted. Default is None.

    Raises:
        - Exception: If an error occurs during the file deletion process.

    Example:
        delete_files("downloads")  # Deletes all files in the "downloads" directory
        delete_files(result_filename="output.txt")  # Deletes a specific file named "output.txt"
    """
    try:
        # Check if a specific file is provided
        if result_filename:
            # Check if the file exists
            if os.path.exists(result_filename):
                # Delete the file
                os.remove(path=result_filename)
        else:
            # Check if the directory exists
            if os.path.exists(directory):
                # Recursively delete the directory and its contents
                rmtree(directory)
    except:
        # Ignore any exceptions that occur during the file deletion process
        return


def recess_time(
    start_time: time, current_time: time, now_date: datetime = datetime.now().date()
) -> str:
    """
    Calculates the remaining time between a given start time and the current time, represented in a human-readable format.

    Parameters:
        - start_time (time): The start time.
        - current_time (time): The current time.
        - now_date (datetime): The date to be used for the time calculation. Defaults to the current date.

    Returns:
        - str: A human-readable representation of the remaining time.

    Example:
        recess_time(time(10, 0), time(11, 30))  # Returns "<b>Зачекайте 1 годину, 30 хвилин</b>"

    Note:
        - The function calculates the difference between the start time and the current time to determine the remaining time.
        - The remaining time is represented in a human-readable format, including hours and minutes.
    """
    return bold_text(
        seconds_converter(
            (
                datetime.combine(now_date, start_time)
                - datetime.combine(now_date, current_time)
            ).total_seconds(),
            recess=True,
        )
    )


def bad_intentions(t_user_role: str, user_role: str, user_is_me: bool) -> bool:
    """
    Check if the target user has bad intentions based on the requester's role and the target user's role.

    Parameters:
    - t_user_role (str): The role of the target user.
    - user_role (str): The role of the requesting user.
    - user_is_me (bool): A boolean value indicating whether the requesting user is the bot itself.

    Returns:
    - bool: True if the target user has bad intentions, False otherwise.
    """
    return (
        False
        if (user_role == DB_Map.ADMIN or user_is_me)
        else (
            (t_user_role == DB_Map.ADMIN and user_role == DB_Map.STAFF)
            or (
                t_user_role in [DB_Map.ADMIN, DB_Map.STAFF]
                and user_role == DB_Map.TEACHER
            )
            or (t_user_role == user_role)
            or (
                t_user_role in [DB_Map.ADMIN, DB_Map.STAFF, DB_Map.TEACHER]
                and user_role == DB_Map.STUDENT
            )
        )
    )


def num_to_emoji(text: str | int) -> str:
    """
    Converts numerical characters in a string to their corresponding emoji representations.

    Parameters:
        - text (str|int): The input text to convert.

    Returns:
        - str: The converted text with numerical characters replaced by emojis.

    Example:
        num_to_emoji("Hello 123")  # Returns "Hello 1️⃣2️⃣3️⃣"
    """
    return "".join(
        Dict_Map.NUM_TO_EMOJI.get(char, char) if char.isdigit() else char
        for char in str(text)
        .replace("100", TG_Emoji_Map.ONE_HUNDRED)
        .replace("10", TG_Emoji_Map.KEYCAP_TEN)
    )


def has_file(
    message: Message
) -> (
    Photo
    | Video
    | Audio
    | Dice
    | VideoNote
    | Voice
    | Document
    | Contact
    | Location
    | Animation
    | Venue
    | Sticker
    | Poll
    | bool
):
    """
    Checks if a message contains a file or media.

    Parameters:
        - message (Message): The message object to check.

    Returns:
        - Photo|Video|Audio|Dice|VideoNote|Voice|Document|Contact|Location|Animation|Venue|Sticker|bool: The message object if it contains a file or media, otherwise False.

    Note:
        - The function checks if the message has a media_group_id, photo, document, audio, video, contact, location, voice, dice, animation, venue, sticker, video_note, poll attribute.
        - If any of the attributes is present, it returns the corresponding object.
        - If none of the attributes is present, it returns False.
    """
    return (
        message.media_group_id
        or message.photo
        or message.document
        or message.audio
        or message.video
        or message.contact
        or message.location
        or message.voice
        or message.dice
        or message.animation
        or message.venue
        or message.sticker
        or message.video_note
        or message.poll
    )


def format_int_number(number: int) -> str:
    """
    Formats an integer number with thousands separators and returns it as a string.

    Parameters:
        - number (int): The integer number to be formatted.

    Returns:
        - str: The formatted number as a string.

    Example:
        number = 1000000
        formatted_number = format_int_number(number)
        print(formatted_number)  # Output: 1 000 000

    Note:
        The function uses the `babel_format_number` function from the `babel` library
        to format the number with the `en_US` locale. It then replaces the commas with
        spaces to provide a consistent formatting style.
    """
    return babel_format_decimal(number, locale="en_US").replace(",", " ")


def is_group_id(id: str | int) -> str | None:
    """
    Check if the provided string or integer is a valid group ID consisting of 13 digits.

    Parameters:
    - id (str | int): The string or integer to check for a valid group ID.

    Returns:
    - str or None: The valid group ID if the input is a valid group ID, otherwise None.
    """
    return re.match(r"^-?\d{13}$", str(id))


def is_school_day(
    day: datetime = datetime.today(), today_year: int = datetime.today().year
) -> bool:
    """
    Check whether the given date is a school day, considering holidays and weekends.

    Parameters:
    - day (datetime, optional): The date to check. Defaults to the current date obtained from datetime.today().
    - today_year (int, optional): The year of the date to check. Defaults to the current year obtained from datetime.today().year.

    Returns:
    - bool: True if the date is a school day, False otherwise.
    """

    # Define a nested function to check for holidays
    def check_holidays(day: datetime):
        return (
            # Check for various holiday date ranges and weekdays
            (
                not (
                    (
                        datetime(today_year, 10, 23)
                        <= day
                        <= datetime(today_year, 10, 29)
                    )  # Autumn holidays
                    or (
                        datetime(today_year, 12, 25)
                        <= day
                        <= datetime(today_year, 12, 31)
                    )  # Winter holidays
                    or (
                        datetime(today_year, 1, 1) <= day <= datetime(today_year, 1, 7)
                    )  # Winter holidays
                    or (
                        datetime(today_year, 3, 25)
                        <= day
                        <= datetime(today_year, 3, 31)
                    )  # Spring holidays
                    or (
                        datetime(today_year, 6, 1) <= day <= datetime(today_year, 8, 31)
                    )  # Summer holidays
                )
            )
            and 0 <= day.weekday() <= 4  # Weekday (Monday to Friday)
        )

    # Check if the provided day is the same as the current day
    if day.date() == datetime.today().date():
        # Use a default value if school_day is not specified
        return school_day if not school_day == "default" else check_holidays(day)
    else:
        # Check holidays for the provided day
        return check_holidays(day)


def is_school_time(current_time: time = datetime.today().time()) -> bool:
    """
    Check if the provided current_time falls within the school time range.

    Args:
        current_time (time, optional): The current time to check. Defaults to the current time when the function is called.

    Returns:
        bool: True if the current_time is within the school time range (from 9:00 AM to 2:30 PM), False otherwise.

    Example:
        current_time = time(11, 30)
        is_school_time(current_time) -> True
    """
    return time(0, 0) <= current_time <= time(15, 25)


def replace_tme(text: str) -> str:
    """
    Remove both "https://t.me/" and "t.me/" prefixes from a given text.

    Parameters:
        text (str): The text from which to remove the prefixes.

    Returns:
        str: The modified text with the prefixes removed.
    """
    return text.replace("https://t.me/", "").replace("t.me/", "")


def tomorrow_day(today: datetime = datetime.today()) -> datetime:
    """
    Calculate and return a datetime object representing the date and time of tomorrow.

    Parameters:
        today (datetime, optional): The reference date. Defaults to the current date and time.

    Returns:
        datetime: A datetime object representing tomorrow's date and time.
    """
    return today + relativedelta(days=1)


def generate_list(user_classroom: str, dictionary: dict) -> str:
    """
    Generate a formatted list of subjects, teachers, and hyperlinks (if applicable) based on the user's classroom.

    Args:
        user_classroom (str): The user's classroom.
        dictionary (dict): The dictionary containing the lesson information.

    Returns:
        str: The formatted list of subjects, teachers, and hyperlinks.
    """

    def get_formatted_item(number: int, subject: str, info: list) -> str:
        """
        Generate a formatted item for a subject, person, and link.

        Args:
            number (int): The number of the item.
            subject (str): The subject of the lesson.
            info (list): The information about the lesson.

        Returns:
            str: The formatted item.

        Notes:
            If info[1] exists and is a valid URL starting with 'https://' or 'https://', use it as the link
            If info[0] exists, use it as the person information
            If info[0] doesn't exist or is default, display 'Невідомий' as the person information
            If info[1] doesn't exist or is not a valid URL, the link will be an default string
            Join all the formatted strings with line breaks to create the final text
        """
        # Get the person information from the info list
        # If info list is empty or doesn't exist, set person to default string 'Невідомий'
        person = str(info[0]) if bool(info) else "Невідомий"

        # Generate the formatted item with the item number, subject, person, and link
        # Use the num_to_emoji function to convert the number to an emoji
        # Use the find_link_in_list function to find the link in the info list
        return f"{num_to_emoji(number)}) {subject} (<a href='{find_link_in_list(info)}'>{person}</a>)\n\n"

    # Initialize an empty string to store the formatted text
    text = ""

    # Check if the user_classroom is not empty
    if user_classroom:
        # Iterate through the items in the dictionary for the user_classroom
        # Start the item number from 1
        for number, (subject, lesson_info) in enumerate(
            dictionary.get(user_classroom, {}).items(), start=1
        ):
            # Check if the lesson_info is a tuple
            if isinstance(lesson_info, tuple):
                # Iterate through each info in the lesson_info tuple
                for info in lesson_info:
                    # Append the formatted item to the text string
                    text += get_formatted_item(number, subject, info)
            else:
                # Append the formatted item to the text string
                text += get_formatted_item(number, subject, lesson_info)

    # Return the formatted text
    return text


def find_link_in_list(lst: list) -> str:
    """
    Find and return the first valid link in a given list.

    Args:
        lst (list): The list to search for a valid link.

    Returns:
        str: The first valid link found in the list. If no valid link is found, an empty string is returned.
    """
    return next(
        (
            item
            for item in lst
            if isinstance(item, str)
            and re.fullmatch(
                r"^(https?://)?([a-z0-9]+([\-.][a-z0-9]+)*\.[a-z]{2,5})(:[0-9]{1,5})?(/.*)?$",
                item,
            )
        ),
        "",
    )


def split_command(text: str, command: str) -> str:
    """
    Splits a command from a text string and returns the part of the text after the command.

    Parameters:
    - text (str): The input text string.
    - command (str): The command to search for in the text.

    Returns:
    - str: The part of the text following the command.
    """
    # Check if the text starts with the prefix or with a modified version of the prefix
    prefix = PREFIX if text.startswith(PREFIX) else change_layout(PREFIX)

    # Check if the text starting from index 1 starts with the command or with a modified version of the command
    cmd = command if text[1:].startswith(command) else change_layout(command)

    # Check if the text starting from index 1 + the length of the command starts with the username or is empty
    username = (
        Text_Map.MY_USERNAME
        if text[(1 + len(command)) :].startswith(Text_Map.MY_USERNAME)
        else ""
    )

    # Split the text using the prefix, command, and username as the separator and return the second part
    return text.split(f"{prefix}{cmd}{username} ", maxsplit=1)[1]


async def delete_full_message(client: Client, message: Message) -> None:
    """
    Delete the given message and any related messages in a media group.

    Args:
        client (Client): The Telegram client instance.
        message (Message): The message to be deleted.
    """
    if message.media_group_id:
        # If the message belongs to a media group, get all the message IDs in the group
        message_ids = [
            msg.id for msg in await client.get_media_group(message.chat.id, message.id)
        ]
    else:
        # If the message does not belong to a media group, use the message ID directly
        message_ids = message.id

    # Delete all the identified message IDs
    await client.delete_messages(message.chat.id, message_ids=message_ids)

    if message.reply_to_message:
        # Recursively delete any related reply messages
        await delete_full_message(client, message.reply_to_message)


def info_phone(user: User) -> dict:
    """
    Get information about a user's phone number.

    Parameters:
    - user (User): The user for which to retrieve information.

    Returns:
    - dict: A dictionary containing phone number information.
    """
    return {
        TG_Emoji_Map.TELEPHONE_RECEIVER: format_phone_number(user.phone_number)
        if user.phone_number
        else Text_Map.NO_RESULTS2
    }


def info_mention(user: User) -> dict:
    """
    Get information about a user's mention name.

    Parameters:
    - user (User): The user for which to retrieve information.

    Returns:
    - dict: A dictionary containing mention information.
    """
    return {
        f"{TG_Emoji_Map.BUST_IN_SILHOUETTE} {user.mention}": user.last_name
        or Text_Map.FAKE_VOID
    }


def info_username(user: User) -> dict:
    """
    Get information about a user's username.

    Parameters:
    - user (User): The user for which to retrieve information.

    Returns:
    - dict: A dictionary containing username information.
    """
    return {
        f"{TG_Emoji_Map.CYCLONE} {'@' + user.username if user.username else Text_Map.NO_RESULTS2_MONO_FONT}": Text_Map.FAKE_VOID
    }


def info_id(user: User) -> dict:
    """
    Get information about a user's ID.

    Parameters:
    - user (User): The user for which to retrieve information.

    Returns:
    - dict: A dictionary containing ID information.
    """
    return {TG_Emoji_Map.ID: user.id}


def info_title(chat: Chat) -> dict:
    """
    Get information about a chat's title.

    Parameters:
    - chat (Chat): The chat for which to retrieve information.

    Returns:
    - dict: A dictionary containing chat title information.
    """
    return {TG_Emoji_Map.BUST_IN_SILHOUETTE: chat.title}


def info_chat_type(chat: Chat) -> dict:
    """
    Get information about a chat's type.

    Parameters:
    - chat (Chat): The chat for which to retrieve information.

    Returns:
    - dict: A dictionary containing chat type information.
    """
    return {TG_Emoji_Map.SPEECH_BALLOON: re.sub(r"^ChatType\.", "", str(chat.type))}


def info_forward_date(msg: Message) -> dict:
    """
    Get information about a message's forward date.

    Parameters:
    - msg (Message): The message for which to retrieve information.

    Returns:
    - dict: A dictionary containing forward date information.
    """
    return {TG_Emoji_Map.CALENDAR_SPIRAL: msg.forward_date}


def info_simple_user(user: User) -> dict:
    """
    Get a combination of simple user information.

    Parameters:
    - user (User): The user for which to retrieve information.

    Returns:
    - dict: A dictionary containing a combination of user information.
    """
    return {
        **info_mention(user),
        **info_id(user),
        **info_username(user),
        **info_phone(user),
    }


def is_private_chat(message: Message, callback: CallbackQuery = None) -> bool:
    """
    Checks if a message or callback query originates from a private chat.

    Args:
        message (Message): The message object received.
        callback (CallbackQuery, optional): The callback query object if available. Defaults to None.

    Returns:
        bool: True if the chat is private, False otherwise.

    Description:
        This function checks whether a message or callback query comes from a private chat.
        It takes the message or callback query and returns a boolean indicating if it's a private chat.

        If the chat is private, it returns True, indicating a private chat.
        If the chat is not private, it returns False, indicating a non-private chat.
    """
    # Use the original message for non-callback scenarios, otherwise, use the callback message
    msg = message if not callback else callback.message

    # Check if the chat type is private
    return str(msg.chat.type) == "ChatType.PRIVATE"


async def check_private_chat(
    client: Client, message: Message, callback: CallbackQuery = None
) -> bool:
    """
    Checks if a message or callback query originates from a private chat.

    Args:
        client (Client): The Telegram client instance.
        message (Message): The message object received.
        callback (CallbackQuery, optional): The callback query object if available. Defaults to None.

    Returns:
        bool: True if the chat is private, False otherwise.

    Description:
        This asynchronous function checks whether a message or callback query comes from a private chat.
        It takes the Telegram client, the message or callback query, and returns a boolean indicating if it's a private chat.

        If the chat is not private, it sends an exception message using the 'send_exception' function,
        providing details about the error and returns True to indicate that the check failed.

        If the chat is private, it returns False, indicating that the check was successful.
    """
    private_chat = is_private_chat(message, callback)

    # If not a private chat, send an exception message and return True
    if not private_chat:
        await send_exception(
            client=client,
            message=message,
            badrequest=True,
            error=Dict_Map.ERRORS["Only_private_chat"],
        )

    # Return False for a successful private chat check
    return private_chat


def unique_filename(file_name: str) -> str:
    """
    Generates a unique filename by appending the current timestamp.

    Args:
        file_name (str): The original filename or identifier.

    Returns:
        str: A unique filename incorporating the original name and current timestamp.

    Description:
        This function takes an original file name or identifier and appends a timestamp to create a unique filename.
        The timestamp includes the year, month, day, hour, minute, second, and microsecond to ensure uniqueness.
    """
    # Append the current timestamp to the original file name
    return f"{file_name}.{datetime.now().strftime('%Y.%m.%d %H.%M.%S.%f')}"


def format_lesson_time(start_time: time, end_time: time) -> str:
    """
    Formats the start and end times of a lesson into a string representation.

    Args:
        start_time (time): The start time of the lesson.
        end_time (time): The end time of the lesson.

    Returns:
        str: A string representing the formatted lesson time in the "HH:MM-HH:MM" format.

    Description:
        This function takes the start and end times of a lesson as `time` objects and formats them
        into a string representation in the "HH:MM-HH:MM" format, indicating the start and end times
        of the lesson.
    """
    # Format the start and end times into a string representation
    return f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"


if __name__ == "__main__":
    try:
        os.system("cls" if os.name == "nt" else "clear")
        print(
            f"""{Dict_Map.COLORS['GREEN']}{Figlet(font='slant').renderText("BorysfenBot")}{Dict_Map.COLORS['WHITE']}"""
        )
        # print("\n".join(f"{command.command} - {command.description}" for command in BOT_COMMANDS))
        create_database(Dict_Map.FILES['database'])
        # app.start()
        # app.run(alert_loop())
        app.run()

    except KeyboardInterrupt:
        exit()
