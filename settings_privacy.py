import pygame
import math
from settings_state import privacy_toggles



def draw_settings_privacy(screen, content_x, content_y, content_w, content_h):
    tiny = pygame.font.SysFont("Arial", 11)
    small = pygame.font.SysFont("Arial", 13, bold=True)
    mono = pygame.font.SysFont("Courier New", 11)
    t = pygame.time.get_ticks() * 0.001



    # === ІНФО КАРТКИ ===
    info_cards = [
        ("ID", "#UA-2841-9XKZ", (124, 58, 237)),
        ("VKHID", "29.06.2026 10:15", (91, 33, 182)),
        ("VERSION", "v2.4.1", (109, 40, 217)),
        ("REGION", "EU-West", (76, 29, 149)),
        ("ENCRYPT", "AKTYVNE", (34, 197, 94)),
    ]




    for i, (label, value, color) in enumerate(info_cards):
        card_x = content_x + 16
        card_y = content_y + 10 + i * 46
        card_w = content_w - 32
        card_h = 38



        pygame.draw.rect(screen, (13, 0, 24),
                         (card_x, card_y, card_w, card_h), border_radius=6)
        pygame.draw.rect(screen, (45, 7, 80),
                         (card_x, card_y, card_w, card_h), 1, border_radius=6)



        # лівий акцент
        pygame.draw.rect(screen, color,
                         (card_x, card_y + 8, 2, card_h - 16), border_radius=1)


        lbl = mono.render("//" + label, True, (59, 7, 100))
        screen.blit(lbl, (card_x + 12, card_y + card_h // 2 - lbl.get_height() // 2))


        val = small.render(value, True, color)
        screen.blit(val, (card_x + card_w - val.get_width() - 12,
                          card_y + card_h // 2 - val.get_height() // 2))



    # === РОЗДІЛЮВАЧ ===
    pygame.draw.line(screen, (45, 7, 80),
                     (content_x + 16, content_y + 248),
                     (content_x + content_w - 16, content_y + 248), 1)



    sec_f = pygame.font.SysFont("Courier New", 10, bold=True)
    sec = sec_f.render("// BEZPEKA", True, (76, 29, 149))
    screen.blit(sec, (content_x + 16, content_y + 256))


    # === ТОГЛИ ===
    toggles = [
        ("Dvofaktorna autentyfikatsiya", "dvofaktorna"),
        ("Zberezhennya statystyky", "statystyka"),
        ("Pokazuvaty profil inshym", "pokazuvaty_profil"),
    ]



    toggle_rects = []
    for i, (name, key) in enumerate(toggles):
        state = privacy_toggles[key]
        row_y = content_y + 274 + i * 46
        row_rect = pygame.Rect(content_x + 16, row_y, content_w - 32, 38)


        pygame.draw.rect(screen, (13, 0, 24), row_rect, border_radius=6)
        border_color = (109, 40, 217) if state else (45, 7, 80)

        pygame.draw.rect(screen, border_color, row_rect, 1, border_radius=6)


        prefix = mono.render("//", True, (59, 7, 100))
        screen.blit(prefix, (row_rect.x + 10,
                             row_rect.centery - prefix.get_height() // 2))








        label = small.render(name, True,
                             (167, 139, 250) if state else (76, 29, 149))

        screen.blit(label, (row_rect.x + 30,
                            row_rect.centery - label.get_height() // 2))




        tog_x = row_rect.right - 54
        tog_y = row_rect.centery - 9
        tog_color = (109, 40, 217) if state else (20, 0, 36)
        pygame.draw.rect(screen, tog_color,
                         (tog_x, tog_y, 34, 18), border_radius=9)
        pygame.draw.rect(screen, (76, 29, 149),
                         (tog_x, tog_y, 34, 18), 1, border_radius=9)
        circle_x = tog_x + (22 if state else 8)







        pygame.draw.circle(screen, (196, 181, 253) if state else (59, 7, 100),
                           (circle_x, tog_y + 9), 7)
        toggle_rects.append((row_rect, key))

    return toggle_rects
































































































































