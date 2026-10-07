import pygame
from game.deck import Deck

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.deck = Deck()

        self.current_card = self.deck.draw()
        self.next_card = None
        self.score = 0
        self.streak = 0
        self.state = "WAITING_FOR_GUESS"
        self.reveal_timer = 0
        self.status_msg = "Will the next card be HIGHER or LOWER?"
        self.status_color = (220, 220, 220)

        btn_w, btn_h = 140, 48
        self.btn_higher = pygame.Rect(width // 2 - btn_w - 20, height - 90, btn_w, btn_h)
        self.btn_lower = pygame.Rect(width // 2 + 20, height - 90, btn_w, btn_h)

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 24)

    def evaluate_guess(self, guess):
        if self.state != "WAITING_FOR_GUESS":
            return
            
        """Draws next card and evaluates prediction."""
        self.next_card = self.deck.draw()
        
        if self.next_card.numeric_rank == self.current_card.numeric_rank:
            self.status_msg = f"PUSH! {self.next_card.rank_str} equals {self.current_card.rank_str}"
            self.status_color = (220, 220, 80)
        else:
            if guess == "HIGHER":
                correct = self.next_card.numeric_rank > self.current_card.numeric_rank
            else:
                correct = self.next_card.numeric_rank < self.current_card.numeric_rank
            
            if correct:
                self.streak += 1
                self.score += self.streak
                self.status_msg = f"CORRECT! {self.next_card.rank_str} vs {self.current_card.rank_str}"
                self.status_color = (80, 220, 80)
            else:
                self.streak = 0
                self.score = max(0, self.score - 1)
                self.status_msg = f"WRONG! {self.next_card.rank_str} vs {self.current_card.rank_str}"
                self.status_color = (235, 75, 75)

        self.state = "REVEALING"
        self.reveal_timer = pygame.time.get_ticks()

    def handle_event(self, event):
        if self.state != "WAITING_FOR_GUESS":
            return
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_higher.collidepoint(event.pos):
                self.evaluate_guess("HIGHER")
            elif self.btn_lower.collidepoint(event.pos):
                self.evaluate_guess("LOWER")

    def update(self):
        if self.state == "REVEALING":
            if pygame.time.get_ticks() - self.reveal_timer > 1000:
                self.current_card = self.next_card
                self.next_card = None
                self.state = "WAITING_FOR_GUESS"

    def render(self, screen):
        screen.fill((25, 80, 45))

        title_surf = self.font_title.render("High-Low Card Predictor", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 25))

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (30, 30))
        
        streak_surf = self.font_medium.render(f"Streak: {self.streak}x", True, (255, 220, 80))
        screen.blit(streak_surf, (30, 60))

        rem_surf = self.font_small.render(f"Deck: {self.deck.remaining} left", True, (210, 210, 210))
        screen.blit(rem_surf, (self.width - rem_surf.get_width() - 30, 35))

        card_w, card_h = 130, 180
        if self.state == "WAITING_FOR_GUESS":
            self.current_card.render(screen, self.width // 2 - card_w // 2, 100, card_w, card_h)
        else:
            self.current_card.render(screen, self.width // 2 - card_w - 10, 100, card_w, card_h)
            if self.next_card:
                self.next_card.render(screen, self.width // 2 + 10, 100, card_w, card_h)

        status_surf = self.font_small.render(self.status_msg, True, self.status_color)
        screen.blit(status_surf, (self.width // 2 - status_surf.get_width() // 2, 310))

        if self.state == "WAITING_FOR_GUESS":
            btn_high_bg = (40, 140, 60)
            btn_low_bg = (170, 50, 50)
            btn_border = (220, 220, 220)
            text_color = (255, 255, 255)
        else:
            btn_high_bg = (100, 120, 100)
            btn_low_bg = (120, 100, 100)
            btn_border = (150, 150, 150)
            text_color = (180, 180, 180)

        pygame.draw.rect(screen, btn_high_bg, self.btn_higher, border_radius=8)
        pygame.draw.rect(screen, btn_border, self.btn_higher, width=2, border_radius=8)
        high_surf = self.font_medium.render("HIGHER", True, text_color)
        screen.blit(
            high_surf,
            (self.btn_higher.centerx - high_surf.get_width() // 2, self.btn_higher.centery - high_surf.get_height() // 2),
        )

        pygame.draw.rect(screen, btn_low_bg, self.btn_lower, border_radius=8)
        pygame.draw.rect(screen, btn_border, self.btn_lower, width=2, border_radius=8)
        low_surf = self.font_medium.render("LOWER", True, text_color)
        screen.blit(
            low_surf,
            (self.btn_lower.centerx - low_surf.get_width() // 2, self.btn_lower.centery - low_surf.get_height() // 2),
        )
