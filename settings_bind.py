import pygame
import math

def draw_settings_bind(screen, content_x, content_y, content_w, content_h):
    tiny = pygame.font.SysFont("Arial", 11)
    small = pygame.font.SysFont("Arial", 13, bold=True)
    mono = pygame.font.SysFont("Courier New", 11)
    t = pygame.time.get_ticks() * 0.001



    # === ІНФО КАРТКИ ===
    bind_info = [
        ("DATA", "12.03.2024 14:32", (124, 58, 237)),
        ("PRYSTRYI", "MacBook Pro 15", (109, 40, 217)),
        ("PLATFORMA", "macOS 14.2", (91, 33, 182)),
    ]


    for i, (label, value, color) in enumerate(bind_info):
        card_x = content_x + 16
        card_y = content_y + 10 + i * 46
        card_w = content_w - 32
        card_h = 38



        pygame.draw.rect(screen, (13, 0, 24),
                         (card_x, card_y, card_w, card_h), border_radius=6)
        pygame.draw.rect(screen, (45, 7, 80),
                         (card_x, card_y, card_w, card_h), 1, border_radius=6)
        pygame.draw.rect(screen, color,
                         (card_x, card_y + 8, 2, card_h - 16), border_radius=1)


        lbl = mono.render("// " + label, True, (59, 7, 100))
        screen.blit(lbl, (card_x + 12, card_y + card_h // 2 - lbl.get_height() // 2))



        val = small.render(value, True, color)
        screen.blit(val, (card_x + card_w - val.get_width() - 12,
                          (card_y + card_h // 2 - val.get_height() // 2)))



    # === РОЗДІЛЮВАЧ ===
    pygame.draw.line(screen, (45, 7, 80),
                     (content_x + 16, content_y + 158),
                     (content_x + content_w - 16, content_y + 158), 1)



    sec_f = pygame.font.SysFont("Courier New", 10, bold=True)
    sec = sec_f.render("// PRYVYAZANI PLATFORMY", True, (76, 29, 149))
    screen.blit(sec, (content_x + 16, content_y + 166))



    # === ПЛАТФОРМИ ===
    platforms = [
        ("Google", True, (234, 67, 53)),
        ("Apple ID", True, (196, 181, 253)),
        ("Discord", False, (88, 101, 242)),
        ("Steam", False, (100, 150, 200)),
    ]




    for i, (name, connected, color) in enumerate(platforms):
        row_y = content_y + 184 + i * 52
        row_rect = pygame.Rect(content_x + 16, row_y, content_w - 32, 42)


        pygame.draw.rect(screen, (13, 0, 24), row_rect, border_radius=6)
        border_color = color if connected else (45, 7, 80)
        pygame.draw.rect(screen, border_color, row_rect, 1, border_radius=6)





        # лівий акцент
        pygame.draw.rect(screen, color if connected else (45, 7, 80),
                        (row_rect.x, row_rect.y + 8, 2, 26), border_radius=1)


        # назва платформи
        name_txt = small.render(name, True, (196, 181, 253) if connected else (76, 29, 149))
        screen.blit(name_txt, (row_rect.x + 16,
                               row_rect.centery - name_txt.get_height() // 2))


        # індикатор
        dot_color = (34, 197, 94) if connected else (59, 7, 100)
        pygame.draw.circle(screen, dot_color,
                           (row_rect.right - 60, row_rect.centery), 5)





        # статус
        if connected:
            status = mono.render("// LINKED", True, (34, 197, 94))
        else:
            status = mono.render("// OFFLINE", True, (59, 7, 100))
        screen.blit(status, (row_rect.right - status.get_width() - 16,
                             row_rect.centery - status.get_height() // 2))

























































































