from datetime import time
from enum import Enum
from urllib.parse import quote

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from ua_alarm.enums import AlertType


# ruff: noqa: E501


class Enum2(Enum):
    def __get__(self, instance, owner):
        return self.value


class TG_Emoji_Map(Enum2):
    GRINNING = "😀"
    GRIN = "😁"
    JOY = "😂"
    ROFL = "🤣"
    SMILEY = "😃"
    SMILE = "😄"
    SWEAT_SMILE = "😅"
    LAUGHING = "😆"
    WINK = "😉"
    BLUSH = "😊"
    YUM = "😋"
    SUNGLASSES = "😎"
    HEART_EYES = "😍"
    KISSING_HEART = "😘"
    KISSING = "😗"
    KISSING_SMILING_EYES = "😙"
    KISSING_CLOSED_EYES = "😚"
    RELAXED = "☺️"
    SLIGHT_SMILE = "🙂"
    HUGGING = "🤗"
    THINKING = "🤔"
    NEUTRAL_FACE = "😐"
    EXPRESSIONLESS = "😑"
    NO_MOUTH = "😶"
    ROLLING_EYES = "🙄"
    SMIRK = "😏"
    PERSEVERE = "😣"
    DISAPPOINTED_RELIEVED = "😥"
    OPEN_MOUTH = "😮"
    ZIPPER_MOUTH = "🤐"
    HUSHED = "😯"
    SLEEPY = "😪"
    TIRED_FACE = "😫"
    SLEEPING = "😴"
    RELIEVED = "😌"
    NERD = "🤓"
    STUCK_OUT_TONGUE = "😛"
    STUCK_OUT_TONGUE_WINKING_EYE = "😜"
    STUCK_OUT_TONGUE_CLOSED_EYES = "😝"
    DROOLING_FACE = "🤤"
    UNAMUSED = "😒"
    SWEAT = "😓"
    PENSIVE = "😔"
    CONFUSED = "😕"
    UPSIDE_DOWN = "🙃"
    MONEY_MOUTH = "🤑"
    ASTONISHED = "😲"
    FROWNING2 = "☹️"
    SLIGHT_FROWN = "🙁"
    CONFOUNDED = "😖"
    DISAPPOINTED = "😞"
    WORRIED = "😟"
    TRIUMPH = "😤"
    CRY = "😢"
    SOB = "😭"
    FROWNING = "😦"
    ANGUISHED = "😧"
    FEARFUL = "😨"
    WEARY = "😩"
    GRIMACING = "😬"
    COLD_SWEAT = "😰"
    SCREAM = "😱"
    FLUSHED = "😳"
    DIZZY_FACE = "😵"
    RAGE = "😡"
    ANGRY = "😠"
    INNOCENT = "😇"
    COWBOY = "🤠"
    CLOWN = "🤡"
    LYING_FACE = "🤥"
    MASK = "😷"
    THERMOMETER_FACE = "🤒"
    HEAD_BANDAGE = "🤕"
    NAUSEATED_FACE = "🤢"
    SNEEZING_FACE = "🤧"
    SMILING_IMP = "😈"
    IMP = "👿"
    JAPANESE_OGRE = "👹"
    JAPANESE_GOBLIN = "👺"
    SKULL = "💀"
    GHOST = "👻"
    ALIEN = "👽"
    ROBOT = "🤖"
    POOP = "💩"
    SMILEY_CAT = "😺"
    SMILE_CAT = "😸"
    JOY_CAT = "😹"
    HEART_EYES_CAT = "😻"
    SMIRK_CAT = "😼"
    KISSING_CAT = "😽"
    SCREAM_CAT = "🙀"
    CRYING_CAT_FACE = "😿"
    POUTING_CAT = "😾"
    BOY = "👦"
    GIRL = "👧"
    MAN = "👨"
    WOMAN = "👩"
    OLDER_MAN = "👴"
    OLDER_WOMAN = "👵"
    BABY = "👶"
    ANGEL = "👼"
    COP = "👮"
    SPY = "🕵️"
    GUARDSMAN = "💂"
    CONSTRUCTION_WORKER = "👷"
    MAN_WITH_TURBAN = "👳"
    PERSON_WITH_BLOND_HAIR = "👱"
    SANTA = "🎅"
    MRS_CLAUS = "🤶"
    PRINCESS = "👸"
    PRINCE = "🤴"
    BRIDE_WITH_VEIL = "👰"
    MAN_IN_TUXEDO = "🤵"
    PREGNANT_WOMAN = "🤰"
    MAN_WITH_GUA_PI_MAO = "👲"
    PERSON_FROWNING = "🙍"
    PERSON_WITH_POUTING_FACE = "🙎"
    NO_GOOD = "🙅"
    OK_WOMAN = "🙆"
    INFORMATION_DESK_PERSON = "💁"
    RAISING_HAND = "🙋"
    BOW = "🙇"
    FACE_PALM = "🤦"
    SHRUG = "🤷"
    MASSAGE = "💆"
    HAIRCUT = "💇"
    WALKING = "🚶"
    RUNNER = "🏃"
    DANCER = "💃"
    MAN_DANCING = "🕺"
    DANCERS = "👯"
    SPEAKING_HEAD = "🗣"
    BUST_IN_SILHOUETTE = "👤"
    BUSTS_IN_SILHOUETTE = "👥"
    COUPLE = "👫"
    TWO_MEN_HOLDING_HANDS = "👬"
    TWO_WOMEN_HOLDING_HANDS = "👭"
    COUPLEKISS = "💏"
    KISS_MM = "👨‍❤️‍💋‍👨"
    KISS_WW = "👩‍❤️‍💋‍👩"
    COUPLE_WITH_HEART = "💑"
    COUPLE_MM = "👨‍❤️‍👨"
    COUPLE_WW = "👩‍❤️‍👩"
    FAMILY = "👪"
    FAMILY_MWG = "👨‍👩‍👧"
    FAMILY_MWGB = "👨‍👩‍👧‍👦"
    FAMILY_MWBB = "👨‍👩‍👦‍👦"
    FAMILY_MWGG = "👨‍👩‍👧‍👧"
    FAMILY_MMB = "👨‍👨‍👦"
    FAMILY_MMG = "👨‍👨‍👧"
    FAMILY_MMGB = "👨‍👨‍👧‍👦"
    FAMILY_MMBB = "👨‍👨‍👦‍👦"
    FAMILY_MMGG = "👨‍👨‍👧‍👧"
    FAMILY_WWB = "👩‍👩‍👦"
    FAMILY_WWG = "👩‍👩‍👧"
    FAMILY_WWGB = "👩‍👩‍👧‍👦"
    FAMILY_WWBB = "👩‍👩‍👦‍👦"
    FAMILY_WWGG = "👩‍👩‍👧‍👧"
    MUSCLE = "💪"
    SELFIE = "🤳"
    POINT_LEFT = "👈"
    POINT_RIGHT = "👉"
    POINT_UP = "☝️"
    POINT_UP_2 = "👆"
    MIDDLE_FINGER = "🖕"
    POINT_DOWN = "👇"
    V = "✌️"
    FINGERS_CROSSED = "🤞"
    VULCAN = "🖖"
    METAL = "🤘"
    CALL_ME = "🤙"
    HAND_SPLAYED = "🖐️"
    RAISED_HAND = "✋"
    OK_HAND = "👌"
    THUMBSUP = "👍"
    THUMBSDOWN = "👎"
    FIST = "✊"
    PUNCH = "👊"
    LEFT_FACING_FIST = "🤛"
    RIGHT_FACING_FIST = "🤜"
    RAISED_BACK_OF_HAND = "🤚"
    WAVE = "👋"
    CLAP = "👏"
    WRITING_HAND = "✍️"
    OPEN_HANDS = "👐"
    RAISED_HANDS = "🙌"
    PRAY = "🙏"
    HANDSHAKE = "🤝"
    NAIL_CARE = "💅"
    EAR = "👂"
    NOSE = "👃"
    FOOTPRINTS = "👣"
    EYES = "👀"
    EYE = "👁"
    TONGUE = "👅"
    LIPS = "👄"
    KISS = "💋"
    ZZZ = "💤"
    EYEGLASSES = "👓"
    DARK_SUNGLASSES = "🕶️"
    NECKTIE = "👔"
    SHIRT = "👕"
    JEANS = "👖"
    DRESS = "👗"
    KIMONO = "👘"
    BIKINI = "👙"
    WOMANS_CLOTHES = "👚"
    PURSE = "👛"
    HANDBAG = "👜"
    POUCH = "👝"
    SCHOOL_SATCHEL = "🎒"
    MANS_SHOE = "👞"
    ATHLETIC_SHOE = "👟"
    HIGH_HEEL = "👠"
    SANDAL = "👡"
    BOOT = "👢"
    CROWN = "👑"
    WOMANS_HAT = "👒"
    TOPHAT = "🎩"
    MORTAR_BOARD = "🎓"
    HELMET_WITH_CROSS = "⛑️"
    LIPSTICK = "💄"
    RING = "💍"
    CLOSED_UMBRELLA = "🌂"
    BRIEFCASE = "💼"
    # Nature
    SEE_NO_EVIL = "🙈"
    HEAR_NO_EVIL = "🙉"
    SPEAK_NO_EVIL = "🙊"
    SWEAT_DROPS = "💦"
    DASH = "💨"
    MONKEY_FACE = "🐵"
    MONKEY = "🐒"
    GORILLA = "🦍"
    DOG = "🐶"
    DOG2 = "🐕"
    POODLE = "🐩"
    WOLF = "🐺"
    FOX = "🦊"
    CAT = "🐱"
    CAT2 = "🐈"
    LION_FACE = "🦁"
    TIGER = "🐯"
    TIGER2 = "🐅"
    LEOPARD = "🐆"
    HORSE = "🐴"
    RACEHORSE = "🐎"
    DEER = "🦌"
    UNICORN = "🦄"
    COW = "🐮"
    OX = "🐂"
    WATER_BUFFALO = "🐃"
    COW2 = "🐄"
    PIG = "🐷"
    PIG2 = "🐖"
    BOAR = "🐗"
    PIG_NOSE = "🐽"
    RAM = "🐏"
    SHEEP = "🐑"
    GOAT = "🐐"
    DROMEDARY_CAMEL = "🐪"
    CAMEL = "🐫"
    ELEPHANT = "🐘"
    RHINO = "🦏"
    MOUSE = "🐭"
    MOUSE2 = "🐁"
    RAT = "🐀"
    HAMSTER = "🐹"
    RABBIT = "🐰"
    RABBIT2 = "🐇"
    CHIPMUNK = "🐿️"
    BAT = "🦇"
    BEAR = "🐻"
    KOALA = "🐨"
    PANDA_FACE = "🐼"
    FEET = "🐾"
    TURKEY = "🦃"
    CHICKEN = "🐔"
    ROOSTER = "🐓"
    HATCHING_CHICK = "🐣"
    BABY_CHICK = "🐤"
    HATCHED_CHICK = "🐥"
    BIRD = "🐦"
    PENGUIN = "🐧"
    DOVE = "🕊️"
    EAGLE = "🦅"
    DUCK = "🦆"
    OWL = "🦉"
    FROG = "🐸"
    CROCODILE = "🐊"
    TURTLE = "🐢"
    LIZARD = "🦎"
    SNAKE = "🐍"
    DRAGON_FACE = "🐲"
    DRAGON = "🐉"
    WHALE = "🐳"
    WHALE2 = "🐋"
    DOLPHIN = "🐬"
    FISH = "🐟"
    TROPICAL_FISH = "🐠"
    BLOWFISH = "🐡"
    SHARK = "🦈"
    OCTOPUS = "🐙"
    SHELL = "🐚"
    CRAB = "🦀"
    SHRIMP = "🦐"
    SQUID = "🦑"
    BUTTERFLY = "🦋"
    SNAIL = "🐌"
    BUG = "🐛"
    ANT = "🐜"
    BEE = "🐝"
    BEETLE = "🐞"
    SPIDER = "🕷️"
    SPIDER_WEB = "🕸️"
    SCORPION = "🦂"
    BOUQUET = "💐"
    CHERRY_BLOSSOM = "🌸"
    ROSETTE = "🏵️"
    ROSE = "🌹"
    WILTED_ROSE = "🥀"
    HIBISCUS = "🌺"
    SUNFLOWER = "🌻"
    BLOSSOM = "🌼"
    TULIP = "🌷"
    SEEDLING = "🌱"
    EVERGREEN_TREE = "🌲"
    DECIDUOUS_TREE = "🌳"
    PALM_TREE = "🌴"
    CACTUS = "🌵"
    EAR_OF_RICE = "🌾"
    HERB = "🌿"
    SHAMROCK = "☘️"
    FOUR_LEAF_CLOVER = "🍀"
    MAPLE_LEAF = "🍁"
    FALLEN_LEAF = "🍂"
    LEAVES = "🍃"
    MUSHROOM = "🍄"
    CHESTNUT = "🌰"
    EARTH_AFRICA = "🌍"
    EARTH_AMERICAS = "🌎"
    EARTH_ASIA = "🌏"
    NEW_MOON = "🌑"
    WAXING_CRESCENT_MOON = "🌒"
    FIRST_QUARTER_MOON = "🌓"
    WAXING_GIBBOUS_MOON = "🌔"
    FULL_MOON = "🌕"
    WANING_GIBBOUS_MOON = "🌖"
    LAST_QUARTER_MOON = "🌗"
    WANING_CRESCENT_MOON = "🌘"
    CRESCENT_MOON = "🌙"
    NEW_MOON_WITH_FACE = "🌚"
    FIRST_QUARTER_MOON_WITH_FACE = "🌛"
    LAST_QUARTER_MOON_WITH_FACE = "🌜"
    SUNNY = "☀️"
    FULL_MOON_WITH_FACE = "🌝"
    SUN_WITH_FACE = "🌞"
    STAR = "⭐️"
    STAR2 = "🌟"
    CLOUD = "☁️"
    PARTLY_SUNNY = "⛅️"
    THUNDER_CLOUD_RAIN = "⛈️"
    WHITE_SUN_SMALL_CLOUD = "🌤️"
    WHITE_SUN_CLOUD = "🌥️"
    WHITE_SUN_RAIN_CLOUD = "🌦️"
    CLOUD_RAIN = "🌧️"
    CLOUD_SNOW = "🌨️"
    CLOUD_LIGHTNING = "🌩️"
    CLOUD_TORNADO = "🌪️"
    FOG = "🌫️"
    WIND_BLOWING_FACE = "🌬️"
    UMBRELLA2 = "☂️"
    UMBRELLA = "☔️"
    ZAP = "⚡️"
    SNOWFLAKE = "❄️"
    SNOWMAN2 = "☃️"
    SNOWMAN = "⛄️"
    COMET = "☄️"
    FIRE = "🔥"
    DROPLET = "💧"
    OCEAN = "🌊"
    JACK_O_LANTERN = "🎃"
    CHRISTMAS_TREE = "🎄"
    SPARKLES = "✨"
    TANABATA_TREE = "🎋"
    BAMBOO = "🎍"
    # Food
    GRAPES = "🍇"
    MELON = "🍈"
    WATERMELON = "🍉"
    TANGERINE = "🍊"
    LEMON = "🍋"
    BANANA = "🍌"
    PINEAPPLE = "🍍"
    APPLE = "🍎"
    GREEN_APPLE = "🍏"
    PEAR = "🍐"
    PEACH = "🍑"
    CHERRIES = "🍒"
    STRAWBERRY = "🍓"
    KIWI = "🥝"
    TOMATO = "🍅"
    AVOCADO = "🥑"
    EGGPLANT = "🍆"
    POTATO = "🥔"
    CARROT = "🥕"
    CORN = "🌽"
    HOT_PEPPER = "🌶️"
    CUCUMBER = "🥒"
    PEANUTS = "🥜"
    BREAD = "🍞"
    CROISSANT = "🥐"
    FRENCH_BREAD = "🥖"
    PANCAKES = "🥞"
    CHEESE = "🧀"
    MEAT_ON_BONE = "🍖"
    POULTRY_LEG = "🍗"
    BACON = "🥓"
    HAMBURGER = "🍔"
    FRIES = "🍟"
    PIZZA = "🍕"
    HOTDOG = "🌭"
    TACO = "🌮"
    BURRITO = "🌯"
    STUFFED_FLATBREAD = "🥙"
    EGG = "🥚"
    COOKING = "🍳"
    SHALLOW_PAN_OF_FOOD = "🥘"
    STEW = "🍲"
    SALAD = "🥗"
    POPCORN = "🍿"
    BENTO = "🍱"
    RICE_CRACKER = "🍘"
    RICE_BALL = "🍙"
    RICE = "🍚"
    CURRY = "🍛"
    RAMEN = "🍜"
    SPAGHETTI = "🍝"
    SWEET_POTATO = "🍠"
    ODEN = "🍢"
    SUSHI = "🍣"
    FRIED_SHRIMP = "🍤"
    FISH_CAKE = "🍥"
    DANGO = "🍡"
    ICECREAM = "🍦"
    SHAVED_ICE = "🍧"
    ICE_CREAM = "🍨"
    DOUGHNUT = "🍩"
    COOKIE = "🍪"
    BIRTHDAY = "🎂"
    CAKE = "🍰"
    CHOCOLATE_BAR = "🍫"
    CANDY = "🍬"
    LOLLIPOP = "🍭"
    CUSTARD = "🍮"
    HONEY_POT = "🍯"
    BABY_BOTTLE = "🍼"
    MILK = "🥛"
    COFFEE = "☕️"
    TEA = "🍵"
    SAKE = "🍶"
    CHAMPAGNE = "🍾"
    WINE_GLASS = "🍷"
    COCKTAIL = "🍸"
    TROPICAL_DRINK = "🍹"
    BEER = "🍺"
    BEERS = "🍻"
    CHAMPAGNE_GLASS = "🥂"
    TUMBLER_GLASS = "🥃"
    FORK_KNIFE_PLATE = "🍽️"
    FORK_AND_KNIFE = "🍴"
    SPOON = "🥄"
    # Activity
    SPACE_INVADER = "👾"
    LEVITATE = "🕴️"
    FENCER = "🤺"
    HORSE_RACING = "🏇"
    SKIER = "⛷️"
    SNOWBOARDER = "🏂"
    GOLFER = "🏌️"
    SURFER = "🏄"
    ROWBOAT = "🚣"
    SWIMMER = "🏊"
    BASKETBALL_PLAYER = "⛹️"
    LIFTER = "🏋️"
    BICYCLIST = "🚴"
    MOUNTAIN_BICYCLIST = "🚵"
    CARTWHEEL = "🤸"
    WRESTLERS = "🤼"
    WATER_POLO = "🤽"
    HANDBALL = "🤾"
    JUGGLING = "🤹"
    CIRCUS_TENT = "🎪"
    PERFORMING_ARTS = "🎭"
    ART = "🎨"
    SLOT_MACHINE = "🎰"
    BATH = "🛀"
    REMINDER_RIBBON = "🎗️"
    TICKETS = "🎟️"
    TICKET = "🎫"
    MILITARY_MEDAL = "🎖️"
    TROPHY = "🏆"
    MEDAL = "🏅"
    FIRST_PLACE = "🥇"
    SECOND_PLACE = "🥈"
    THIRD_PLACE = "🥉"
    SOCCER = "⚽️"
    BASEBALL = "⚾️"
    BASKETBALL = "🏀"
    VOLLEYBALL = "🏐"
    FOOTBALL = "🏈"
    RUGBY_FOOTBALL = "🏉"
    TENNIS = "🎾"
    BALL = "🎱"
    BOWLING = "🎳"
    CRICKET = "🏏"
    FIELD_HOCKEY = "🏑"
    HOCKEY = "🏒"
    PING_PONG = "🏓"
    BADMINTON = "🏸"
    BOXING_GLOVE = "🥊"
    MARTIAL_ARTS_UNIFORM = "🥋"
    GOAL = "🥅"
    DART = "🎯"
    GOLF = "⛳️"
    ICE_SKATE = "⛸️"
    FISHING_POLE_AND_FISH = "🎣"
    RUNNING_SHIRT_WITH_SASH = "🎽"
    SKI = "🎿"
    VIDEO_GAME = "🎮"
    GAME_DIE = "🎲"
    MUSICAL_SCORE = "🎼"
    MICROPHONE = "🎤"
    HEADPHONES = "🎧"
    SAXOPHONE = "🎷"
    GUITAR = "🎸"
    MUSICAL_KEYBOARD = "🎹"
    TRUMPET = "🎺"
    VIOLIN = "🎻"
    DRUM = "🥁"
    CLAPPER = "🎬"
    BOW_AND_ARROW = "🏹"
    # Travel
    RACE_CAR = "🏎️"
    MOTORCYCLE = "🏍️"
    JAPAN = "🗾"
    MOUNTAIN_SNOW = "🏔️"
    MOUNTAIN = "⛰️"
    VOLCANO = "🌋"
    MOUNT_FUJI = "🗻"
    CAMPING = "🏕️"
    BEACH = "🏖️"
    DESERT = "🏜️"
    ISLAND = "🏝️"
    PARK = "🏞️"
    STADIUM = "🏟️"
    CLASSICAL_BUILDING = "🏛️"
    CONSTRUCTION_SITE = "🏗️"
    HOMES = "🏘️"
    CITYSCAPE = "🏙️"
    HOUSE_ABANDONED = "🏚️"
    HOUSE = "🏠"
    HOUSE_WITH_GARDEN = "🏡"
    OFFICE = "🏢"
    POST_OFFICE = "🏣"
    EUROPEAN_POST_OFFICE = "🏤"
    HOSPITAL = "🏥"
    BANK = "🏦"
    HOTEL = "🏨"
    LOVE_HOTEL = "🏩"
    CONVENIENCE_STORE = "🏪"
    SCHOOL = "🏫"
    DEPARTMENT_STORE = "🏬"
    FACTORY = "🏭"
    JAPANESE_CASTLE = "🏯"
    EUROPEAN_CASTLE = "🏰"
    WEDDING = "💒"
    TOKYO_TOWER = "🗼"
    STATUE_OF_LIBERTY = "🗽"
    CHURCH = "⛪️"
    MOSQUE = "🕌"
    SYNAGOGUE = "🕍"
    SHINTO_SHRINE = "⛩️"
    KAABA = "🕋"
    FOUNTAIN = "⛲️"
    TENT = "⛺️"
    FOGGY = "🌁"
    NIGHT_WITH_STARS = "🌃"
    SUNRISE_OVER_MOUNTAINS = "🌄"
    SUNRISE = "🌅"
    CITY_DUSK = "🌆"
    CITY_SUNSET = "🌇"
    BRIDGE_AT_NIGHT = "🌉"
    MILKY_WAY = "🌌"
    CAROUSEL_HORSE = "🎠"
    FERRIS_WHEEL = "🎡"
    ROLLER_COASTER = "🎢"
    STEAM_LOCOMOTIVE = "🚂"
    RAILWAY_CAR = "🚃"
    BULLETTRAIN_SIDE = "🚄"
    BULLETTRAIN_FRONT = "🚅"
    TRAIN2 = "🚆"
    METRO = "🚇"
    LIGHT_RAIL = "🚈"
    STATION = "🚉"
    TRAM = "🚊"
    MONORAIL = "🚝"
    MOUNTAIN_RAILWAY = "🚞"
    TRAIN = "🚋"
    BUS = "🚌"
    ONCOMING_BUS = "🚍"
    TROLLEYBUS = "🚎"
    MINIBUS = "🚐"
    AMBULANCE = "🚑"
    FIRE_ENGINE = "🚒"
    POLICE_CAR = "🚓"
    ONCOMING_POLICE_CAR = "🚔"
    TAXI = "🚕"
    ONCOMING_TAXI = "🚖"
    RED_CAR = "🚗"
    ONCOMING_AUTOMOBILE = "🚘"
    BLUE_CAR = "🚙"
    TRUCK = "🚚"
    ARTICULATED_LORRY = "🚛"
    TRACTOR = "🚜"
    BIKE = "🚲"
    SCOOTER = "🛴"
    MOTOR_SCOOTER = "🛵"
    BUSSTOP = "🚏"
    MOTORWAY = "🛣️"
    RAILWAY_TRACK = "🛤️"
    FUELPUMP = "⛽️"
    ROTATING_LIGHT = "🚨"
    TRAFFIC_LIGHT = "🚥"
    VERTICAL_TRAFFIC_LIGHT = "🚦"
    CONSTRUCTION = "🚧"
    ANCHOR = "⚓️"
    SAILBOAT = "⛵️"
    CANOE = "🛶"
    SPEEDBOAT = "🚤"
    CRUISE_SHIP = "🛳️"
    FERRY = "⛴️"
    MOTORBOAT = "🛥️"
    SHIP = "🚢"
    AIRPLANE = "✈️"
    AIRPLANE_SMALL = "🛩️"
    AIRPLANE_DEPARTURE = "🛫"
    AIRPLANE_ARRIVING = "🛬"
    SEAT = "💺"
    HELICOPTER = "🚁"
    SUSPENSION_RAILWAY = "🚟"
    MOUNTAIN_CABLEWAY = "🚠"
    AERIAL_TRAMWAY = "🚡"
    ROCKET = "🚀"
    SATELLITE_ORBITAL = "🛰️"
    STARS = "🌠"
    RAINBOW = "🌈"
    FIREWORKS = "🎆"
    SPARKLER = "🎇"
    RICE_SCENE = "🎑"
    CHECKERED_FLAG = "🏁"
    # Objects
    SKULL_CROSSBONES = "☠️"
    LOVE_LETTER = "💌"
    BOMB = "💣"
    HOLE = "🕳️"
    SHOPPING_BAGS = "🛍️"
    PRAYER_BEADS = "📿"
    GEM = "💎"
    KNIFE = "🔪"
    AMPHORA = "🏺"
    MAP = "🗺️"
    BARBER = "💈"
    FRAME_PHOTO = "🖼️"
    BELLHOP = "🛎️"
    DOOR = "🚪"
    SLEEPING_ACCOMMODATION = "🛌"
    BED = "🛏️"
    COUCH = "🛋️"
    TOILET = "🚽"
    SHOWER = "🚿"
    BATHTUB = "🛁"
    HOURGLASS = "⌛️"
    HOURGLASS_FLOWING_SAND = "⏳"
    WATCH = "⌚️"
    ALARM_CLOCK = "⏰"
    STOPWATCH = "⏱️"
    TIMER = "⏲️"
    CLOCK = "🕰️"
    THERMOMETER = "🌡️"
    BEACH_UMBRELLA = "⛱️"
    BALLOON = "🎈"
    TADA = "🎉"
    CONFETTI_BALL = "🎊"
    DOLLS = "🎎"
    FLAGS = "🎏"
    WIND_CHIME = "🎐"
    RIBBON = "🎀"
    GIFT = "🎁"
    JOYSTICK = "🕹️"
    POSTAL_HORN = "📯"
    MICROPHONE2 = "🎙️"
    LEVEL_SLIDER = "🎚️"
    CONTROL_KNOBS = "🎛️"
    RADIO = "📻"
    IPHONE = "📱"
    CALLING = "📲"
    TELEPHONE = "☎️"
    TELEPHONE_RECEIVER = "📞"
    PAGER = "📟"
    FAX = "📠"
    BATTERY = "🔋"
    ELECTRIC_PLUG = "🔌"
    COMPUTER = "💻"
    DESKTOP = "🖥️"
    PRINTER = "🖨️"
    KEYBOARD = "⌨️"
    MOUSE_THREE_BUTTON = "🖱️"
    TRACKBALL = "🖲️"
    MINIDISC = "💽"
    FLOPPY_DISK = "💾"
    CD = "💿"
    DVD = "📀"
    MOVIE_CAMERA = "🎥"
    FILM_FRAMES = "🎞️"
    PROJECTOR = "📽️"
    TV = "📺"
    CAMERA = "📷"
    CAMERA_WITH_FLASH = "📸"
    VIDEO_CAMERA = "📹"
    VHS = "📼"
    MAG = "🔍"
    MAG_RIGHT = "🔎"
    MICROSCOPE = "🔬"
    TELESCOPE = "🔭"
    SATELLITE = "📡"
    CANDLE = "🕯️"
    BULB = "💡"
    FLASHLIGHT = "🔦"
    IZAKAYA_LANTERN = "🏮"
    NOTEBOOK_WITH_DECORATIVE_COVER = "📔"
    CLOSED_BOOK = "📕"
    BOOK = "📖"
    GREEN_BOOK = "📗"
    BLUE_BOOK = "📘"
    ORANGE_BOOK = "📙"
    BOOKS = "📚"
    NOTEBOOK = "📓"
    LEDGER = "📒"
    PAGE_WITH_CURL = "📃"
    SCROLL = "📜"
    PAGE_FACING_UP = "📄"
    NEWSPAPER = "📰"
    NEWSPAPER2 = "🗞️"
    BOOKMARK_TABS = "📑"
    BOOKMARK = "🔖"
    LABEL = "🏷️"
    MONEYBAG = "💰"
    YEN = "💴"
    DOLLAR = "💵"
    EURO = "💶"
    POUND = "💷"
    MONEY_WITH_WINGS = "💸"
    CREDIT_CARD = "💳"
    ENVELOPE = "✉️"
    E_MAIL = "📧"
    INCOMING_ENVELOPE = "📨"
    ENVELOPE_WITH_ARROW = "📩"
    OUTBOX_TRAY = "📤"
    INBOX_TRAY = "📥"
    PACKAGE = "📦"
    MAILBOX = "📫"
    MAILBOX_CLOSED = "📪"
    MAILBOX_WITH_MAIL = "📬"
    MAILBOX_WITH_NO_MAIL = "📭"
    POSTBOX = "📮"
    BALLOT_BOX = "🗳️"
    PENCIL2 = "✏️"
    BLACK_NIB = "✒️"
    PEN_FOUNTAIN = "🖋️"
    PEN_BALLPOINT = "🖊️"
    PAINTBRUSH = "🖌️"
    CRAYON = "🖍️"
    PENCIL = "📝"
    FILE_FOLDER = "📁"
    OPEN_FILE_FOLDER = "📂"
    DIVIDERS = "🗂️"
    DATE = "📅"
    CALENDAR = "📆"
    NOTEPAD_SPIRAL = "🗒️"
    CALENDAR_SPIRAL = "🗓️"
    CARD_INDEX = "📇"
    CHART_WITH_UPWARDS_TREND = "📈"
    CHART_WITH_DOWNWARDS_TREND = "📉"
    BAR_CHART = "📊"
    CLIPBOARD = "📋"
    PUSHPIN = "📌"
    ROUND_PUSHPIN = "📍"
    PAPERCLIP = "📎"
    PAPERCLIPS = "🖇️"
    STRAIGHT_RULER = "📏"
    TRIANGULAR_RULER = "📐"
    SCISSORS = "✂️"
    CARD_BOX = "🗃️"
    FILE_CABINET = "🗄️"
    WASTEBASKET = "🗑️"
    LOCK = "🔒"
    UNLOCK = "🔓"
    LOCK_WITH_INK_PEN = "🔏"
    CLOSED_LOCK_WITH_KEY = "🔐"
    KEY = "🔑"
    KEY2 = "🗝️"
    HAMMER = "🔨"
    PICK = "⛏️"
    HAMMER_PICK = "⚒️"
    TOOLS = "🛠️"
    DAGGER = "🗡️"
    CROSSED_SWORDS = "⚔️"
    GUN = "🔫"
    SHIELD = "🛡️"
    WRENCH = "🔧"
    NUT_AND_BOLT = "🔩"
    GEAR = "⚙️"
    COMPRESSION = "🗜️"
    ALEMBIC = "⚗️"
    SCALES = "⚖️"
    LINK = "🔗"
    CHAINS = "⛓️"
    SYRINGE = "💉"
    PILL = "💊"
    SMOKING = "🚬"
    COFFIN = "⚰️"
    URN = "⚱️"
    MOYAI = "🗿"
    OIL = "🛢️"
    CRYSTAL_BALL = "🔮"
    SHOPPING_CART = "🛒"
    TRIANGULAR_FLAG_ON_POST = "🚩"
    CROSSED_FLAGS = "🎌"
    FLAG_BLACK = "🏴"
    FLAG_WHITE = "🏳️"
    RAINBOW_FLAG = "🏳🌈"
    # Symbols
    EYE_IN_SPEECH_BUBBLE = "👁‍🗨"
    CUPID = "💘"
    HEART = "❤️"
    HEARTBEAT = "💓"
    BROKEN_HEART = "💔"
    TWO_HEARTS = "💕"
    SPARKLING_HEART = "💖"
    HEARTPULSE = "💗"
    BLUE_HEART = "💙"
    GREEN_HEART = "💚"
    YELLOW_HEART = "💛"
    PURPLE_HEART = "💜"
    BLACK_HEART = "🖤"
    GIFT_HEART = "💝"
    REVOLVING_HEARTS = "💞"
    HEART_DECORATION = "💟"
    HEART_EXCLAMATION = "❣️"
    ANGER = "💢"
    BOOM = "💥"
    DIZZY = "💫"
    SPEECH_BALLOON = "💬"
    SPEECH_LEFT = "🗨️"
    ANGER_RIGHT = "🗯️"
    THOUGHT_BALLOON = "💭"
    WHITE_FLOWER = "💮"
    GLOBE_WITH_MERIDIANS = "🌐"
    HOTSPRINGS = "♨️"
    OCTAGONAL_SIGN = "🛑"
    CLOCK12 = "🕛"
    CLOCK1230 = "🕧"
    CLOCK1 = "🕐"
    CLOCK130 = "🕜"
    CLOCK2 = "🕑"
    CLOCK230 = "🕝"
    CLOCK3 = "🕒"
    CLOCK330 = "🕞"
    CLOCK4 = "🕓"
    CLOCK430 = "🕟"
    CLOCK5 = "🕔"
    CLOCK530 = "🕠"
    CLOCK6 = "🕕"
    CLOCK630 = "🕡"
    CLOCK7 = "🕖"
    CLOCK730 = "🕢"
    CLOCK8 = "🕗"
    CLOCK830 = "🕣"
    CLOCK9 = "🕘"
    CLOCK930 = "🕤"
    CLOCK10 = "🕙"
    CLOCK1030 = "🕥"
    CLOCK11 = "🕚"
    CLOCK1130 = "🕦"
    CYCLONE = "🌀"
    SPADES = "♠️"
    HEARTS = "♥️"
    DIAMONDS = "♦️"
    CLUBS = "♣️"
    BLACK_JOKER = "🃏"
    MAHJONG = "🀄️"
    FLOWER_PLAYING_CARDS = "🎴"
    MUTE = "🔇"
    SPEAKER = "🔈"
    SOUND = "🔉"
    LOUD_SOUND = "🔊"
    LOUDSPEAKER = "📢"
    MEGA = "📣"
    BELL = "🔔"
    NO_BELL = "🔕"
    MUSICAL_NOTE = "🎵"
    NOTES = "🎶"
    CHART = "💹"
    CURRENCY_EXCHANGE = "💱"
    HEAVY_DOLLAR_SIGN = "💲"
    ATM = "🏧"
    PUT_LITTER_IN_ITS_PLACE = "🚮"
    POTABLE_WATER = "🚰"
    WHEELCHAIR = "♿️"
    MENS = "🚹"
    WOMENS = "🚺"
    RESTROOM = "🚻"
    BABY_SYMBOL = "🚼"
    WC = "🚾"
    PASSPORT_CONTROL = "🛂"
    CUSTOMS = "🛃"
    BAGGAGE_CLAIM = "🛄"
    LEFT_LUGGAGE = "🛅"
    WARNING = "⚠️"
    CHILDREN_CROSSING = "🚸"
    NO_ENTRY = "⛔️"
    NO_ENTRY_SIGN = "🚫"
    NO_BICYCLES = "🚳"
    NO_SMOKING = "🚭"
    DO_NOT_LITTER = "🚯"
    NON_POTABLE_WATER = "🚱"
    NO_PEDESTRIANS = "🚷"
    NO_MOBILE_PHONES = "📵"
    UNDERAGE = "🔞"
    RADIOACTIVE = "☢️"
    BIOHAZARD = "☣️"
    ARROW_UP = "⬆️"
    ARROW_UPPER_RIGHT = "↗️"
    ARROW_RIGHT = "➡️"
    ARROW_LOWER_RIGHT = "↘️"
    ARROW_DOWN = "⬇️"
    ARROW_LOWER_LEFT = "↙️"
    ARROW_LEFT = "⬅️"
    ARROW_UPPER_LEFT = "↖️"
    ARROW_UP_DOWN = "↕️"
    LEFT_RIGHT_ARROW = "↔️"
    LEFTWARDS_ARROW_WITH_HOOK = "↩️"
    ARROW_RIGHT_HOOK = "↪️"
    ARROW_HEADING_UP = "⤴️"
    ARROW_HEADING_DOWN = "⤵️"
    ARROWS_CLOCKWISE = "🔃"
    ARROWS_COUNTERCLOCKWISE = "🔄"
    BACK = "🔙"
    END = "🔚"
    ON = "🔛"
    SOON = "🔜"
    TOP = "🔝"
    PLACE_OF_WORSHIP = "🛐"
    ATOM = "⚛️"
    OM_SYMBOL = "🕉️"
    STAR_OF_DAVID = "✡️"
    WHEEL_OF_DHARMA = "☸️"
    YIN_YANG = "☯️"
    CROSS = "✝️"
    ORTHODOX_CROSS = "☦️"
    STAR_AND_CRESCENT = "☪️"
    PEACE = "☮️"
    MENORAH = "🕎"
    SIX_POINTED_STAR = "🔯"
    ARIES = "♈️"
    TAURUS = "♉️"
    GEMINI = "♊️"
    CANCER = "♋️"
    LEO = "♌️"
    VIRGO = "♍️"
    LIBRA = "♎️"
    SCORPIUS = "♏️"
    SAGITTARIUS = "♐️"
    CAPRICORN = "♑️"
    AQUARIUS = "♒️"
    PISCES = "♓️"
    OPHIUCHUS = "⛎"
    TWISTED_RIGHTWARDS_ARROWS = "🔀"
    REPEAT = "🔁"
    REPEAT_ONE = "🔂"
    ARROW_FORWARD = "▶️"
    FAST_FORWARD = "⏩"
    TRACK_NEXT = "⏭️"
    PLAY_PAUSE = "⏯️"
    ARROW_BACKWARD = "◀️"
    REWIND = "⏪"
    TRACK_PREVIOUS = "⏮️"
    ARROW_UP_SMALL = "🔼"
    ARROW_DOUBLE_UP = "⏫"
    ARROW_DOWN_SMALL = "🔽"
    ARROW_DOUBLE_DOWN = "⏬"
    PAUSE_BUTTON = "⏸️"
    STOP_BUTTON = "⏹️"
    RECORD_BUTTON = "⏺️"
    EJECT = "⏏️"
    CINEMA = "🎦"
    LOW_BRIGHTNESS = "🔅"
    HIGH_BRIGHTNESS = "🔆"
    SIGNAL_STRENGTH = "📶"
    VIBRATION_MODE = "📳"
    MOBILE_PHONE_OFF = "📴"
    RECYCLE = "♻️"
    NAME_BADGE = "📛"
    FLEUR_DE_LIS = "⚜️"
    BEGINNER = "🔰"
    TRIDENT = "🔱"
    CIRCLE = "⭕️"
    WHITE_CHECK_MARK = "✅"
    BALLOT_BOX_WITH_CHECK = "☑️"
    HEAVY_CHECK_MARK = "✔️"
    HEAVY_MULTIPLICATION_X = "✖️"
    X = "❌"
    NEGATIVE_SQUARED_CROSS_MARK = "❎"
    HEAVY_PLUS_SIGN = "➕"
    HEAVY_MINUS_SIGN = "➖"
    HEAVY_DIVISION_SIGN = "➗"
    CURLY_LOOP = "➰"
    LOOP = "➿"
    PART_ALTERNATION_MARK = "〽️"
    EIGHT_SPOKED_ASTERISK = "✳️"
    EIGHT_POINTED_BLACK_STAR = "✴️"
    SPARKLE = "❇️"
    BANGBANG = "‼️"
    INTERROBANG = "⁉️"
    QUESTION = "❓"
    GREY_QUESTION = "❔"
    GREY_EXCLAMATION = "❕"
    EXCLAMATION = "❗️"
    WAVY_DASH = "〰️"
    COPYRIGHT = "©️"
    REGISTERED = "®️"
    TM = "™️"
    HASH = "#️⃣"
    ASTERISK = "*️⃣"
    ZERO = "0️⃣"
    ONE = "1️⃣"
    TWO = "2️⃣"
    THREE = "3️⃣"
    FOUR = "4️⃣"
    FIVE = "5️⃣"
    SIX = "6️⃣"
    SEVEN = "7️⃣"
    EIGHT = "8️⃣"
    NINE = "9️⃣"
    KEYCAP_TEN = "🔟"
    ONE_HUNDRED = "💯"
    CAPITAL_ABCD = "🔠"
    ABCD = "🔡"
    ONE_TWO_THREE_FOUR = "🔢"
    SYMBOLS = "🔣"
    ABC = "🔤"
    A = "🅰"
    AB = "🆎"
    B = "🅱"
    CL = "🆑"
    COOL = "🆒"
    FREE = "🆓"
    INFORMATION_SOURCE = "ℹ️"
    ID = "🆔"
    M = "Ⓜ️"
    NEW = "🆕"
    NG = "🆖"
    O2 = "🅾"
    OK = "🆗"
    PARKING = "🅿️"
    SOS = "🆘"
    UP = "🆙"
    VS = "🆚"
    KOKO = "🈁"
    SA = "🈂️"
    U6708 = "🈷️"
    U6709 = "🈶"
    U6307 = "🈯️"
    IDEOGRAPH_ADVANTAGE = "🉐"
    U5272 = "🈹"
    U7121 = "🈚️"
    U7981 = "🈲"
    ACCEPT = "🉑"
    U7533 = "🈸"
    U5408 = "🈴"
    U7A7A = "🈳"
    CONGRATULATIONS = "㊗️"
    SECRET = "㊙️"
    U55B6 = "🈺"
    U6E80 = "🈵"
    BLACK_SMALL_SQUARE = "▪️"
    WHITE_SMALL_SQUARE = "▫️"
    WHITE_MEDIUM_SQUARE = "◻️"
    BLACK_MEDIUM_SQUARE = "◼️"
    WHITE_MEDIUM_SMALL_SQUARE = "◽️"
    BLACK_MEDIUM_SMALL_SQUARE = "◾️"
    BLACK_LARGE_SQUARE = "⬛️"
    WHITE_LARGE_SQUARE = "⬜️"
    LARGE_ORANGE_DIAMOND = "🔶"
    LARGE_BLUE_DIAMOND = "🔷"
    SMALL_ORANGE_DIAMOND = "🔸"
    SMALL_BLUE_DIAMOND = "🔹"
    SMALL_RED_TRIANGLE = "🔺"
    SMALL_RED_TRIANGLE_DOWN = "🔻"
    DIAMOND_SHAPE_WITH_A_DOT_INSIDE = "💠"
    RADIO_BUTTON = "🔘"
    BLACK_SQUARE_BUTTON = "🔲"
    WHITE_SQUARE_BUTTON = "🔳"
    WHITE_CIRCLE = "⚪️"
    BLACK_CIRCLE = "⚫️"
    RED_CIRCLE = "🔴"
    BLUE_CIRCLE = "🔵"
    # Flags
    FLAG_AC = "🇦🇨"
    FLAG_AD = "🇦🇩"
    FLAG_AE = "🇦🇪"
    FLAG_AF = "🇦🇫"
    FLAG_AG = "🇦🇬"
    FLAG_AI = "🇦🇮"
    FLAG_AL = "🇦🇱"
    FLAG_AM = "🇦🇲"
    FLAG_AO = "🇦🇴"
    FLAG_AQ = "🇦🇶"
    FLAG_AR = "🇦🇷"
    FLAG_AS = "🇦🇸"
    FLAG_AT = "🇦🇹"
    FLAG_AU = "🇦🇺"
    FLAG_AW = "🇦🇼"
    FLAG_AX = "🇦🇽"
    FLAG_AZ = "🇦🇿"
    FLAG_BA = "🇧🇦"
    FLAG_BB = "🇧🇧"
    FLAG_BD = "🇧🇩"
    FLAG_BE = "🇧🇪"
    FLAG_BF = "🇧🇫"
    FLAG_BG = "🇧🇬"
    FLAG_BH = "🇧🇭"
    FLAG_BI = "🇧🇮"
    FLAG_BJ = "🇧🇯"
    FLAG_BL = "🇧🇱"
    FLAG_BM = "🇧🇲"
    FLAG_BN = "🇧🇳"
    FLAG_BO = "🇧🇴"
    FLAG_BQ = "🇧🇶"
    FLAG_BR = "🇧🇷"
    FLAG_BS = "🇧🇸"
    FLAG_BT = "🇧🇹"
    FLAG_BV = "🇧🇻"
    FLAG_BW = "🇧🇼"
    FLAG_BY = "🇧🇾"
    FLAG_BZ = "🇧🇿"
    FLAG_CA = "🇨🇦"
    FLAG_CC = "🇨🇨"
    FLAG_CD = "🇨🇩"
    FLAG_CF = "🇨🇫"
    FLAG_CG = "🇨🇬"
    FLAG_CH = "🇨🇭"
    FLAG_CI = "🇨🇮"
    FLAG_CK = "🇨🇰"
    FLAG_CL = "🇨🇱"
    FLAG_CM = "🇨🇲"
    FLAG_CN = "🇨🇳"
    FLAG_CO = "🇨🇴"
    FLAG_CP = "🇨🇵"
    FLAG_CR = "🇨🇷"
    FLAG_CU = "🇨🇺"
    FLAG_CV = "🇨🇻"
    FLAG_CW = "🇨🇼"
    FLAG_CX = "🇨🇽"
    FLAG_CY = "🇨🇾"
    FLAG_CZ = "🇨🇿"
    FLAG_DE = "🇩🇪"
    FLAG_DG = "🇩🇬"
    FLAG_DJ = "🇩🇯"
    FLAG_DK = "🇩🇰"
    FLAG_DM = "🇩🇲"
    FLAG_DO = "🇩🇴"
    FLAG_DZ = "🇩🇿"
    FLAG_EA = "🇪🇦"
    FLAG_EC = "🇪🇨"
    FLAG_EE = "🇪🇪"
    FLAG_EG = "🇪🇬"
    FLAG_EH = "🇪🇭"
    FLAG_ER = "🇪🇷"
    FLAG_ES = "🇪🇸"
    FLAG_ET = "🇪🇹"
    FLAG_EU = "🇪🇺"
    FLAG_FI = "🇫🇮"
    FLAG_FJ = "🇫🇯"
    FLAG_FK = "🇫🇰"
    FLAG_FM = "🇫🇲"
    FLAG_FO = "🇫🇴"
    FLAG_FR = "🇫🇷"
    FLAG_GA = "🇬🇦"
    FLAG_GB = "🇬🇧"
    FLAG_GD = "🇬🇩"
    FLAG_GE = "🇬🇪"
    FLAG_GF = "🇬🇫"
    FLAG_GG = "🇬🇬"
    FLAG_GH = "🇬🇭"
    FLAG_GI = "🇬🇮"
    FLAG_GL = "🇬🇱"
    FLAG_GM = "🇬🇲"
    FLAG_GN = "🇬🇳"
    FLAG_GP = "🇬🇵"
    FLAG_GQ = "🇬🇶"
    FLAG_GR = "🇬🇷"
    FLAG_GS = "🇬🇸"
    FLAG_GT = "🇬🇹"
    FLAG_GU = "🇬🇺"
    FLAG_GW = "🇬🇼"
    FLAG_GY = "🇬🇾"
    FLAG_HK = "🇭🇰"
    FLAG_HM = "🇭🇲"
    FLAG_HN = "🇭🇳"
    FLAG_HR = "🇭🇷"
    FLAG_HT = "🇭🇹"
    FLAG_HU = "🇭🇺"
    FLAG_IC = "🇮🇨"
    FLAG_ID = "🇮🇩"
    FLAG_IE = "🇮🇪"
    FLAG_IL = "🇮🇱"
    FLAG_IM = "🇮🇲"
    FLAG_IN = "🇮🇳"
    FLAG_IO = "🇮🇴"
    FLAG_IQ = "🇮🇶"
    FLAG_IR = "🇮🇷"
    FLAG_IS = "🇮🇸"
    FLAG_IT = "🇮🇹"
    FLAG_JE = "🇯🇪"
    FLAG_JM = "🇯🇲"
    FLAG_JO = "🇯🇴"
    FLAG_JP = "🇯🇵"
    FLAG_KE = "🇰🇪"
    FLAG_KG = "🇰🇬"
    FLAG_KH = "🇰🇭"
    FLAG_KI = "🇰🇮"
    FLAG_KM = "🇰🇲"
    FLAG_KN = "🇰🇳"
    FLAG_KP = "🇰🇵"
    FLAG_KR = "🇰🇷"
    FLAG_KW = "🇰🇼"
    FLAG_KY = "🇰🇾"
    FLAG_KZ = "🇰🇿"
    FLAG_LA = "🇱🇦"
    FLAG_LB = "🇱🇧"
    FLAG_LC = "🇱🇨"
    FLAG_LI = "🇱🇮"
    FLAG_LK = "🇱🇰"
    FLAG_LR = "🇱🇷"
    FLAG_LS = "🇱🇸"
    FLAG_LT = "🇱🇹"
    FLAG_LU = "🇱🇺"
    FLAG_LV = "🇱🇻"
    FLAG_LY = "🇱🇾"
    FLAG_MA = "🇲🇦"
    FLAG_MC = "🇲🇨"
    FLAG_MD = "🇲🇩"
    FLAG_ME = "🇲🇪"
    FLAG_MF = "🇲🇫"
    FLAG_MG = "🇲🇬"
    FLAG_MH = "🇲🇭"
    FLAG_MK = "🇲🇰"
    FLAG_ML = "🇲🇱"
    FLAG_MM = "🇲🇲"
    FLAG_MN = "🇲🇳"
    FLAG_MO = "🇲🇴"
    FLAG_MP = "🇲🇵"
    FLAG_MQ = "🇲🇶"
    FLAG_MR = "🇲🇷"
    FLAG_MS = "🇲🇸"
    FLAG_MT = "🇲🇹"
    FLAG_MU = "🇲🇺"
    FLAG_MV = "🇲🇻"
    FLAG_MW = "🇲🇼"
    FLAG_MX = "🇲🇽"
    FLAG_MY = "🇲🇾"
    FLAG_MZ = "🇲🇿"
    FLAG_NA = "🇳🇦"
    FLAG_NC = "🇳🇨"
    FLAG_NE = "🇳🇪"
    FLAG_NF = "🇳🇫"
    FLAG_NG = "🇳🇬"
    FLAG_NI = "🇳🇮"
    FLAG_NL = "🇳🇱"
    FLAG_NO = "🇳🇴"
    FLAG_NP = "🇳🇵"
    FLAG_NR = "🇳🇷"
    FLAG_NU = "🇳🇺"
    FLAG_NZ = "🇳🇿"
    FLAG_OM = "🇴🇲"
    FLAG_PA = "🇵🇦"
    FLAG_PE = "🇵🇪"
    FLAG_PF = "🇵🇫"
    FLAG_PG = "🇵🇬"
    FLAG_PH = "🇵🇭"
    FLAG_PK = "🇵🇰"
    FLAG_PL = "🇵🇱"
    FLAG_PM = "🇵🇲"
    FLAG_PN = "🇵🇳"
    FLAG_PR = "🇵🇷"
    FLAG_PS = "🇵🇸"
    FLAG_PT = "🇵🇹"
    FLAG_PW = "🇵🇼"
    FLAG_PY = "🇵🇾"
    FLAG_QA = "🇶🇦"
    FLAG_RE = "🇷🇪"
    FLAG_RO = "🇷🇴"
    FLAG_RS = "🇷🇸"
    FLAG_RU = "🇷🇺"
    FLAG_RW = "🇷🇼"
    FLAG_SA = "🇸🇦"
    FLAG_SB = "🇸🇧"
    FLAG_SC = "🇸🇨"
    FLAG_SD = "🇸🇩"
    FLAG_SE = "🇸🇪"
    FLAG_SG = "🇸🇬"
    FLAG_SH = "🇸🇭"
    FLAG_SI = "🇸🇮"
    FLAG_SJ = "🇸🇯"
    FLAG_SK = "🇸🇰"
    FLAG_SL = "🇸🇱"
    FLAG_SM = "🇸🇲"
    FLAG_SN = "🇸🇳"
    FLAG_SO = "🇸🇴"
    FLAG_SR = "🇸🇷"
    FLAG_SS = "🇸🇸"
    FLAG_ST = "🇸🇹"
    FLAG_SV = "🇸🇻"
    FLAG_SX = "🇸🇽"
    FLAG_SY = "🇸🇾"
    FLAG_SZ = "🇸🇿"
    FLAG_TA = "🇹🇦"
    FLAG_TC = "🇹🇨"
    FLAG_TD = "🇹🇩"
    FLAG_TF = "🇹🇫"
    FLAG_TG = "🇹🇬"
    FLAG_TH = "🇹🇭"
    FLAG_TJ = "🇹🇯"
    FLAG_TK = "🇹🇰"
    FLAG_TL = "🇹🇱"
    FLAG_TM = "🇹🇲"
    FLAG_TN = "🇹🇳"
    FLAG_TO = "🇹🇴"
    FLAG_TR = "🇹🇷"
    FLAG_TT = "🇹🇹"
    FLAG_TV = "🇹🇻"
    FLAG_TW = "🇹🇼"
    FLAG_TZ = "🇹🇿"
    FLAG_UA = "🇺🇦"
    FLAG_UG = "🇺🇬"
    FLAG_UM = "🇺🇲"
    FLAG_US = "🇺🇸"
    FLAG_UY = "🇺🇾"
    FLAG_UZ = "🇺🇿"
    FLAG_VA = "🇻🇦"
    FLAG_VC = "🇻🇨"
    FLAG_VE = "🇻🇪"
    FLAG_VG = "🇻🇬"
    FLAG_VI = "🇻🇮"
    FLAG_VN = "🇻🇳"
    FLAG_VU = "🇻🇺"
    FLAG_WF = "🇼🇫"
    FLAG_WS = "🇼🇸"
    FLAG_XK = "🇽🇰"
    FLAG_YE = "🇾🇪"
    FLAG_YT = "🇾🇹"
    FLAG_ZA = "🇿🇦"
    FLAG_ZM = "🇿🇲"
    FLAG_ZW = "🇿🇼"

    # Custom aliases _ These aliases exist in the legacy versions and
    # the non_conflicting ones are kept here for backward compatibility
    HM = "🤔"
    SATISFIED = "😌"
    COLLISION = "💥"
    SHIT = "💩"
    _1 = "👎"
    FACEPUNCH = "👊"
    HAND = "✋"
    RUNNING = "🏃"
    HONEYBEE = "🐝"
    PAW_PRINTS = "🐾"
    MOON = "🌙"
    HOCHO = "🔪"
    SHOE = "👞"
    TSHIRT = "👕"
    FLAG_UK = "🇬🇧"
    CHEMISTRY = "🧪"
    MAN_LIFTING_WEIGHTS = "🏋️‍♂️"
    WOMAN_OFFICE_WORKER = "👩‍💼"
    ABACUS = "🧮"
    PURPLE_CIRCLE = "🟣"
    MAN_TEACHER = "👨‍🏫"
    KITE = "🪁"
    CORONAVIRUS = "🦠"
    BLUE_CAP = "🧢"
    NO_IDEA = "🤷‍♂️"
    DNA = "🧬"


