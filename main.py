import pygame
import math
import random
import json
import os
from chest_3d import draw_chest_animation_3d
from settings_screen import draw_settings, SETTINGS_TAB
from settings_state import (audio_toggles, audio_volumes, privacy_toggles,
                            quality_toggles, quality_selected,
                             load_settings, save_settings)
from settings_state import quality_toggles
from settings_state import kills_stats
from settings_screen import _init_cars, _init_matrix
from client import draw_auth_screen, draw_login_screen, draw_registration_screen
import requests
from rare_screen import draw_rare_screen
from epic_screen import draw_epic_screen
from legendary_screen import draw_legendary_screen
from gold_screen import draw_gold_screen
from owned_screen import draw_owned_screen








os.environ['SDL_VIDEO_HIGHDPI_DISABLED'] = '1'
pygame.init()


DATA_FILE = "data.json"

SHOP_TAB = ["Rare"]

SHOP_SCROLL = 0
RARE_SCROLL = 0
EPIC_SCROLL = 0
LEGENDARY_SCROLL = 0
GOLD_SCROLL = 0
OWNED_SCROLL = 0
SCROLLBAR_DRAGGING = False

RARITY_XP = {
    "none": 10,
    "common": 15,
    "rare": 30,
    "epic": 60,
    "legendary": 120,
    "gold": 200,
}

rarity_colors = {
    "common": (150,150,150),
    "rare": (50,150,255),
    "epic": (180,70,255),
    "legendary": (255,200,0),
    "gold": (255, 215, 0)
}

TABS = ["Rare", "Epic", "Legendary", "Official", "Owned", "Custom", "Gems"]

TAB_FILTER = {
    "Rare": ["rare"],
    "Epic": ["epic"],
    "Legendary": ["legendary"],
    "Official": ["none", "common", "rare", "epic", "legendary"],
    "Owned": None,
}

default_data = {
    "coins": 1000,
    "dna": 100,
    "owned_skins": ["default"],
    "selected_skin": "default",
    "custom_player":{
        "color": [0, 255, 120],
        "eye_color": [255, 255, 255],
        "border_color": [0, 0, 0],
    },
}









def load_data():
    if not os.path.exists(DATA_FILE):
        data = default_data.copy()
        save_data(data)
        return data
    with open(DATA_FILE, "r") as f:
        loaded = json.load(f)
    data = default_data.copy()
    data.update(loaded)
    data["custom_player"] = {
        **default_data["custom_player"],
        **loaded.get("custom_player", {})
    }
    return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


data = load_data()
load_settings(data)
if "custom_player" not in data:
    data["custom_player"] = {
        "color": [0, 255, 120],
        "eye_color": [255, 255, 255],
        "border_color": [0, 0, 0],
    }
    save_data(data)

coins = data.get("coins", 1000)
owned_skins = data.get("owned_skins", ["default"])
player_skin = data.get("selected_skin", "default")
gems = data.get("gems", 0)

from pygame.constants import K_UP
pygame.mixer.init()


try:
    pygame.mixer.music.load("music2.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)


except:
    print("Музику не знайдено")
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
print(WIDTH, HEIGHT)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
clock = pygame.time.Clock()

win_img = pygame.image.load("lose.jpg")
win_img = pygame.transform.scale(win_img, (WIDTH, HEIGHT))
lose_img = pygame.image.load("lose.jpg")
lose_img = pygame.transform.scale(lose_img, (WIDTH, HEIGHT))

start_time = 0
GAME_DURATION = 60
TARGET_MASS = 100

VISION_R = 300
radar_surf = pygame.Surface((VISION_R * 2, VISION_R * 2), pygame.SRCALPHA)
pygame.draw.circle(radar_surf, (0, 255, 0, 20), (VISION_R, VISION_R), VISION_R)
pygame.draw.circle(radar_surf, (0, 255, 0, 60), (VISION_R, VISION_R), VISION_R, 2)

petal_cache = {}
for angle in range(0, 360, 10):
    surf = pygame.Surface((18, 18), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (255, 182, 193, 200), (0, 0, 18, 9))
    petal_cache[angle] = pygame.transform.rotate(surf, angle)

xp = 0
level = 1
notification_text = ""
notification_timer = 0

case_animation = {
    "active": False,
    "phase": 0,
    "timer": 0,
    "result_skin": None,
    "angle": 0,
}

chest_anim = {
    "active": False,
    "phase": 0,
    "timer": 0,
    "angle": 0,
    "scale": 1.0,
    "result_skin": None,
    "is_duplicate": False,
    "particles": [],
    "lid_offset": 0,
}

pause_menu_open = False

GEM_CASES = [
    {
        "name": "Spring Case",
        "gem_price": 10,
        "color": (255, 150, 200),
        "color2": (255, 100, 150),
        "icon": "S",
        "description": "Rare+",
    },
    {
        "name": "Blossom Case",
        "gem_price": 25,
        "color": (150, 100, 255),
        "color2": (100, 50, 220),
        "icon": "B",
        "description": "Epic+"
    },
    {
        "name": "Gold Case",
        "gem_price": 50,
        "color": (255, 200, 0),
        "color2": (200, 140, 0),
        "icon": "G",
        "description": "Legendary+",
    },
    {
        "name": "Diamond Case",
        "gem_price": 100,
        "color": (0, 220, 255),
        "color2": (0, 150, 220),
        "icon": "D",
        "description": "Gold Only",
    },
]

skins = {
    "default": {"img": "skin1.png", "price": 0, "rarity": "none"},
    "spider": {"img": "skin2.png", "price": 200, "rarity": "rare"},
    "turtle": {"img": "skin3.png", "price": 300, "rarity": "rare"},
    "fox": {"img": "skin4.png", "price": 400, "rarity": "rare"},
    "lion": {"img": "skin5.png", "price": 500, "rarity": "rare"},
    "green": {"img": "skin6.png", "price": 800, "rarity": "rare"},
    "man": {"img": "skin7.png", "price": 1400, "rarity": "rare"},
    "sth": {"img": "skin8.png", "price": 2400, "rarity": "rare"},
    "dino": {"img": "skin9.png", "price": 3400, "rarity": "rare"},
    "wolf": {"img": "skin10.png", "price": 47400, "rarity": "rare"},
    "sth51": {"img": "skin61.png", "price": 10000, "rarity": "rare"},
    "sth52": {"img": "skin62.png", "price": 11000, "rarity": "rare"},
    "sth53": {"img": "skin63.png", "price": 12000, "rarity": "rare"},
    "sth54": {"img": "skin64.png", "price": 13000, "rarity": "rare"},
    "sth55": {"img": "skin65.png", "price": 13450, "rarity": "rare"},
    "sth56": {"img": "skin66.png", "price": 13650, "rarity": "rare"},
    "sth57": {"img": "skin67.png", "price": 15550, "rarity": "rare"},
    "sth58": {"img": "skin68.png", "price": 16700, "rarity": "rare"},
    "sth59": {"img": "skin69.png", "price": 18500, "rarity": "rare"},
    "sth60": {"img": "skin70.png", "price": 34000, "rarity": "rare"},
    "sth61": {"img": "skin71.png", "price": 35550, "rarity": "rare"},
    "sth62": {"img": "skin72.png", "price": 36790, "rarity": "rare"},
    "sth63": {"img": "skin73.png", "price": 37790, "rarity": "rare"},
    "sth64": {"img": "skin74.png", "price": 37850, "rarity": "rare"},
    "sth65": {"img": "skin75.png", "price": 37920, "rarity": "rare"},

    #########################
    "sth2": {"img": "skin12.png", "price": 88400, "rarity": "epic"},
    "sth3": {"img": "skin13.png", "price": 99400, "rarity": "epic"},
    "sth4": {"img": "skin14.png", "price": 210400, "rarity": "epic"},
    "sth5": {"img": "skin15.png", "price": 311400, "rarity": "epic"},
    "sth6": {"img": "skin16.png", "price": 312400, "rarity": "epic"},
    "sth7": {"img": "skin17.png", "price": 313400, "rarity": "epic"},
    "sth8": {"img": "skin18.png", "price": 314400, "rarity": "epic"},
    "sth9": {"img": "skin19.png", "price": 315400, "rarity": "epic"},
    "sth10": {"img": "skin20.png", "price": 316400, "rarity": "epic"},
    "sth11": {"img": "skin21.png", "price": 416400, "rarity": "epic"},
    "sth12": {"img": "skin22.png", "price": 416400, "rarity": "epic"},
    "sth13": {"img": "skin23.png", "price": 416400, "rarity": "epic"},
    "sth14": {"img": "skin24.png", "price": 416400, "rarity": "epic"},
    "sth15": {"img": "skin25.png", "price": 416400, "rarity": "epic"},
    "sth16": {"img": "skin26.png", "price": 416400, "rarity": "epic"},
    "sth17": {"img": "skin27.png", "price": 416400, "rarity": "epic"},
    #############################

    "sth18": {"img": "skin28.png", "price": 516400, "rarity": "legendary"},
    "sth19": {"img": "skin29.png", "price": 516400, "rarity": "legendary"},
    "sth20": {"img": "skin30.png", "price": 516400, "rarity": "legendary"},
    "sth21": {"img": "skin31.png", "price": 516400, "rarity": "legendary"},
    "sth22": {"img": "skin32.png", "price": 516400, "rarity": "legendary"},
    "sth23": {"img": "skin33.png", "price": 516400, "rarity": "legendary"},
    "sth24": {"img": "skin34.png", "price": 516400, "rarity": "legendary"},
    "sth25": {"img": "skin35.png", "price": 516400, "rarity": "legendary"},
    "sth26": {"img": "skin36.png", "price": 616400, "rarity": "legendary"},
    "sth27": {"img": "skin37.png", "price": 916400, "rarity": "legendary"},
    "sth28": {"img": "skin38.png", "price": 1016400, "rarity": "legendary"},
    "sth29": {"img": "skin39.png", "price": 2164000, "rarity": "legendary"},
    "sth30": {"img": "skin40.png", "price": 3516400, "rarity": "legendary"},
    "custom": {"img": "skin1.png", "price": 5000000 , "rarity": "none"},
    "sth31": {"img": "skin41.png", "price": 6500000, "gem_price": 0, "rarity": "legendary"},
    "sth32": {"img": "skin42.png", "price": 712300, "gem_price": 0, "rarity": "legendary"},
    "sth33": {"img": "skin43.png", "price": 9814000, "gem_price": 0, "rarity": "legendary"},
    "sth34": {"img": "skin44.png", "price": 9900000, "gem_price": 0, "rarity": "legendary"},
    "sth35": {"img": "skin45.png", "price": 10000000, "gem_price": 0, "rarity": "legendary"},
    "sth36": {"img": "skin46.png", "price": 10500000, "gem_price": 0, "rarity": "legendary"},
    "sth37": {"img": "skin47.png", "price": 11800000, "gem_price": 0, "rarity": "legendary"},
    "sth38": {"img": "skin48.png", "price": 14500000, "gem_price": 0, "rarity": "legendary"},
    "sth39": {"img": "skin49.png", "price": 18799900, "gem_price": 0, "rarity": "legendary"},
    "sth40": {"img": "skin50.png", "price": 20000000, "gem_price": 0, "rarity": "legendary"},
    "sth41": {"img": "skin51.png", "price": 21000000, "gem_price": 0, "rarity": "legendary"},
    "sth42": {"img": "skin52.png", "price": 22000000, "gem_price": 0, "rarity": "legendary"},
    "sth44": {"img": "skin54.png", "price": 22500000, "gem_price": 0, "rarity": "legendary"},
    "sth45": {"img": "skin55.png", "price": 23000000, "gem_price": 0, "rarity": "legendary"},
    "sth46": {"img": "skin56.png", "price": 23899990, "gem_price": 0, "rarity": "legendary"},
    "sth47": {"img": "skin57.png", "price": 25000000, "gem_price": 0, "rarity": "legendary"},
    "sth48": {"img": "skin58.png", "price": 31000000, "gem_price": 0, "rarity": "legendary"},
    "sth49": {"img": "skin59.png", "price": 48799990, "gem_price": 0, "rarity": "legendary"},
    "sth50": {"img": "skin60.png", "price": 95000000, "gem_price": 0, "rarity": "legendary"},





    "R": {"img": "goldskin1.png", "price": 0, "gem_price": 435, "rarity": "gold"},
    "Ri": {"img": "goldskin2.png", "price": 0, "gem_price": 620, "rarity": "gold"},
    "Bad boy": {"img": "goldskin3.png", "price": 0, "gem_price": 699, "rarity": "gold"},
    "Gangster": {"img": "goldskin4.png", "price": 0, "gem_price": 650, "rarity": "gold"},
    "Alien": {"img": "goldskin5.png", "price": 0, "gem_price": 700, "rarity": "gold"},
    "Painter": {"img": "goldskin6.png", "price": 0, "gem_price": 799, "rarity": "gold"},
    "Robotics alien": {"img": "goldskin7.png", "price": 0, "gem_price": 829, "rarity": "gold"},
    "Faster": {"img": "goldskin8.png", "price": 0, "gem_price": 870, "rarity": "gold"},
    "Princess Gere": {"img": "goldskin9.png", "price": 0, "gem_price": 925, "rarity": "gold"},
    "Prince Alvard": {"img": "goldskin10.png", "price": 0, "gem_price": 1025, "rarity": "gold"},
    "Crazyy ball": {"img": "goldskin11.png", "price": 0, "gem_price": 1070, "rarity": "gold"},
    "Elegant killer": {"img": "goldskin12.png", "price": 0, "gem_price": 1199, "rarity": "gold"},
    "Queen Salamandra": {"img": "goldskin13.png", "price": 0, "gem_price": 1250, "rarity": "gold"},
    "King Arthur": {"img": "goldskin14.png", "price": 0, "gem_price": 1350, "rarity": "gold"},
    "Baby": {"img": "goldskin15.png", "price": 0, "gem_price": 1500, "rarity": "gold"},
    "Detective Daron": {"img": "goldskin16.png", "price": 0, "gem_price": 1525, "rarity": "gold"},
    "Kronlerg": {"img": "goldskin17.png", "price": 0, "gem_price": 1930, "rarity": "gold"},
    "Lamada": {"img": "goldskin18.png", "price": 0, "gem_price": 2599, "rarity": "gold"},




}



    ###########################



loaded_skins = {}
show_drop_rates = [False]

for name, data in skins.items():
    img = pygame.image.load(data["img"]).convert_alpha()
    loaded_skins[name] = img

loot_table = [
    ("rare", 65),
    ("epic", 30),
    ("legendary", 10)
]



_init_cars(WIDTH, HEIGHT)
_init_matrix(WIDTH, HEIGHT)



############### Authentification buttons

log_btn = pygame.image.load("log_btn.png").convert_alpha()
log_btn = pygame.transform.scale(log_btn, (600, 300))


reg_btn = pygame.image.load("reg_btn.png").convert_alpha()
reg_btn = pygame.transform.scale(reg_btn, (600, 330))


ramka1 = pygame.image.load("ramka1.png").convert_alpha()
ramka1 = pygame.transform.scale(ramka1, (400, 200))


login_btn = pygame.image.load("log_btn.png").convert_alpha()
login_btn = pygame.transform.scale(login_btn, (400, 200))

##############################################
#BACKGROUNDS
image = pygame.image.load("background_auth.png")
image = pygame.transform.scale(image, (WIDTH, HEIGHT))


login_bg = pygame.image.load("background_btn.png")
login_bg = pygame.transform.scale(login_bg, (WIDTH, HEIGHT))



reg_bg = pygame.image.load("background_btn.png")
reg_bg = pygame.transform.scale(reg_bg, (WIDTH, HEIGHT))


background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))



