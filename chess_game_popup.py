import pygame

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)


def draw_button(rect, text, selected=False):
    color = BLUE if selected else GRAY
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def show_popup():
    popup_rect = pygame.Rect(250, 200, 300, 200)
    button_width, button_height = 120, 40
    spacing = 20

    # Create 4 buttons
    buttons = []
    labels = ["Queen", "Knight", "Rook", "Bishop"]
    for i in range(4):
        x = popup_rect.x + 30 + (i % 2) * (button_width + spacing)
        y = popup_rect.y + 50 + (i // 2) * (button_height + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)
        buttons.append((rect, labels[i]))

    selected_option = None
    running = True
    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, popup_rect)
        pygame.draw.rect(screen, BLACK, popup_rect, 2)

        for rect, label in buttons:
            draw_button(rect, label)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, label in buttons:
                    if rect.collidepoint(event.pos):
                        selected_option = label
                        running = False
                        break
    return selected_option
