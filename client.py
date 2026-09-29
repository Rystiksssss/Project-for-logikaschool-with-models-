import pygame
import requests




def draw_auth_screen(screen, WIDTH, HEIGHT, image, log_btn, reg_btn):
    tiny_font = pygame.font.SysFont("Arial", 13)
    small_font = pygame.font.SysFont("Arial", 15, bold=True)
    sth_font = pygame.font.SysFont("Courier New", 14, bold=True)


    screen.blit(image, (0, 0))
    screen.blit(log_btn, (WIDTH // 2 - 600 // 2 - 200, HEIGHT // 2 - 320 // 2 - 80))
    screen.blit(reg_btn, (WIDTH // 2 - 600 // 2 + 200, HEIGHT // 2 - 420 // 2 - 30))





    rect_log_btn = pygame.Rect(WIDTH // 2 - 600 // 2 - 200, HEIGHT // 2 - 300 // 2 - 80, 600, 300)
    rect_reg_btn = pygame.Rect(WIDTH // 2 - 600 // 2 + 200, HEIGHT // 2 - 400 // 2 - 10, 600, 400)


    return rect_log_btn, rect_reg_btn






def draw_login_screen(screen, WIDTH, HEIGHT, login_bg, nickname_box, password_box, login_btn, backs_btn, ramka1):


    screen.blit(login_bg, (0, 0))

    #############
    offset_x = (400 - 300) // 2
    offset_y = (200 - 50) // 2
    ###############
    screen.blit(ramka1, (nickname_box.rect.x - offset_x, nickname_box.rect.y - offset_y))
    nickname_box.draw(screen)

    ##############

    screen.blit(ramka1, (password_box.rect.x - offset_x, password_box.rect.y - offset_y))
    password_box.draw(screen)


    #############
    screen.blit(login_btn, (WIDTH // 2 - login_btn.get_width() // 2, HEIGHT // 2 - login_btn.get_height() // 2 + 100))
    rect_login_btn = pygame.Rect(WIDTH // 2 - login_btn.get_width() // 2, HEIGHT // 2 - login_btn.get_height() // 2 + 100, 400, 200)
    screen.blit(backs_btn, (-40, -60))
    rect_backs_btn = pygame.Rect(-40, -60, 400, 200)

    return rect_login_btn, rect_backs_btn



def draw_registration_screen(screen, WIDTH, HEIGHT, reg_bg, name_box, przv_box, date_box, nickname2_box, password2_box,
                             password3_box, login_btn, backs_btn, ramka1):


    screen.blit(reg_bg, (0, 0))
    ###############################
    offset_x = (400 - 300) // 2
    offset_y = (200 - 50) // 2

    ##############################

    screen.blit(ramka1, (name_box.rect.x - offset_x, name_box.rect.y - offset_y))
    name_box.draw(screen)


    ##################################
    screen.blit(ramka1, (przv_box.rect.x - offset_x, przv_box.rect.y - offset_y))
    przv_box.draw(screen)

    #######################################
    screen.blit(ramka1, (date_box.rect.x - offset_x, date_box.rect.y - offset_y))
    date_box.draw(screen)


    ##############################################
    screen.blit(ramka1, (nickname2_box.rect.x - offset_x, nickname2_box.rect.y - offset_y))
    nickname2_box.draw(screen)


    #########################
    screen.blit(ramka1, (password2_box.rect.x - offset_x, password2_box.rect.y - offset_y))
    password2_box.draw(screen)



    ###################################
    screen.blit(ramka1, (password3_box.rect.x - offset_x, password3_box.rect.y - offset_y))
    password3_box.draw(screen)




    ############################
    screen.blit(login_btn, (WIDTH // 2 - login_btn.get_width() // 2, HEIGHT // 2 - login_btn.get_height() // 2 + 260))
    rect_login_btn = pygame.Rect(WIDTH // 2 - login_btn.get_width() // 2,
                                 HEIGHT // 2 - login_btn.get_height() // 2 + 260, 400, 200)

    screen.blit(backs_btn, (-40, -60))
    rect_backs_btn = pygame.Rect(-40, -60, 400, 200)



    return rect_login_btn, rect_backs_btn