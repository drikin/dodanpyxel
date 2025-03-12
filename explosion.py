import pyxel
from constants import *

class Explosion:
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.radius = 1
        self.max_radius = 10
        self.growth_rate = 0.8
        self.shrink_rate = 0.4
        self.growing = True
        self.scale = scale  # 爆発の大きさスケール (初期値は引数から)
        self.particles = []
        
        # 粒子数をスケールに応じて調整
        import math
        num_particles = int(8 + (self.scale * 4))  # スケールが大きいほど粒子も増える
        
        # Create particles
        for i in range(num_particles):
            angle = i * (3.14159 * 2 / num_particles)
            speed = 1.5 * self.scale  # 速度もスケールに比例
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'dx': dx,
                'dy': dy,
                'size': int(2 * math.sqrt(self.scale)),  # サイズもスケールに応じて調整（二乗根で調整）
                'life': int(20 * self.scale)  # 寿命もスケールに比例
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
        # Draw main explosion (スケール適用)
        if self.radius > 0:
            scaled_radius = self.radius * self.scale
            pyxel.circ(self.x, self.y, int(scaled_radius), YELLOW)
            if scaled_radius > 3:
                pyxel.circ(self.x, self.y, int(scaled_radius) - 3, RED)
        
        # Draw particles (スケール適用)
        for p in self.particles:
            if p['life'] > 0:
                size = min(p['size'], p['life'] // 4 + 1) * self.scale
                # 速度もスケールに合わせる
                scaled_x = self.x + (p['x'] - self.x) * self.scale
                scaled_y = self.y + (p['y'] - self.y) * self.scale
                pyxel.rect(int(scaled_x), int(scaled_y), int(size), int(size), ORANGE)
