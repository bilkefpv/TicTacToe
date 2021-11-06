from imports import *
class Ball:
    def __init__(self, size, screen, wheel):
        self.channel = pygame.mixer.find_channel(True)
        self.channel.set_volume(0.1)

        self.bounce_sound = pygame.mixer.Sound("bounce.wav")
        self.screen = screen
        self.w, self.h = size
        self.block_size = 13
        self.wheel = wheel
        self.restore()
        self.audio=True

    def mute(self):
        self.audio = not self.audio
    def restore(self):
        velocity = [choice([a for a in np.arange(2,2.65,0.15)]), choice([a for a in np.arange(2.65,3.25,0.15)])]
        multiply = self.wheel.next_state()
        velocity = [v1 * v2 for v1, v2 in zip(velocity, multiply)]
        self.velocity = velocity
        self.pos_x = self.w / 2
        self.pos_y = self.h / 2
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.block_size, self.block_size)

    def trajectory(self):
        OFFSETX = 30
        OFFSETY = 50
        pos_x, pos_y = self.pos_x, self.pos_y
        velocity_dummy = self.velocity.copy()
        while pos_x > 57:
            pos_x += velocity_dummy[0]
            pos_y += velocity_dummy[1]
            if pos_x + self.block_size > self.w + OFFSETX or pos_x < 0 + OFFSETX:
                velocity_dummy[0] = -velocity_dummy[0]

            if pos_y + self.block_size > self.h + OFFSETY or pos_y < 0 + OFFSETY:
                velocity_dummy[1] = -velocity_dummy[1]
        target = pygame.Rect(pos_x, pos_y, self.block_size, self.block_size)

        return target

    def update(self):
        OFFSETX = 30
        OFFSETY = 50
        self.pos_x += self.velocity[0]
        self.pos_y += self.velocity[1]
        val = 0
        if self.pos_x + self.block_size > self.w - OFFSETX + 26:
            val = 2
        if self.pos_x + self.block_size < OFFSETX + 26:
            val = 1
        if self.pos_x + self.block_size >= self.w + OFFSETX or self.pos_x <= 0 + OFFSETX:
            self.velocity[0] = -self.velocity[0]

        if self.pos_y + self.block_size >= self.h + OFFSETY or self.pos_y <= 0 + OFFSETY:
            self.velocity[1] = -self.velocity[1]

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.block_size, self.block_size)
        pygame.draw.rect(self.screen, white, self.rect)
        return val

    def bounce(self, vel=None):
        if self.audio:
            self.channel.play(self.bounce_sound)

        if vel:
            state_matrx = vel[1]
            vel = [a * b for a, b in zip(vel[0], state_matrx)]
            self.velocity = vel

        self.velocity[0] = -self.velocity[0]

        self.pos_x += self.velocity[0]