class Subjects_Map(Enum2):
    ENGLISH = f"{TG_Emoji_Map.FLAG_UK} Англійська мова"
    CHEMISTRY = f"{TG_Emoji_Map.CHEMISTRY} Хімія"
    BIOLOGY = f"{TG_Emoji_Map.MICROSCOPE} Біологія"
    INFORMATICS = f"{TG_Emoji_Map.COMPUTER} Інформатика"
    ALGEBRA = f"{TG_Emoji_Map.HEAVY_PLUS_SIGN} Алгебра"
    GEOMETRY = f"{TG_Emoji_Map.SMALL_RED_TRIANGLE} Геометрія"
    MATHEMATICS = f"{TG_Emoji_Map.TRIANGULAR_RULER} Математика"
    CIVIC_EDUCATION = f"{TG_Emoji_Map.CLASSICAL_BUILDING} Громадянська освіта"
    JURISPRUDENCE = f"{TG_Emoji_Map.SCALES} Правознавство"
    UKRAINIAN = f"{TG_Emoji_Map.FLAG_UA} Українська мова"
    UKRAINIAN_LITERATURE = f"{TG_Emoji_Map.BOOK} Українська література"
    PHYSICS = f"{TG_Emoji_Map.ATOM} Фізика"
    FOREIGN_LITERATURE = f"{TG_Emoji_Map.EARTH_ASIA} Зарубіжна література"
    DEFENCE_OF_UKRAINE = f"{TG_Emoji_Map.SHIELD} Захист України"
    TECHNOLOGY = f"{TG_Emoji_Map.WRENCH} Технології"
    GEOGRAPHY = f"{TG_Emoji_Map.MAP} Географія"
    HISTORY_OF_UKRAINE = f"{TG_Emoji_Map.BOOKS} Історія України"
    WORLD_HISTORY = f"{TG_Emoji_Map.EARTH_AMERICAS} Всесвітня історія"
    FINE_ARTS = f"{TG_Emoji_Map.ART} Образотворче мистецтво"
    PHYSICAL_EDUCATION = f"{TG_Emoji_Map.MAN_LIFTING_WEIGHTS} Фізкультура"
    MUSICAL_ART = f"{TG_Emoji_Map.MUSICAL_NOTE} Музичне мистецтво"
    LEARNING_ABOUT_NATURE = f"{TG_Emoji_Map.HERB} Пізнаємо природу"
    ASTRONOMY = f"{TG_Emoji_Map.TELESCOPE} Астрономія"


