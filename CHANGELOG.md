# Changelog

## [v91](https://github.com/user-sspmynxdvb/Borysfen/tree/7c6f2b73b5b88e77d8012b7c1de7e55aa93f37f1) - 02.11.2023

### Improved
- **files: Borysfen_DB_V91.py, BorysfenBotV91.py**

### Added
- **libraries: from dotenv import load_dotenv**
- **files: .env.template and .env**

### Removed
- **functions: load_config, download_message**
- **variables: config**
- **files: config.json**

### Fixed
- **functions: commands_list**

### More info
- **Borysfen_DB_V91.py, BorysfenBotV91.py: .env insted of config.json**
- **commands_list: get_tg_info(message) 👉 get_tg_info(message, callback)**

## [v90](https://github.com/user-sspmynxdvb/Borysfen/tree/c5544612ea56b673507481835535cfceb97745d8) - 02.11.2023

### Improved
- **functions: alert_loop, callback_buttons, get_timetable, send_exception**
- **files: poetry files**
- **classes: Any_Map, Markup_Map, ALERT_LOOP, Text_Map**

### Added
- **files: CHANGELOG.md and CHANGELOG.md.template**

### Removed
- **variables: CHANGELOG_TEXT**

### More info
- **alert_loop: get_region_alerts 👉 get_alerts**
- **callback_buttons: removed case "changelog_again"**
- **Any_Map, Markup_Map: variables: removed changelog**
- **ALERT_LOOP: variables: ALERT_LOOP: url="https://alerts.in.ua/" 👉 url="https://map.ukrainealarm.com/"**
- **poetry files: updated libraries**
- **Text_Map: variables: SPACER: TG_Emoji_Map.HEAVY_MINUS_SIGN * 11 👉 f"\n{TG_Emoji_Map.HEAVY_MINUS_SIGN * 11}\n"**
- **get_timetable, send_exception: Text_Map.SPACER**

## [v89](https://github.com/user-sspmynxdvb/Borysfen/tree/48912d47aac5a87bfe1198c4ed9cb7339f2b9957) - 27.11.2023

### Improved
- **functions: callback_buttons**
- **imports: import sqlite3 👉 from sqlite3 import connect**

### Fixed
- **functions: get_info**

### More info
- **callback_buttons: match callback.data**
- **get_info: result = (None,) * len(search_column) if search_is_tuple else None**

## [v88](https://github.com/user-sspmynxdvb/Borysfen/tree/a05f427b295c9056ff8063921ff8a7de78ba2240) - 20.11.2023

### Improved
- **functions: alert_loop**

### More info
- **alert_loop: Dict_Map.ALERT_TYPE**

## [v87](https://github.com/user-sspmynxdvb/Borysfen/tree/ce5ea1829a57197bcc8fa48543f9ff00d8936509) - 19.11.2023

### Improved
- **functions: upload, commands_list, alert, alert_loop**
- **libraries: ukrainealarm**

### More info
- **commands_list: PermissionError**
- **upload: moved except IndexError**
- **alert: inline_keyboard[0].pop**
- **alert_loop: changed API site**

## [v86](https://github.com/user-sspmynxdvb/Borysfen/tree/7322d625763548c903748f69f68d17b772309f1d) - 05.11.2023

### Improved
- **functions: info**

### More info
- **info: information about the file**

## [v85](https://github.com/user-sspmynxdvb/Borysfen/tree/3986467da4a0ea49b60fca23e7738fb434509117) - 03.11.2023

### Improved
- **functions: personal_data_agreement, send_exception, get_info, now_is**

### Added
- **poetry support**

### More info
- **personal_data_agreement, get_info: "Згоден" = DB_Map.AGREED**
- **send_exception: if to_me: info_simple_user(message.from_user)**
- **info_forward_date, now_is: 🗓 = TG_Emoji_Map.CALENDAR_SPIRAL**

## [v84](https://github.com/user-sspmynxdvb/Borysfen/tree/cc9b95ba9bc0a76f19ca37d95fcbed80452d30b0) - 01.11.2023

### Improved
- **functions: num_to_emoji, url_shortener**

### Added
- **classes: TG_Emoji_Map**

### More info
- **num_to_emoji: str(text)**
- **url_shortener: num_to_emoji(i): link**

## [v83](https://github.com/user-sspmynxdvb/Borysfen/tree/acdd8cb5fded2a15d5f230ae84ec2d13d1d8804b) - 31.10.2023

### Improved
- **functions: help, search_people, alert, tomorrow_day**
- **files: Borysfen_DB**