background_shop = pygame.image.load("background_shop.jpeg")
background_shop = pygame.transform.scale(background_shop, (WIDTH, HEIGHT))










###############################################################################
####BUTTONS FOR MENU
Classic_btn = pygame.image.load("Classic_btn.png")
Classic_btn = pygame.transform.scale(Classic_btn, (400, 200))


Rush_btn = pygame.image.load("Rush_btn.png")
Rush_btn = pygame.transform.scale(Rush_btn, (400, 200))



Play_btn = pygame.image.load("Play_btn.png")
Play_btn = pygame.transform.scale(Play_btn, (400, 200))


Settings_btn = pygame.image.load("Settings_btn.png")
Settings_btn = pygame.transform.scale(Settings_btn, (400, 200))




Shop_btn = pygame.image.load("Shop_btn.png")
Shop_btn = pygame.transform.scale(Shop_btn, (400, 200))

###############################################################################
######### Buttons for shop
rare_btn = pygame.image.load("rare_btn.png")
rare_btn = pygame.transform.scale(rare_btn, (400, 200))


epic_btn = pygame.image.load("epic_btn.png")
epic_btn = pygame.transform.scale(epic_btn, (400, 200))



legendary_btn = pygame.image.load("legendary_btn.png")
legendary_btn = pygame.transform.scale(legendary_btn, (400, 200))



gold_btn = pygame.image.load("gold_btn.png")
gold_btn = pygame.transform.scale(gold_btn, (400, 200))



owned_btn = pygame.image.load("owned_btn.png")
owned_btn = pygame.transform.scale(owned_btn, (400, 200))


ramka2 = pygame.image.load("ramka2.png")
ramka2 = pygame.transform.scale(ramka2, (700, 200))


ramka3 = pygame.image.load("ramka3.png")
ramka3 = pygame.transform.scale(ramka3, (350, 200))


ramka4 = pygame.image.load("ramka4.png")
ramka4 = pygame.transform.scale(ramka4, (300, 200))

# Cases ############################################
rare_case = pygame.image.load("rare_case.png")
rare_case = pygame.transform.scale(rare_case, (400, 300))


epic_case = pygame.image.load("epic_case.png")
epic_case = pygame.transform.scale(epic_case, (400, 300))


legendary_case = pygame.image.load("legendary_case.png")
legendary_case = pygame.transform.scale(legendary_case, (400, 300))


gold_case = pygame.image.load("gold_case.png")
gold_case = pygame.transform.scale(gold_case, (400, 300))


# Boosts ########################################################


# rare
rare_boost1 = pygame.image.load("rare_boost1.png")
rare_boost1 = pygame.transform.scale(rare_boost1, (400, 300))


rare_boost2 = pygame.image.load("rare_boost2.png")
rare_boost2 = pygame.transform.scale(rare_boost2, (400, 300))


rare_boost3 = pygame.image.load("rare_boost3.png")
rare_boost3 = pygame.transform.scale(rare_boost3, (400, 300))




# epic
epic_boost1 = pygame.image.load("epic_boost1.png")
epic_boost1 = pygame.transform.scale(epic_boost1, (400, 300))

epic_boost2 = pygame.image.load("epic_boost2.png")
epic_boost2 = pygame.transform.scale(epic_boost2, (400, 300))


epic_boost3 = pygame.image.load("epic_boost3.png")
epic_boost3 = pygame.transform.scale(epic_boost3, (400, 300))


# legendary

legendary_boost1 = pygame.image.load("legendary_boost1.png")
legendary_boost1 = pygame.transform.scale(legendary_boost1, (400, 300))



legendary_boost2 = pygame.image.load("legendary_boost2.png")
legendary_boost2 = pygame.transform.scale(legendary_boost2, (400, 300))


legendary_boost3 = pygame.image.load("legendary_boost3.png")
legendary_boost3 = pygame.transform.scale(legendary_boost3, (400, 300))




# gold

gold_boost1 = pygame.image.load("gold_boost1.png")
gold_boost1 = pygame.transform.scale(gold_boost1, (400, 300))


gold_boost2 = pygame.image.load("gold_boost2.png")
gold_boost2 = pygame.transform.scale(gold_boost2, (400, 300))




gold_boost3 = pygame.image.load("gold_boost3.png")
gold_boost3 = pygame.transform.scale(gold_boost3, (400, 300))




######## Sculptures ####################
sculpture1 = pygame.image.load("sculpture1.png")
sculpture1 = pygame.transform.scale(sculpture1, (800, 400))


sculpture2 = pygame.image.load("sculpture2.png")
sculpture2 = pygame.transform.scale(sculpture2, (800, 400))




sculpture3 = pygame.image.load("sculpture3.png")
sculpture3 = pygame.transform.scale(sculpture3, (400, 500))


sculpture4 = pygame.image.load("sculpture4.png")
sculpture4 = pygame.transform.scale(sculpture4, (500, 600))










######################################################################
####### GENERAL BUTTONS those l use many times

backs_btn = pygame.image.load("backs_btn.png")
backs_btn = pygame.transform.scale(backs_btn, (400, 200))






################################################################################
################ Button for rare_screen











######################################################
def open_case():
    roll = random.randint(1, 100)
    total = 0
    for rarity, chance in loot_table:
        total += chance
        if roll <= total:
            possible = [s for s in skins if skins[s].get("rarity") == rarity]
            if not possible:
                possible = [s for s in skins if s != "default"]
            return random.choice(possible)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mass = 20
        self.radius = int(self.mass ** 0.5 * 4)
        self.base_speed = 5
        self.speed = self.base_speed
        self.name = "Player"
        self.skin = "default"
        custom = data.get("custom_player", default_data["custom_player"])
        self.custom_color = custom.get("color", [0, 255, 120])
        self.eye_color = custom.get("eye_color", [255, 255, 255])
        self.border_color = custom.get("border_color", [0, 0, 0])

    def movement(self, keys):
        self.speed = self.base_speed / (self.radius * 0.1 + 1)
        self.speed = max(self.speed, 1.5)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_mouse_x = mouse_x + camera.x
        world_mouse_y = mouse_y + camera.y
        dx = world_mouse_x - self.x
        dy = world_mouse_y - self.y
        dist = math.hypot(dx, dy)
        if keys[pygame.K_UP]: dy -= dist * 0.3
        if keys[pygame.K_DOWN]: dy += dist * 0.3
        if keys[pygame.K_LEFT]: dx -= dist * 0.3
        if keys[pygame.K_RIGHT]: dx += dist * 0.3
        dist = math.hypot(dx, dy)
        if dist > 5:
            dx /= dist
            dy /= dist
            self.x += dx * self.speed
            self.y += dy * self.speed
        self.x = max(self.radius, min(WORLD_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(WORLD_HEIGHT - self.radius, self.y))

    def update(self):
        target_radius = int(self.mass ** 0.5 * 4)
        self.radius += (target_radius - self.radius) * 0.1

    def draw(self, screen):
        if self.skin == "custom":
            pygame.draw.circle(screen, self.custom_color,
                               (int(self.x - camera.x), int(self.y - camera.y)), self.radius)
            pygame.draw.circle(screen, self.border_color,
                               (int(self.x - camera.x), int(self.y - camera.y)), self.radius, 4)
            eye_y = int(self.y - camera.y - 10)
            pygame.draw.circle(screen, self.eye_color,
                               (int(self.x - camera.x - 12), eye_y), 6)
            pygame.draw.circle(screen, self.eye_color,
                               (int(self.x - camera.x + 12), eye_y), 6)
        else:
            skin_img = loaded_skins[self.skin]
            size = int(self.radius * 2)
            print("radius:", self.radius, "size:", size)
            scaled = pygame.transform.smoothscale(skin_img, (size, size))
            if self.skin in ["R", "Ri"]:
                print("scaled:", scaled.get_width(), scaled.get_height())
            sx = int(self.x - camera.x)
            sy = int(self.y - camera.y)
            screen.blit(scaled, (sx - self.radius, sy - self.radius))



class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target):
        self.x = target.x - WIDTH // 2
        self.y = target.y - HEIGHT // 2


class Food:
    def __init__(self, world_width, world_height):
        self.x = random.randint(0, world_width)
        self.y = random.randint(0, world_height)
        self.radius = 3
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.radius)


class Bot(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.target = None
        self.vision_radius = 300
        self.ai_timer = random.randint(0, 10)
        self.last_dx = 0
        self.last_dy = 0
        available_skins = [name for name in skins if name not in ("custom", "default")]
        self.skin = random.choice(available_skins)

    def ai_move(self, foods, bots):
        self.ai_timer += 1
        if self.ai_timer % 3 != 0:
            self.x += getattr(self, 'last_dx', 0)
            self.y += getattr(self, 'last_dy', 0)
            return
        nearby_foods = [f for f in foods
                        if abs(f.x - self.x) < 300 and abs(f.y - self.y) < 300]
        nearby_bots = [b for b in bots
                       if b != self and abs(b.x - self.x) < 300 and abs(b.y - self.y) < 300]
        for b in nearby_bots:
            if b.mass > self.mass * 1.1:
                dx = self.x - b.x
                dy = self.y - b.y
                dist = math.hypot(dx, dy) or 1
                self.last_dx = (dx / dist) * self.speed
                self.last_dy = (dy / dist) * self.speed
                self.x += self.last_dx
                self.y += self.last_dy
                return
        if nearby_foods:
            if self.target is None or self.target not in nearby_foods:
                self.target = min(nearby_foods,
                                  key=lambda f: math.hypot(f.x - self.x, f.y - self.y))
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy) or 1
            self.speed = self.base_speed / (self.radius * 0.1 + 1)
            self.last_dx = (dx / dist) * self.speed
            self.last_dy = (dy / dist) * self.speed
            self.x += self.last_dx
            self.y += self.last_dy
            return
        self.x = max(self.radius, min(WORLD_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(WORLD_HEIGHT - self.radius, self.y))


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, mouse_pos):
        color = (70, 70, 70) if self.rect.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click


class InputBox:
    def __init__(self, x, y, w, h, placeholder="Enter your name..."):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False
        self.placeholder = placeholder

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 12:
                self.text += event.unicode

    def draw(self, screen):
        font = pygame.font.SysFont("Impact", 30)
        color = (0, 245, 255) if self.active else (0, 255, 255)
        txt = font.render(self.text or self.placeholder, True, (0, 245, 255))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))


# ----------- OBJECTS -----------
player = Player(400, 300)
player.skin = data.get("selected_skin", "default")
camera = Camera()
foods = []
WORLD_WIDTH = 3000
WORLD_HEIGHT = 3000


# login screen
nickname_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 - 60, 300, 50, "Введіть частоту")
password_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 + 10, 300, 50, "Введіть Аватар-код")



# registration screen
name_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 - 160 - 20, 300, 50, "Введіть сигнал")
przv_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 - 110, 300, 50, "Введіть прозву")
date_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 - 60 + 20, 300, 50, "Введіть Вектор нуль")
nickname2_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 50, "Введіть частоту")
password2_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 + 60 + 20, 300, 50, "Введіть Аватар-код")
password3_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 + 110 + 30, 300, 50, "Введіть Аватар-код")







###################
for _ in range(800):
    foods.append(Food(WORLD_WIDTH, WORLD_HEIGHT))

bots = []
for i in range(80):
    bot = Bot(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
    bot.name = f"Bot_{i}"
    bots.append(bot)

particles = []
for _ in range(60):
    particles.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(2, 6),
        (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    ])


def draw_particles():
    for p in particles:
        pygame.draw.circle(screen, p[3], (int(p[0]), int(p[1])), p[2])
        p[1] += 0.3
        if p[1] > HEIGHT:
            p[1] = 0
            p[0] = random.randint(0, WIDTH)


camera_x = 0
camera_y = 0
GRID_SIZE = 50


def draw_grid(screen, camera_x, camera_y):
    for x in range(-2000, 2000, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40),
                         (x - camera_x, -2000 - camera_y),
                         (x - camera_x, 2000 - camera_y))
    for y in range(-2000, 2000, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40),
                         (-2000 - camera_x, y - camera_y),
                         (2000 - camera_x, y - camera_y))


font = pygame.font.SysFont("Arial", 24)
game_state = "auth"
game_mode = "free"
winner = None


def draw_shadow_text(surface, text, font, color, x, y):
    shadow = font.render(text, True, (0, 0, 0))
    surface.blit(shadow, (x + 2, y + 2))
    main = font.render(text, True, color)
    surface.blit(main, (x, y))


