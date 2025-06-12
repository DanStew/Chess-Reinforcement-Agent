import pygame

pygame.init()

# Screen setup
screen = pygame.display.set_mode((340, 340))
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)

# Object to get the images
images = {
    "Queen": "./images/queen.png",
    "Knight": "./images/knight.png",
    "Rook": "./images/rook.png",
    "Bishop": "./images/bishop.png",
}


def draw_button(rect, text, selected=False):
    color = BLUE if selected else GRAY
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    imageSrc = images[text]
    image = pygame.image.load(imageSrc).convert_alpha()
    scaled_image = pygame.transform.scale(image, (120, 120))
    screen.blit(
        scaled_image,
        (
            rect.x + 10,
            rect.y + 10,
        ),
    )


def show_popup():
    popup_rect = pygame.Rect(0, 0, 340, 340)
    button_width, button_height = 140, 140
    spacing = 20

    # Create 4 buttons
    buttons = []
    labels = ["Queen", "Knight", "Rook", "Bishop"]
    for i in range(4):
        x = popup_rect.x + 20 + (i % 2) * (button_width + spacing)
        y = popup_rect.y + 20 + (i // 2) * (button_height + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)
        buttons.append((rect, labels[i]))

    selected_option = None
    running = True
    while running:
        pygame.draw.rect(screen, GRAY, popup_rect)

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
