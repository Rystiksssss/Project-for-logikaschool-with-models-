import pygame
import math
import random


from settings_audio import draw_settings_audio
from settings_privacy import draw_settings_privacy
from settings_account import draw_settings_account
from settings_bind import draw_settings_bind
from settings_quality import draw_settings_quality
from settings_achievements import draw_settings_achievements
from settings_rules import draw_settings_rules



SETTINGS_TAB = ["achievements"]


# матричний дощ
_matrix_drops = []




def _init_matrix(WIDTH, HEIGHT):
    global _matrix_drops
    if not _matrix_drops:
        chars = "アイウエオカキクケコ01001101"
        for _ in range(20):
            _matrix_drops.append({
                "x": random.randint(0, WIDTH),
                "y": random.randint(-HEIGHT, 0),
                "speed": random.uniform(0.5, 2.0),
                "char": random.choice(chars),
                "timer": 0,
                "size": random.randint(9, 13),
                "alpha": random.randint(60, 150),


            })




def _draw_matrix(screen, WIDTH, HEIGHT):
    chars = "アイウエオカキクケコ01001101"
    for d in _matrix_drops:
        d["y"] += d["speed"]
        d["timer"] += 1
        if d["timer"] % 30 == 0:
            d["char"] = random.choice(chars)

        if d["y"] > HEIGHT + 20:
            d["y"] = random.randint(-100, -10)
            d["x"] = random.randint(0, WIDTH)
        surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        f = pygame.font.SysFont("Arial", d["size"])
        t = f.render(d["char"], True, (59, 7, 100, d["alpha"]))
        screen.blit(t, (int(d["x"]), int(d["y"])))







# машини
_cars = []


