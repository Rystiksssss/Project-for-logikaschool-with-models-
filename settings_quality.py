import pygame
import math
from settings_state import quality_toggles, quality_selected



def draw_settings_quality(screen, content_x, content_y, content_w, content_h):
    tiny = pygame.font.SysFont("Arial", 11)
    small = pygame.font.SysFont("Arial", 13, bold=True)
    mono = pygame.font.SysFont("Courier New", 11)



    # === ЯКІСТЬ ГРАФІКИ ===
    sec_f = pygame.font.SysFont("Courier New", 10, bold=True)
    sec = sec_f.render("// HRAFIKA", True, (76, 29, 149))
    screen.blit(sec, (content_x + 16, content_y + 10))



    quality_options = [
        ("YAKIST HRAFIKY", ["NYZKA", "SEREDNYA", "VYSOKA"], "yakist"),
        ("LIMIT FPS", ["30", "60", "120"], "fps"),

    ]


    btn_rects = []
    for i, (label, options, key) in enumerate(quality_options):
        row_y = content_y + 30 + i * 62
        row_rect = pygame.Rect(content_x + 16, row_y, content_w - 32, 52)


        pygame.draw.rect(screen, (13, 0, 24), row_rect, border_radius=6)
        pygame.draw.rect(screen, (45, 7, 80), row_rect, 1, border_radius=6)



        lbl = mono.render("// " + label, True, (76, 29, 149))
        screen.blit(lbl, (row_rect.x + 12, row_rect.y + 8))



        btn_w = 80
        btn_gap = 6
        total_btn_w = len(options) * btn_w + (len(options) - 1) * btn_gap
        btn_start_x = row_rect.right - total_btn_w - 12
        for j, option in enumerate(options):
            btn_x = btn_start_x + j * (btn_w + btn_gap)
            btn_rect = pygame.Rect(btn_x, row_rect.y + 24, btn_w, 20)
            is_sel = j == quality_selected[key]
            pygame.draw.rect(screen, (109, 40, 217) if is_sel else (20, 0, 36),
                             btn_rect, border_radius=4)
            pygame.draw.rect(screen, (124, 58, 237) if is_sel else (45, 7, 80),
                             btn_rect, 1, border_radius=4)




            opt_txt = tiny.render(option, True,
                                  (196, 181, 253) if is_sel else (76, 29, 149))



            screen.blit(opt_txt, (btn_rect.centerx - opt_txt.get_width() // 2,
                                  btn_rect.centery - opt_txt.get_height() // 2))


            btn_rects.append((btn_rect, key, j))




    # === РОЗДІЛЮВАЧ ===
    pygame.draw.line(screen, (45, 7, 80),
                     (content_x + 16, content_y + 162),
                     (content_x + content_w - 16, content_y + 162), 1)





    sec2 = sec_f.render("// EFEKTY", True, (76, 29, 149))
    screen.blit(sec2, (content_x + 16, content_y + 170))






    # === ТОГЛИ ===
    toggles = [
        ("Pelyustky sakury", "pelyustky"),
        ("Animatsiya khmarok", "khmarky"),
        ("Radar botiv", "radar"),
        ("Tini personazhiv", "tini"),
    ]



    toggle_rects = []

    for i, (name, key) in enumerate(toggles):
        state = quality_toggles[key]
        row_y = content_y + 188 + i * 46
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


    return toggle_rects, btn_rects






















































