class Any_Map(Enum2):
    CLASSROOMS = ["5", "6-А", "6-Б", "7", "8", "9", "10", "11"]
    RESULTS_PER_PAGE = 7
    CITY_ALERT_ID = 9


class Text_Map(Enum2):
    SPACER = f"\n{TG_Emoji_Map.HEAVY_MINUS_SIGN * 11}\n"
    SELECT_ITEM = f"<b>Оберіть необхідний пункт {TG_Emoji_Map.POINT_DOWN}</b>"
    NO_RESULTS = f"Інформація не знайдена {TG_Emoji_Map.CONFUSED}"
    NO_RESULTS2 = "Не знайдено"
    NO_RESULTS2_MONO_FONT = f"<code>{NO_RESULTS2}</code>"
    DATA_UPDATED = f"Дані оновлено {TG_Emoji_Map.SLIGHT_SMILE}"
    MAIN = f"{TG_Emoji_Map.HOUSE} Головна"
    BACK = f"{TG_Emoji_Map.BACK} Назад"
    TRY_TYPE_CORRECT = f"{TG_Emoji_Map.X} Спробуйте написати команду коректно"
    USERNAME_NOT_FOUND = "Користувач з username \n{} \nне знайдений"
    IT_IS_IN_BASE = "Цей {} вже є в базі"
    IT_IS_NOT_IN_BASE = "{} немає в базі"
    WAIT_FOR_RESPONSE = "<b>Очікуйте на відповідь</b>"
    REVERSED_POINT = "Ви вже обрали цей пункт"
    HELP_TEXT = TG_Emoji_Map.QUESTION
    NO_EMOJI = "Використання емодзі заборонено"
    RECESS = f"{TG_Emoji_Map.PAUSE_BUTTON} Перерва"
    CHILL = f"{TG_Emoji_Map.BEACH} Відпочинок"
    MY_USERNAME = "@borysfen_dp_bot"
    MY_CITY = "Дніпро"
    SENDING_FAILED = "Відправлення не вдалось"
    GOOD_RESULTS = f"Інформація знайдена {TG_Emoji_Map.SLIGHT_SMILE}"
    MESSAGES_BASE_ID = "-1001908541413"
    NO_THREATS = f"{TG_Emoji_Map.WHITE_CHECK_MARK} Загроз не виявлено"
    IN_PROCESS = "<b>У процесі...</b>"
    WIKI_LINK = "<a href='https://uk.wikipedia.org/wiki/{}'>{}</a>"
    CONFIG_DIR = "Additions/BorysfenBot_Required_additions"
    FAKE_VOID = "ㅤ"
    YES = f"{TG_Emoji_Map.WHITE_CHECK_MARK} Так"
    PERSONAL_DATA_AGREEMENT_SHORT = f"<b>Відповідно до Закону України «Про захист персональних даних»\n\nНатискаючи «{YES}», \
я даю згоду на обробку моїх персональних даних.</b>"
    PERSONAL_DATA_AGREEMENT = f"""<b>
Відповідно до Закону України «Про захист персональних даних» натискаючи «{YES}», я даю згоду на обробку моїх персональних даних у такому обсязі:

Відомості про освіту, номери телефонів; 
Використання персональних даних, що передбачає дії володільця бази щодо обробки цих даних, в тому числі використання персональних даних відповідно до їх дії щодо їх захисту, а також дії щодо надання часткового або повного права обробки персональних даних іншим суб’єктам відносин, пов’язаних із персональними даними (стаття 10 зазначеного Закону);
Поширення персональних даних, що передбачає дії володільця бази персональних даних щодо передачі відомостей про фізичну особу з бази персональних даних (стаття 14 зазначеного Закону);
Доступ до персональних даних третіх осіб, що визначає дії володільця бази персональних даних у разі отримання запиту від третьої особи щодо доступу до персональних даних, у тому числі порядок доступу суб’єкта персональних даних до відомостей про себе (стаття 16 зазначеного Закону).
</b>"""
    CLICK_ON_THE_BUTTON = f"Натисніть на кнопку {TG_Emoji_Map.POINT_DOWN}"
    DELETE = f"{TG_Emoji_Map.WASTEBASKET} Видалити"
    DATA_SEARCH_SEP = f"_{TG_Emoji_Map.SCROLL}_"
    GOOGLE = "<a href='https://www.google.com/search?q={}'>{}</a>"
    GOOGLE_LAMBDA = (
        lambda error: "<a href='https://www.google.com/search?q=%22{}%22'>{}</a>".format(
            quote(str(error)), error
        )
    )
    TELEPHONE = "<code>{}</code>"
    T_ME = "<a href='https://t.me/{}'>Telegram</a>"
    VIBER_CLICK = "<a href='https://viber.click/+{}'>Viber</a>"
    INSTEAD_OF = "текст</code> \nзамість "
    NO_CHANGES = f"Нічого не змінилося{TG_Emoji_Map.EXCLAMATION}{SPACER}Ничего не изменилось{TG_Emoji_Map.EXCLAMATION}"
    FILE_TOO_LARGE = "{} Відправлений файл занадто великий, ви можете завантажувати файли розміром до {}"
    DETECTION = "{} Виявлення {} / {}\n\n"
    DETECTION_BUTTON = f"{TG_Emoji_Map.CHEMISTRY} Виявлення"
    SIGNATURE_BUTTON = f"{TG_Emoji_Map.SYRINGE} Сигнатури"
    THREAT_FOUND = (
        "{} Виявлено загрозу {}\n\n<a href='{}'>{} Посилання на VirusTotal</a>"
    )
    BOOKS = f"{TG_Emoji_Map.BOOKS} Книжки"
    COMMANDS_LIST = f"{TG_Emoji_Map.CLIPBOARD} Список команд"
    TIMETABLE = f"{TG_Emoji_Map.PENCIL} Розклад"


