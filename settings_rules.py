import pygame



def draw_settings_rules(screen, content_x, content_y, content_w, content_h):
    tiny = pygame.font.SysFont("Arial", 11)
    small = pygame.font.SysFont("Arial", 13, bold=True)
    mono = pygame.font.SysFont("Courier New", 11)



    # === ПРАВИЛА ===
    sec_f = pygame.font.SysFont("Courier New", 10, bold=True)
    sec = sec_f.render("// OSNOVNI PRAVYLA", True, (76, 29, 149))
    screen.blit(sec, (content_x + 16, content_y + 10))



    rules = [
        ("01", "Yizh yizhu shchob rosty", (124, 58, 237)),
        ("02", "Yizh menshykh hravtsiv", (109, 40, 217)),
        ("03", "Tikay vid bilshykh hravtsiv", (91, 33, 182)),
        ("04", "Za vbyvstvo bota otrymuesh XP", (76, 29, 149)),
        ("05", "Kpzhnyi riven = sylnishi boty", (124, 58, 237)),
        ("06", "Zaroblyay monety i kupuy skiny", (109, 40, 217)),

    ]



    for i, (num, text, color) in enumerate(rules):
        row_y = content_y + 28 + i * 50
        row_rect = pygame.Rect(content_x + 16, row_y, content_w - 32, 40)


        pygame.draw.rect(screen, (13, 0, 24), row_rect, border_radius=6)
        pygame.draw.rect(screen, (45, 7, 80), row_rect, 1, border_radius=6)



        # лівий акцент
        pygame.draw.rect(screen, color,
                         (row_rect.x, row_rect.y + 8, 2, 24), border_radius=1)



        # номер
        num_f = pygame.font.SysFont("Courier New", 13, bold=True)
        num_txt = num_f.render(num + " //", True, color)
        screen.blit(num_txt, (row_rect.x + 10,
                              row_rect.centery - num_txt.get_height() // 2))




        # текст правила
        rule_txt = small.render(text, True, (167, 139, 250))
        screen.blit(rule_txt, (row_rect.x + 70,
                               row_rect.centery - rule_txt.get_height() // 2))




    # === РЕЖИМИ ГРИ ===
    pygame.draw.line(screen, (45, 7, 80),
                     (content_x + 16, content_y + 332),
                     (content_x + content_w - 16, content_y + 332), 1)


    sec2 = sec_f.render("// REZHYMY HRY", True, (76, 29, 149))
    screen.blit(sec2, (content_x + 16, content_y + 340))






    modes = [
        ("CLASSIC", "Hray bez obmezhen chasu", (31, 163, 255)),
        ("RUSH", "Nabery masu za 60 secund", (255, 133, 26)),
    ]


    for i, (mode, desc, color) in enumerate(modes):
        row_y = content_y + 358 + i * 52
        row_rect = pygame.Rect(content_x + 16, row_y, content_w - 32, 42)



        pygame.draw.rect(screen, (13,0, 24), row_rect, border_radius=6)
        pygame.draw.rect(screen, color, row_rect, 1, border_radius=6)



        pygame.draw.rect(screen, color,
                         (row_rect.x, row_rect.y + 8, 2, 26), border_radius=1)


        mode_txt = pygame.font.SysFont("Courier New", 13, bold=True).render(
            "// " + mode, True, color)


        screen.blit(mode_txt, (row_rect.x + 12,
                               row_rect.centery - mode_txt.get_height() // 2))


        desc_txt  = tiny.render(desc, True, (76, 29, 149))
        screen.blit(desc_txt, (row_rect.right - desc_txt.get_width() - 12,
                               row_rect.centery - desc_txt.get_height() // 2))






















































































