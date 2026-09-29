import pygame
import math
from settings_state import audio_toggles, audio_volumes



def draw_settings_audio(screen, content_x, content_y, content_w, content_h):
    tiny = pygame.font.SysFont("Arial", 11)
    small = pygame.font.SysFont("Arial", 13, bold=True)
    mono = pygame.font.SysFont("Courier New", 11)
    t = pygame.time.get_ticks() * 0.001


    # === ВІЗУАЛІЗАТОР ЗВУКУ ===
    bars_x = content_x + 20
    bars_y = content_y + 10
    bar_w = 10
    bar_gap = 3
    num_bars = 14




    for i in range(num_bars):
        h = int(20 + abs(math.sin(t * 2 + i * 0.4)) * 30)
        alpha = int(100 + abs(math.sin(t * 1.5 + i * 0.3)) * 155)
        bx = bars_x + i * (bar_w + bar_gap)
        color = (109, 40, 217)
        pygame.draw.rect(screen, color,
                         (bx, bars_y + 40 - h, bar_w, h), border_radius=2)
        pygame.draw.rect(screen, (167, 139, 250),
                         (bx, bars_y + 40 - h, bar_w, 2))








    # === КОЛОНКИ ===
    spk1_x = content_x + content_w // 2 - 90
    spk2_x = content_x + content_w // 2 + 90
    spk_y = content_y + 26





    for spk_x in [spk1_x, spk2_x]:
        pygame.draw.rect(screen, (13, 0, 24),
                         (spk_x - 22, spk_y - 36, 44, 62), border_radius=6)





        pygame.draw.rect(screen, (76, 29, 149),
                         (spk_x - 22, spk_y - 36, 44, 62), 1, border_radius=6)


        glow = int(60 + abs(math.sin(t * 3)) * 60)


        pygame.draw.circle(screen, (glow // 3, 0, glow),
                           (spk_x, spk_y), 16)
        pygame.draw.circle(screen, (109, 40, 217), (spk_x, spk_y), 16, 1)

        pygame.draw.circle(screen, (59, 7, 100), (spk_x, spk_y), 10)

        pygame.draw.circle(screen, (124, 58, 237), (spk_x, spk_y), 4)

        pygame.draw.rect(screen, (45, 0, 80),
                         (spk_x - 8, spk_y + 28, 16, 6), border_radius=6)





    # === КРУТИЛКА ===
    knob_x = content_x + content_w // 2
    knob_y = content_y + 26
    knob_angle = t * 40 % 360
    pygame.draw.circle(screen, (20, 0, 36), (knob_x, knob_y), 20)
    pygame.draw.circle(screen, (109, 40, 217), (knob_x, knob_y), 20, 2)
    kx = knob_x + int(math.cos(math.radians(knob_angle - 90)) * 13)
    ky = knob_y + int(math.sin(math.radians(knob_angle - 90)) * 13)
    pygame.draw.line(screen, (167, 139, 250), (knob_x, knob_y), (kx, ky), 2)
    pygame.draw.circle(screen, (124, 58, 237), (knob_x, knob_y), 4)
    lbl = tiny.render("// VOL", True, (76, 29, 149))
    screen.blit(lbl, (knob_x - lbl.get_width() // 2, knob_y + 24))






    # === ТОГЛИ ===
    toggles = [
        ("Zvuky hry", "zvuky_hry"),
        ("Muzyka", "muzyka"),
        ("Zvuky menu", "zvuky_menu"),
        ("Spovishchennya", "spovishchennya"),
    ]


    toggle_rects = []
    for i, (name, key) in enumerate(toggles):
        state = audio_toggles[key]
        row_y = content_y + 70 + i * 46
        row_rect = pygame.Rect(content_x + 16, row_y, content_w - 32, 38)


        pygame.draw.rect(screen, (13, 0, 24), row_rect, border_radius=6)
        border_color = (109, 40, 217) if state else (45, 7, 80)
        pygame.draw.rect(screen, border_color, row_rect, 1, border_radius=6)


        # префікс у стилі коду
        prefix = mono.render("//", True, (59, 7, 100))
        screen.blit(prefix, (row_rect.x + 10, row_rect.centery - prefix.get_height() // 2))


        label = small.render(name, True, (167, 139, 250) if state else (76, 29, 149))
        screen.blit(label, (row_rect.x + 30, row_rect.centery - label.get_height() // 2))


        # тогл
        tog_x = row_rect.right - 54
        tog_y = row_rect.centery - 9
        tog_color = (109, 40, 217) if state else(20, 0, 36)
        pygame.draw.rect(screen, tog_color, (tog_x, tog_y, 34, 18), border_radius=9)
        pygame.draw.rect(screen, (76, 29, 149), (tog_x, tog_y, 34, 18), 1, border_radius=9)
        circle_x = tog_x + (22 if state else 8)
        pygame.draw.circle(screen, (196, 181, 253) if state else (59, 7, 100),
                           (circle_x, tog_y + 9), 7)
        toggle_rects.append((row_rect, key))




    # === СЛАЙДЕРИ ===
    sliders = [
        ("ZVUKY", "zvuky"),
        ("MUZYKA", "muzyka"),
    ]



    slider_rects = []
    for i, (name, key) in enumerate(sliders):
        val = audio_volumes[key]
        row_y = content_y + 260 + i * 50
        label = mono.render(f"// {name}: {val}%", True, (76, 29, 149))
        screen.blit(label, (content_x + 16, row_y))



        bar_x = content_x + 16
        bar_y = row_y + 18
        bar_w2 = content_w - 32



        pygame.draw.rect(screen, (20, 0, 36),
                         (bar_x, bar_y, bar_w2, 6), border_radius=3)
        pygame.draw.rect(screen, (45, 7, 80),
                         (bar_x, bar_y, bar_w2, 6), 1, border_radius=3)
        fill_w = int(bar_w2 * val / 100)
        pygame.draw.rect(screen, (109, 40, 217),
                        (bar_x, bar_y, fill_w, 6), border_radius=3)
        pygame.draw.circle(screen, (167, 139, 250),
                           (bar_x + fill_w, bar_y + 3), 9)


        pygame.draw.circle(screen, (109, 40, 217),
                           (bar_x + fill_w, bar_y + 3), 9, 1)


        slider_rects.append((pygame.Rect(bar_x, bar_y - 10, bar_w2, 26),
                             key, bar_x, bar_w2))





    return toggle_rects, slider_rects

























































