class DB_Map(Enum2):
    NAME = TG_Emoji_Map.BUST_IN_SILHOUETTE
    ID = TG_Emoji_Map.ID
    ROLE = TG_Emoji_Map.PERFORMING_ARTS
    CLASSROOM = TG_Emoji_Map.DOOR
    PHONE_NUMBER = TG_Emoji_Map.TELEPHONE_RECEIVER
    USERNAME = TG_Emoji_Map.CYCLONE
    MAIL_ADDRESS = TG_Emoji_Map.MAILBOX_WITH_MAIL
    ADDER_ID = TG_Emoji_Map.PENCIL
    DATE = "🗓"
    PERSONAL_DATA_AGREEMENT = TG_Emoji_Map.PAGE_WITH_CURL
    KEY = TG_Emoji_Map.KEY
    ADMIN = "Admin"
    STAFF = "Staff"
    TEACHER = "Вчитель"
    STUDENT = "Студент"
    USER_COLUMNS = {
        NAME: "TEXT",
        ID: "TEXT",
        ROLE: "TEXT",
        CLASSROOM: f"TEXT DEFAULT {Text_Map.FAKE_VOID}",
        PHONE_NUMBER: f"TEXT DEFAULT {Text_Map.FAKE_VOID}",
        USERNAME: "TEXT",
        MAIL_ADDRESS: f"TEXT DEFAULT {Text_Map.FAKE_VOID}",
        ADDER_ID: "TEXT",
        DATE: "TEXT",
        PERSONAL_DATA_AGREEMENT: f"TEXT DEFAULT {Text_Map.FAKE_VOID}",
    }
    MESSAGE_COLUMNS = {
        ADDER_ID: "INTEGER",
        ID: "INTEGER PRIMARY KEY",
        KEY: "TEXT UNIQUE",
    }
    AGREED = "Згоден"