### Added
- **libraries: from dateutil.relativedelta import relativedelta**

### More info
- **help: .get(symbol)**
- **search_people, alert: Markup_Map.DELETE_FULL**
- **now_is: .get(lesson)**
- **Borysfen_DB: removed unnecessary Enum**
- **tomorrow_day: return today + relativedelta(days=1)**

## [v82](https://github.com/user-sspmynxdvb/Borysfen/tree/cd99e880236fb78f5a0ff8e742e272ec3e1fd7ad) - 30.10.2023

### Improved
- **functions: personal_data_agreement, info, get_info, alert, now_is**
- **classes: Text_Map**

### Added
- **functions: info_phone, info_mention, info_username, info_id, info_title, info_chat_type, info_forward_date, info_simple_user**

### More info
- **personal_data_agreement: get_info(user_id, DB_Map.NAME)**
- **Текст_мапи: FAKE_VOID**
- **info: msg = message.reply_to_message, Text_Map.FAKE_VOID**
- **get_info: result = (None,) * len(search_column) if search_is_tuple else None**
- **alert, now_is: except PermissionError**

## [v81](https://github.com/user-sspmynxdvb/Borysfen/tree/f69f93e00e861b5b20c77b9829cb35b2ffa0e7eb) - 29.10.2023

### Improved
- **functions: get_info, personal_data_agreement, upload, create_database, ask, add_info, send, upload, get_message**
- **classes: DB_Map**

### Added
- **functions: personal_data_agreement, delete_full_message**

### More info
- **DB_Map: перенесены роли в класс**
- **get_info: check_agreement**
- **upload, create_database: DB_Map.MESSAGE_COLUMNS**
- **ask, add_info, send, upload, get_message: убран лишний join и split, пример: (' '.join(split_command(text, command).split(" ")))**

## [v80](https://github.com/user-sspmynxdvb/Borysfen/tree/6e749564451caed5583ddc6f6900c3c8c36d1519) - 28.10.2023

### Improved
- **functions: search_people, info, ask, data_search, add_info, send, wiki, qr_def, text2speech, upload, get_message, c, password_generator**

### More info
- **search_people, info, ask, data_search, add_info, send, wiki, qr_def, text2speech, upload, get_message, c, password_generator: split_command**
- **send: send_column_DB_Map.CLASSROOM**

## [v79](https://github.com/user-sspmynxdvb/Borysfen/tree/6a6ec34f5a151250f8430eb2ecbb137265740b52) - 27.10.2023

### Improved
- **functions: add_info, create_database, upload, send, now_is, who_is_this, get_info**
- **files: Borysfen_DB**

### More info
- **Borysfen_DB: all dictionaries are converted to Enum classes**
- **add_info: separate methods for changing email and name, improve the query for adding to the user database**
- **upload: tuple([key for key in Dict_Map.MESSAGE_COLUMNS.keys()])**
- **send, now_is, who_is_this: shortened, optimised use of get_info()**
- **get_info: added support for tuple**

## [v78](https://github.com/user-sspmynxdvb/Borysfen/tree/b3b7d3a8c58d76b4d2cfa916d36556a5157a7dcc) - 26.10.2023

### Improved
- **functions: forwards_cover, seconds_converter, get_info, username2id, get_tg_info, get_greeting, delete_files, generate_list, changelog, info, upload, c**

### More info
- **forwards_cover, seconds_converter, get_info, username2id, get_tg_info, get_greeting, delete_files, generate_list, changelog, info, upload, c: added comments**

## [v77](https://github.com/user-sspmynxdvb/Borysfen/tree/50084d872d888719928256ef15e4ff267a665b06) - 25.10.2023

### Improved
- **functions: now_is, send, add_info**

### More info
- **now_is: book_info, a href='link'>lesson/a>**
- **send: or user_role != 'Student'**
- **add_info: improved email validation**
- **find_link_in_list: improved email link validation**
- **add_info_column student: removed 👤**

## [v76](https://github.com/user-sspmynxdvb/Borysfen/tree/6d6c1013efb10748eaf1de895e589f286282deaf) - 23.10.2023

### Improved
- **functions: get_tg_info, now_is**

### More info
- **get_tg_info: fix bug with str(None), added if user.username else ''**
- **now_is: else link = ''**

## [v75](https://github.com/user-sspmynxdvb/Borysfen/tree/73c02ccc2d7854f7595dba6ef68aa1a454a2cca8) - 23.10.2023

### Improved
- **functions: now_is, find_link_in_list**

