import pyxel
import random
from constants import *

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.2, 1.0)
        self.brightness = random.choice([GRAY, WHITE])
    
    def update(self):
        self.y += self.speed * SCROLL_SPEED
        
        # Reset star when it goes off-screen
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def draw(self):
        pyxel.pset(int(self.x), int(self.y), self.brightness)

class Background:
    def __init__(self):
        # Create stars
        self.stars = [Star() for _ in range(50)]
        
        # Create distant planets
        self.planets = []
        for _ in range(2):
            self.planets.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-100, SCREEN_HEIGHT),
                'radius': random.randint(10, 20),
                'color': random.choice([NAVY, PURPLE, DARK_BLUE]),
                'speed': 0.1
            })
    
    def update(self):
        # Update stars
        for star in self.stars:
            star.update()
        
        # Update planets
        for planet in self.planets:
            planet['y'] += planet['speed'] * SCROLL_SPEED
            
            # Reset planets when they go off-screen
            if planet['y'] - planet['radius'] > SCREEN_HEIGHT:
                planet['y'] = -planet['radius'] * 2
                planet['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw(self):
        # Draw background color
        pyxel.cls(BLACK)
        
        # Draw stars
        for star in self.stars:
            star.draw()
        
        # Draw planets
        for planet in self.planets:
            pyxel.circ(
                int(planet['x']), 
                int(planet['y']), 
                planet['radius'], 
                planet['color']
            )
            
            # Draw a highlight on the planet
            pyxel.circ(
                int(planet['x']) - planet['radius'] // 3, 
                int(planet['y']) - planet['radius'] // 3, 
                planet['radius'] // 4, 
                LIGHT_BLUE
            )