class Dict_Map(Enum2):
    CONTACT_INFORMATION = {
        f"{TG_Emoji_Map.HOUSE} Адреса": "м. Дніпро, вул. Конотопська, 15",
        f"{TG_Emoji_Map.WOMAN_OFFICE_WORKER} Секретар": "+380 50 065 2258",
        f"{TG_Emoji_Map.ABACUS} Бухгалтерія": "+380 56 717 0315",
        f"{TG_Emoji_Map.MAILBOX_WITH_MAIL} E-mail": "boardingschool4@gmail.com",
    }
    DAYS_OF_WEEK_MAP = {
        "Monday": "Понеділок",
        "Tuesday": "Вівторок",
        "Wednesday": "Середа",
        "Thursday": "Четвер",
        "Friday": "Пʼятниця",
        "Saturday": "Субота",
        "Sunday": "Неділя",
    }
    PEOPLE_MAP = {
        "Norman Preston": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Norman Preston",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Arnita Lowe": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Arnita Lowe",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Brendon Pennington": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Brendon Pennington",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
            TG_Emoji_Map.MAILBOX_WITH_MAIL: "fought1880@protonmail.com",
        },
        "Velvet Hays": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Velvet Hays",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
            TG_Emoji_Map.MAILBOX_WITH_MAIL: "vpharmaceuticals2070@example.com",
        },
        "Terrence Fulton": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Terrence Fulton",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
            TG_Emoji_Map.MAILBOX_WITH_MAIL: "opening1948@example.com",
        },
        "Julieann Nielsen": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Julieann Nielsen",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Ria Leonard": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Ria Leonard",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Roselia Vance": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Roselia Vance",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Victor Tran": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Victor Tran",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "17173327892"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
            TG_Emoji_Map.MAILBOX_WITH_MAIL: "pharmaceuticals2070@example.com",
        },
        "Jolie Jacobs": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Jolie Jacobs",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
            TG_Emoji_Map.MAILBOX_WITH_MAIL: "pharmaceuticals2070@example.com",
        },
        "Arnold Guthrie": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Arnold Guthrie",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Monty Davenport": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Monty Davenport",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Gertrudis Hood": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Gertrudis Hood",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Julius Frost": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Julius Frost",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-747-774-8976"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Ted Puckett": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Ted Puckett",
            TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.TELEPHONE.format(
                "+1-704-419-6281"
            ),
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("+17173327892"),
            TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.VIBER_CLICK.format("17173327892"),
        },
        "Janay Gilliam": {
            TG_Emoji_Map.BUST_IN_SILHOUETTE: "Janay Gilliam",
            TG_Emoji_Map.BLUE_CIRCLE: Text_Map.T_ME.format("walk_2088"),
            TG_Emoji_Map.MAILBOX_WITH_MAIL: "pharmaceuticals2070@example.com",
        },
    }
    SUBJECTS = {
        Subjects_Map.ENGLISH: [
            PEOPLE_MAP["Norman Preston"],
            PEOPLE_MAP["Arnold Guthrie"],
        ],
        Subjects_Map.CHEMISTRY: PEOPLE_MAP["Arnita Lowe"],
        Subjects_Map.BIOLOGY: PEOPLE_MAP["Arnita Lowe"],
        Subjects_Map.INFORMATICS: [
            PEOPLE_MAP["Janay Gilliam"],
            PEOPLE_MAP["Jolie Jacobs"],
        ],
        Subjects_Map.ALGEBRA: [
            PEOPLE_MAP["Ted Puckett"],
            PEOPLE_MAP["Monty Davenport"],
        ],
        Subjects_Map.GEOMETRY: [
            PEOPLE_MAP["Ted Puckett"],
            PEOPLE_MAP["Monty Davenport"],
        ],
        Subjects_Map.MATHEMATICS: [
            PEOPLE_MAP["Ted Puckett"],
            PEOPLE_MAP["Monty Davenport"],
        ],
        Subjects_Map.UKRAINIAN: PEOPLE_MAP["Velvet Hays"],
        Subjects_Map.UKRAINIAN_LITERATURE: PEOPLE_MAP["Velvet Hays"],
        Subjects_Map.PHYSICS: PEOPLE_MAP["Terrence Fulton"],
        Subjects_Map.FOREIGN_LITERATURE: PEOPLE_MAP["Julieann Nielsen"],
        Subjects_Map.DEFENCE_OF_UKRAINE: [
            PEOPLE_MAP["Ria Leonard"],
            PEOPLE_MAP["Roselia Vance"],
        ],
        Subjects_Map.TECHNOLOGY: PEOPLE_MAP["Jolie Jacobs"],
        Subjects_Map.GEOGRAPHY: PEOPLE_MAP["Victor Tran"],
        Subjects_Map.HISTORY_OF_UKRAINE: PEOPLE_MAP["Brendon Pennington"],
        Subjects_Map.WORLD_HISTORY: PEOPLE_MAP["Brendon Pennington"],
        Subjects_Map.FINE_ARTS: PEOPLE_MAP["Jolie Jacobs"],
        Subjects_Map.PHYSICAL_EDUCATION: PEOPLE_MAP["Julius Frost"],
        Subjects_Map.MUSICAL_ART: PEOPLE_MAP["Gertrudis Hood"],
        Subjects_Map.ASTRONOMY: PEOPLE_MAP["Terrence Fulton"],
    }
    ERRORS = {
        "IndexError": {
            "try": f"Упс!.. Хибний запит. Спробуйте так {TG_Emoji_Map.POINT_DOWN}\n\n",
            "SEARCH_TEACHER": f"{Text_Map.INSTEAD_OF}'текст' написати ім'я, прізвище, по батькові",
            "ASK": {"user": "текст</code>", "admin": "ID текст</code>"},
            "DATA_SEARCH": "шуканий текст</code>",
            "ADD_INFO": {
                DB_Map.NAME: f"{Text_Map.INSTEAD_OF}'текст' написати ім'я, прізвище, по батькові",
                DB_Map.MAIL_ADDRESS: f"{Text_Map.INSTEAD_OF}'текст' написати адресу електронної пошти, можливо, ви ввели її неправильно.",
                "id_and_text": f"ID {Text_Map.INSTEAD_OF} 'ID' (Telegram {TG_Emoji_Map.ID}) можна написати {TG_Emoji_Map.CYCLONE} (Ім'я користувача)\nзамість 'текст' написати ім'я, прізвище, по батькові",
                "id": f"{Text_Map.INSTEAD_OF}'текст' написати (Telegram {TG_Emoji_Map.ID}) можна написати username {TG_Emoji_Map.CYCLONE} (Ім'я користувача)",
            },
            "WIKI": f"{Text_Map.INSTEAD_OF}'текст' написати шуканий текст",
            "SEND": f"{Text_Map.INSTEAD_OF}'текст' написати текст повідомлення",
            "QR": """фото або текст</code>
замість фото надіслати фото з QR-кодом для зчитування, можна відповісти командою на повідомлення з QR-кодом 

замість 'текст' написати текст для створення QR, можна відповісти командою на повідомлення з текстом для створення QR""",
            "TEXT_2_SPEECH": f"{Text_Map.INSTEAD_OF}'текст' написати текст для читання (англійською мовою)",
            "UPLOAD": "медіафайл або текст </code>\nможна відповісти командою на повідомлення",
            "VIRUSTOTAL": """файл або посилання</code>
замість файл надіслати файл для зчитування, можна відповісти командою на повідомлення з файлом

замість 'посилання' написати посилання, можна відповісти командою на повідомлення з посиланням (вибереться перше посилання в тексті)""",
            "URL_SHORTENER": """текст з посиланням</code>
можна відповісти командою на повідомлення з посиланням (вибереться перше посилання в тексті)""",
        },
        "PermissionError": "Не вистачає прав",
        "Only_private_chat": f"{TG_Emoji_Map.X} Ця функція працює тільки в особистому діалозі з <a href='https://t.me/{Text_Map.MY_USERNAME[1:]}'>ботом</a>",
    }
    ADD_INFO_COLUMN = {
        "student": [DB_Map.PHONE_NUMBER, DB_Map.USERNAME, DB_Map.MAIL_ADDRESS],
        "Teacher": [
            DB_Map.NAME,
            DB_Map.PHONE_NUMBER,
            DB_Map.ROLE,
            DB_Map.CLASSROOM,
            DB_Map.USERNAME,
            DB_Map.MAIL_ADDRESS,
        ],
    }
    SYMBOLS_HELP = {
        TG_Emoji_Map.BUST_IN_SILHOUETTE: Text_Map.WIKI_LINK.format("Ім%27я", "Ім'я"),
        TG_Emoji_Map.ID: Text_Map.WIKI_LINK.format(
            "Telegram",
            "Telegram ID, спеціальний індивідуальний ідентифікаційний номер, який автоматично присвоюється кожному користувачеві Telegram з метою можливості його ідентифікації в системі",
        ),
        DB_Map.ROLE: f"Роль, приклади: {Text_Map.WIKI_LINK.format('Студент', f'{TG_Emoji_Map.SCHOOL_SATCHEL} {DB_Map.STUDENT}')}, {Text_Map.WIKI_LINK.format('Учитель', f'{TG_Emoji_Map.MAN_TEACHER} {DB_Map.TEACHER}')}, {TG_Emoji_Map.BUSTS_IN_SILHOUETTE} {DB_Map.STAFF}, {TG_Emoji_Map.CROWN} {DB_Map.ADMIN}",
        TG_Emoji_Map.DOOR: Text_Map.WIKI_LINK.format(
            "Класна_кімната", "Класна кімната"
        ),
        TG_Emoji_Map.TELEPHONE_RECEIVER: Text_Map.WIKI_LINK.format(
            "Телефонний_номер", "Телефонний номер"
        ),
        TG_Emoji_Map.CYCLONE: "<a href='https://educalingo.com/uk/dic-en/username'>Ім'я користувача</a>, наприклад @borysfen_dp_bot",
        DB_Map.ADDER_ID: Text_Map.WIKI_LINK.format(
            "Telegram",
            "Telegram ID користувача, який додав вас (або іншого користувача) до бази",
        ),
        DB_Map.DATE: Text_Map.WIKI_LINK.format("Дата", "Дата"),
        TG_Emoji_Map.BLUE_CIRCLE: Text_Map.WIKI_LINK.format(
            "Посилання",
            "Посилання</a> на <a href='{Text_Map.WIKI_LINK}Обліковий_запис",
            "обліковий запис</a> <a href='{Text_Map.WIKI_LINK}Telegram",
            "Telegram",
        ),
        TG_Emoji_Map.PURPLE_CIRCLE: Text_Map.WIKI_LINK.format(
            "Посилання",
            "Посилання</a> на <a href='{Text_Map.WIKI_LINK}Обліковий_запис",
            "обліковий запис</a> <a href='{Text_Map.WIKI_LINK}Viber",
            "Viber",
        ),
        TG_Emoji_Map.MAILBOX_WITH_MAIL: Text_Map.WIKI_LINK.format(
            "Адреса_електронної_пошти", "Адреса електронної пошти"
        ),
        TG_Emoji_Map.X: Text_Map.WIKI_LINK.format("Помилка", "Помилка"),
        TG_Emoji_Map.WASTEBASKET: f"Видалити {Text_Map.WIKI_LINK.format('Повідомлення', 'повідомлення')}",
        Text_Map.HELP_TEXT: Text_Map.WIKI_LINK.format("Умовні_знаки", "Умовні знаки"),
        TG_Emoji_Map.ALARM_CLOCK: Text_Map.WIKI_LINK.format("Час", "Час"),
        TG_Emoji_Map.DROPLET: Text_Map.WIKI_LINK.format(
            "Вологість_повітря", "Вологість повітря"
        ),
        TG_Emoji_Map.KITE: Text_Map.WIKI_LINK.format(
            "Швидкість_вітру", "Швидкість вітру"
        ),
        TG_Emoji_Map.SUNRISE: Text_Map.WIKI_LINK.format("Світанок", "Світанок"),
        TG_Emoji_Map.SUNRISE_OVER_MOUNTAINS: Text_Map.WIKI_LINK.format(
            "Захід_Сонця", "Захід Сонця"
        ),
        TG_Emoji_Map.HIGH_BRIGHTNESS: Text_Map.WIKI_LINK.format("День", "День"),
        TG_Emoji_Map.EYE: "Кількість переглядів повідомлення",
        TG_Emoji_Map.COP: "Автор повідомлення",
        TG_Emoji_Map.PAGE_FACING_UP: Text_Map.WIKI_LINK.format("Опис", "Опис"),
        TG_Emoji_Map.BUSTS_IN_SILHOUETTE: "Кількість учасників групи/каналу",
        TG_Emoji_Map.BIRTHDAY: Text_Map.WIKI_LINK.format(
            "День_народження", "День народження"
        ),
        TG_Emoji_Map.HOUSE_WITH_GARDEN: Text_Map.WIKI_LINK.format(
            "Поштова_адреса", "Домашня адреса"
        ),
        TG_Emoji_Map.BRIEFCASE: Text_Map.WIKI_LINK.format("Професія", "Професія"),
        TG_Emoji_Map.HOURGLASS_FLOWING_SAND: Text_Map.WIKI_LINK.format(
            "Вік_(біологія)", "Вік"
        ),
        DB_Map.PERSONAL_DATA_AGREEMENT: f"Згода на обробку {Text_Map.WIKI_LINK.format('Персональні_дані', 'персональних даних')}",
        TG_Emoji_Map.PACKAGE: f"Розмір {Text_Map.WIKI_LINK.format('Файл', 'файлу')}",
        # "": Text_Map.WIKI_LINK.format("", ""),
    }
    FILES = {
        "WEATHER": "Additions/weather_data.json",
        "database": f"{Text_Map.CONFIG_DIR}/database.db",
    }
    CODE_TO_SMILE = {
        "Clear": TG_Emoji_Map.SUNNY,
        "Clouds": TG_Emoji_Map.CLOUD,
        "Rain": TG_Emoji_Map.UMBRELLA,
        "Drizzle": TG_Emoji_Map.UMBRELLA,
        "Thunderstorm": TG_Emoji_Map.ZAP,
        "Snow": TG_Emoji_Map.SNOWFLAKE,
        "Mist": TG_Emoji_Map.FOG,
    }
    LESSON_TIMES = {
        "1": (time(8, 30), time(9, 15)),
        "2": (time(9, 30), time(10, 15)),
        "3": (time(10, 35), time(11, 20)),
        "4": (time(11, 35), time(12, 20)),
        "5": (time(12, 35), time(13, 20)),
        "6": (time(13, 35), time(14, 20)),
        "7": (time(14, 40), time(15, 25)),
    }
    LAYOUT_EN_2_UA = {
        "q": "й",
        "w": "ц",
        "e": "у",
        "r": "к",
        "t": "е",
        "y": "н",
        "u": "г",
        "i": "ш",
        "o": "щ",
        "p": "з",
        "[": "х",
        "]": "ї",
        "a": "ф",
        "s": "і",
        "d": "в",
        "f": "а",
        "g": "п",
        "h": "р",
        "j": "о",
        "k": "л",
        "l": "д",
        "'": "є",
        '"': "є",
        "z": "я",
        "x": "ч",
        "c": "с",
        "v": "м",
        "b": "и",
        "n": "т",
        "m": "ь",
        ",": "б",
        ".": "ю",
        "/": ".",
        "\\": "ґ",
    }
    COLORS = {
        "BLACK": "\033[30m\033[1m",
        "RED": "\033[31m\033[1m",
        "GREEN": "\033[32m\033[1m",
        "YELLOW": "\033[33m\033[1m",
        "BLUE": "\033[34m\033[1m",
        "MAGENTA": "\033[35m\033[1m",
        "CYAN": "\033[36m\033[1m",
        "WHITE": "\033[37m\033[1m",
        "ORANGE": "\033[38;5;202m",
    }
    NUM_TO_EMOJI = {
        "0": TG_Emoji_Map.ZERO,
        "1": TG_Emoji_Map.ONE,
        "2": TG_Emoji_Map.TWO,
        "3": TG_Emoji_Map.THREE,
        "4": TG_Emoji_Map.FOUR,
        "5": TG_Emoji_Map.FIVE,
        "6": TG_Emoji_Map.SIX,
        "7": TG_Emoji_Map.SEVEN,
        "8": TG_Emoji_Map.EIGHT,
        "9": TG_Emoji_Map.NINE,
    }
    CLASS_BOOKS = {
        "10": {
            Subjects_Map.ENGLISH: [
                "Карпюк О. Д. 2018",
                "https://file.4book.org/images/shcoolbook_ua/10/10_am_kar_2018.pdf",
            ],
            Subjects_Map.GEOGRAPHY: [
                "Безуглий, Лисичарова 2018",
                "https://files.pidruchnyk.com.ua/uploads/book/10-klas-geografija-bezuglij-2018.pdf",
            ],
        },
        "11": {
            Subjects_Map.UKRAINIAN_LITERATURE: [
                "Авраменко О.",
                "https://files.pidruchnyk.com.ua/uploads/book/11-klas-ukrajinska-literatura-avramenko-2019.pdf",
            ],
            Subjects_Map.UKRAINIAN: [
                "Авраменко О.",
                "https://files.pidruchnyk.com.ua/uploads/book/11-klas-ukrajinska-mova-avramenko-2019.pdf",
            ],
            Subjects_Map.FOREIGN_LITERATURE: [
                "Паращич В.",
                "https://files.pidruchnyk.com.ua/uploads/book/11-klas-zarubizhna-literatura-paraschych-2019.pdf",
            ],
            Subjects_Map.ENGLISH: [
                "Буренко В.",
                "https://file.4book.org/images/shcoolbook_ua/11/11_am_b_2019.pdf",
            ],
            Subjects_Map.HISTORY_OF_UKRAINE: [
                "Даниленко В.",
                "https://files.pidruchnyk.com.ua/uploads/book/11-klas-istorija-ukrajini-danylenko-2019.pdf",
            ],
            Subjects_Map.WORLD_HISTORY: [
                "Щупак І.",
                "https://pidruchnyk.com.ua/uploads/book/11-klas-vsesvitnja-istorija-shhupak-2019.pdf",
            ],
            Subjects_Map.GEOMETRY: [
                "Бевз В.Г.",
                "https://files.pidruchnyk.com.ua/uploads/book/11-klas-matematika-bevz-2019.pdf",
            ],
            Subjects_Map.ALGEBRA: [
                "Бевз В.Г.",
                "https://files.pidruchnyk.com.ua/uploads/book/11-klas-matematika-bevz-2019.pdf",
            ],
            Subjects_Map.PHYSICS: [
                "Кірик Л.А.",
                "https://drive.google.com/file/d/1bhVBZl0X6cyucoB2nU7J9BERScRfQM2v/view?usp=sharing",
            ],
            Subjects_Map.CHEMISTRY: [
                "Савчин Н.",
                "https://pidruchnyk.com.ua/uploads/book/11-klas-khimija-savchin-2019.pdf",
            ],
            Subjects_Map.INFORMATICS: [
                "Бондаренко О.",
                "https://lib.imzo.gov.ua/wa-data/public/site/books2/pidruchnyky-10-klas-2018/18-Informatyka-10-klas/Informatika-riven-standartu-pidr-dlia-10-11-kl.-ZZSO-Bondarenko-Lastovetskii-Pilipchuk-Shestopalov.pdf",
            ],
            Subjects_Map.BIOLOGY: [
                "Остапченко Л.І.",
                "https://files.pidruchnyk.com.ua/uploads/book/11-klas-biologija-ostapchenko-2019.pdf",
            ],
            Subjects_Map.GEOGRAPHY: [
                "Безуглий В.",
                "https://pidruchnyk.com.ua/uploads/book/11-klas-geografija-bezuglyi-2019.pdf",
            ],
        },
        "5": {
            Subjects_Map.MATHEMATICS: [
                "Тарасенкова Н.",
                "https://files.pidruchnyk.com.ua/uploads/book/Matematyka_5klas_Tarasenkova.pdf",
            ],
            Subjects_Map.LEARNING_ABOUT_NATURE: [
                "Біда Д.",
                "https://pidruchnyk.com.ua/1718-piznaiemo-pryrodu-bida-5-klas.html",
            ],
        },
        "6": {
            Subjects_Map.UKRAINIAN_LITERATURE: [
                "Авраменко О.",
                "https://pidruchnyk.com.ua/uploads/book/Ukrliteratura_6klas_2014_Avramenko.pdf",
            ],
            Subjects_Map.UKRAINIAN: [
                "Заболотний О.",
                "https://pidruchnyk.com.ua/uploads/book/Ukrmova_6klas_Zabolotnyj.pdf",
            ],
            Subjects_Map.FOREIGN_LITERATURE: [
                "Ніколенко О.",
                "https://pidruchnyk.com.ua/uploads/book/Svitova_literatura_6klas_Nikolenko.pdf",
            ],
            Subjects_Map.ENGLISH: [
                "Несвіт А.",
                "https://pidruchnyk.com.ua/uploads/book/Anlijska_mova_6klas_Nesvit_2014.pdf",
            ],
            Subjects_Map.WORLD_HISTORY: [
                "Гісем О.",
                "https://drive.google.com/uc?&id=1dAPtuP8bzsBBlafA0BD38Y8JEVWuRFBg",
            ],
            Subjects_Map.HISTORY_OF_UKRAINE: [
                "Гісем О.",
                "https://drive.google.com/uc?&id=1dAPtuP8bzsBBlafA0BD38Y8JEVWuRFBg",
            ],
            Subjects_Map.MATHEMATICS: [
                "Тарасенкова Н.",
                "https://pidruchnyk.com.ua/uploads/book/Matematyka_6klas_Tarasenkova.pdf",
            ],
            Subjects_Map.INFORMATICS: [
                "Бондаренко О.",
                "https://drive.google.com/uc?&id=1vcPd2csJ8ONmbT36fe-C3xf_kRi2C122",
            ],
            Subjects_Map.TECHNOLOGY: [
                "Ходзицька І.",
                "https://pidruchnyk.com.ua/uploads/book/Trudove_6klas_Hodzycka.pdf",
            ],
        },
    }
    """
    # класс: {}
    # Subjects_Map.GEOGRAPHY: ["автор", "посилання"],
    """
    TIMETABLE_MAP = {
        "11": {
            DAYS_OF_WEEK_MAP["Monday"]: {
                "1": Subjects_Map.GEOMETRY,
                "2": Subjects_Map.GEOMETRY,
                "3": Subjects_Map.CHEMISTRY,
                "4": Subjects_Map.INFORMATICS,
                "5": Subjects_Map.WORLD_HISTORY,
                "6": Subjects_Map.BIOLOGY,
                "8": Subjects_Map.HISTORY_OF_UKRAINE,
            },
            DAYS_OF_WEEK_MAP["Tuesday"]: {
                "1": Subjects_Map.PHYSICAL_EDUCATION,
                "2": Subjects_Map.PHYSICS,
                "3": Subjects_Map.ENGLISH,
                "4": Subjects_Map.UKRAINIAN,
                "5": Subjects_Map.UKRAINIAN_LITERATURE,
                "6": Subjects_Map.FOREIGN_LITERATURE,
                "7": Subjects_Map.ENGLISH,
            },
            DAYS_OF_WEEK_MAP["Wednesday"]: {
                "1": Subjects_Map.ALGEBRA,
                "2": Subjects_Map.BIOLOGY,
                "3": Subjects_Map.GEOGRAPHY,
                "5": Subjects_Map.DEFENCE_OF_UKRAINE,
                "6": Subjects_Map.ENGLISH,
                "7": Subjects_Map.HISTORY_OF_UKRAINE,
            },
            DAYS_OF_WEEK_MAP["Thursday"]: {
                "1": Subjects_Map.UKRAINIAN,
                "2": Subjects_Map.UKRAINIAN_LITERATURE,
                "3": Subjects_Map.PHYSICAL_EDUCATION,
                "4": Subjects_Map.BIOLOGY,
                "5": Subjects_Map.CHEMISTRY,
                "6": Subjects_Map.PHYSICS,
                "7": Subjects_Map.UKRAINIAN,
            },
            DAYS_OF_WEEK_MAP["Friday"]: {
                "1": Subjects_Map.PHYSICS,
                "2": Subjects_Map.HISTORY_OF_UKRAINE,
                "3": Subjects_Map.BIOLOGY,
                "4": Subjects_Map.TECHNOLOGY,
                "5": Subjects_Map.PHYSICAL_EDUCATION,
                "6": Subjects_Map.CHEMISTRY,
                "7": Subjects_Map.INFORMATICS,
            },
        },
    }
    LESSON_LINKS = {
        "11": {
            Subjects_Map.ENGLISH: (
                [
                    "Norman Preston",
                    "https://us05web.zoom.us/j/",
                ],
                [
                    "Arnold Guthrie",
                    "https://us05web.zoom.us/j/",
                ],
            ),
            Subjects_Map.HISTORY_OF_UKRAINE: [
                "Brendon Pennington",
                "https://us05web.zoom.us/j/",
            ],
            Subjects_Map.WORLD_HISTORY: [
                "Brendon Pennington",
                "https://us05web.zoom.us/j/",
            ],
            Subjects_Map.PHYSICS: [
                "Terrence Fulton",
                "https://meet.google.com/random_link",
            ],
            Subjects_Map.CHEMISTRY: [
                "Arnita Lowe",
                "https://meet.google.com/random_link",
            ],
            Subjects_Map.BIOLOGY: [
                "Arnita Lowe",
                "https://meet.google.com/random_link",
            ],
            Subjects_Map.FOREIGN_LITERATURE: [
                "Julieann Nielsen",
                "https://us05web.zoom.us/j/",
            ],
            Subjects_Map.GEOGRAPHY: [
                "Victor Tran",
                "https://us05web.zoom.us/j/",
            ],
            Subjects_Map.ALGEBRA: [
                "Ted Puckett",
                "https://us05web.zoom.us/j/",
            ],
            Subjects_Map.GEOMETRY: [
                "Ted Puckett",
                "https://us05web.zoom.us/j/",
            ],
            Subjects_Map.INFORMATICS: [
                "Janay Gilliam",
                "https://meet.google.com/random_link",
            ],
            Subjects_Map.UKRAINIAN: [
                "Velvet Hays",
                "https://us05web.zoom.us/j/",
            ],
            Subjects_Map.UKRAINIAN_LITERATURE: [
                "Velvet Hays",
                "https://us05web.zoom.us/j/",
            ],
            Subjects_Map.DEFENCE_OF_UKRAINE: (
                [
                    "Roselia Vance",
                    "https://us05web.zoom.us/j/",
                ],
                [
                    "Ria Leonard",
                    "https://us05web.zoom.us/j/",
                ],
            ),
            Subjects_Map.TECHNOLOGY: [
                "Jolie Jacobs",
                "https://us05web.zoom.us/j/",
            ],
            Subjects_Map.PHYSICAL_EDUCATION: [
                "Julius Frost",
                "https://us05web.zoom.us/j/",
            ],
        },
    }
    ALERT_TYPE = {
        AlertType.ARTILLERY: f"{TG_Emoji_Map.BOW_AND_ARROW} Загроза артобстрілу",
        AlertType.URBAN_FIGHTS: f"{TG_Emoji_Map.GUN} Загроза вуличних боїв",
        AlertType.CHEMICAL: f"{TG_Emoji_Map.CHEMISTRY} Хімічна загроза",
        AlertType.NUCLEAR: f"{TG_Emoji_Map.RADIOACTIVE} Радіаційна загроза ",
    }
    GREETINGS = {
        range(5, 10): "Доброго ранку",  # From 5 am to 10 am
        range(10, 17): "Доброго дня",  # From 10 am to 5 pm
        range(17, 21): "Доброго вечора",  # From 5 pm to 9 pm
    }


