import pygame



def draw_legendary_screen(screen, WIDTH, HEIGHT, backs_btn, background_shop, legendary_boost1, legendary_boost2, legendary_boost3, skins, loaded_skins, owned_skins, player, rarity_colors, coins, gems, ramka2, ramka4, LEGENDARY_SCROLL):
    screen.blit(background_shop, (0, 0))
    screen.blit(backs_btn, (0, 100))
    back_rect = pygame.Rect(0, 100, 400, 200)

    # Boosters

    font = pygame.font.SysFont("Impact", 30, bold=False)


    #1
    screen.blit(legendary_boost1, (0, 270))
    screen.blit(ramka4, (20, 470))
    txt = font.render("Price: 200 000", True, (0, 0, 0))
    screen.blit(txt, (80, 545))


    #2
    screen.blit(legendary_boost2, (1230, 70))
    screen.blit(ramka4, (1250, 270))
    txt = font.render("Price: 300 000", True, (0, 0, 0))
    screen.blit(txt, (1310, 345))





    #3
    screen.blit(legendary_boost3, (1230, 470))
    screen.blit(ramka4, (1250, 670))
    txt = font.render("Price: 400 000", True, (0, 0, 0))
    screen.blit(txt, (1310, 745))





    # ramku

    screen.blit(ramka2, (WIDTH // 2 - 280, -60))
    font = pygame.font.SysFont("Impact", 30, bold=False)
    txt = font.render(f"Coins: {coins} Gems: {gems}", True, (0, 0, 0))
    screen.blit(txt,
                (WIDTH // 2 - txt.get_width() // 2 + 40, 10 + ramka2.get_height() // 2 - txt.get_height() // 2 - 68))



    legendary_skins = [(n, d) for n, d in skins.items() if d.get("rarity") == "legendary"]

    COLS = 3
    ROWS = 10
    CARD_W = 250
    CARD_H = 350
    H_GAP = 20
    V_GAP = 120
    total_w = COLS * CARD_W + (COLS - 1) * H_GAP
    total_h = ROWS * CARD_H + (ROWS - 1) * V_GAP
    x_start = WIDTH // 2 - total_w // 2
    y_start = 0 + 130



    skin_rects = []


    for i, (name, data) in enumerate(legendary_skins):
        col = i % COLS
        row = i // COLS
        cx = x_start + col * (CARD_W + H_GAP)
        cy = y_start + row * (CARD_W + V_GAP) + LEGENDARY_SCROLL




        card = pygame.Rect(cx, cy, CARD_W, CARD_H)
        pygame.draw.rect(screen, (20, 0, 36), card, border_radius=12)
        pygame.draw.rect(screen, (255, 100, 200), card, 2, border_radius=12)



        img = loaded_skins[name]
        scaled = pygame.transform.smoothscale(img, (100, 100))



        mask = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (50, 50), 50)
        scaled.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(scaled, (cx + CARD_W // 2 - 50, cy + 50))



        font = pygame.font.SysFont("Impact", 28, bold=False)
        txt = font.render(name, True, (255, 100, 200))
        screen.blit(txt, (cx + CARD_W // 2 - 30, cy + CARD_H // 2 + 40))



        text_rect = pygame.Rect(cx + CARD_W // 2 - 60, cy + CARD_H // 2 + 90, 120, 35)
        pygame.draw.rect(screen, (255, 100, 200), text_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 0, 155), text_rect, 2, border_radius=12)



        if name == player.skin:
            txt = font.render("SELECTED", True, (255, 255, 255))
        elif name in owned_skins:
            txt = font.render("SELECT", True, (255, 255, 255))
        else:
            txt = font.render("BUY", True, (255, 255, 255))




        screen.blit(txt, (text_rect.centerx - txt.get_width() // 2, text_rect.centery - txt.get_height() // 2))



        price_txt = font.render(f"Price: {data['price']}", True, (255, 215, 0))
        screen.blit(price_txt, (cx + CARD_W // 2 - price_txt.get_width() // 2 - 40 + 30, cy + CARD_H // 2 + 135))







        skin_rects.append((text_rect, name))


        if name == player.skin:
            badge_txt = font.render("ON", True, (0, 255, 100))
            badge_x = card.right - 55
            badge_y = card.top + 5
            screen.blit(badge_txt, (badge_x, badge_y))

        elif name in owned_skins:
            badge_txt = font.render("OWN", True, (100, 200, 255))
            screen.blit(badge_txt, (card.right - 55, card.top + 5))



    return back_rect, skin_rects






























