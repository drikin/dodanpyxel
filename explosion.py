import pyxel
from constants import *

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1
        self.max_radius = 10
        self.growth_rate = 0.8
        self.shrink_rate = 0.4
        self.growing = True
        self.particles = []
        
        # Create particles
        for _ in range(8):
            angle = _ * (3.14159 * 2 / 8)
            import math
            dx = math.cos(angle) * 1.5
            dy = math.sin(angle) * 1.5
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'dx': dx,
                'dy': dy,
                'size': 2,
                'life': 20
            })
    
    def update(self):
        # Handle main explosion radius
        if self.growing:
            self.radius += self.growth_rate
            if self.radius >= self.max_radius:
                self.growing = False
        else:
            self.radius -= self.shrink_rate
        
        # Update particles
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 1
    
    def is_finished(self):
        return self.radius <= 0
    
    def draw(self):
        # Draw main explosion
        if self.radius > 0:
            pyxel.circ(self.x, self.y, int(self.radius), YELLOW)
            if self.radius > 3:
                pyxel.circ(self.x, self.y, int(self.radius) - 3, RED)
        
        # Draw particles
        for p in self.particles:
            if p['life'] > 0:
                size = min(p['size'], p['life'] // 4 + 1)
                pyxel.rect(int(p['x']), int(p['y']), size, size, ORANGE)