class Buttons_Map(Enum2):
    START_MAIN = InlineKeyboardButton(text=Text_Map.MAIN, callback_data="start_main")
    DELETE = InlineKeyboardButton(
        text=Text_Map.DELETE, callback_data="delete_bot_message"
    )
    DELETE_FULL = InlineKeyboardButton(
        text=Text_Map.DELETE, callback_data="delete_full_message"
    )
    ADD_ROLE_STUDENT = InlineKeyboardButton(
        text=f"{TG_Emoji_Map.SCHOOL_SATCHEL} {DB_Map.STUDENT}",
        callback_data=f"add_role_{DB_Map.STUDENT}",
    )
    GET_NUMBER = InlineKeyboardButton(
        text=f"{TG_Emoji_Map.TELEPHONE_RECEIVER} Контакт", callback_data="get_number"
    )
    CONTACT_INFORMATION = InlineKeyboardButton(
        text=f"{TG_Emoji_Map.TELEPHONE} Контактна iнформацiя",
        callback_data="contact_information",
    )
    BACK_LESSONS = [
        InlineKeyboardButton(text=Text_Map.BACK, callback_data="lessons"),
        START_MAIN,
    ]
    ADD_ROLE_STAFF = InlineKeyboardButton(
        text=f"{TG_Emoji_Map.BUSTS_IN_SILHOUETTE} {DB_Map.STAFF}",
        callback_data=f"add_role_{DB_Map.STAFF}",
    )
    DATA_SEARCH_MAIN = [
        InlineKeyboardButton(text=Text_Map.MAIN, callback_data="data_search_main"),
        DELETE_FULL,
    ]
    STAFF_DB_S = InlineKeyboardButton(
        text=f"{TG_Emoji_Map.BUSTS_IN_SILHOUETTE} {DB_Map.STAFF}",
        callback_data=f"{DB_Map.STAFF}db_s{DB_Map.ROLE}",
    )
    TEACHER_AND_STUDENT_DB_S = [
        InlineKeyboardButton(
            text=f"{TG_Emoji_Map.MAN_TEACHER} {DB_Map.TEACHER}",
            callback_data=f"{DB_Map.TEACHER}db_s{DB_Map.ROLE}",
        ),
        InlineKeyboardButton(
            text=f"{TG_Emoji_Map.SCHOOL_SATCHEL} {DB_Map.STUDENT}",
            callback_data=f"{DB_Map.STUDENT}db_s{DB_Map.ROLE}",
        ),
    ]
    ADD_INFO_MAIN = [
        InlineKeyboardButton(text=Text_Map.MAIN, callback_data="add_info_main"),
        DELETE_FULL,
    ]
    SYMBOLS_HELP = [
        [
            InlineKeyboardButton(text=key, callback_data=f"symbols_help_{key}")
            for key in Dict_Map.SYMBOLS_HELP
        ][i : i + 4]
        for i in range(0, len(Dict_Map.SYMBOLS_HELP), 4)
    ]
    GET_TIMETABLE = InlineKeyboardButton(
        text=Text_Map.TIMETABLE, callback_data="get_timetable"
    )
    SCHOOL_DAY = [
        InlineKeyboardButton(text=Text_Map.CHILL, callback_data="school_day_false"),
        InlineKeyboardButton(
            text=f"{TG_Emoji_Map.BELL} Навчання", callback_data="school_day_true"
        ),
        InlineKeyboardButton(
            text=f"{TG_Emoji_Map.LEFTWARDS_ARROW_WITH_HOOK} Стандарт",
            callback_data="school_day_default",
        ),
    ]
    SEND_MAIN = [
        InlineKeyboardButton(
            text=Text_Map.MAIN, callback_data=f"send_column_{DB_Map.ROLE}"
        ),
        DELETE_FULL,
    ]
    COMMANDS_LIST = InlineKeyboardButton(
        text=Text_Map.COMMANDS_LIST, callback_data="commands_list"
    )
    SHARE_BOT = [
        InlineKeyboardButton(
            text=f"{TG_Emoji_Map.BUSTS_IN_SILHOUETTE} Додати до групи",
            url="https://t.me/borysfen_dp_bot?startgroup=start",
        ),
        InlineKeyboardButton(
            text=f"{TG_Emoji_Map.SPEECH_BALLOON} Поділитися ботом",
            switch_inline_query='🤖 Бот помічник Ліцею "Борисфен"',
        ),
    ]
    TEACHERS = InlineKeyboardButton(
        text=f"{TG_Emoji_Map.BELL} Вчителі", callback_data="lessons"
    )
    BACK_SEARCH_AGAIN = [
        InlineKeyboardButton(text=Text_Map.BACK, callback_data="search_again"),
        DELETE_FULL,
    ]
    ME = [
        [
            InlineKeyboardButton(
                text=Text_Map.HELP_TEXT,
                callback_data=f"{Text_Map.HELP_TEXT}me_again",
            ),
            InlineKeyboardButton(
                text=TG_Emoji_Map.ARROWS_COUNTERCLOCKWISE, callback_data="me_again"
            ),
        ],
        [DELETE_FULL],
    ]
    ADD_INFO_MAIN_HELP = [
        [
            InlineKeyboardButton(
                text=Text_Map.HELP_TEXT,
                callback_data=f"{Text_Map.HELP_TEXT}add_info_main",
            ),
            DELETE_FULL,
        ]
    ]