### Fixed
- **functions: now_is, add_lesson_link**

### More info
- **now_is: disable_web_page_preview=True**
- **find_link_in_list: code reduced, optimised, more versatile**

## [v74](https://github.com/user-sspmynxdvb/Borysfen/tree/493b20dbdbf74d1130620717b6c21c57942cc359) - 21.10.2023

### Improved
- **functions: now_is, get_timetable**

### Added
- **functions: find_link_in_list, add_lesson_link**

### More info
- **get_timetable: rsplit(f"COMMONLY_TEXT_MAP['spacer']", 1)[0])**
- **now_is: add_lesson_link**

## [v73](https://github.com/user-sspmynxdvb/Borysfen/tree/16bbdc79e099f914f0c765dd7dd1575b28156c19) - 19.10.2023

### Improved
- **functions: generate_list, seconds_converter, password_generator**

### More info
- **generate_list: improved documentation, changed variable names**.
- **seconds_converter: shortened and improved code**.
- **password_generator: removed 🌐**

## [v72](https://github.com/user-sspmynxdvb/Borysfen/tree/d450ec9f18c0409b22158a58e8e9ea6976b49b50) - 18.10.2023

### Improved
- **functions: callback_buttons, get_greeting**

### Added
- **functions: generate_list**

### Removed
- **functions: class_books_list, lesson_links_list**

### More info
- **callback_buttons: moved improved code of class_books_list, lesson_links_list functions here**
- **get_greeting: greetings made by constant GREETINGS**

## [v71](https://github.com/user-sspmynxdvb/Borysfen/tree/80e411d426fc879f664ed2aa09d5a62b58cb937a) - 16.10.2023

### Improved
- **functions: load_config, get_greeting, is_school_day**

### More info
- **load_config: more efficient and cleaner code; added comments**
- **get_greeting: more efficient and cleaner code**
- **is_school_day: fix bug (now day.date() == datetime.today().date())**

## [v70](https://github.com/user-sspmynxdvb/Borysfen/tree/e9ae4dc55412118aff631697ccabbb07cac431f4) - 03.10.2023

### Improved
- **functions: password_generator, is_school_day**

### Removed
- **fake.credit_card_full() from function password_generator**

### Added
- **functions: check_holidays**

### More info
- **password_generator: datetime.combine(date_of_birth_date, datetime.min.time()) и добавлено кнопку ❓**
- **is_school_day: def check_holidays(day: datetime)**

## [v69](https://github.com/user-sspmynxdvb/Borysfen/tree/af058593ca4d756a12ab38b12371d8a8272b86ac) - 30.09.2023

### Improved
- **functions:  load_config, save_config, create_database, class_books_list, upload, password_generator, lesson_links_list, is_school_time**

### More info
- **load_config, save_config, create_database: added recommended typing**
- **class_books_list: 📚 Книжки**
- **upload: code = fake.password(length=40, special_chars=False)**
- **password_generator: fake.password(length=length), 📬, 🏡, 💼, 🌐, 💳, ⏳**
- **lesson_links_list: 🔗 Посилання**
- **is_school_time: time(0, 0) <= current_time <= time(16, 20)**

## [v68](https://github.com/user-sspmynxdvb/Borysfen/tree/68a49d0ec6088d355d24141e202cbd95a4537ff2) - 08.09.2023

### Improved
- **functions: now_is, get_timetabl**

### Added
- **functions: tomorrow_day**

### More info
- **now_is, get_timetable: tomorrow_day**

## [v67](https://github.com/user-sspmynxdvb/Borysfen/tree/b9d0a14702ef103c9bcca3a3d79df7f9f6a48b41) - 07.09.2023

### Improved
- **code: small pep-8 fixes with ruff**

## [v66](https://github.com/user-sspmynxdvb/Borysfen/tree/a1b50c7b1c8b88f233cde1f53f999b50abe0ede3) - 05.09.2023

### Improved
- **functions: data_search, send, who_is_this, get_message, is_school_time**

### More info
- **data_search, send, who_is_this, get_message: str(row) 👉 row**
- **is_school_time: time(8, 0) <= current_time <= time(15, 40) 👉 time(0, 0) <= current_time <= time(15, 40)**

## [v65](https://github.com/user-sspmynxdvb/Borysfen/tree/f741fd272dfd309865cffd8a7aa4254de2ba3823) - 04.09.2023

### Improved
- **functions: data_search, get_timetable, is_school_time**

### Added
- **functions: replace_tme**

