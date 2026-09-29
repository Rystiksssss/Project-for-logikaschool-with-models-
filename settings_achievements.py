import pygame
from settings_state import kills_stats


def draw_settings_achievements(screen, content_x, content_y, content_w, content_h, panel_x, panel_y):
    tiny = pygame.font.SysFont("Arial", 11)
    small = pygame.font.SysFont("Arial", 13, bold=True)
    mono = pygame.font.SysFont("Courier New", 11)





    # === СТАТИСТИКА ===
    sec_f = pygame.font.SysFont("Courier New", 10, bold=True)
    sec = sec_f.render("// STATYSTYKA", True, (76, 29, 149))
    screen.blit(sec, (content_x + 16, content_y + 10))



    stats = [
        ("TOTAL", kills_stats["total"], (167, 139, 250)),
        ("RARE", kills_stats["rare"], (59, 130, 246)),
        ("EPIC", kills_stats["epic"], (167, 139, 250)),
        ("LEGEND", kills_stats["legendary"], (234, 179, 8)),
        ("GOLD", kills_stats["gold"], (245, 158, 11)),
    ]



    available_w = content_w - 32
    gap = 6
    stat_w = (available_w - (len(stats) - 1) * gap) // len(stats)

    for i, (label, value, color) in enumerate(stats):
        card_x = content_x + 16 + i * (stat_w + gap)
        card_y = content_y + 28
        card_rect = pygame.Rect(card_x, card_y, stat_w, 56)



        pygame.draw.rect(screen, (13, 0, 24), card_rect, border_radius=6)
        pygame.draw.rect(screen, color, card_rect, 1, border_radius=6)


        num = pygame.font.SysFont("Courier New", 20, bold=True).render(
            str(value), True, color)
        screen.blit(num, (card_rect.centerx - num.get_width() // 2,
                          card_rect.y + 8))


        lbl = tiny.render(label, True, (59, 7, 100))
        screen.blit(lbl, (card_rect.centerx - lbl.get_width() // 2,
                          card_rect.y + 36))



    # === РОЗДІЛЮВАЧ ===
    pygame.draw.line(screen, (45, 7, 80),
                     (content_x + 16, content_y + 96),
                     (content_x + content_w - 16, content_y + 96), 1)



    sec2 = sec_f.render("// DOSYAHNENNYA", True, (76, 29, 149))
    screen.blit(sec2, (content_x + 16, content_y + 104))



    # === ДОСЯГНЕННЯ ===
    achievements = [
        ("Persha krov", "Vbyt 1 bota", kills_stats["total"] >= 1, (234, 179, 8), 20),
        ("Myslyvets", "Vbyy 10 Rare", kills_stats["rare"] >= 10, (59, 130, 246), 200),
        ("Epichnyi", "Vbyy 5 Epic", kills_stats["epic"] >= 5, (167, 139, 250), 350),
        ("Lehenda", "Vbyy Legend bota", kills_stats["legendary"] >= 1, (234, 179, 8), 500),
        ("Zolota ruka", "Vbyy Gold bota", kills_stats["gold"] >= 1, (245, 158, 11), 750),
        ("Neshchadnyi", "Vbyy 50 botiv", kills_stats["total"] >= 50, (239, 68, 68), 1000),
        ("Veteran", "Vbyy 100 botiv", kills_stats["total"] >= 100, (167, 139, 250), 2000),
        ("Znyshchuvach", "Vbyy 200 botiv", kills_stats["total"] >= 200, (239, 68, 68), 5000),
        ("Rare hunter", "Vbyy 50 Rare botiv", kills_stats["rare"] >= 50, (59, 130, 246), 1500),
        ("Epic hunter", "Vbyy 20 Epic botiv", kills_stats["epic"] >= 20, (167, 139, 250), 2500),
        ("Gold hunter", "Vbyy 5 Gold botiv", kills_stats["gold"] >= 5, (245, 158, 11), 3000),
        ("Legenda myth", "Vbyy 5 Legend botiv", kills_stats["legendary"] >= 5, (234, 179, 8), 4000),


    ]




    # мигаючий напис
    blink = int(pygame.time.get_ticks() / 500) % 2
    if blink:
        blink_f = pygame.font.SysFont("Courier New", 13, bold=True)
        blink_txt = blink_f.render("// TSI ZAVDANNYA ZA MONETY //", True, (124, 58, 237))
        pygame.draw.line(screen, (45, 7, 80),
                         (content_x + 16, content_y + 108),
                         (content_x + content_w - 16, content_y + 108), 1)
        screen.blit(blink_txt, (content_x + content_w//2 - blink_txt.get_width()//2,
                                content_y + 112))




    ach_w = (content_w - 32 - 8) // 2
    for i, (name, desc, unlocked, color, coins_reward) in enumerate(achievements):
        col = i % 2
        row = i // 2
        ach_x = content_x + 16 + col * (ach_w + 8)
        ach_y = content_y + 122 + row * 72
        ach_rect = pygame.Rect(ach_x, ach_y, ach_w, 62)


        bg_color = (18, 0, 32) if unlocked else ( 10, 0, 18)
        pygame.draw.rect(screen, bg_color, ach_rect, border_radius=6)
        pygame.draw.rect(screen, color if unlocked else (45, 7, 80),
                         ach_rect, 1, border_radius=6)


        pygame.draw.rect(screen, color if unlocked else (45, 7, 80),
                         (ach_rect.x, ach_rect.y + 8, 2, ach_rect.height - 16),
                         border_radius=1)


        icons = ["*", "*", "~", "^", "@", "!", "#", "%", "&", "?", "$", "="]
        icon_f = pygame.font.SysFont("Courier New", 18, bold=True)
        icon = icon_f.render(icons[i % len(icons)], True,
                             color if unlocked else ( 45, 7, 80))
        screen.blit(icon, (ach_rect.x + 10,
                           ach_rect.centery - icon.get_height() // 2))



        name_color = (196, 181, 253) if unlocked else (59, 7, 100)
        name_txt = small.render(name, True, name_color)
        max_w = ach_w - 56
        if name_txt.get_width() > max_w:
            name = name[:int(len(name) * max_w / name_txt.get_width()) - 2] + ".."
            name_txt = small.render(name, True, name_color)


        screen.blit(name_txt, (ach_rect.x + 30, ach_rect.y + 6))




        desc_surf = tiny.render(desc, True, (59, 7, 100))
        if desc_surf.get_width() > max_w:
            desc = desc[:int(len(desc) * max_w / desc_surf.get_width()) - 2] + ".."
            desc_surf = tiny.render(desc, True, (59, 7, 100))
        screen.blit(desc_surf, (ach_rect.x + 30, ach_rect.y + 22))




        # монети за виконання
        if unlocked:
            coin_txt = mono.render(f"// DONE +{coins_reward}", True, (34, 197, 94))
        else:
            coin_txt = mono.render(f"// + {coins_reward} coins", True, (45, 7, 80))
        screen.blit(coin_txt, (ach_rect.x + 30, ach_rect.y + 38))





    reset_btn = pygame.Rect(panel_x + 50, panel_y - 50,
                            160, 34)


    mouse_pos = pygame.mouse.get_pos()
    hover = reset_btn.collidepoint(mouse_pos)


    pygame.draw.rect(screen, (40, 0, 60) if hover else (20, 0, 36),
                     reset_btn, border_radius=6)
    pygame.draw.rect(screen, (239, 68, 8), reset_btn, 1, border_radius=6)



    reset_f = pygame.font.SysFont("Courier New", 12, bold=True)
    reset_txt = reset_f.render("// RESET ACHIEVEMENTS", True, (239, 68, 68))
    screen.blit(reset_txt, (reset_btn.centerx - reset_txt.get_width()//2,
                            reset_btn.centery - reset_txt.get_height()//2))



    return reset_btn

























