class Markup_Map(Enum2):
    MARKUP_MAIN_BUTTON = InlineKeyboardMarkup([[Buttons_Map.START_MAIN]])
    DELETE = InlineKeyboardMarkup([[Buttons_Map.DELETE]])
    DELETE_FULL = InlineKeyboardMarkup([[Buttons_Map.DELETE_FULL]])
    SEARCH_TEACHER_NUMBER = InlineKeyboardMarkup(
        [[Buttons_Map.GET_NUMBER, Buttons_Map.DELETE_FULL]]
    )
    START = InlineKeyboardMarkup(
        [
            Buttons_Map.SHARE_BOT,
            [Buttons_Map.CONTACT_INFORMATION, Buttons_Map.TEACHERS],
            [Buttons_Map.COMMANDS_LIST],
        ]
    )
    START_NOT_REGISTERED = InlineKeyboardMarkup([[Buttons_Map.CONTACT_INFORMATION]])
    START_WITH_CLASS_INFORMATION = InlineKeyboardMarkup(
        [
            Buttons_Map.SHARE_BOT,
            [
                Buttons_Map.CONTACT_INFORMATION,
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.LINK} Посилання",
                    callback_data="lesson_links_list",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=Text_Map.BOOKS,
                    callback_data="class_books_list",
                ),
                Buttons_Map.TEACHERS,
            ],
            [
                Buttons_Map.COMMANDS_LIST,
                InlineKeyboardButton(
                    text=Text_Map.TIMETABLE,
                    callback_data="get_timetable_week",
                ),
            ],
        ]
    )
    CONTACT_INFORMATION = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.MAP} Мапа",
                    url="https://www.openstreetmap.org/#map=18/48.50056/35.04665&layers=N",
                ),
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.GLOBE_WITH_MERIDIANS} Сайт",
                    url="https://www.borysfen.dp.ua/",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.BLUE_CIRCLE} Facebook",
                    url="https://www.facebook.com/Ліцей-Борисфен-107234057311249",
                ),
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.RED_CIRCLE} YouTube",
                    url="https://www.youtube.com/@user-ut5di4ww7f/videos",
                ),
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.CAMERA_WITH_FLASH} Instagram",
                    url="https://www.instagram.com/lyceum_borisfen4",
                ),
            ],
            [Buttons_Map.START_MAIN],
        ]
    )
    LESSONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=key, callback_data=key)
                for key in Dict_Map.SUBJECTS
            ][i : i + 2]
            for i in range(0, len(Dict_Map.SUBJECTS), 2)
        ]
        + [[Buttons_Map.START_MAIN]]
    )
    BACK_SEARCH_AGAIN = InlineKeyboardMarkup([Buttons_Map.BACK_SEARCH_AGAIN])
    BACK_SEARCH_AGAIN_NUMBER = InlineKeyboardMarkup(
        [[Buttons_Map.GET_NUMBER], Buttons_Map.BACK_SEARCH_AGAIN]
    )
    BACK_LESSONS = InlineKeyboardMarkup([Buttons_Map.BACK_LESSONS])
    BACK_LESSONS_NUMBER = InlineKeyboardMarkup(
        [[Buttons_Map.GET_NUMBER], Buttons_Map.BACK_LESSONS]
    )
    ADD_ROLE_ADMIN = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.CROWN} {DB_Map.ADMIN}",
                    callback_data=f"add_role_{DB_Map.ADMIN}",
                ),
                Buttons_Map.ADD_ROLE_STAFF,
            ],
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.MAN_TEACHER} {DB_Map.TEACHER}",
                    callback_data=f"add_role_{DB_Map.TEACHER}",
                ),
                Buttons_Map.ADD_ROLE_STUDENT,
            ],
            Buttons_Map.ADD_INFO_MAIN,
        ]
    )
    ADD_ROLE_STAFF = InlineKeyboardMarkup(
        [
            [Buttons_Map.ADD_ROLE_STAFF],
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.MAN_TEACHER} {DB_Map.TEACHER}",
                    callback_data=f"add_role_{DB_Map.TEACHER}",
                ),
                Buttons_Map.ADD_ROLE_STUDENT,
            ],
            Buttons_Map.ADD_INFO_MAIN,
        ]
    )
    SELECT_COLUMN = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=column, callback_data=f"search_column_{column}"
                )
                for column in DB_Map.USER_COLUMNS
            ][i : i + 5]
            for i in range(0, len(DB_Map.USER_COLUMNS), 5)
        ]
        + [
            [
                InlineKeyboardButton(
                    text=Text_Map.HELP_TEXT,
                    callback_data=f"{Text_Map.HELP_TEXT}data_search_main",
                ),
                Buttons_Map.DELETE_FULL,
            ]
        ]
    )
    SELECT_COLUMN_ROLE_ADMIN = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.CROWN} {DB_Map.ADMIN}",
                    callback_data=f"{DB_Map.ADMIN}db_s{DB_Map.ROLE}",
                ),
                Buttons_Map.STAFF_DB_S,
            ],
            Buttons_Map.TEACHER_AND_STUDENT_DB_S,
            Buttons_Map.DATA_SEARCH_MAIN,
        ]
    )
    SELECT_COLUMN_ROLE_NOT_ADMIN = InlineKeyboardMarkup(
        [
            [Buttons_Map.STAFF_DB_S],
            Buttons_Map.TEACHER_AND_STUDENT_DB_S,
            Buttons_Map.DATA_SEARCH_MAIN,
        ]
    )
    ADD_INFO_COLUMN_STUDENT = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=column, callback_data=f"edit_column_{column}")
                for column in Dict_Map.ADD_INFO_COLUMN["student"]
            ][i : i + 5]
            for i in range(0, len(Dict_Map.ADD_INFO_COLUMN["student"]), 5)
        ]
        + Buttons_Map.ADD_INFO_MAIN_HELP
    )
    ADD_INFO_COLUMN_TEACHER = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=column, callback_data=f"edit_column_{column}")
                for column in Dict_Map.ADD_INFO_COLUMN["Teacher"]
            ][i : i + 5]
            for i in range(0, len(Dict_Map.ADD_INFO_COLUMN["Teacher"]), 5)
        ]
        + Buttons_Map.ADD_INFO_MAIN_HELP
    )
    REQUEST_CONTACT = (
        ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text=f"Надіслати контакт {TG_Emoji_Map.TELEPHONE_RECEIVER}",
                        request_contact=True,
                    )
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
            placeholder=Text_Map.CLICK_ON_THE_BUTTON,
        ),
    )
    CLASSROOMS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=key, callback_data=f"add_classroom_{key}")
                for key in Any_Map.CLASSROOMS
            ][i : i + 4]
            for i in range(0, len(Any_Map.CLASSROOMS), 4)
        ]
        + [Buttons_Map.ADD_INFO_MAIN]
    )
    ME = InlineKeyboardMarkup(Buttons_Map.ME)
    ME_NUMBER = InlineKeyboardMarkup([[Buttons_Map.GET_NUMBER]] + Buttons_Map.ME)
    SELECT_COLUMN_CLASSROOM = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=key, callback_data=f"{key}db_s{DB_Map.CLASSROOM}"
                )
                for key in Any_Map.CLASSROOMS
            ][i : i + 4]
            for i in range(0, len(Any_Map.CLASSROOMS), 4)
        ]
        + [Buttons_Map.DATA_SEARCH_MAIN]
    )
    NOW_IS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=TG_Emoji_Map.ARROWS_COUNTERCLOCKWISE,
                    callback_data="now_is_again",
                )
            ],
            [
                InlineKeyboardButton(
                    text=Text_Map.HELP_TEXT,
                    callback_data=f"{Text_Map.HELP_TEXT}now_is_again",
                ),
                Buttons_Map.DELETE_FULL,
            ],
        ]
    )
    SEND_COLUMN_ROLE = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.BUSTS_IN_SILHOUETTE} {DB_Map.STAFF}",
                    callback_data=f"{DB_Map.STAFF}se_s{DB_Map.ROLE}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.MAN_TEACHER} {DB_Map.TEACHER}",
                    callback_data=f"{DB_Map.TEACHER}se_s{DB_Map.ROLE}",
                ),
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.SCHOOL_SATCHEL} {DB_Map.STUDENT}",
                    callback_data=f"send_column_{DB_Map.CLASSROOM}",
                ),
            ],
            [Buttons_Map.DELETE_FULL],
        ]
    )
    SEND_COLUMN_CLASSROOM = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=key, callback_data=f"{key}se_s{DB_Map.CLASSROOM}"
                )
                for key in Any_Map.CLASSROOMS
            ][i : i + 4]
            for i in range(0, len(Any_Map.CLASSROOMS), 4)
        ]
        + [Buttons_Map.SEND_MAIN]
    )
    WEATHER = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.MAP} {Text_Map.MY_CITY}",
                    url=f"https://www.openstreetmap.org/search?query={quote(Text_Map.MY_CITY)}",
                ),
                InlineKeyboardButton(
                    text=TG_Emoji_Map.ARROWS_COUNTERCLOCKWISE,
                    callback_data="weather_again",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=Text_Map.HELP_TEXT,
                    callback_data=f"{Text_Map.HELP_TEXT}weather_again",
                ),
                Buttons_Map.DELETE_FULL,
            ],
        ]
    )
    GET_MESSAGE = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.SPEECH_BALLOON} Отримати",
                    callback_data="get_message_get",
                ),
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.X} Видалити", callback_data="get_message_del"
                ),
            ],
            [Buttons_Map.DELETE_FULL],
        ]
    )
    C = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=str(key), callback_data=f"MV5yNR9N0BKvheO{key}"
                )
                for key in range(2, 12)
            ][i : i + 5]
            for i in range(0, 10, 5)
        ]
        + [[Buttons_Map.DELETE_FULL]]
    )
    MAZE = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    TG_Emoji_Map.ARROW_LEFT, callback_data="maze_left"
                ),
                InlineKeyboardButton(TG_Emoji_Map.ARROW_UP, callback_data="maze_up"),
                InlineKeyboardButton(
                    TG_Emoji_Map.ARROW_DOWN, callback_data="maze_down"
                ),
                InlineKeyboardButton(
                    TG_Emoji_Map.ARROW_RIGHT, callback_data="maze_right"
                ),
            ],
            [InlineKeyboardButton(text=Text_Map.DELETE, callback_data="maze_delete")],
        ]
    )
    PASSWORD_GENERATOR = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=TG_Emoji_Map.ARROWS_COUNTERCLOCKWISE,
                    callback_data="password_generator",
                )
            ],
            [
                InlineKeyboardButton(
                    text=Text_Map.HELP_TEXT,
                    callback_data=f"{Text_Map.HELP_TEXT}password_generator",
                ),
                Buttons_Map.DELETE_FULL,
            ],
        ]
    )
    ALERT_LOOP = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.MAP} Мапа тривог",
                    url="https://map.ukrainealarm.com/",
                ),
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.ZAP} Пункти незламності",
                    url="https://www.google.com/maps/d/embed?mid=1_FIGiCmtPVm6tHMhEHxIh3FgmvuSC6k&ehbc=2E312F",
                ),
            ],
            [Buttons_Map.DELETE_FULL],
        ]
    )
    PERSONAL_DATA_AGREEMENT = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=Text_Map.YES, callback_data="Personal_Data_Agree"
                ),
                InlineKeyboardButton(
                    text=f"{TG_Emoji_Map.PAGE_WITH_CURL} Згода",
                    callback_data="Personal_Data_Agreement",
                ),
            ]
        ]
    )
    ALERT_ON = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{TG_Emoji_Map.BELL} Вкл.", callback_data="alert_on"
                ),
                Buttons_Map.DELETE_FULL,
            ]
        ]
    )
    ALERT_OFF = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{TG_Emoji_Map.NO_BELL} Викл.", callback_data="alert_off"
                ),
                Buttons_Map.DELETE_FULL,
            ]
        ]
    )
