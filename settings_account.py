import pygame
import math


def draw_settings_account(screen, content_x, content_y, content_w, content_h):
    tiny = pygame.font.SysFont("Arial", 11)
    small =  pygame.font.SysFont("Arial", 13, bold=True)
    mono = pygame.font.SysFont("Courier New", 11)
    t = pygame.time.get_ticks() * 0.001



    # === АВАТАР ===
    av_x = content_x + 50
    av_y = content_y + 40
    av_r = 36




    # пульсуючий ефект
    glow = int(40 + abs(math.sin(t * 1.5)) * 40)
    pygame.draw.circle(screen, (glow // 3, 0, glow),
                       (av_x, av_y), av_r + 6)
    pygame.draw.circle(screen, (20, 0, 36), (av_x, av_y), av_r)
    pygame.draw.circle(screen, (109, 40, 217), (av_x, av_y), av_r, 2)


    # ініціали
    af = pygame.font.SysFont("Arial", 22, bold=True)
    initials = af.render("VS", True, (167, 139, 250))
    screen.blit(initials, (av_x - initials.get_width() // 2,
                           av_y - initials.get_height() // 2))



    # кутові маркери навколо аватара
    c = (124, 58, 237)
    s = 10
    for dx, dy, angles in [
        (-av_r - 8, -av_r - 8, [(1, 0), (0, 1)]),
        (av_r + 8, -av_r - 8, [(-1, 0), (0, 1)]),
        (-av_r - 8, av_r + 8, [(1, 0), (0, -1)]),
        (av_r + 8, av_r + 8, [(-1, 0), (0, -1)]),

    ]:
        cx = av_x + dx
        cy = av_y + dy
        for ax, ay in angles:
            pygame.draw.line(screen, c, (cx, cy), (cx + ax * s, cy + ay * s), 2)






    # ім'я і email
    name_f = pygame.font.SysFont("Arial", 18, bold=True)
    name_txt = name_f.render("Vasyl Stepanenko", True, (196, 181, 253))
    screen.blit(name_txt, (av_x + av_r + 20, av_y - 20))


    email_txt = mono.render("vasyl.stepanenko@gmail.com", True, (76, 20, 149))
    screen.blit(email_txt, (av_x + av_r + 20, av_y + 4))



    date_txt = mono.render("// hravets z 12.03.2024", True, (59, 7, 100))
    screen.blit(date_txt, (av_x + av_r + 20, av_y + 22))



    # === РОЗДІЛЮВАЧ ===
    pygame.draw.line(screen, (45, 7, 80),
                     (content_x + 16, content_y + 96),
                     (content_x + content_w - 16, content_y + 96), 1)


    sec_f = pygame.font.SysFont("Courier New", 10, bold=True)
    sec = sec_f.render("// OSOBYSTA INFORMATSIYA", True, (76, 29, 149))
    screen.blit(sec, (content_x + 16, content_y + 104))



    # === ІНФО РЯДКИ ===
    info_rows = [
        ("IMYA", "Vasyl", (124, 58, 237)),
        ("PRIZVYSHE", "Stepanenko", (109, 40, 217)),
        ("DATA", "14.08.2003", (91, 33, 182)),
        ("KRAINA", "Ukraina", (76, 29, 149)),
        ("NIKNEIM", "VasyaS_UA", (124, 58, 237)),
    ]



    for i, (label, value, color) in enumerate(info_rows):
        row_y = content_y + 122 + i * 46
        row_rect = pygame.Rect(content_x + 16, row_y, content_w - 32, 38)




        pygame.draw.rect(screen, (13, 0, 24), row_rect, border_radius=6)
        pygame.draw.rect(screen, (45, 7, 80), row_rect, 1, border_radius=6)



        # лівий акцент
        pygame.draw.rect(screen, color,
                         (row_rect.x, row_rect.y + 8, 2, 22), border_radius=1)


        lbl = mono.render("// " + label, True, (59, 7, 100))
        screen.blit(lbl, (row_rect.x + 12,
                          row_rect.centery - lbl.get_height() // 2))


        val = small.render(value, True, color)
        screen.blit(val, (row_rect.right - val.get_width() - 12,
                          row_rect.centery - val.get_height() // 2))






































































































































