def draw_menu(screen, WIDTH, HEIGHT):
    screen.blit(background, (0, 0))
    draw_particles()


    classic_y = HEIGHT // 2 - 200 // 2 + 100
    rush_y = HEIGHT // 2 - 200 // 2 + 100


    if game_mode == "free":
        classic_y -= 10

    if game_mode == "competition":
        rush_y -= 10


    screen.blit(Play_btn, (WIDTH // 2 - 400 // 2, HEIGHT // 2 - 200 // 2))
    screen.blit(Classic_btn, (WIDTH // 2 - 400 // 2 - 400, classic_y))
    screen.blit(Rush_btn, (WIDTH // 2 - 400 // 2 + 400, rush_y))
    screen.blit(Settings_btn, (WIDTH // 2 - 400 // 2 - 400, HEIGHT // 2 - 200 // 2 + 250))
    screen.blit(Shop_btn, (WIDTH // 2 - 400 // 2 + 400, HEIGHT // 2 - 200 // 2 + 250))





    Play_btn_rect = pygame.Rect(WIDTH // 2 - 400 // 2, HEIGHT // 2 - 200 // 2, 400, 200)
    Classic_btn_rect = pygame.Rect(WIDTH // 2 - 400 // 2 - 400, classic_y, 400, 200)
    Rush_btn_rect = pygame.Rect(WIDTH // 2 - 400 // 2 + 400, rush_y, 400, 200)
    Settings_btn_rect = pygame.Rect(WIDTH // 2 - 400 // 2 - 400, HEIGHT // 2 - 200 // 2 + 250, 400, 200)
    Shop_btn_rect = pygame.Rect(WIDTH // 2 - 400 // 2 + 400, HEIGHT // 2 - 200 // 2 + 250, 400, 200)


    return Play_btn_rect, Classic_btn_rect, Rush_btn_rect, Settings_btn_rect, Shop_btn_rect



def draw_win():
    screen.blit(win_img, (0, 0))
    text = font.render("Press R to restart", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT - 100))


def draw_lose():
    screen.blit(lose_img, (0, 0))
    text = font.render("Press R to restart", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT - 100))


def draw_leaderboard():
    entities = bots + [player]
    entities = sorted(entities, key=lambda e: e.mass, reverse=True)
    top = entities[:5]
    pygame.draw.rect(screen, (0, 0, 0, 100), (WIDTH - 220, 20, 200, 200))
    title = font.render("Leaderboard", True, (255, 255, 255))
    screen.blit(title, (WIDTH - 200, 30))
    y_offset = 60
    for i, entity in enumerate(top):
        color = (255, 255, 0) if entity == player else (255, 255, 255)
        text = font.render(f"{i+1}. {entity.name} - {entity.mass}", True, color)
        screen.blit(text, (WIDTH - 200, y_offset))
        y_offset += 30


def draw_top_ui():
    panel = pygame.Rect(WIDTH - 300, 20, 260, 60)
    pygame.draw.rect(screen, (240, 240, 240), panel, border_radius=15)
    pygame.draw.circle(screen, (255, 210, 0), (panel.x + 30, panel.y + 30), 15)
    pygame.draw.circle(screen, (255, 255, 100), (panel.x + 25, panel.y + 25), 5)
    coin_text = font.render(str(coins), True, (0, 0, 0))
    screen.blit(coin_text, (panel.x + 60, panel.y + 20))
    plus_rect = pygame.Rect(panel.x + 150, panel.y + 15, 30, 30)
    pygame.draw.rect(screen, (0, 200, 0), plus_rect, border_radius=8)
    screen.blit(font.render("+", True, (255, 255, 255)), (plus_rect.x + 8, plus_rect.y + 2))
    shop_rect = pygame.Rect(panel.x + 210, panel.y + 20, 70, 35)
    pygame.draw.rect(screen, (0, 150, 255), shop_rect, border_radius=10)
    shop_text = font.render("Shop", True, (255, 255, 255))
    screen.blit(shop_text, (shop_rect.x + 5, shop_rect.y + 5))
    return plus_rect, shop_rect


custom_color = list(data.get("custom_player", default_data["custom_player"])["color"])
custom_text = [""]
active_slider = [None]

sakura_particles = []
for _ in range(80):
    sakura_particles.append({
        "x": random.randint(0, 300),
        "y": random.randint(-100, 2000),
        "speed": random.uniform(0.5, 2.0),
        "sway": random.uniform(-0.5, 0.5),
        "size": random.randint(4, 10),
        "angle": random.uniform(0, 360),
        "rot_speed": random.uniform(-2, 2),
        "alpha": random.randint(150, 255),
    })

clouds_with_petals = []
for _ in range(7):
    cx = random.uniform(0, WIDTH + 200)
    cy = random.uniform(25, 140)
    speed = random.uniform(0.15, 0.55)
    size = random.uniform(0.65, 1.35)
    petals = []
    for _ in range(random.randint(5, 10)):
        petals.append({
            "x": cx + random.uniform(-45, 45),
            "y": cy + random.uniform(5, 25),
            "vx": random.uniform(-0.3, 0.3),
            "vy": random.uniform(0.3, 0.8),
            "angle": random.uniform(0, 360),
            "rot_speed": random.uniform(-1.2, 1.2),
            "size": random.randint(4, 9),
            "alpha": random.randint(160, 240),
            "timer": random.uniform(0, 400),
            "wave_offset": random.uniform(0, 6.28),
        })
    clouds_with_petals.append({
        "x": cx, "y": cy,
        "speed": speed, "size": size,
        "petals": petals,
    })

gem_case_anim = {
    "active": False,
    "case_index": 0,
    "angle_x": 0,
    "angle_y": 0,
    "phase": 0,
    "timer": 0,
    "result_skin": None,
    "is_duplicate": False,
}


def draw_sakura(surface):
    from settings_state import quality_toggles, audio_toggles
    t = pygame.time.get_ticks() * 0.001



    if quality_toggles["pelyustky"]:
        for p in sakura_particles:
            p["y"] += p["speed"]
            p["x"] += p["sway"] + math.sin(p["y"] * 0.02) * 0.5
            p["angle"] += p["rot_speed"]
            if p["y"] > HEIGHT + 20:
                p["y"] = random.randint(-50, -10)
                p["x"] = random.randint(0, WIDTH)
            cached_angle = (int(p["angle"]) // 10) * 10 % 360
            rotated = petal_cache[cached_angle]
            surface.blit(rotated, (int(p["x"]), int(p["y"])))





    if quality_toggles["khmarky"]:
        for cloud in clouds_with_petals:
            cloud["x"] -= cloud["speed"]
            if cloud["x"] < -260:
                cloud["x"] = float(WIDTH + random.randint(50, 200))
                cloud["y"] = float(random.uniform(25, 140))

                for p in cloud["petals"]:
                    p["x"] = cloud["x"] + random.uniform(-45, 45)
                    p["y"] = cloud["y"] + random.uniform(5, 25)

            cx = int(cloud["x"])
            cy = int(cloud["y"])
            s = cloud["size"]
            for ox, oy, r in [
                (0, 0, int(30*s)),
                (int(35*s), int(8*s), int(22*s)),
                (int(-35*s), int(8*s), int(22*s)),
                (int(18*s), int(-12*s), int(20*s)),
                (int(-18*s), int(-12*s), int(18*s)),
                (int(50*s), int(14*s), int(16*s)),
                (int(-50*s), int(14*s), int(16*s)),
            ]:
                pygame.draw.circle(surface, (255, 255, 255), (cx + ox, cy + oy), r)
            for p in cloud["petals"]:
                p["timer"] += 1
                if p["y"] > HEIGHT + 20 or p["x"] < -20 or p["x"] > WIDTH + 20:
                    p["x"] = cloud["x"] + random.uniform(-45, 45)
                    p["y"] = cloud["y"] + random.uniform(8, 28)
                    p["vx"] = random.uniform(-0.3, 0.3)
                    p["vy"] = random.uniform(0.3, 0.8)
                    p["timer"] = 0



                sway = math.sin(t * 1.1 + p["wave_offset"]) * 0.5
                p["x"] += p["vx"] + sway
                p["y"] += p["vy"]
                p["angle"] += p["rot_speed"]
                sz = p["size"]
                petal_surf = pygame.Surface((sz * 2 + 2, sz * 2 + 2), pygame.SRCALPHA)
                color = (255, 182, 193, p["alpha"])
                pygame.draw.ellipse(petal_surf, color, (0, 0, sz * 2, sz))
                rotated = pygame.transform.rotate(petal_surf, p["angle"])
                screen.blit(rotated, (int(p["x"] - rotated.get_width() // 2),
                                      int(p["y"] - rotated.get_height() // 2)))


























def draw_sakura_tree(surface, x, y, size=1.0):
    trunk_color = (101, 67, 33)
    pygame.draw.rect(surface, trunk_color,
                     (int(x - 8*size), int(y - 80*size), int(16*size), int(80*size)), border_radius=4)
    branch_color = (120, 80, 40)
    pygame.draw.line(surface, branch_color,
                     (int(x), int(y - 60*size)), (int(x - 40*size), int(y - 100*size)), int(6*size))
    pygame.draw.line(surface, branch_color,
                     (int(x), int(y - 50*size)), (int(x + 35*size), int(y - 90*size)), int(5*size))
    pygame.draw.line(surface, branch_color,
                     (int(x), int(y - 70*size)), (int(x - 20*size), int(y - 120*size)), int(4*size))
    blossoms = [
        (x, y - 120*size, 45*size),
        (x - 45*size, y - 100*size, 35*size),
        (x + 40*size, y - 95*size, 38*size),
        (x - 20*size, y - 140*size, 30*size),
        (x + 15*size, y - 145*size, 32*size),
        (x, y - 160*size, 28*size),
    ]
    for bx, by, br in blossoms:
        pygame.draw.circle(surface, (220, 130, 150), (int(bx), int(by)), int(br))
        pygame.draw.circle(surface, (255, 192, 203),
                           (int(bx - br*0.2), int(by - br*0.2)), int(br * 0.7))
        for _ in range(5):
            fx = bx + random.randint(-int(br), int(br))
            fy = by + random.randint(-int(br), int(br))
            pygame.draw.circle(surface, (255, 220, 230), (int(fx), int(fy)), 3)


def draw_spring_ground(surface):
    grass_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
    pygame.draw.rect(surface, (34, 139, 34), grass_rect)
    pygame.draw.rect(surface, (50, 160, 50), pygame.Rect(0, HEIGHT - 60, WIDTH, 15))
    for i in range(0, WIDTH, 15):
        h = random.randint(10, 25)
        pygame.draw.line(surface, (0, 180, 0),
                         (i, HEIGHT - 60),
                         (i + random.randint(-3, 3), HEIGHT - 60 - h), 2)
    flowers = [
        (100, HEIGHT - 65, (255, 255, 0)),
        (250, HEIGHT - 70, (255, 100, 100)),
        (400, HEIGHT - 68, (255, 200, 0)),
        (600, HEIGHT - 72, (200, 100, 255)),
        (800, HEIGHT - 66, (255, 150, 200)),
        (WIDTH-100, HEIGHT-68, (255, 255, 0)),
        (WIDTH-250, HEIGHT-70, (100, 200, 255)),
        (WIDTH-400, HEIGHT-65, (255, 100, 150)),
    ]
    for fx, fy, fc in flowers:
        pygame.draw.line(surface, (0, 150, 0), (fx, HEIGHT - 60), (fx, fy), 2)
        for angle in range(0, 360, 60):
            px = fx + int(8 * math.cos(math.radians(angle)))
            py = fy + int(8 * math.sin(math.radians(angle)))
            pygame.draw.circle(surface, fc, (px, py), 5)
        pygame.draw.circle(surface, (255, 255, 100), (fx, fy), 4)


def draw_sky(surface):
    sun_x, sun_y = WIDTH - 120, 80
    angle_offset = pygame.time.get_ticks() * 0.04
    for i in range(12):
        angle = math.radians(i * 30 + angle_offset)
        x1 = sun_x + int(math.cos(angle) * 38)
        y1 = sun_y + int(math.sin(angle) * 38)
        x2 = sun_x + int(math.cos(angle) * 60)
        y2 = sun_y + int(math.sin(angle) * 60)
        pygame.draw.line(surface, (255, 220, 0), (x1, y1), (x2, y2), 3)
    for i in range(12):
        angle = math.radians(i * 30 + 15 + angle_offset)
        x1 = sun_x + int(math.cos(angle) * 36)
        y1 = sun_y + int(math.sin(angle) * 36)
        x2 = sun_x + int(math.cos(angle) * 52)
        y2 = sun_y + int(math.sin(angle) * 52)
        pygame.draw.line(surface, (255, 200, 0), (x1, y1), (x2, y2), 2)
    pygame.draw.circle(surface, (255, 200, 0), (sun_x, sun_y), 34)
    pygame.draw.circle(surface, (255, 230, 80), (sun_x - 8, sun_y - 8), 14)


def draw_scrollbar(surface, scroll, max_scroll):
    if max_scroll <= 0:
        return None
    bar_w = 8
    bar_x = WIDTH - 24
    bar_y = 110
    bar_h = HEIGHT - 180
    pygame.draw.rect(surface, (20, 20, 35), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
    pygame.draw.rect(surface, (50, 50, 80), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=4)
    thumb_h = max(30, int(bar_h * (bar_h / (bar_h + max_scroll))))
    thumb_y = bar_y + int((bar_h - thumb_h) * (-scroll / max_scroll))
    pygame.draw.rect(surface, (120, 70, 255), (bar_x, thumb_y, bar_w, thumb_h), border_radius=4)
    pygame.draw.rect(surface, (180, 120, 255), (bar_x, thumb_y, bar_w, thumb_h), 1, border_radius=4)
    return pygame.Rect(bar_x, thumb_y, bar_w, thumb_h)


def draw_shop_topbar(screen, font, coins, dna=0):
    bar_rect = pygame.Rect(0, 0, WIDTH, 64)
    pygame.draw.rect(screen, (18, 18, 28), bar_rect)
    back_rect = pygame.Rect(12, 12, 40, 40)
    pygame.draw.rect(screen, (40, 40, 60), back_rect, border_radius=10)
    arrow = font.render("<---", True, (200, 200, 255))
    screen.blit(arrow, (back_rect.x + 10, back_rect.y + 8))
    big_font = pygame.font.SysFont("Arial", 28, bold=True)
    title = big_font.render("Shop", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 16))
    coin_pill = pygame.Rect(WIDTH - 280, 10, 120, 42)
    pygame.draw.rect(screen, (40, 35, 10), coin_pill, border_radius=21)
    pygame.draw.rect(screen, (255, 200, 0), coin_pill, 2, border_radius=21)
    pygame.draw.circle(screen, (255, 200, 0), (coin_pill.x + 22, coin_pill.centery), 14)
    pygame.draw.circle(screen, (255, 230, 80), (coin_pill.x + 18, coin_pill.centery - 4), 5)
    coin_txt = font.render(str(coins), True, (255, 230, 100))
    screen.blit(coin_txt, (coin_pill.x + 42, coin_pill.centery - coin_txt.get_height() // 2))
    plus1 = font.render("+", True, (255, 200, 0))
    screen.blit(plus1, (coin_pill.right + 4, coin_pill.centery - plus1.get_height() // 2))
    dna_pill = pygame.Rect(WIDTH - 140, 10, 120, 42)
    pygame.draw.rect(screen, (10, 35, 40), dna_pill, border_radius=21)
    pygame.draw.rect(screen, (0, 220, 180), dna_pill, 2, border_radius=21)
    pygame.draw.circle(screen, (0, 200, 160), (dna_pill.x + 22, dna_pill.centery), 14)
    dna_txt = font.render(str(dna), True, (100, 255, 220))
    screen.blit(dna_txt, (dna_pill.x + 42, dna_pill.centery - dna_txt.get_height() // 2))
    plus2 = font.render("+", True, (0, 220, 180))
    screen.blit(plus2, (dna_pill.right + 4, dna_pill.centery - plus2.get_height() // 2))
    return back_rect


def draw_tab_bar(screen, font, active_tab):
    tab_y = 68
    tab_h = 40
    tab_w = WIDTH // len(TABS)

    for i, tab in enumerate(TABS):
        r = pygame.Rect(i * tab_w, tab_y, tab_w, tab_h)
        if tab == SHOP_TAB[0]:
            pygame.draw.rect(screen, (30, 30, 50), r)
            pygame.draw.line(screen, (80, 160, 255), (r.x, r.bottom - 3), (r.right, r.bottom - 3), 3)
            txt_color = (255, 255, 255)
        else:
            pygame.draw.rect(screen, (18, 18, 28), r)
            txt_color = (120, 120, 160)
        label = font.render(tab, True, txt_color)
        screen.blit(label, (r.centerx - label.get_width() // 2, r.centery - label.get_height() // 2))
        tab_rects.append((r, tab))
    pygame.draw.line(screen, (40, 40, 60), (0, tab_y + tab_h), (WIDTH, tab_y + tab_h), 1)

    return tab_rects


def draw_create_tab():
    cx = WIDTH // 2
    small_font = pygame.font.SysFont("Arial", 16, bold=True)
    tiny_font = pygame.font.SysFont("Arial", 13)
    mouse_pos = pygame.mouse.get_pos()
    tf = pygame.font.SysFont("Arial", 26, bold=True)
    title = tf.render("Створи свій скін", True, (200, 200, 255))
    screen.blit(title, (cx - title.get_width()//2, 130))
    preview_center = (cx - 260, 320)
    r, g, b = custom_color
    pygame.draw.circle(screen, (r, g, b), preview_center, 80)
    pygame.draw.circle(screen, player.border_color, preview_center, 80, 4)
    pygame.draw.circle(screen, player.eye_color, (preview_center[0]-25, preview_center[1]-15), 10)
    pygame.draw.circle(screen, player.eye_color, (preview_center[0]+25, preview_center[1]-15), 10)
    if custom_text[0]:
        pf = pygame.font.SysFont("Arial", 28, bold=True)
        pt = pf.render(custom_text[0], True, (255, 255, 255))
        screen.blit(pt, (preview_center[0] - pt.get_width()//2, preview_center[1] - pt.get_height()//2))
    lbl = tiny_font.render("Попередній перегляд", True, (150, 150, 200))
    screen.blit(lbl, (preview_center[0] - lbl.get_width()//2, preview_center[1] + 95))
    slider_x = cx - 50
    slider_w = 320
    slider_h = 18
    names = ["R", "G", "B"]
    colors = [(255, 80, 80), (80, 255, 80), (80, 150, 255)]
    slider_rects = []
    for i in range(3):
        sy = 185 + 1 * 65
        label = small_font.render(f"{names[i]}: {custom_color[i]}", True, colors[i])
        screen.blit(label, (slider_x - 55, sy - 2))
        bg = pygame.Rect(slider_x, sy, slider_w, slider_h)
        pygame.draw.rect(screen, (40, 40, 60), bg, border_radius=9)
        pygame.draw.rect(screen, colors[i], bg, 2, border_radius=9)
        fill_w = int(slider_w * custom_color[i] / 255)
        if fill_w > 0:
            pygame.draw.rect(screen, colors[i], pygame.Rect(slider_x, sy, fill_w, slider_h), border_radius=9)
        knob_x = slider_x + fill_w
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, sy + slider_h//2), 11)
        pygame.draw.circle(screen, colors[i], (knob_x, sy + slider_h//2), 8)
        slider_rects.append(bg)
    eye_btn = pygame.Rect(slider_x - 55, 390, 150, 36)
    pygame.draw.rect(screen, (60, 60, 90), eye_btn, border_radius=10)
    pygame.draw.rect(screen, (200, 200, 255), eye_btn, 2, border_radius=10)
    et = tiny_font.render("Kolir ochei", True, (255, 255, 255))
    screen.blit(et, (eye_btn.centerx - et.get_width()//2, eye_btn.centery - et.get_height()//2))
    border_btn = pygame.Rect(slider_x + 110, 390, 160, 36)
    pygame.draw.rect(screen, (60, 60, 90), border_btn, border_radius=10)
    pygame.draw.rect(screen, (200, 200, 255), border_btn, 2, border_radius=10)
    bt = tiny_font.render("Kolir ramky", True, (255, 255, 255))
    screen.blit(bt, (border_btn.centerx - bt.get_width()//2, border_btn.centery - bt.get_height()//2))
    text_label = small_font.render("Tekst abo emoji:", True, (200, 200, 255))
    screen.blit(text_label, (slider_x - 55, 442))
    text_box = pygame.Rect(slider_x - 55, 466, 370, 40)
    pygame.draw.rect(screen, (30, 30, 50), text_box, border_radius=10)
    pygame.draw.rect(screen, (100, 100, 180), text_box, 2, border_radius=10)
    disp = custom_text[0] if custom_text[0] else "Vvedy tekst abo emoji..."
    col = (255, 255, 255) if custom_text[0] else (100, 100, 130)
    screen.blit(pygame.font.SysFont("Arial", 20).render(disp, True, col), (text_box.x + 10, text_box.y + 8))
    save_btn = pygame.Rect(slider_x - 55, 525, 370, 52)
    hover = save_btn.collidepoint(mouse_pos)
    pygame.draw.rect(screen, (0, 180, 80) if hover else (0, 140, 60), save_btn, border_radius=14)
    pygame.draw.rect(screen, (100, 255, 160), save_btn, 2, border_radius=14)
    st = small_font.render("ZBEREHTY", True, (255, 255, 255))
    screen.blit(st, (save_btn.centerx - st.get_width()//2, save_btn.centery - st.get_height()//2))
    return slider_rects, text_box, save_btn, eye_btn, border_btn


def draw_gem_case_box(surface, cx, cy, color, color2, icon_text, size=1.0, angle_x=0, angle_y=0):
    w = int(100 * size)
    h = int(100 * size)
    depth = int(20 * size)
    offset_x = int(math.sin(math.radians(angle_y)) * depth)
    offset_y = int(math.sin(math.radians(angle_x)) * depth * 0.5)
    scale_x = abs(math.cos(math.radians(angle_y)))
    scale_y = abs(math.cos(math.radians(angle_x)))
    draw_w = max(4, int(w * scale_x))
    draw_h = max(4, int(h * scale_y))
    pygame.draw.rect(surface, (5, 5, 15),
                     pygame.Rect(cx - draw_w//2 + 6, cy - draw_h//2 + 6, draw_w, draw_h), border_radius=12)
    if offset_x > 0:
        side = pygame.Rect(cx + draw_w//2 - offset_x, cy - draw_h//2 + offset_y, offset_x, draw_h)
        pygame.draw.rect(surface, color2, side, border_radius=4)
    elif offset_x < 0:
        side = pygame.Rect(cx - draw_w//2, cy - draw_h//2 + offset_y, abs(offset_x), draw_h)
        pygame.draw.rect(surface, color2, side, border_radius=4)
    main_rect = pygame.Rect(cx - draw_w//2, cy - draw_h//2 + offset_y, draw_w, draw_h)
    pygame.draw.rect(surface, color, main_rect, border_radius=12)
    mid_y = cy + offset_y
    pygame.draw.line(surface, color2, (cx - draw_w//2 + 4, mid_y), (cx + draw_w//2 - 4, mid_y), 3)
    lock_size = int(14 * size * scale_x)
    if lock_size > 4:
        pygame.draw.rect(surface, color2,
                         pygame.Rect(cx - lock_size//2, mid_y - lock_size//2, lock_size, lock_size), border_radius=4)
        pygame.draw.circle(surface, (255, 255, 200), (cx, mid_y), lock_size//3)
    pygame.draw.rect(surface, (255, 255, 255), main_rect, 2, border_radius=12)
    if draw_w > 30 and draw_h > 30:
        icon_font = pygame.font.SysFont("Arial", int(32 * size * min(scale_x, scale_y)))
        icon_surf = icon_font.render(icon_text, True, (255, 255, 255))
        surface.blit(icon_surf, (cx - icon_surf.get_width()//2,
                                 cy - draw_h//4 + offset_y - icon_surf.get_height()//2))


def draw_gems_tab():
    cx = WIDTH // 2
    small_font = pygame.font.SysFont("Arial", 16, bold=True)
    tiny_font = pygame.font.SysFont("Arial", 13)
    mouse_pos = pygame.mouse.get_pos()
    screen.fill((12, 12, 22))
    shop_panel = pygame.Rect(WIDTH//2 - 500, 110, 1000, HEIGHT - 130)
    pygame.draw.rect(screen, (12, 12, 25), shop_panel, border_radius=20)
    pygame.draw.rect(screen, (0, 200, 170), shop_panel, 2, border_radius=20)
    for y in range(108, HEIGHT - 60):
        ratio = (y - 108) / (HEIGHT - 60 - 108)
        r = int(10 + ratio * 20)
        g = int(10 + ratio * 30)
        b = int(20 + ratio * 20)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    draw_sakura_tree(screen, 80, HEIGHT - 60, size=0.9)
    draw_sakura_tree(screen, WIDTH - 80, HEIGHT - 60, size=0.9)
    draw_sakura_tree(screen, 200, HEIGHT - 60, size=0.6)
    draw_sakura_tree(screen, WIDTH - 200, HEIGHT - 60, size=0.6)
    draw_spring_ground(screen)
    draw_sakura(screen)
    tf = pygame.font.SysFont("Arial", 32, bold=True)
    title = tf.render("Gem Shop", True, (0, 240, 220))
    title_shadow = tf.render("Gem Shop", True, (0, 80, 70))
    screen.blit(title_shadow, (cx - title.get_width()//2 + 2, 132))
    screen.blit(title, (cx - title.get_width()//2, 130))
    gf = pygame.font.SysFont("Arial", 18, bold=True)
    gem_bal = gf.render(f"{gems} gemiv", True, (0, 255, 200))
    bal_bg = pygame.Rect(cx - gem_bal.get_width()//2 - 16, 166, gem_bal.get_width() + 32, 30)
    pygame.draw.rect(screen, (0, 40, 35), bal_bg, border_radius=15)
    pygame.draw.rect(screen, (0, 200, 160), bal_bg, 2, border_radius=15)
    screen.blit(gem_bal, (cx - gem_bal.get_width()//2, 170))
    n_cases = len(GEM_CASES)
    case_w = 180
    gap = 20
    total_cases_w = n_cases * case_w + (n_cases - 1) * gap
    case_start_x = WIDTH // 2 - total_cases_w // 2 + case_w // 2
    gem_case_rects = []
    for i, case in enumerate(GEM_CASES):
        case_cx = case_start_x + i * (case_w + gap)
        case_cy = 240
        ax = 0
        ay = 0
        if gem_case_anim["active"] and gem_case_anim["case_index"] == i:
            ax = gem_case_anim["angle_x"]
            ay = gem_case_anim["angle_y"]
        draw_gem_case_box(screen, case_cx, case_cy, case["color"], case["color2"],
                          case["icon"], size=1.0, angle_x=ax, angle_y=ay)
        nf = small_font.render(case["name"], True, (230, 230, 255))
        screen.blit(nf, (case_cx - nf.get_width()//2, case_cy + 60))
        df = tiny_font.render(case["description"], True, case["color"])
        screen.blit(df, (case_cx - df.get_width()//2, case_cy + 82))
        btn = pygame.Rect(case_cx - 60, case_cy + 105, 120, 34)
        hover = btn.collidepoint(mouse_pos)
        pygame.draw.rect(screen, case["color"] if hover else case["color2"], btn, border_radius=10)
        pygame.draw.rect(screen, case["color"], btn, 2, border_radius=10)
        bt = tiny_font.render(f"{case['gem_price']}", True, (255, 255, 255))
        screen.blit(bt, (btn.centerx - bt.get_width()//2, btn.centery - bt.get_height()//2))
        gem_case_rects.append((btn, case["name"], case["gem_price"], i))
    gem_skins = [(n, d) for n, d in skins.items() if "gem_price" in d]
    COLS = min(5, len(gem_skins)) if gem_skins else 1
    CARD_W = 140
    CARD_H = 185
    H_GAP = 14
    total_w = COLS * CARD_W + (COLS - 1) * H_GAP
    x_start = (WIDTH - total_w) // 2
    gem_skin_rects = []
    for i, (name, skin_data) in enumerate(gem_skins):
        col = i % COLS
        row = i // COLS
        cx2 = x_start + col * (CARD_W + H_GAP)
        cy2 = 480 + row * (CARD_H + H_GAP)
        card = pygame.Rect(cx2, cy2, CARD_W, CARD_H)
        glow = rarity_colors.get(skin_data.get("rarity", "none"), (180, 180, 180))
        is_owned = name in owned_skins
        is_sel = name == player.skin
        pygame.draw.rect(screen, (5, 5, 12), card.move(4, 6), border_radius=18)
        pygame.draw.rect(screen, (20, 40, 30) if is_sel else (28, 28, 45), card, border_radius=18)
        pygame.draw.rect(screen, glow, card, 3, border_radius=18)
        if skin_data.get("rarity") == "gold":
            pygame.draw.rect(screen, (255, 215, 0), card.inflate(6, 6), 2, border_radius=20)
            pygame.draw.rect(screen, (180, 140, 0), card.inflate(12, 12), 1, border_radius=22)
        if name in loaded_skins:
            img = loaded_skins[name]
            scaled = pygame.transform.smoothscale(img, (90, 90))
            mask = pygame.Surface((90, 90), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255, 255), (45, 45), 45)
            scaled.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(scaled, (card.centerx - 45, card.y + 14))
        nf = pygame.font.SysFont("Arial", 13, bold=True)
        nt = nf.render(name.upper(), True, (230, 230, 255))
        screen.blit(nt, (card.centerx - nt.get_width()//2, card.y + 112))
        pt = tiny_font.render(f"{skin_data['gem_price']}", True, (0, 220, 200))
        screen.blit(pt, (card.centerx - pt.get_width()//2, card.y + 130))
        btn = pygame.Rect(card.x + 12, card.bottom - 40, CARD_W - 24, 30)
        if is_sel:
            pygame.draw.rect(screen, (0, 130, 60), btn, border_radius=9)
            bt = tiny_font.render("EQUIPPED", True, (200, 255, 200))
        elif is_owned:
            pygame.draw.rect(screen, (0, 120, 60), btn, border_radius=9)
            bt = tiny_font.render("SELECT", True, (255, 255, 255))
        else:
            hover = btn.collidepoint(mouse_pos)
            pygame.draw.rect(screen, (0, 200, 180) if hover else (0, 140, 130), btn, border_radius=9)
            bt = tiny_font.render(f"{skin_data['gem_price']}", True, (255, 255, 255))
        screen.blit(bt, (btn.centerx - bt.get_width()//2, btn.centery - bt.get_height()//2))
        gem_skin_rects.append((btn, name))
    back_btn = pygame.Rect(WIDTH//2 - 500, 118, 44, 36)
    mouse_pos = pygame.mouse.get_pos()
    hover = back_btn.collidepoint(mouse_pos)
    pygame.draw.rect(screen, (0, 180, 150) if hover else (0, 120, 100), back_btn, border_radius=10)
    pygame.draw.rect(screen, (0, 255, 210), back_btn, 2, border_radius=10)
    arrow_font = pygame.font.SysFont("Arial", 18, bold=True)
    arrow = arrow_font.render("<-", True, (255, 255, 255))
    screen.blit(arrow, (back_btn.centerx - arrow.get_width()//2, back_btn.centery - arrow.get_height()//2))
    return gem_case_rects, gem_skin_rects, back_btn


def update_gem_case_anim():
    if not gem_case_anim["active"]:
        return
    gem_case_anim["timer"] += 1
    t = gem_case_anim["timer"]
    if gem_case_anim["phase"] == 0:
        gem_case_anim["angle_x"] += 6
        gem_case_anim["angle_y"] += 4
        if t > 150:
            gem_case_anim["phase"] = 1
            gem_case_anim["timer"] = 0
            gem_case_anim["angle_x"] = 0
            gem_case_anim["angle_y"] = 0


def draw_chest_animation():
    ca = chest_anim
    cx, cy = WIDTH // 2, HEIGHT // 2
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    info_btn = pygame.Rect(WIDTH - 130, 75, 110, 36)
    hover = info_btn.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, (40, 20, 80) if hover else (25, 12, 50), info_btn, border_radius=10)
    pygame.draw.rect(screen, (180, 70, 255), info_btn, 2, border_radius=10)
    ib = pygame.font.SysFont("Arial", 14, bold=True).render("i  Shansy", True, (200, 150, 255))
    screen.blit(ib, (info_btn.centerx - ib.get_width()//2, info_btn.centery - ib.get_height()//2))
    for i in range(20):
        sx = (cx - 300 + i * 30 + ca["timer"] * 2) % WIDTH
        sy = (cy - 200 + i * 20) % HEIGHT
        pygame.draw.circle(screen, (255, 255, 200), (int(sx), int(sy)), 2)
    ca["timer"] += 1
    if ca["phase"] == 0:
        ca["angle"] += 6
        scale_x = abs(math.cos(math.radians(ca["angle"])))
        scale_y = 1.0 + abs(math.sin(math.radians(ca["angle"] * 0.5))) * 0.2
        w = int(180 * scale_x)
        h = int(180 * scale_y)
        if w < 4:
            w = 4
        pygame.draw.rect(screen, (20, 0, 40), pygame.Rect(cx - w//2 + 8, cy - h//2 + 8, w, h), border_radius=16)
        pygame.draw.rect(screen, (100, 40, 10), pygame.Rect(cx - w//2, cy, w, h//2), border_radius=10)
        pygame.draw.rect(screen, (160, 80, 20), pygame.Rect(cx - w//2, cy, w, h//2), 3, border_radius=10)
        pygame.draw.rect(screen, (140, 60, 15),
                         pygame.Rect(cx - w//2, cy - h//2, w, h//2 - ca["lid_offset"]), border_radius=10)
        pygame.draw.rect(screen, (200, 120, 40),
                         pygame.Rect(cx - w//2, cy - h//2, w, h//2 - ca["lid_offset"]), 3, border_radius=10)
        pygame.draw.rect(screen, (200, 150, 50), pygame.Rect(cx - w//2, cy - 8, w, 16), border_radius=4)
        lock_w = max(4, int(28 * scale_x))
        pygame.draw.rect(screen, (220, 180, 0),
                         pygame.Rect(cx - lock_w//2, cy - lock_w//2, lock_w, lock_w), border_radius=6)
        if lock_w > 10:
            pygame.draw.circle(screen, (255, 220, 50), (cx, cy), lock_w//3)
        corner_size = max(2, int(12 * scale_x))
        for corn_x, corn_y in [(cx-w//2, cy-h//2), (cx+w//2-corner_size, cy-h//2),
                                (cx-w//2, cy+h//2-corner_size), (cx+w//2-corner_size, cy+h//2-corner_size)]:
            pygame.draw.rect(screen, (200, 160, 0), pygame.Rect(corn_x, corn_y, corner_size, corner_size), border_radius=3)
        f = pygame.font.SysFont("Arial", 22, bold=True)
        txt = f.render("Vidkryvaemo keis...", True, (255, 220, 100))
        screen.blit(txt, (cx - txt.get_width()//2, cy + 120))
        bar_w = 300
        pygame.draw.rect(screen, (40, 40, 60), pygame.Rect(cx - bar_w//2, cy + 155, bar_w, 8), border_radius=4)
        progress = min(ca["timer"] / 150, 1.0)
        pygame.draw.rect(screen, (255, 180, 0),
                         pygame.Rect(cx - bar_w//2, cy + 155, int(bar_w * progress), 8), border_radius=4)
        if ca["timer"] > 150:
            ca["phase"] = 1
            ca["timer"] = 0
            ca["angle"] = 0
            for _ in range(40):
                ca["particles"].append({
                    "x": float(cx), "y": float(cy),
                    "vx": random.uniform(-8, 8),
                    "vy": random.uniform(-12, -2),
                    "color": random.choice([(255,200,0),(180,70,255),(0,220,180),(255,100,150),(100,200,255),(255,150,0)]),
                    "size": random.randint(4, 10),
                    "life": 1.0,
                })
        return None, None
    if ca["phase"] == 1:
        ca["lid_offset"] = min(ca["lid_offset"] + 4, 100)
        w, h = 180, 180
        glow_surf = pygame.Surface((300, 300), pygame.SRCALPHA)
        glow_alpha = int(min(ca["lid_offset"] * 2, 180))
        pygame.draw.circle(glow_surf, (255, 220, 100, glow_alpha), (150, 150), 150)
        screen.blit(glow_surf, (cx - 150, cy - 150))
        pygame.draw.rect(screen, (100, 40, 10), pygame.Rect(cx - w//2, cy, w, h//2), border_radius=10)
        pygame.draw.rect(screen, (160, 80, 20), pygame.Rect(cx - w//2, cy, w, h//2), 3, border_radius=10)
        lid_y = cy - h//2 - ca["lid_offset"]
        pygame.draw.rect(screen, (140, 60, 15), pygame.Rect(cx - w//2, lid_y, w, h//2), border_radius=10)
        pygame.draw.rect(screen, (200, 120, 40), pygame.Rect(cx - w//2, lid_y, w, h//2), 3, border_radius=10)
        pygame.draw.rect(screen, (200, 150, 50), pygame.Rect(cx - w//2, cy - 8, w, 16), border_radius=4)
        for p in ca["particles"][:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.3
            p["life"] -= 0.02
            if p["life"] <= 0:
                ca["particles"].remove(p)
                continue
            size = int(p["size"] * p["life"])
            if size > 0:
                pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), size)
        if ca["lid_offset"] >= 100:
            ca["phase"] = 2
            ca["timer"] = 0
        return None, None
    if ca["phase"] == 2:
        ca["timer"] += 1
        skin_name = ca["result_skin"]
        if not skin_name or skin_name not in skins:
            return None, None
        rarity = skins[skin_name].get("rarity", "none")
        glow = rarity_colors.get(rarity, (255, 255, 255))
        price = skins[skin_name].get("price", 0)
        refund = price // 2
        is_dup = ca["is_duplicate"]
        scale = min(ca["timer"] / 20, 1.0)
        card_w = int(280 * scale)
        card_h = int(360 * scale)
        if card_w < 10:
            return None, None
        card = pygame.Rect(cx - card_w//2, cy - card_h//2, card_w, card_h)
        pygame.draw.rect(screen, (5, 5, 20), card.move(6, 8), border_radius=20)
        pygame.draw.rect(screen, (18, 18, 35), card, border_radius=20)
        pygame.draw.rect(screen, glow, pygame.Rect(card.x, card.y, card_w, 8), border_radius=4)
        pygame.draw.rect(screen, glow, card, 3, border_radius=20)
        if rarity in ("legendary", "gold"):
            pygame.draw.rect(screen, tuple(c//2 for c in glow), card.inflate(8, 8), 2, border_radius=22)
        if skin_name in loaded_skins and card_w > 80:
            img_size = int(130 * scale)
            img = loaded_skins[skin_name]
            scaled_img = pygame.transform.smoothscale(img, (img_size, img_size))
            mask = pygame.Surface((img_size, img_size), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255,255,255,255), (img_size//2, img_size//2), img_size//2)
            scaled_img.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            pygame.draw.circle(screen, tuple(c//4 for c in glow), (cx, card.y + int(90*scale)), int(70*scale))
            pygame.draw.circle(screen, glow, (cx, card.y + int(90*scale)), int(70*scale), 2)
            screen.blit(scaled_img, (cx - img_size//2, card.y + int(25*scale)))
        if card_w > 150:
            nf = pygame.font.SysFont("Arial", int(22*scale), bold=True)
            nt = nf.render(skin_name.upper(), True, (255, 255, 255))
            screen.blit(nt, (cx - nt.get_width()//2, card.y + int(175*scale)))
            rf = pygame.font.SysFont("Arial", int(15*scale), bold=True)
            rt = rf.render(rarity.upper(), True, glow)
            screen.blit(rt, (cx - rt.get_width()//2, card.y + int(203*scale)))
            pygame.draw.line(screen, tuple(c//2 for c in glow),
                             (card.x + 20, card.y + int(228*scale)), (card.right - 20, card.y + int(228*scale)), 1)
            pf = pygame.font.SysFont("Arial", int(13*scale))
            props = [
                ("Rarnist", rarity.capitalize(), glow),
                ("Tsina", f"{price}", (255, 210, 50)),
                ("Status", "Duplikat!" if is_dup else "Novyi!", (255, 120, 50) if is_dup else (0, 220, 100)),
            ]
            for j, (label, val, col) in enumerate(props):
                y_prop = card.y + int((242 + j*22)*scale)
                screen.blit(pf.render(label, True, (150,150,180)), (card.x + 16, y_prop))
                vt = pf.render(val, True, col)
                screen.blit(vt, (card.right - vt.get_width() - 16, y_prop))
        close_btn = None
        exchange_btn = None
        if ca["timer"] > 25 and card_w > 200:
            close_btn = pygame.Rect(cx - card_w//2 + 16,
                                    card.bottom - int(52*scale),
                                    int((card_w-32) * (0.55 if is_dup else 1.0)),
                                    int(38*scale))
            pygame.draw.rect(screen, (0, 180, 80), close_btn, border_radius=12)
            pygame.draw.rect(screen, (100, 255, 150), close_btn, 2, border_radius=12)
            cf = pygame.font.SysFont("Arial", int(14*scale), bold=True)
            ct = cf.render("ZABRATY", True, (255, 255, 255))
            screen.blit(ct, (close_btn.centerx - ct.get_width()//2, close_btn.centery - ct.get_height()//2))
            if is_dup and refund > 0:
                exchange_btn = pygame.Rect(close_btn.right + 8,
                                           card.bottom - int(52*scale),
                                           card_w - close_btn.width - 40,
                                           int(38*scale))
                pygame.draw.rect(screen, (180, 120, 0), exchange_btn, border_radius=12)
                pygame.draw.rect(screen, (255, 200, 50), exchange_btn, 2, border_radius=12)
                et = cf.render(f"+{refund}", True, (255, 255, 255))
                screen.blit(et, (exchange_btn.centerx - et.get_width()//2, exchange_btn.centery - et.get_height()//2))
        for p in ca["particles"][:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.2
            p["life"] -= 0.015
            if p["life"] <= 0:
                ca["particles"].remove(p)
                continue
            size = int(p["size"] * p["life"])
            if size > 0:
                pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), size)
        return close_btn, exchange_btn
    return None, None


def draw_drop_rates_panel():
    panel = pygame.Rect(WIDTH//2 - 140, HEIGHT//2 - 140, 280, 260)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, (18, 18, 40), panel, border_radius=16)
    pygame.draw.rect(screen, (180, 70, 255), panel, 2, border_radius=16)
    tf = pygame.font.SysFont("Arial", 16, bold=True)
    sf = pygame.font.SysFont("Arial", 13)
    title = tf.render("Shansy vypadinnya", True, (255, 255, 255))
    screen.blit(title, (panel.centerx - title.get_width()//2, panel.y + 14))
    rates = [
        ("Legendary", 5, (255,200,0)),
        ("Epic", 30, (180,70,255)),
        ("Rare", 65, (50,150,255)),
    ]
    bar_x = panel.x + 20
    bar_max_w = 140
    for i, (name, pct, color) in enumerate(rates):
        y = panel.y + 55 + i * 52
        label = sf.render(f"{name}", True, color)
        pct_txt = sf.render(f"{pct}%", True, color)
        screen.blit(label, (bar_x, y))
        screen.blit(pct_txt, (panel.right - 40, y))
        bg_bar = pygame.Rect(bar_x, y + 20, bar_max_w, 10)
        pygame.draw.rect(screen, (30, 30, 50), bg_bar, border_radius=5)
        fill_w = int(bar_max_w * pct / 100)
        pygame.draw.rect(screen, color, pygame.Rect(bar_x, y+20, fill_w, 10), border_radius=5)
    close = pygame.Rect(panel.centerx - 50, panel.bottom - 44, 100, 32)
    pygame.draw.rect(screen, (60, 30, 100), close, border_radius=10)
    pygame.draw.rect(screen, (180, 70, 255), close, 2, border_radius=10)
    ct = sf.render("Zakryty", True, (255, 255, 255))
    screen.blit(ct, (close.centerx - ct.get_width()//2, close.centery - ct.get_height()//2))
    return close


def draw_shop():
    screen.blit(background_shop, (0, 0))
    draw_sky(screen)
    # back_btn
    screen.blit(backs_btn, (-40, -60))
    back_rect = pygame.Rect(-30, -40, backs_btn.get_width(), backs_btn.get_height())
    ########



    # Buttons
    screen.blit(rare_btn, (0, 200))
    rare_btn_rect = pygame.Rect(0, 200, 200, 100)
    #
    screen.blit(epic_btn, (1330, 180))
    epic_btn_rect = pygame.Rect(1330, 180, 200, 100)
    #
    screen.blit(legendary_btn, (350, 100))
    legendary_btn_rect = pygame.Rect(350, 100, 200, 100)

    #
    screen.blit(gold_btn, (980, 80))
    gold_btn_rect = pygame.Rect(980, 80, 200, 100)
    #
    screen.blit(owned_btn, (650, 20))
    owned_btn_rect = pygame.Rect(650, 20, 200, 100)


    # cases
    screen.blit(rare_case, (0, 400))
    rare_case_rect = pygame.Rect(0, 400, 400, 300)
    #
    screen.blit(epic_case, (1330, 380))
    epic_case_rect = pygame.Rect(1330, 380, 400, 300)
    #
    screen.blit(legendary_case, (350, 300))
    legendary_case_rect = pygame.Rect(350, 300, 400, 300)
    #
    screen.blit(gold_case, (980, 280))
    gold_case_rect = pygame.Rect(980, 280, 400, 300)

    # ramku

    screen.blit(ramka2, (WIDTH // 2 - 280, -60))
    font = pygame.font.SysFont("Impact", 30, bold=False)
    txt = font.render(f"Coins: {coins} Gems: {gems}", True, (0, 0, 0))
    screen.blit(txt,
                (WIDTH // 2 - txt.get_width() // 2 + 40, 10 + ramka2.get_height() // 2 - txt.get_height() // 2 - 68))






    # Sculptures
    #1
    screen.blit(sculpture1, (-180, 650))
    font = pygame.font.SysFont("Impact", 30, bold=False)
    screen.blit(ramka3, (45, 575))
    txt = font.render("Price: 250 000", True, (0, 0, 0))
    screen.blit(txt, (120, 10 + ramka3.get_height() // 2 - txt.get_height() // 2 - 60 + 620))






    #2
    screen.blit(sculpture2, (1150, 650))
    font = pygame.font.SysFont("Impact", 30, bold=False)
    screen.blit(ramka3, (1350, 555))
    txt = font.render("Price: 400 000", True, (0, 0, 0))
    screen.blit(txt, (1420, ramka3.get_height() // 2 - txt.get_height() // 2 + 550))




    #3
    screen.blit(sculpture3, (500, 500))
    font = pygame.font.SysFont("Impact", 30, bold=False)
    screen.blit(ramka4, (400, 475))
    txt = font.render("Price: 750 000", True, (0, 0, 0))
    screen.blit(txt, (450, ramka4.get_height() // 2 - txt.get_height() // 2 + 470))





    #4
    screen.blit(sculpture4, (730, 430))
    font = pygame.font.SysFont("Impact", 30, bold=False)
    screen.blit(ramka4, (1010, 460))
    txt = font.render("Price: 1 000 000", True, (0, 0, 0))
    screen.blit(txt, (1050, ramka4.get_height() // 2 - txt.get_height() // 2 + 455))

















    draw_sakura_tree(screen, 80, HEIGHT - 60, size=0.9)
    draw_sakura_tree(screen, WIDTH - 80, HEIGHT - 60, size=0.9)
    draw_sakura_tree(screen, 200, HEIGHT - 60, size=0.6)
    draw_sakura_tree(screen, WIDTH - 200, HEIGHT - 60, size=0.6)
    draw_spring_ground(screen)
    draw_sakura(screen)

    for gx in range(0, WIDTH, 32):
        for gy in range(108, HEIGHT, 32):
            pygame.draw.circle(screen, (25, 25, 40), (gx, gy), 1)

    case_rects_left = []
    boost_rects_left = []
    tab_rects = [
        (rare_btn_rect, "Rare"),
        (epic_btn_rect, "Epic"),
        (legendary_btn_rect, "Legendary"),
        (gold_btn_rect, "Gold"),
        (owned_btn_rect, "Owned"),
    ]
    if SHOP_TAB[0] == "Custom":
        skin_rects = []

        banner = pygame.Rect(0, 0, 1, 1)
        return skin_rects, banner, back_rect, tab_rects, case_rects_left, boost_rects_left
    if SHOP_TAB[0] == "Gems":
        skin_rects = []

        banner = pygame.Rect(0, 0, 1, 1)
        return skin_rects, banner, back_rect, tab_rects, case_rects_left, boost_rects_left

    skin_rects = []
    banner = pygame.Rect(0, 0, 1, 1)



    return skin_rects, banner, tab_rects, back_rect, case_rects_left, boost_rects_left, rare_btn_rect, epic_btn_rect, legendary_btn_rect, gold_btn_rect, owned_btn_rect, rare_case_rect, epic_case_rect, legendary_case_rect, gold_case_rect



def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    panel = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 180, 300, 360)
    pygame.draw.rect(screen, (20, 20, 35), panel, border_radius=20)
    pygame.draw.rect(screen, (80, 80, 140), panel, 2, border_radius=20)
    tf = pygame.font.SysFont("Arial", 28, bold=True)
    title = tf.render("PAUZA", True, (255, 255, 255))
    screen.blit(title, (panel.centerx - title.get_width()//2, panel.y + 24))
    bf = pygame.font.SysFont("Arial", 20, bold=True)
    mouse_pos = pygame.mouse.get_pos()
    buttons = [
        ("Nalashtuvannya", True, (60, 60, 90)),
        ("Pochaty znovu", True, (50, 120, 255)),
        ("Menu", True, (50, 180, 100)),
    ]
    rects = []
    for i, (label, active, color) in enumerate(buttons):
        r = pygame.Rect(panel.x + 30, panel.y + 90 + i * 85, 240, 60)
        if not active:
            pygame.draw.rect(screen, (40, 40, 55), r, border_radius=14)
            pygame.draw.rect(screen, (70, 70, 90), r, 2, border_radius=14)
            txt = bf.render(label, True, (100, 100, 120))
        else:
            hover = r.collidepoint(mouse_pos)
            bg = tuple(min(255, c + 30) for c in color) if hover else color
            pygame.draw.rect(screen, bg, r, border_radius=14)
            pygame.draw.rect(screen, (255, 255, 255), r, 2, border_radius=14)
            txt = bf.render(label, True, (255, 255, 255))
        screen.blit(txt, (r.x + 16, r.centery - txt.get_height()//2))
        rects.append((r, label, active))
    return rects


def reset_game():
    global foods, bots, game_state, winner, start_time
    if hasattr(player, '_win_saved'):
        del player._win_saved
    if hasattr(player, '_lose_saved'):
        del player._lose_saved
    save_data({
        "coins": coins, "gems": gems, "owned_skins": owned_skins,
        "selected_skin": player.skin,
        "custom_player": data.get("custom_player", default_data["custom_player"]),
        **save_settings()
    })
    player.mass = 20
    player.x, player.y = 400, 300
    player.radius = int(player.mass ** 0.5 * 4)
    foods = [Food(WORLD_WIDTH, WORLD_HEIGHT) for _ in range(450)]
    bots = []
    for i in range(80):
        bot = Bot(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
        bot.name = f"Bot_{i}"
        bots.append(bot)
    winner = None
    start_time = 0
    game_state = "menu"





def draw_notification(screen, text, font):
    if text:
        txt = font.render(text, True, (255, 50, 50))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 20))


btn_competition = Button(WIDTH//2 - 150, 250, 300, 60, "Competition")
btn_free = Button(WIDTH//2 - 150, 330, 300, 60, "Free Play")
input_box = InputBox(WIDTH//2 - 150, HEIGHT//2 - 50, 300, 50)

# ============ MAIN LOOP ============
running = True
settings_clicked = False
while running:
    clock.tick(60)
    settings_clicked = False

    # музика
    if audio_toggles["muzyka"]:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(audio_volumes["muzyka"] / 100)
    else:
        pygame.mixer.music.stop()

    screen.fill((255, 255, 255))
    for event in pygame.event.get():

        input_box.handle_event(event)
        nickname_box.handle_event(event)
        password_box.handle_event(event)
        name_box.handle_event(event)
        przv_box.handle_event(event)
        date_box.handle_event(event)
        nickname2_box.handle_event(event)
        password2_box.handle_event(event)
        password3_box.handle_event(event)


        if event.type == pygame.MOUSEWHEEL:
            if game_state == "shop":
                SHOP_SCROLL += event.y * 15
                SHOP_SCROLL += event.x * 5
                SHOP_SCROLL = min(0, SHOP_SCROLL)


            if game_state == "rare":
                RARE_SCROLL += event.y * 20
                RARE_SCROLL = min(0, RARE_SCROLL)



            if game_state == "epic":
                EPIC_SCROLL += event.y * 20
                EPIC_SCROLL = min(0, EPIC_SCROLL)



            if game_state == "legendary":
                LEGENDARY_SCROLL += event.y * 20
                LEGENDARY_SCROLL = min(0, LEGENDARY_SCROLL)




            if game_state == "gold":
                GOLD_SCROLL += event.y * 20
                GOLD_SCROLL = min(0, GOLD_SCROLL)



            if game_state == "owned":
                OWNED_SCROLL += event.y * 20
                OWNED_SCROLL = min(0, OWNED_SCROLL)





        if event.type == pygame.FINGERMOTION:
            if game_state == "shop":
                SHOP_SCROLL += int(event.dy * HEIGHT * 0.3)
                SHOP_SCROLL = min(0, SHOP_SCROLL)

            if game_state == "rare":
                RARE_SCROLL += event.y * 20
                RARE_SCROLL = min(0, RARE_SCROLL)


            if game_state == "epic":
                EPIC_SCROLL += event.y * 20
                EPIC_SCROLL = min(0, EPIC_SCROLL)



            if game_state == "legendary":
                LEGENDARY_SCROLL += event.y * 20
                LEGENDARY_SCROLL = min(0, LEGENDARY_SCROLL)


            if game_state == "gold":
                GOLD_SCROLL += event.y * 20
                GOLD_SCROLL = min(0, GOLD_SCROLL)



        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            settings_clicked = True
            if game_state == "game":
                pause_btn = pygame.Rect(16, 16, 48, 48)
                if pause_btn.collidepoint(event.pos):
                    pause_menu_open = not pause_menu_open
        if event.type == pygame.KEYDOWN and SHOP_TAB[0] == "Custom":
            if event.key == pygame.K_BACKSPACE:
                custom_text[0] = custom_text[0][:-1]
            elif len(custom_text[0]) < 6:
                custom_text[0] += event.unicode

    keys = pygame.key.get_pressed()

    if game_state == "auth":
        rect_log_btn, rect_reg_btn = draw_auth_screen(screen, WIDTH, HEIGHT, image,
                                                                     log_btn, reg_btn)



        if pygame.mouse.get_pressed()[0] and rect_log_btn.collidepoint(pygame.mouse.get_pos()):
            game_state = "login"


        if pygame.mouse.get_pressed()[0] and rect_reg_btn.collidepoint(pygame.mouse.get_pos()):
            game_state = "registration"

        pygame.display.flip()
        continue

    if game_state == "login":
        rect_login_btn, rect_backs_btn = draw_login_screen(screen, WIDTH, HEIGHT, login_bg, nickname_box, password_box, login_btn, backs_btn, ramka1)

        if pygame.mouse.get_pressed()[0] and rect_login_btn.collidepoint(pygame.mouse.get_pos()):
            response = requests.post("http://127.0.0.1:5000/login", json={
                "nickneim": nickname_box.text,
                "klyuch_bezpeky": password_box.text
            })

            result = response.json()
            if result["status"] == "ok":
                game_state = "menu"
            else:
                # показати помилку
                print("Користувача не знайдено!")

        if pygame.mouse.get_pressed()[0] and rect_backs_btn.collidepoint(pygame.mouse.get_pos()):
            game_state = "auth"


        pygame.display.flip()
        continue


    if game_state == "registration":
        rect_login_btn, rect_backs_btn = draw_registration_screen(screen, WIDTH, HEIGHT, reg_bg,
                                                  name_box, przv_box, date_box, nickname2_box, password2_box, password3_box, login_btn, backs_btn, ramka1)



        if pygame.mouse.get_pressed()[0] and rect_login_btn.collidepoint(pygame.mouse.get_pos()):
            response = requests.post("http://127.0.0.1:5000/register", json={
                "imya": name_box.text,
                "prizvyshe": przv_box.text,
                "data_narodzhennya": date_box.text,
                "nickneim": nickname2_box.text,
                "klyuch_bezpeky": password2_box.text
            })

            result = response.json()
            if result["status"] == "ok":
                game_state = "auth"

            else:
                print("Помилка реєстрації!")


        if pygame.mouse.get_pressed()[0] and rect_backs_btn.collidepoint(pygame.mouse.get_pos()):
            game_state = "auth"

        pygame.display.flip()
        continue


    # ===== MENU =====
    if game_state == "menu":
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        Play_btn_rect, Classic_btn_rect, Rush_btn_rect, Settings_btn_rect, Shop_btn_rect = draw_menu(screen, WIDTH, HEIGHT)

        if settings_clicked:


            if Play_btn_rect.collidepoint(mouse_pos):
                start_time = pygame.time.get_ticks()
                game_state = "game"

            if Classic_btn_rect.collidepoint(mouse_pos):
                game_mode = "free"

            if Rush_btn_rect.collidepoint(mouse_pos):
                game_mode = "competition"


            if Settings_btn_rect.collidepoint(mouse_pos):
                game_state = "settings"


            if Shop_btn_rect.collidepoint(mouse_pos):
                game_state = "shop"


        pygame.display.flip()
        continue


    ######### ====== RARE SCREEN =======

    if game_state == "rare":
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        back_rect, skin_rects = draw_rare_screen(screen, WIDTH, HEIGHT, backs_btn, background_shop, rare_boost1, rare_boost2, rare_boost3, skins, loaded_skins, owned_skins, player, rarity_colors, coins, gems, ramka2, ramka3, RARE_SCROLL)

        if settings_clicked:
            if back_rect.collidepoint(mouse_pos):
                game_state = "shop"

            for text_rect, name in skin_rects:
                if text_rect.collidepoint(mouse_pos):
                    if name in owned_skins:
                       player.skin = name
                    else:
                        if coins >= skins[name]["price"]:
                            coins -= skins[name]["price"]
                            owned_skins.append(name)
                        else:
                            notification_text = "Не вистачає монет!!!"
                            notification_timer = pygame.time.get_ticks() + 2000



        if notification_text and pygame.time.get_ticks() < notification_timer:
            txt = font.render(notification_text, True, (255, 50, 50))
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 20))


        else:
            notification_text = ""








        pygame.display.flip()
        continue


    ############ ====== EPIC SCREEN =======
    if game_state == "epic":
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        back_rect, skin_rects = draw_epic_screen(screen, WIDTH, HEIGHT, backs_btn, background_shop, epic_boost1, epic_boost2, epic_boost3, skins, loaded_skins, owned_skins, player, rarity_colors, coins, gems, ramka2, ramka3, EPIC_SCROLL)
        if settings_clicked:
            if back_rect.collidepoint(mouse_pos):
                game_state = "shop"


            for text_rect, name in skin_rects:
                if text_rect.collidepoint(mouse_pos):
                    if name in owned_skins:
                        player.skin = name
                    else:
                        if coins >= skins[name]["price"]:
                            coins -= skins[name]["price"]
                            owned_skins.append(name)




        pygame.display.flip()
        continue



    ########### ========== LEGENDARY SCREEN ==============
    if game_state == "legendary":
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        back_rect, skin_rects = draw_legendary_screen(screen, WIDTH, HEIGHT, backs_btn, background_shop, legendary_boost1, legendary_boost2, legendary_boost3, skins, loaded_skins, owned_skins, player, rarity_colors, coins, gems, ramka2, ramka4, LEGENDARY_SCROLL)
        if settings_clicked:
            if back_rect.collidepoint(mouse_pos):
                game_state = "shop"



            for text_rect, name in skin_rects:
                if text_rect.collidepoint(mouse_pos):
                    if name in owned_skins:
                        player.skin = name
                    else:
                        if coins >= skins[name]["price"]:
                            coins -= skins[name]["price"]
                            owned_skins.append(name)




        pygame.display.flip()
        continue


    ########### ======= GOLD SCREEN =====================

    if game_state == "gold":
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        back_rect, skin_rects = draw_gold_screen(screen, WIDTH, HEIGHT, backs_btn, background_shop, gold_boost1, gold_boost2, gold_boost3, skins, loaded_skins, owned_skins, player, rarity_colors, coins, gems, ramka2, ramka4, GOLD_SCROLL)
        if settings_clicked:
            if back_rect.collidepoint(mouse_pos):
                game_state = "shop"


            for text_rect, name in skin_rects:
                if text_rect.collidepoint(mouse_pos):
                    if name in owned_skins:
                        player.skin = name

                    else:
                        if gems >= skins[name]["gem_price"]:
                            gems -= skins[name]["gem_price"]
                            owned_skins.append(name)



        pygame.display.flip()
        continue

    ############ ========= OWNED SCREEN =======================

    if game_state == "owned":
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        back_rect, skin_rects = draw_owned_screen(screen, WIDTH, HEIGHT, backs_btn, background_shop, skins, loaded_skins, owned_skins, player, rarity_colors, coins, gems, ramka2, OWNED_SCROLL)

        if settings_clicked:
            if back_rect.collidepoint(mouse_pos):
                game_state = "shop"


            for text_rect, name in skin_rects:
                if text_rect.collidepoint(mouse_pos):
                    if name in owned_skins:
                        player.skin = name












        pygame.display.flip()
        continue












    # ===== SHOP =====
    if game_state == "shop":
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        skin_rects, case_button, tab_rects, back_rect, case_rects_left, boost_rects_left, rare_btn_rect, epic_btn_rect, legendary_btn_rect, gold_btn_rect, owned_btn_rect, rare_case_rect, epic_case_rect, legendary_case_rect, gold_case_rect = draw_shop()
        info_btn = pygame.Rect(WIDTH - 145, 115, 125, 36)
        hover = info_btn.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (40, 20, 80) if hover else (25, 12, 50), info_btn, border_radius=10)
        pygame.draw.rect(screen, (180, 70, 255), info_btn, 2, border_radius=10)
        ib = pygame.font.SysFont("Arial", 14, bold=True).render("i  Shansy", True, (200, 150, 255))
        screen.blit(ib, (info_btn.centerx - ib.get_width() // 2, info_btn.centery - ib.get_height() // 2))
        if info_btn.collidepoint(mouse_pos) and mouse_click:
            show_drop_rates[0] = not show_drop_rates[0]
        if show_drop_rates[0]:
            close_rates = draw_drop_rates_panel()
            if mouse_click and close_rates.collidepoint(mouse_pos):
                show_drop_rates[0] = False
        if chest_anim["active"]:
            close_btn, exchange_btn = draw_chest_animation_3d(screen, chest_anim, skins, loaded_skins, rarity_colors, WIDTH, HEIGHT, font)
            if close_btn and mouse_click and close_btn.collidepoint(mouse_pos):
                chest_anim["active"] = False
                chest_anim["phase"] = 0
                chest_anim["timer"] = 0
                chest_anim["angle"] = 0
                chest_anim["lid_offset"] = 0
                chest_anim["particles"] = []
                show_drop_rates[0] = False
            if exchange_btn and mouse_click and exchange_btn.collidepoint(mouse_pos):
                skin_name = chest_anim["result_skin"]
                if skin_name:
                    refund = skins[skin_name]["price"] // 2
                    coins += refund
                    save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                               "selected_skin": player.skin,
                               "custom_player": data.get("custom_player", default_data["custom_player"]),
                               **save_settings()})
                    chest_anim["active"] = False
                    chest_anim["phase"] = 0
                    chest_anim["timer"] = 0
                    chest_anim["lid_offset"] = 0
                    chest_anim["particles"] = []
                    show_drop_rates[0] = False
            pygame.display.flip()
            continue
        for btn, name, price, info_i_btn in case_rects_left:
            if info_i_btn.collidepoint(mouse_pos) and mouse_click:
                show_drop_rates[0] = not show_drop_rates[0]
            if btn.collidepoint(mouse_pos) and mouse_click:
                if coins >= price:
                    coins -= price
                    new_skin = open_case()
                    is_dup = new_skin in owned_skins
                    if new_skin not in owned_skins:
                        owned_skins.append(new_skin)
                    chest_anim["active"] = True
                    chest_anim["phase"] = 0
                    chest_anim["timer"] = 0
                    chest_anim["angle"] = 0
                    chest_anim["lid_offset"] = 0
                    chest_anim["particles"] = []
                    chest_anim["result_skin"] = new_skin
                    chest_anim["is_duplicate"] = is_dup
                    save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                               "selected_skin": player.skin,
                               "custom_player": data.get("custom_player", default_data["custom_player"]),
                               **save_settings()})
                else:
                    print("Nedostatno monetiv!")
        for btn, name, price in boost_rects_left:
            if btn.collidepoint(mouse_pos) and mouse_click:
                if coins >= price:
                    coins -= price
                    save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                               "selected_skin": player.skin,
                               "custom_player": data.get("custom_player", default_data["custom_player"]),
                               **save_settings()})
                    if name == "Mass Boost x2":
                        player.mass *= 2
                    elif name == "Speed Boost":
                        player.base_speed *= 1.5
                else:
                    print("Nedostatno monetiv!")

        if settings_clicked:
            if rare_btn_rect.collidepoint(mouse_pos):
                game_state = "rare"

            if epic_btn_rect.collidepoint(mouse_pos):
                game_state = "epic"
            if legendary_btn_rect.collidepoint(mouse_pos):
                game_state = "legendary"
            if gold_btn_rect.collidepoint(mouse_pos):
                game_state = "gold"
            if owned_btn_rect.collidepoint(mouse_pos):
                game_state = "owned"



        if settings_clicked:
            if rare_case_rect.collidepoint(mouse_pos):
                new_skin = open_case()
                is_dup = new_skin in owned_skins
                if new_skin not in owned_skins:
                    owned_skins.append(new_skin)
                chest_anim["active"] = True
                chest_anim["phase"] = 0
                chest_anim["timer"] = 0
                chest_anim["angle"] = 0
                chest_anim["lid_offset"] = 0
                chest_anim["particles"] = []
                chest_anim["result_skin"] = new_skin
                chest_anim["is_duplicate"] = is_dup

            if epic_case_rect.collidepoint(mouse_pos):
                new_skin = open_case()
                is_dup = new_skin in owned_skins
                if new_skin not in owned_skins:
                    owned_skins.append(new_skin)
                chest_anim["active"] = True
                chest_anim["phase"] = 0
                chest_anim["timer"] = 0
                chest_anim["angle"] = 0
                chest_anim["lid_offset"] = 0
                chest_anim["particles"] = []
                chest_anim["result_skin"] = new_skin
                chest_anim["is_duplicate"] = is_dup



            if legendary_case_rect.collidepoint(mouse_pos):
                new_skin = open_case()
                is_dup = new_skin in owned_skins
                if new_skin not in owned_skins:
                    owned_skins.append(new_skin)
                chest_anim["active"] = True
                chest_anim["phase"] = 0
                chest_anim["timer"] = 0
                chest_anim["angle"] = 0
                chest_anim["lid_offset"] = 0
                chest_anim["particles"] = []
                chest_anim["result_skin"] = new_skin
                chest_anim["is_duplicate"] = is_dup




            if gold_case_rect.collidepoint(mouse_pos):
                new_skin = open_case()
                is_dup = new_skin in owned_skins
                if new_skin not in owned_skins:
                    owned_skins.append(new_skin)
                chest_anim["active"] = True
                chest_anim["phase"] = 0
                chest_anim["timer"] = 0
                chest_anim["angle"] = 0
                chest_anim["lid_offset"] = 0
                chest_anim["particles"] = []
                chest_anim["result_skin"] = new_skin
                chest_anim["is_duplicate"] = is_dup









        if SHOP_TAB[0] == "Custom":
            slider_rects, text_box, save_btn, eye_btn, border_btn = draw_create_tab()
            if pygame.mouse.get_pressed()[0]:
                for i, sr in enumerate(slider_rects):
                    if sr.collidepoint(mouse_pos) or active_slider[0] == i:
                        active_slider[0] = i
                        rel_x = mouse_pos[0] - sr.x
                        custom_color[i] = max(0, min(255, int(rel_x / sr.w * 255)))
                        player.custom_color = list(custom_color)
            else:
                active_slider[0] = None
            if eye_btn.collidepoint(mouse_pos) and mouse_click:
                player.eye_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            if border_btn.collidepoint(mouse_pos) and mouse_click:
                player.border_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            if save_btn.collidepoint(mouse_pos) and mouse_click:
                player.custom_color = list(custom_color)
                player.skin = "custom"
                if "custom_player" not in data:
                    data["custom_player"] = {"color": [0, 255, 120], "eye_color": [255, 255, 255], "border_color": [0, 0, 0]}
                data["custom_player"]["color"] = list(custom_color)
                data["custom_player"]["eye_color"] = list(player.eye_color)
                data["custom_player"]["border_color"] = list(player.border_color)
                save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                           "selected_skin": "custom", "custom_player": data["custom_player"], **save_settings()})
                if "custom" not in owned_skins:
                    owned_skins.append("custom")
            pygame.display.flip()
            continue
        if SHOP_TAB[0] == "Gems":
            update_gem_case_anim()
            gem_case_rects, gem_skin_rects, gems_back_btn = draw_gems_tab()
            if gems_back_btn.collidepoint(mouse_pos) and mouse_click:
                SHOP_TAB[0] = "Rare"
            for btn, name, price, idx in gem_case_rects:
                if btn.collidepoint(mouse_pos) and mouse_click:
                    if not gem_case_anim["active"]:
                        if gems >= price:
                            gems -= price
                            new_skin = open_case()
                            gem_case_anim["is_duplicate"] = new_skin in owned_skins
                            if new_skin not in owned_skins:
                                owned_skins.append(new_skin)
                            gem_case_anim["active"] = True
                            gem_case_anim["phase"] = 0
                            gem_case_anim["timer"] = 0
                            gem_case_anim["angle_x"] = 0
                            gem_case_anim["angle_y"] = 0
                            gem_case_anim["case_index"] = idx
                            gem_case_anim["result_skin"] = new_skin
                            save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                                       "selected_skin": player.skin,
                                       "custom_player": data.get("custom_player", default_data["custom_player"]),
                                       **save_settings()})
                        else:
                            print("Nedostatno gemiv!")
            if gem_case_anim["active"] and gem_case_anim["phase"] == 1:
                chest_anim["active"] = True
                chest_anim["phase"] = 1
                chest_anim["result_skin"] = gem_case_anim["result_skin"]
                chest_anim["is_duplicate"] = gem_case_anim["is_duplicate"]
                gem_case_anim["active"] = False
            if chest_anim["active"]:
                close_btn, exchange_btn = draw_chest_animation()
                if close_btn and mouse_click and close_btn.collidepoint(mouse_pos):
                    chest_anim["active"] = False
                    chest_anim["phase"] = 0
                    chest_anim["timer"] = 0
                    chest_anim["lid_offset"] = 0
                    chest_anim["particles"] = []
                if exchange_btn and mouse_click and exchange_btn.collidepoint(mouse_pos):
                    skin_name = case_animation["result_skin"]
                    if skin_name:
                        refund = skins[skin_name]["price"] // 2
                        coins += refund
                        save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                                   "selected_skin": player.skin,
                                   "custom_player": data.get("custom_player", default_data["custom_player"]),
                                   **save_settings()})
                    chest_anim["active"] = False
                    chest_anim["phase"] = 0
                    chest_anim["timer"] = 0
                    chest_anim["lid_offset"] = 0
                    chest_anim["particles"] = []
            for btn, name in gem_skin_rects:
                if btn.collidepoint(mouse_pos) and mouse_click:
                    gem_price = skins[name].get("gem_price", 0)
                    if name not in owned_skins:
                        if gems >= gem_price:
                            gems -= gem_price
                            owned_skins.append(name)
                            save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                                       "selected_skin": player.skin,
                                       "custom_player": data.get("custom_player", default_data["custom_player"]),
                                       **save_settings()})
                    else:
                        player.skin = name
            pygame.display.flip()
            continue
        if back_rect.collidepoint(mouse_pos) and mouse_click:
            game_state = "menu"
        for rect, name in skin_rects:
            if rect.collidepoint(mouse_pos) and mouse_click:
                price = skins[name]["price"]
                if name not in owned_skins:
                    if coins >= price:
                        coins -= price
                        owned_skins.append(name)
                else:
                    player.skin = name
        if case_button.collidepoint(mouse_pos) and mouse_click:
            new_skin = open_case()
            if new_skin not in owned_skins:
                owned_skins.append(new_skin)
        if keys[pygame.K_ESCAPE]:
            game_state = "menu"
        pygame.display.flip()
        continue

    # ===== SETTINGS =====
    if game_state == "settings":
        mouse_pos = pygame.mouse.get_pos()


        (tab_rects, back_rect, cx, cy, cw, ch,
         audio_toggle_rects, audio_slider_rects,
         privacy_toggle_rects,
         quality_toggle_rects, quality_btn_rects,
         achievements_reset_btn) = draw_settings(screen, WIDTH, HEIGHT)




        if settings_clicked:
            for rect, key in audio_toggle_rects:
                if rect.collidepoint(mouse_pos):
                    audio_toggles[key] = not audio_toggles[key]



            for rect, key in privacy_toggle_rects:
                if rect.collidepoint(mouse_pos):
                    privacy_toggles[key] = not privacy_toggles[key]




            for rect, key in quality_toggle_rects:
                if rect.collidepoint(mouse_pos):
                    quality_toggles[key] = not quality_toggles[key]

            for rect, key, idx in quality_btn_rects:
                if rect.collidepoint(mouse_pos):
                    quality_selected[key] = idx


            for r, tab_id in tab_rects:
                if r.collidepoint(mouse_pos):
                    SETTINGS_TAB[0] = tab_id




            if back_rect.collidepoint(mouse_pos):
                game_state = "menu"


            if achievements_reset_btn and achievements_reset_btn.collidepoint(mouse_pos):
                kills_stats["total"] = 0
                kills_stats["rare"] = 0
                kills_stats["epic"] = 0
                kills_stats["legendary"] = 0
                kills_stats["gold"] = 0






        # слайдери - окремо бо треба тримати мишку


        if pygame.mouse.get_pressed()[0]:
            for rect, key, bar_x, bar_w in audio_slider_rects:
                if rect.collidepoint(mouse_pos):
                    rel_x = mouse_pos[0] - bar_x
                    audio_volumes[key] = max(0, min(100, int(rel_x / bar_w * 100)))


        pygame.display.flip()
        continue










    # ===== PAUSE =====
    if pause_menu_open:
        draw_grid(screen, camera.x, camera.y)
        for food in foods:
            food.draw(screen, camera.x, camera.y)
        player.draw(screen)
        pause_rects = draw_pause_menu()
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            for r, label, active in pause_rects:
                if active and r.collidepoint(mouse_pos):
                    if "Nalashtuvannya" in label:
                        pause_menu_open = False
                        game_state = "settings"
                    if "znovu" in label:
                        pause_menu_open = False
                        coins += int(player.mass * 0.5)
                        save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                                   "selected_skin": player.skin,
                                   "custom_player": data.get("custom_player", default_data["custom_player"]),
                                   **save_settings()})
                        reset_game()
                    elif "Menu" in label:
                        pause_menu_open = False
                        coins += int(player.mass * 0.5)
                        save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                                   "selected_skin": player.skin,
                                   "custom_player": data.get("custom_player", default_data["custom_player"]),
                                   **save_settings()})
                        game_state = "menu"
        pygame.display.flip()
        continue

    # ===== GAME =====
    draw_sky(screen)
    player.movement(keys)
    player.update()
    camera.update(player)

    if player.mass > 30:
        player.mass -= 0.01

    for food in foods[:]:
        dist = math.hypot(player.x - food.x, player.y - food.y)
        if dist < player.radius:
            player.mass += 1
            foods.remove(food)
            foods.append(Food(WORLD_WIDTH, WORLD_HEIGHT))

    for bot in bots:
        bot.ai_move(foods, bots)
        bot.update()
        if bot.mass > 30:
            bot.mass -= 0.008

    for bot in bots:
        for food in foods[:]:
            dist = math.hypot(bot.x - food.x, bot.y - food.y)
            if dist < bot.radius:
                bot.mass += 1
                foods.remove(food)
                foods.append(Food(WORLD_WIDTH, WORLD_HEIGHT))

    for i, bot_a in enumerate(bots):
        if bot_a not in bots:
            continue
        for bot_b in bots[i + 1:]:
            if bot_b not in bots:
                continue
            dist = math.hypot(bot_a.x - bot_b.x, bot_a.y - bot_b.y)
            if dist >= (bot_a.radius + bot_b.radius) * 0.55:
                continue
            if bot_a.mass > bot_b.mass * 1.03:
                bot_a.mass += int(bot_b.mass * 0.8)
                bot_a.radius = int(bot_a.mass ** 0.5 * 4)
                bots.remove(bot_b)
                new_bot = Bot(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
                new_bot.name = bot_b.name
                bots.append(new_bot)
                continue
            if bot_b.mass > bot_a.mass * 1.03:
                bot_b.mass += int(bot_a.mass * 0.8)
                bot_b.radius = int(bot_b.mass ** 0.5 * 4)
                bots.remove(bot_a)
                new_bot = Bot(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
                new_bot.name = bot_a.name
                bots.append(new_bot)
                break

    for bot in bots[:]:
        dist = math.hypot(bot.x - player.x, bot.y - player.y)
        if dist < bot.radius and bot.mass > player.mass * 1.1:
            bot.mass += player.mass
            game_state = "lose"
            break
        if dist < player.radius and player.mass > bot.mass * 1.1:
            player.mass += int(bot.mass * 0.8)
            gems += 1
            bot_rarity = skins.get(bot.skin, {}).get("rarity", "none")
            xp_reward = RARITY_XP.get(bot_rarity, 10)
            xp += xp_reward
            # оновлюємо статистику
            kills_stats["total"] += 1
            if bot_rarity == "rare":
                kills_stats["rare"] += 1
            elif bot_rarity == "epic":
                kills_stats["epic"] += 1
            elif bot_rarity == "legendary":
                kills_stats["legendary"] += 1
            elif bot_rarity == "gold":
                kills_stats["gold"] += 1


            achievements_check = [
                (kills_stats["total"] == 1, 50),
                (kills_stats["rare"] == 10, 200),
                (kills_stats["epic"] == 5, 350),
                (kills_stats["legendary"] == 1, 500),
                (kills_stats["gold"] == 1, 750),
                (kills_stats["total"] == 50, 1000),
                (kills_stats["total"] == 100, 2000),
                (kills_stats["total"] == 200, 5000),
                (kills_stats["rare"] == 50, 1500),
                (kills_stats["epic"] == 20, 2500),
                (kills_stats["gold"] == 5, 3000),
                (kills_stats["legendary"] == 5, 4000),
            ]
            for condition, reward in achievements_check:
                if condition:
                    coins += reward




            if xp >= level * 100:
                xp -= level * 100
                level += 1
                for b in bots:
                    b.mass *= 1 + level * 0.1
                    b.base_speed *= 1 + level * 0.05
                    b.radius = int(b.mass ** 0.5 * 4)
            bots.remove(bot)
            new_bot = Bot(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
            new_bot.name = bot.name
            bots.append(new_bot)

    draw_grid(screen, camera.x, camera.y)

    pause_btn = pygame.Rect(16, 16, 48, 48)
    color_pb = (60, 60, 90) if not pause_btn.collidepoint(pygame.mouse.get_pos()) else (90, 90, 130)
    pygame.draw.rect(screen, color_pb, pause_btn, border_radius=10)
    pf = pygame.font.SysFont("Arial", 22, bold=True)
    pt = pf.render("=", True, (255, 255, 255))
    screen.blit(pt, (pause_btn.x + 10, pause_btn.y + 10))

    for food in foods:
        if (abs(food.x - camera.x - WIDTH//2) > WIDTH//2 + 20 or
                abs(food.y - camera.y - HEIGHT//2) > HEIGHT//2 + 20):
            continue
        food.draw(screen, camera.x, camera.y)

    for bot in bots:
        if (abs(bot.x - player.x) > WIDTH // 2 + 100 or
                abs(bot.y - player.y) > HEIGHT // 2 + 100):
            continue
        if quality_toggles["radar"]:
            screen.blit(radar_surf, (int(bot.x - camera.x - VISION_R),
                                     int(bot.y - camera.y - VISION_R)))


        skin_img = loaded_skins[bot.skin]
        size = int(bot.radius) * 2
        if size > 0:
            scaled = pygame.transform.smoothscale(skin_img, (size, size))
            mask = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255, 255), (bot.radius, bot.radius), bot.radius)
            scaled.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            sx = int(bot.x - camera.x)
            sy = int(bot.y - camera.y)
            if quality_toggles["tini"]:
                pygame.draw.circle(screen, (0, 0, 0), (sx, sy), int(bot.radius) + 3)


            screen.blit(scaled, (sx - bot.radius, sy - bot.radius))
        shadow_text = font.render(str(int(bot.mass)), True, (0, 0, 0))
        screen.blit(shadow_text,
                    (int(bot.x - camera.x - shadow_text.get_width() // 2) + 2,
                     int(bot.y - camera.y - int(bot.radius) - 22) + 2))
        bot_mass_text = font.render(str(int(bot.mass)), True, (255, 255, 255))
        screen.blit(bot_mass_text,
                    (int(bot.x - camera.x - bot_mass_text.get_width() // 2),
                     int(bot.y - camera.y - int(bot.radius) - 22)))

    player.draw(screen)
    name_text = font.render(player.name, True, (0, 0, 0))
    screen.blit(name_text, (player.x - camera.x - 20, player.y - camera.y - player.radius - 20))

    if game_mode == "competition":
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        time_left = max(0, int(GAME_DURATION - elapsed_time))
        if player.mass >= TARGET_MASS:
            game_state = "win"
            winner = 'PLAYER'
        for bot in bots:
            if bot.mass >= TARGET_MASS:
                game_state = "win"
                winner = "BOT"
        if time_left <= 0:
            biggest_bot = max(bots, key=lambda b: b.mass)
            winner = "PLAYER" if player.mass > biggest_bot.mass else "BOT"
            game_state = "win"

    if game_state == "win":
        if not hasattr(player, "_win_saved"):
            reward = int(player.mass * 0.3)
            if winner == "PLAYER":
                reward += 100
            coins += reward
            xp += int(player.mass * 2)
            if xp >= level * 100:
                xp -= level * 100
                level += 1
            save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                       "selected_skin": player.skin,
                       "custom_player": data.get("custom_player", default_data["custom_player"]), **save_settings()})
            player._win_saved = True
        draw_win()
        reward_text = font.render(f"+{int(player.mass * 0.3)} coins", True, (255, 215, 0))
        screen.blit(reward_text, (WIDTH//2 - 80, HEIGHT//2))
        if keys[pygame.K_r]:
            reset_game()
        pygame.display.flip()
        continue

    if game_state == "lose":
        if not hasattr(player, '_lose_saved'):
            reward = int(player.mass * 1)
            coins += reward
            xp += int(player.mass * 2)
            if xp >= level * 100:
                xp -= level * 100
                level += 1
            save_data({"coins": coins, "gems": gems, "owned_skins": owned_skins,
                       "selected_skin": player.skin,
                       "custom_player": data.get("custom_player", default_data["custom_player"]), **save_settings()})
            player._lose_saved = True
        draw_lose()
        reward_text = font.render(f"+{int(player.mass * 1)} coins", True, (255, 215, 0))
        screen.blit(reward_text, (WIDTH//2 - 80, HEIGHT//2))
        if keys[pygame.K_r]:
            reset_game()
        pygame.display.flip()
        continue

    draw_leaderboard()
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]




    if game_mode == "competition":
        timer_text = font.render(f"Time: {time_left}", True, (30, 30, 30))
        screen.blit(timer_text, (10, 40))

    fps = int(clock.get_fps())
    draw_shadow_text(screen, f"FPS: {fps}", font, (255, 255, 0), 10, 10)
    draw_shadow_text(screen, f"Mass: {int(player.mass)}", font, (255, 255, 255), 160, 10)
    draw_shadow_text(screen, f"Level: {level}", font, (100, 200, 255), 360, 10)
    draw_shadow_text(screen, f"Gems: {gems}", font, (0, 255, 220), 510, 10)

    bar_w = 200
    bar_x = WIDTH // 2 - bar_w // 2
    bar_y = 14
    pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_w, 16), border_radius=8)
    fill = int(bar_w * (xp / (level * 100)))
    pygame.draw.rect(screen, (100, 200, 255), (bar_x, bar_y, fill, 16), border_radius=8)
    pygame.draw.rect(screen, (150, 150, 255), (bar_x, bar_y, bar_w, 16), 2, border_radius=8)
    draw_shadow_text(screen, f"Lv. {level}", font, (255, 255, 255), bar_x - 55, bar_y - 4)
    draw_shadow_text(screen, f"{xp}/{level * 100} XP", font, (150, 220, 255), bar_x + bar_w + 8, bar_y - 4)

    pygame.display.flip()

save_data({
    "coins": coins, "gems": gems, "owned_skins": owned_skins,
    "selected_skin": player.skin,
    "custom_player": data.get("custom_player", default_data["custom_player"]),
    **save_settings()
})

pygame.quit()