### More info
- **data_search: replace_tme(search_text) if search_column == '🌀' else search_text**
- **get_timetable: COMMONLY_TEXT_MAP['spacer'] if callback.data == 'get_timetable_week' else ''**
- **is_school_time: time(8, 0) <= current_time <= time(15, 40)**

## [v64](https://github.com/user-sspmynxdvb/Borysfen/tree/1f09880f1eab89b62cecf896fa7502f889165dd8) - 03.09.2023

### Improved
- **functions: get_timetable, commands_list, class_books_list, lesson_links_list**

### Renamed
- **functions: account_generator 👉 password_generator**

### More info
- **get_timetable: прибрано 'if is_school_day(today, today.year)'**
- **commands_list, class_books_list, lesson_links_list: num_to_emoji(str(number))**

## [v63](https://github.com/user-sspmynxdvb/Borysfen/tree/990f6fefbac5897e2c34effd7670657e2c7f0e62) - 02.09.2023

### Improved
- **functions: lesson_links_list, start, class_books_list, alert**

### More info
- **lesson_links_list: callback**
- **start: start_with_class_information**
- **class_books_list: MARKUP_MAIN_BUTTON**
- **alert: removed: 'у вашій області'**

## [v62](https://github.com/user-sspmynxdvb/Borysfen/tree/c89f72d7005be3b31dfd2ddfc0e9cc0cf895b61e) - 02.09.2023

### Improved
- **code: if not is_me(user_id) and not get_info(user_id) 👉 if not (is_me(user_id) or get_info(user_id))**

### Added
- **functions: lesson_links_list**

### Removed
- **functions: math_help**

## [v61](https://github.com/user-sspmynxdvb/Borysfen/tree/7ed3a38b14f2e65b841e8b307f8a6102b42fa7e0) - 31.08.2023

### Improved
- **functions: data_search**

### Fixed
- **functions: edit_column_number**

### More info
- **data_search: if not search_column == '🚪' else ''**
- **edit_column_number: if message.contact.phone_number.startswith('+') else '+' + message.contact.phone_number**

## [v60](https://github.com/user-sspmynxdvb/Borysfen/tree/e45ef5512a7eb4358f14256842961a4ccd35bfed) - 30.09.2023

### Improved
- **functions: add_info, username2id**

### More info
- **add_info, username2id: .replace("https://t.me/", "")**

## [v59](https://github.com/user-sspmynxdvb/Borysfen/tree/aa28883544acf55759d5387ca703b53883049e93) - 18.08.2023

### Improved
- **files: Additions/Borysfen_DB_V59.py**

### More info
- **Additions/Borysfen_DB_V59.py: teachers update**

## [v58](https://github.com/user-sspmynxdvb/Borysfen/tree/6d0e3313eeec1fb5578bc7cf4e49e57f0feecdda) - 03.08.2023

### Improved
- **functions: maze, who_is_this**
- **variables: message_columns, user_columns**

### Fixed
- **functions: who_is_this**