def _init_cars(WIDTH, HEIGHT):
    global _cars
    if not _cars:
        for _ in range(4):
            _cars.append({
                "x": random.uniform(0, WIDTH),
                "y": random.uniform(60, HEIGHT // 2),
                "speed": random.uniform(0.4, 1.8),
                "size": random.uniform(0.55, 0.95),
                "offset": random.uniform(0, 6.28),
            })






def _draw_cars(screen):
    t = pygame.time.get_ticks() * 0.001
    for car in _cars:
        x = int(car["x"])
        y = int(car["y"] + math.sin(t + car["offset"]) * 6)
        s = car["size"]
        w = int(60 * s)
        h = int(20 * s)
        # тінь
        pygame.draw.rect(screen, (10, 0, 20),
                         (x - w//2 + 4, y + 4, w, h), border_radius=4)



        # корпус
        pygame.draw.rect(screen, (26, 0, 48),
                         (x - w//2, y, w, h), border_radius=4)
        pygame.draw.rect(screen, (109, 40, 217),
                         (x - w//2, y, w, h), 1, border_radius=4)



        # кабіна
        pygame.draw.rect(screen, (45, 0, 80),
                         (x - int(w*0.3), y - int(h*0.8),
                          int(w*0.6), int(h*0.9)), border_radius=3)

        pygame.draw.rect(screen, (91, 33, 182),
                         (x - int(w*0.3), y - int(h*0.8),
                          int(w*0.6), int(h*0.9)), 1, border_radius=3)



        # колеса
        pygame.draw.circle(screen, (196, 181, 253),
                           (x - w//2 + int(8*s), y + int(10*s)), int(5*s))
        pygame.draw.circle(screen, (196, 181, 253),
                           (x + w//2 - int(8*s), y + int(10*s)), int(5*s))
        # крила
        pygame.draw.line(screen, (124, 58, 237),
                         (x - w//2, y + int(5*s)),
                         (x - w//2 - int(20*s), y - int(10*s)), 2)

        pygame.draw.line(screen, (124, 58, 237),
                         (x + w//2, y + int(5*s)),
                         (x + w//2 + int(20*s), y - int(10*s)), 2)



        car["x"] -= car["speed"]
        if car["x"] < -120:
            car["x"] = float(pygame.display.get_surface().get_width() + 120)



def _draw_palm(screen, x, HEIGHT, flip=False):
    t = pygame.time.get_ticks() * 0.001


    # стовбур
    tx = x + (30 if not flip else -30)
    trunk_points = []
    for i in range(HEIGHT):
        sway = math.sin(t * 0.5 + i * 0.01) * (i * 0.02)
        if flip:
            sway = -sway

        trunk_points.append((int(tx + sway), HEIGHT - i))




    for i in range(len(trunk_points) - 1):
        thickness = max(2, int(18 * (1 - i / HEIGHT)))
        color_val = int(20 + 30 * (i / HEIGHT))
        pygame.draw.line(screen, (color_val, 0, color_val * 2),
                         trunk_points[i], trunk_points[i + 1], thickness)




    # листя
    top_x = int(tx + math.sin(t * 0.5) * 10)
    top_y = int(HEIGHT * 0.15)



    leaf_colors = [
        (59, 7, 100), (76, 29, 149), (91, 33, 182),
        (109, 40, 217), (124, 58, 237), (139, 70, 255),
    ]


    leaves = [
        (-60, -120, 0),
        (-100, -80, -20),
        (-8, -150, 15),
        (60, -120, 0),
        (100, -80, 20),
        (80, -150, -15),
        (0, -160, 0),
        (-40, -170, 10),
        (40, -170, -10),

    ]



    for j, (lx, ly, angle_offset) in enumerate(leaves):
        if flip:
            lx = -lx
        wave = math.sin(t * 0.8 + j * 0.5) * 15
        end_x = top_x + lx + int(wave)
        end_y = top_y + ly
        color = leaf_colors[j % len(leaf_colors)]


        # малюємо листок як товсту лінію з декількох ліній
        for k in range(4):
            offset = k * 3
            pygame.draw.line(screen, color,
                             (top_x, top_y),
                             (end_x + offset, end_y + offset),
                             max(1, 5 - k))









def _draw_sun(screen, WIDTH):
    t = pygame.time.get_ticks() * 0.001
    sun_x = WIDTH // 2
    sun_y = 120



    # промінчики що крутяться і пульсують
    num_rays = 16
    for i in range(num_rays):
        angle = math.radians(i * (360 / num_rays) + t * 20)


        # довжина промінчика пульсує
        ray_len = int(40 + abs(math.sin(t + 2 + i * 0.3)) * 30)


        x1 = sun_x + int(math.cos(angle) * 38)
        y1 = sun_y + int(math.sin(angle) * 38)
        x2 = sun_x + int(math.cos(angle) * (38 + ray_len))
        y2 = sun_y + int(math.sin(angle) * (38 + ray_len))




        # колір промінчика теж пульсує
        brightness = int(100 + abs(math.sin(t + i * 0.2)) * 100)
        pygame.draw.line(screen, (brightness // 2, 0 , brightness),
                         (x1, y1), (x2, y2), 2)




    # тонші промінчики між основними
    for i in range(num_rays):
        angle = math.radians(i * (360 / num_rays) + 360 / num_rays / 2 + t * 20)
        ray_len = int(20 + abs(math.sin(t * 1.5 + i * 0.4)) * 20)
        x1 = sun_x + int(math.cos(angle) * 38)
        y1 = sun_y + int(math.sin(angle) * 38)
        x2 = sun_x + int(math.cos(angle) * (38 + ray_len))
        y2 = sun_y + int(math.sin(angle) * (38 + ray_len))


        pygame.draw.line(screen, (80, 0, 160), (x1, y1), (x2, y2), 1)


    # ореол навколо сонця
    glow_r = int(44 + math.sin(t * 2) * 6)
    glow_surf = pygame.Surface((glow_r * 4, glow_r * 4), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (109, 40, 217, 40),
                       (glow_r * 2, glow_r * 2), glow_r * 2)
    screen.blit(glow_surf, (sun_x - glow_r * 2, sun_y - glow_r * 2))

    # саме сонце
    pygame.draw.circle(screen, (20, 0, 40), (sun_x, sun_y), 36)
    pygame.draw.circle(screen, (124, 58, 237), (sun_x, sun_y), 36, 2)
    pygame.draw.circle(screen, (76, 29, 149), (sun_x, sun_y), 28)
    pygame.draw.circle(screen, (109, 40, 217), (sun_x, sun_y), 20)
    pygame.draw.circle(screen, (167, 139, 250), (sun_x, sun_y), 10)



    # саме сонце




    pygame.draw.circle(screen, (20, 0, 40), (sun_x, sun_y), 36)
    pygame.draw.circle(screen, (124, 58, 237), (sun_x, sun_y), 36, 2)
    pygame.draw.circle(screen, (76, 29, 149), (sun_x, sun_y), 28)
    pygame.draw.circle(screen, (109, 40, 217), (sun_x, sun_y), 20)
    pygame.draw.circle(screen, (167, 139, 250), (sun_x, sun_y), 10)

















def _draw_capsule(screen, x, y, w):
    t = pygame.time.get_ticks() * 0.001
    pygame.draw.rect(screen, (13, 0, 24),
                     (x, y, w, 14), border_radius=7)
    pygame.draw.rect(screen, (76, 29, 149),
                     (x, y, w, 14), 1, border_radius=7)


    for i in range(3):
        offset = (t * 80 + i * 60) % (w + 20) - 10
        sx = int(x + offset)
        if x <= sx <= x + w - 10:
            spark = pygame.Surface((10, 8), pygame.SRCALPHA)
            pygame.draw.ellipse(spark, (167, 139, 250, 200), (0, 0 ,10, 8))
            screen.blit(spark, (sx, y + 3))




def _draw_cubes(screen, content_x, content_y, content_w):
    positions = [
        (content_x + 40, content_y + 20),
        (content_x + content_w - 60, content_y + 80),
    ]

    for px, py in positions:
        s = 18
        pygame.draw.rect(screen, (59, 7, 100),
                         (px, py + s//2, s, s), 1)


        pygame.draw.rect(screen, (45, 0, 80),
                         (px + s//2, py, s, s), 1)


        pygame.draw.line(screen, (76, 29, 149),
                         (px, py + s//2), (px + s//2, py), 1)
        pygame.draw.line(screen, (76, 29, 149),
                         (px + s, py + s//2), (px + s + s//2, py), 1)
        pygame.draw.line(screen, (76, 29, 149),
                         (px + s, py + s + s//2), (px + s + s//2, py + s), 1)



def _draw_corners(screen, x, y, w, h):
    c = (124, 58, 237)


    size = 14
    pygame.draw.line(screen, c, (x + 8, y + 8), (x + 8 + size, y + 8), 2)
    pygame.draw.line(screen, c, (x + 8, y + 8), (x + 8, y + 8 + size), 2)
    pygame.draw.line(screen, c, (x + w - 8, y + 8), (x + w - 8 - size, y + 8), 2)
    pygame.draw.line(screen, c, (x + w - 8, y + 8), (x + w - 8, y + 8 + size), 2)
    pygame.draw.line(screen, c, (x + 8, y + h - 8), (x + 8 + size, y + h - 8), 2)
    pygame.draw.line(screen, c, (x + 8, y + h - 8), (x + 8, y + h - 8 - size), 2)
    pygame.draw.line(screen, c, (x + w - 8, y + h - 8), (x + w - 8 - size, y + h - 8), 2)
    pygame.draw.line(screen, c, (x + w - 8, y + h - 8), (x + w - 8, y + h - 8 - size), 2)












def _draw_vines(screen, content_x, content_y, content_w, content_h):
    t = pygame.time.get_ticks() * 0.001


    # === ЛІАНИ ЗІ СТЕЛІ ===
    vine_positions = [
        content_x + content_w * 0.08,
        content_x + content_w * 0.22,
        content_x + content_w * 0.38,
        content_x + content_w * 0.52,
        content_x + content_w * 0.68,
        content_x + content_w * 0.82,
        content_x + content_w * 0.95,

    ]


    for j, vx in enumerate(vine_positions):
        vx = int(vx)
        vine_len = int(150 + math.sin(j * 1.3) * 60)



        for k in range(vine_len):
            ratio = k / vine_len
            sway = math.sin(t * 0.6 + j * 0.8 + ratio * 3) * 12 * ratio
            thickness = max(1, int(3 * (1 - ratio * 0.5)))
            green = int(40 + ratio * 40)
            pygame.draw.circle(screen, (green, 0, green * 2),
                               (int(vx + sway), content_y + k),
                               thickness)








            # листочки на ліані
            if k % 20 == 0 and k > 10:
                leaf_angle = math.sin(t * 0.5 + j + k) * 30 + (45 if k % 40 == 0 else -45)
                leaf_len = int(15 * (1 - ratio * 0.3))
                lx = int(vx + sway + math.cos(math.radians(leaf_angle)) * leaf_len)
                ly = content_y + k + int(math.sin(math.radians(leaf_angle)) * leaf_len)
                pygame.draw.line(screen, (76, 29, 149),
                                 (int(vx + sway), content_y + k),
                                 (lx, ly), 2)
                pygame.draw.circle(screen, (109, 40, 217), (lx, ly), 4)








    # === МАЛЕНЬКІ ДЕРЕВА ===
    trees = [
        (content_x + content_w * 0.03, content_y + content_h - 20, 0.7),
        (content_x + content_w * 0.97, content_y + content_h - 20, 0.65),
        (content_x + content_w * 0.18, content_y + content_h - 20, 0.55),
        (content_x + content_w * 0.82, content_y + content_h - 20, 0.6),
    ]





    for j, (tx, ty, size) in enumerate(trees):
        tx = int(tx)
        ty = int(ty)
        trunk_h = int(120 * size)



        # стовбур
        for k in range(trunk_h):
            ratio = k / trunk_h
            sway = math.sin(t * 0.4 + j * 1.2 + ratio * 4 * ratio)
            thickness = max(2, int(8 * ( 1 - ratio * 0.6) * size))
            col_val = int(30 + ratio * 20)
            pygame.draw.circle(screen, (col_val, 0, col_val * 2),
                               (int(tx + sway), ty - k), thickness)



        # гілки
        top_x = int(tx + math.sin(t * 0.4 + j * 1.2) * 4)
        top_y = ty - trunk_h



        branches = [
            (-50, -40, -30, -70),
            (50, -40, 30, -70),
            (-30, -20, -60, -50),
            (30, -20, 60, -50),
            (0, -10, 0, -60),
        ]



        for bx1, by1, bx2, by2 in branches:
            wave = math.sin(t * 0.6 + j * 0.5) * 5
            pygame.draw.line(screen, (59, 7, 100),
                             (int(top_x + bx1 * size), int(top_y + by1 * size)),
                             (int(top_x + bx2 * size), int(top_y + by2 * size)),
                             max(1, int(2 * size)))






            # листя на гілках
            end_x = int(top_x + bx2 * size + wave)
            end_y = int(top_y + by2 * size)
            for leaf in range(5):
                la = leaf * 72 + t * 15 * (1 if j % 2 == 0 else -1)
                lr = int((8 + abs(math.sin(t + leaf))) * size)
                lx = end_x + int(math.cos(math.radians(la)) * lr * 2)
                ly = end_y + int(math.sin(math.radians(la)) * lr)



                leaf_color = [
                    (76, 29, 149), (91, 33, 182),
                    (109, 40, 217), (124, 58, 237),
                    (139, 70, 255)
                ][leaf % 5]
                pygame.draw.circle(screen, leaf_color, (lx, ly), lr)




    # === ТРАВА ЗНИЗУ ===
    for i in range(0, content_w, 8):
        gx = content_x + i
        gh = int(20 + abs(math.sin(t * 1.2 + i * 0.1)) * 15)
        sway = math.sin(t * 0.8 + i * 0.05) * 5
        pygame.draw.line(screen, (59, 7, 100),
                         (gx, content_y + content_h - 20),
                         (int(gx + sway), content_y + content_h - 20 -gh), 2)














































def _draw_flowers(screen, content_x, content_y, content_w, content_h):
    t = pygame.time.get_ticks() * 0.001




    flowers = [
        (content_x + content_w * 0.05, content_y + content_h, 1.4),
        (content_x + content_w * 0.15, content_y + content_h, 1.1),
        (content_x + content_w * 0.25, content_y + content_h, 1.6),
        (content_x + content_w * 0.35, content_y + content_h, 1.2),
        (content_x + content_w * 0.45, content_y + content_h, 1.5),
        (content_x + content_w * 0.55, content_y + content_h, 1.3),
        (content_x + content_w * 0.65, content_y + content_h, 1.7),
        (content_x + content_w * 0.75, content_y + content_h, 1.2),
        (content_x + content_w * 0.85, content_y + content_h, 1.5),
        (content_x + content_w * 0.93, content_y + content_h, 1.1),


        # другий ряд менших квітів між великими

        (content_x + content_w * 0.10, content_y + content_h, 0.7),
        (content_x + content_w * 0.20, content_y + content_h, 0.8),
        (content_x + content_w * 0.30, content_y + content_h, 0.6),
        (content_x + content_w * 0.40, content_y + content_h, 0.9),
        (content_x + content_w * 0.50, content_y + content_h, 0.7),
        (content_x + content_w * 0.60, content_y + content_h, 0.8),
        (content_x + content_w * 0.70, content_y + content_h, 0.6),
        (content_x + content_w * 0.80, content_y + content_h, 0.9),
        (content_x + content_w * 0.90, content_y + content_h, 0.7),
    ]






    for j, (fx, fy, size) in enumerate(flowers):
        fx = int(fx)
        fy = int(fy)



        # стебло
        stem_sway = math.sin(t * 0.8 + j * 0.7) * 8
        stem_h = int(200 * size)
        for k in range(stem_h):
            ratio = k / stem_h
            sw = math.sin(t * 0.8 + j * 0.7 + ratio * 2) * 6 * ratio
            pygame.draw.circle(screen, (45, 0, 80),
                               (int(fx + sw), int(fy) - k),
                               max(1, int(2 * size)))




        # центр квітки
        flower_x = int(fx + stem_sway)
        flower_y = int(fy) - stem_h + int(math.sin(t * 1.2 + j * 0.5) * 4)



        # пелюстки
        num_petals = 6
        petal_len = int(22 * size)
        for p in range(num_petals):
            petal_angle = p * (360 / num_petals) + t * 20 * (1 if j % 2 == 0 else -1)
            px = flower_x + int(math.cos(math.radians(petal_angle)) * petal_len)
            py = flower_y + int(math.sin(math.radians(petal_angle)) * petal_len)






            # пульсування розміру пелюстки
            petal_r = int((8 + abs(math.sin(t * 2 + p * 0.5)) * 4) * size)



            colors = [
                (109, 40, 217), (124, 58, 237),
                (76, 29, 149), (139, 70, 255),
                (91, 33, 182), (167, 139, 250),
            ]


            pygame.draw.circle(screen, colors[p % len(colors)],
                                        (px, py), petal_r)




            # світіння пелюстки
            glow_surf = pygame.Surface((petal_r*4, petal_r*4), pygame.SRCALPHA)
            glow_alpha = int(40 + abs(math.sin(t * 2 + p * 0.5)) * 40)
            pygame.draw.circle(glow_surf, (124, 58, 237, glow_alpha),
                               (petal_r*2, petal_r*2), petal_r*2)


            screen.blit(glow_surf, (px - petal_r*2, py - petal_r*2))




        # центр квітки
        center_r = int(10 * size)
        pygame.draw.circle(screen, (20, 0, 36), (flower_x, flower_y), center_r)
        pygame.draw.circle(screen, (167, 139, 250), (flower_x, flower_y), center_r, 2)
        pygame.draw.circle(screen, (109, 40, 217), (flower_x, flower_y), center_r // 2)






        # маленькі комахи що летять до квітки
        for b in range(3):
            bug_angle = t * 80 + j * 120 + b * 120
            bug_dist = int(15 + abs(math.sin(t * 1.5 + b)) * 25)
            bug_x = flower_x + int(math.cos(math.radians(bug_angle)) * bug_dist)
            bug_y = flower_y + int(math.sin(math.radians(bug_angle)) * bug_dist)
            pygame.draw.circle(screen, (196, 181, 253), (bug_x, bug_y), 2)
            pygame.draw.circle(screen, (124, 58, 237), (bug_x, bug_y), 1)




            # крильця комахи
            wing_angle = t * 200  + b * 60
            for w in range(2):
                wx = bug_x + int(math.cos(math.radians(wing_angle + w*180)) * 4)
                wy = bug_y + int(math.sin(math.radians(wing_angle + w*180)) * 2)
                pygame.draw.line(screen, (167, 139, 250, 100),
                                 (bug_x, bug_y), (wx, wy), 1)






 








def draw_settings(screen, WIDTH, HEIGHT):
    _init_matrix(WIDTH, HEIGHT)
    _init_cars(WIDTH, HEIGHT)


    # фон
    screen.fill((5, 0, 15))


    # сітка
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, (30, 8, 50), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (30, 8, 50), (0, y), (WIDTH, y), 1)




    # матричний дощ
    _draw_matrix(screen, WIDTH, HEIGHT)


    # машини
    _draw_cars(screen)


    # пальми
    _draw_palm(screen, 0, HEIGHT, flip=False)
    _draw_palm(screen, WIDTH, HEIGHT, flip=True)


    # сонце
    _draw_sun(screen, WIDTH)


    # сканлінія
    scan_y = (pygame.time.get_ticks() // 12) % HEIGHT
    scan_surf = pygame.Surface((WIDTH, 3), pygame.SRCALPHA)
    scan_surf.fill((167, 139, 250, 18))
    screen.blit(scan_surf, (0, scan_y))




    panel_x = 40
    panel_y = 80
    panel_w = 200
    panel_h = HEIGHT - 120





    # ліва панель
    pygame.draw.rect(screen, (8, 0, 16),
                     (panel_x, panel_y, panel_w, panel_h), border_radius=14)
    pygame.draw.rect(screen, (76, 29, 149),
                     (panel_x, panel_y, panel_w, panel_h), 1, border_radius=14)


    # логотип
    t = pygame.time.get_ticks() * 0.001
    glow = int(128 + 80 * math.sin(t * 2))
    pygame.draw.circle(screen, (glow // 4, 0, glow // 2),
                       (panel_x + 30, panel_y + 30), 18)
    pygame.draw.circle(screen, (124, 58, 237),
                       (panel_x + 30, panel_y + 30), 18, 2)

    lf = pygame.font.SysFont("Arial", 14, bold=True)
    lt = lf.render("A", True, (167, 139, 250))
    screen.blit(lt, (panel_x + 30 - lt.get_width()//2,
                     panel_y + 30 - lt.get_height()//2))


    sf = pygame.font.SysFont("Arial", 10, bold=True)
    logo_txt = sf.render("AGAR.SYS", True, (109, 40, 217))
    screen.blit(logo_txt, (panel_x + 50, panel_y + 24))






    # розділювач



    pygame.draw.line(screen, (59, 7, 100),
                     (panel_x + 12, panel_y + 52),
                     (panel_x + panel_w - 12, panel_y + 52), 1)



    # заголовок


    nav_title = sf.render("//NAVIGATOR", True, (76, 29, 149))
    screen.blit(nav_title, (panel_x + 16, panel_y + 58))



    tabs = [
        ("achievements", "Dosyahnennya"),
        ("audio", "Zvuk i audio"),
        ("account", "Akkaunt"),
        ("privacy", "Konfid."),
        ("quality", "Yakist"),
        ("bind", "Pryvyazka"),
        ("rules", "Pravyla"),
    ]



    tab_rects = []
    for i, (tab_id, tab_label) in enumerate(tabs):
        r = pygame.Rect(panel_x + 8, panel_y + 74 + i * 48, panel_w - 16, 40)
        is_active = SETTINGS_TAB[0] == tab_id
        hover  = r.collidepoint(pygame.mouse.get_pos())


        if is_active:
            pygame.draw.rect(screen, (20, 0, 38), r, border_radius=8)
            pygame.draw.rect(screen, (109, 40, 217), r, 1, border_radius=8)
            pygame.draw.rect(screen, (124, 58, 237),
                             pygame.Rect(panel_x + 8, r.y + 8, 3, 24),
                             border_radius=2)



            dot_color = (167, 139, 250)
        elif hover:
            pygame.draw.rect(screen, (15, 0, 28), r, border_radius=8)
            dot_color = (91, 33, 182)
        else:
            dot_color = (45, 7, 80)


        pygame.draw.circle(screen, dot_color, (r.x + 16, r.centery), 4)


        tf = pygame.font.SysFont("Arial", 12, bold=is_active)
        color = (196, 181, 253) if is_active else (109, 40, 217)
        txt = tf.render(tab_label, True, color)
        screen.blit(txt, (r.x + 28, r.centery - txt.get_height()//2))
        tab_rects.append((r, tab_id))





    # статус бар знизу
    status_y = panel_y + panel_h - 50
    pygame.draw.line(screen, (30, 8, 50),
                     (panel_x + 12, status_y),
                     (panel_x + panel_w - 12, status_y), 1)



    sys_f = pygame.font.SysFont("Arial", 9)
    sys_t = sys_f.render("SYS_ONLINE // v2.4.1", True, (59, 7, 100))
    screen.blit(sys_t, (panel_x + 16, status_y + 6))
    bar_x = panel_x + 16
    bar_w = panel_w - 32
    pygame.draw.rect(screen, (20, 0, 38), (bar_x, status_y + 22, bar_w, 4), border_radius=2)
    fill = int(bar_x * 0.72)
    pygame.draw.rect(screen, (109, 40, 217),
                     (bar_x, status_y + 22, fill, 4), border_radius=2)




    # права обалсть
    content_x = panel_x + panel_w + 20
    content_y = panel_y
    content_w = WIDTH - content_x - 40
    content_h = panel_h





    pygame.draw.rect(screen, (8, 0, 16),
                     (content_x, content_y, content_w, content_h), border_radius=14)
    pygame.draw.rect(screen, (59, 7, 100),
                     (content_x, content_y, content_w, content_h), 1, border_radius=14)




    # сітка в парвій панелі


    for gx in range(content_x + 40, content_x + content_w, 40):
        pygame.draw.line(screen, (20, 5, 35),
                         (gx, content_y), (gx, content_y + content_h), 1)


    for gy in range(content_y + 40, content_y + content_h, 40):
        pygame.draw.line(screen, (20, 5, 35),
                         (content_x, gy), (content_x + content_w, gy), 1)





    # кутові маркери
    _draw_corners(screen, content_x, content_y, content_w, content_h)



    # куби
    _draw_cubes(screen, content_x, content_y, content_w)




    # заголовок вкладки
    tab_names = {
        "achievements": "DOSYAHNENNYA",
        "audio": "ZVUK I AUDIO",
        "account": "AKKAUNT",
        "privacy": "KONFIDENTSIJNIST",
        "quality": "YAKIST KARTYNKY",
        "bind": "PRIVYAZKA",
        "rules": "PRAVYLA HRY",
    }


    title_f = pygame.font.SysFont("Arial", 16, bold=True)
    title = title_f.render("// " + tab_names.get(SETTINGS_TAB[0], ""),
                           True, (124, 58, 237))



    screen.blit(title, (content_x + 20, content_y + 16))
    pygame.draw.line(screen, (59, 7, 100),
                     (content_x + 16, content_y + 46),
                     (content_x + content_w - 16, content_y + 46), 1)



    # капсула знизу
    _draw_capsule(screen, content_x + 20, content_y + content_h - 30,
                  content_w - 40)


    cap_f = pygame.font.SysFont("Arial", 8)
    cap_t = cap_f.render("// POWER LINE ACTIVE", True, (59, 7, 100))
    screen.blit(cap_t, (content_x + content_w//2 - cap_t.get_width()//2,
                        content_y + content_h - 14))


    # вміст вкладки
    audio_toggle_rects = []
    audio_slider_rects = []
    privacy_toggle_rects = []
    quality_toggle_rects = []
    quality_btn_rects = []



    if SETTINGS_TAB[0] == "audio":
        audio_toggle_rects, audio_slider_rects = draw_settings_audio(
            screen, content_x, content_y + 50, content_w, content_h - 80)
        _draw_vines(screen, content_x, content_y, content_w, content_h)
        _draw_flowers(screen, content_x, content_y, content_w, content_h)
    if SETTINGS_TAB[0] == "privacy":
        privacy_toggle_rects = draw_settings_privacy(
            screen, content_x, content_y + 50, content_w, content_h - 80)
        _draw_vines(screen, content_x, content_y, content_w, content_h)
        _draw_flowers(screen, content_x, content_y, content_w, content_h)
    if SETTINGS_TAB[0] == "account":
        draw_settings_account(
            screen, content_x, content_y + 50, content_w, content_h - 80)
        _draw_vines(screen, content_x, content_y, content_w, content_h)
        _draw_flowers(screen, content_x, content_y, content_w, content_h)


    if SETTINGS_TAB[0] == "bind":
        draw_settings_bind(
            screen, content_x, content_y + 50, content_w, content_h - 80)
        _draw_vines(screen, content_x, content_y, content_w, content_h)
        _draw_flowers(screen, content_x, content_y, content_w, content_h)



    if SETTINGS_TAB[0] == "quality":
        quality_toggle_rects, quality_btn_rects = draw_settings_quality(
            screen, content_x, content_y + 50, content_w, content_h - 80)
        _draw_vines(screen, content_x, content_y, content_w, content_h)
        _draw_flowers(screen, content_x, content_y, content_w, content_h)

    achievements_reset_btn = None
    if SETTINGS_TAB[0] == "achievements":
        achievements_reset_btn = draw_settings_achievements(
            screen, content_x, content_y + 50, content_w, content_h - 80, panel_x, panel_y)




    if SETTINGS_TAB[0] == "rules":
        draw_settings_rules(
            screen, content_x, content_y + 50, content_w, content_h - 80)
        _draw_vines(screen, content_x, content_y, content_w, content_h)
        _draw_flowers(screen, content_x, content_y, content_w, content_h)





    # кнопка назад
    back_rect = pygame.Rect(panel_x, panel_y - 50, 44, 36)
    pygame.draw.rect(screen, (20, 0, 38), back_rect, border_radius=10)
    pygame.draw.rect(screen, (76, 29, 149), back_rect, 1, border_radius=10)
    arrow = pygame.font.SysFont("Arial", 16, bold=True).render(
        "<-", True, (167, 139, 250))
    screen.blit(arrow, (back_rect.centerx - arrow.get_width()//2,
                        back_rect.centery - arrow.get_height()//2))



    return (tab_rects, back_rect, content_x, content_y, content_w, content_h,
            audio_toggle_rects, audio_slider_rects,
            privacy_toggle_rects,
            quality_toggle_rects, quality_btn_rects,
            achievements_reset_btn)





































