### More info
- **message_columns, user_columns: tuple**
- **maze: PermissionError, "Ви вже граєте"**
- **who_is_this: Fixed + callback.answer(text="".join...**

## [v57](https://github.com/user-sspmynxdvb/Borysfen/tree/9e9c8e64340c060c6bdc70aed41993fe497d890b) - 29.07.2023

### Renamed
- **code: message=callback.message 👉 message=message**

## [v56](https://github.com/user-sspmynxdvb/Borysfen/tree/eb63f6e5833284f5981ca0151fbccc104aac9b3c) - 29.07.2023

### Improved
- **functions: url_shortener, get_timetable, now_is, alert, upload, create_database, file_report**

### More info
- **get_timetable: get_timetable_week**
- **url_shortener: written documentation**
- **now_is: today.year**
- **alert: reply_markup.inline_keyboard[0].insert(0, (button))**
- **upload: (int(user_id), int(forwarded_msg.id)**
- **create_database:  alert_users (ID INTEGER PRIMARY KEY); (📝 INTEGER, 🆔 INTEGER PRIMARY KEY, 🔑 TEXT UNIQUE)**
- **file_report: result['response']**

## [v55](https://github.com/user-sspmynxdvb/Borysfen/tree/441f2784ab293697f41defbdd29219a9e9b82cbf) - 26.07.2023

### Improved
- **functions: virus_total, weather, start, alert_loop, alert**

### Renamed
- **virus_total_obj 👉 virus_total**
- **obj_report 👉 report**

### Added
- **functions: file_report, url_shortener**
- **libraries: ConnectionError**

### Removed
- **code: excess returns**

### More info
- **weather: "Additions/weather_data.json"**
- **start: "бот помічник" and "💬 Поділитися ботом"**
- **alert_loop: bold_text(text + duration), button "⚡️ Пункти незламності"**

## [v54](https://github.com/user-sspmynxdvb/Borysfen/tree/fdfee1fed1f9268e4a6258d4613b52149fd08a3b) - 25.07.2023

### Improved
- **functions: alert_loop, wiki, qr_def, virustotal**

### Renamed
- **code: DELETEE 👉 DELETE**

### Added
- **libraries: ConnectTimeout**

### More info
- **alert_loop: app.start() While True**
- **wiki, qr_def, virustotal: ChatAction.TYPING**
- **virustotal: IndexError, MongoDB**

## [v53](https://github.com/user-sspmynxdvb/Borysfen/tree/6e06ce210ccbcc47c8724c9dbf2ea4d8ee54d629) - 24.07.2023

### Improved
- **functions: qr_def, virustotal, account_generator, seconds_converter**

### Renamed
- **variables: maps 👉 maze_maps**

### More info
- **qr_def: ValueError**
- **virustotal: JSONDecodeError**
- **account_generator: randint(15, 25)**
- **seconds_converter: alert**

## [v52](https://github.com/user-sspmynxdvb/Borysfen/tree/fbb072a9f8fc7bce8cab74d13e392e40f2adfd23) - 23.07.2023

### Improved
- **functions: upload**

### Added
- **libraries: from qrcode import make as qrcode_make**

### More info
- **upload: qrcode_make**

## [v51](https://github.com/user-sspmynxdvb/Borysfen/tree/a636c7bcb34ed4f357998f93133bacdd9e69bbd3) - 22.07.2023

### Improved
- **functions: bad_intentions, maze, edit_column_number, now_is, get_tg_info, search_people, info, text2speech**

### Added
- **functions: is_school_time, virustotal**

### More info
- **bad_intentions: return False**
- **maze: "Зараз урок, потрібно вчитися"**
- **edit_column_number: filters.private**
- **now_is: COMMONLY_BUTTONS_MAP["school_day"]**
- **get_tg_info: (callback or message).from_user.id**
- **search_people, info, text2speech: text.caption**
- **text2speech: message.reply_to_message**

## [v50](https://github.com/user-sspmynxdvb/Borysfen/tree/dda750e23dd590dcc4396f51fc3a79c409102e43) - 21.07.2023

### Improved
- **functions: is_id, info, bad_intentions, account_generator, add_info, recess_time, callback_buttons, forwards_cover, qr_def, has_file, send_exception, maze, qr_def, weather, help, now_is, wiki, qr_def, text2speech**

### Renamed
- **functions: is_id 👉 is_user_id**

### More info
- **bad_intentions: u_is_me**
- **account_generator: 👤 ryan_mills02051926**
- **add_info: written documentation and improved code syntax**
- **recess_time: now_date default**
- **callback_buttons: written documentation**
- **forwards_cover: thumbs[-1]**
- **qr_def: file = (message.reply_to_message.photo or message.reply_to_message.document) if message.reply_to_message else message.photo or message.document**
- **has_file: обновил документацию**
- **send_exception, qr_def, weather, help, now_is, wiki, qr_def, text2speech: PermissionError**
- **maze: Only_private_chat**

## [v49](https://github.com/user-sspmynxdvb/Borysfen/tree/2ca60a32ea0beda67862bc634c844408749d4754) - 20.07.2023

### Improved
- **functions: maze, get_message, data_search**
- **code: any(text == callback.data for text in  👉 callback.data in ...**

### Renamed
- **functions: db_search 👉 data_search**
- **code: 💬 Отримати повідомлення 👉 💬 Отримати; 🗑 Видалити повідомлення👉 ❌ Видалити**

### Added
- **functions: account_generator**

### More info
- **maze: FloodWait + try in callback**
- **get_message: bug fix**
- **data_search: added functionality for deletion from the database, "Ця функція працює тільки в особистому діалозі з ботом", documentation is written**

## [V48]() - 19.07.2023

### Improved
- **functions: upload, forwards_cover, ask**
- **files: **
- **classes: **
- **code: with sqlite3.connect**
- **variables: **

### Renamed
- **functions: 👉**
- **code: **
- **variables: **

### Added
- **functions: maze**
- **libraries: maze_game**
- **classes: **
- **files: **

### Removed
- **functions: **
- **libraries: **
- **classes: **
- **variables: **

### Fixed
- **functions: **

### More info
- **text**

