from ursina import *
from math import sin, cos, radians
from random import uniform

app = Ursina()

window.title = "3D Solar System Simulator"
window.color = color.black
window.fps_counter.enabled = True

# -------------------------------------------------
# CAMERA
# -------------------------------------------------

EditorCamera(rotation_speed=200, panning_speed=20)

# -------------------------------------------------
# LIGHTING
# -------------------------------------------------

sun_light = PointLight(parent=scene, color=color.white)
sun_light.position = (0,0,0)

AmbientLight(color=color.rgba(100,100,100,0.35))

# -------------------------------------------------
# STARS
# -------------------------------------------------

for i in range(2000):

    Entity(
        model='sphere',
        scale=0.08,
        color=color.white,
        position=(
            uniform(-250,250),
            uniform(-250,250),
            uniform(-250,250)
        )
    )

# -------------------------------------------------
# SUN
# -------------------------------------------------

sun = Entity(
    model='sphere',
    color=color.yellow,
    scale=4
)

# Glow

Entity(
    parent=sun,
    model='sphere',
    color=color.rgba(255,255,0,40),
    scale=5
)

# -------------------------------------------------
# PLANET CLASS
# -------------------------------------------------

class Planet(Entity):
    def __init__(self, name, radius, orbit_radius, orbit_speed, planet_color):
        
        super().__init__(
    model='sphere',
    color=planet_color,
    scale=radius
)

        self.name=name
        self.orbit_radius=orbit_radius
        self.orbit_speed=orbit_speed
        self.angle=0

        Text(
            text=name,
            parent=self,
            y=1.3,
            scale=8,
            billboard=True
        )

        # Orbit Ring
        Entity(
    model=Mesh(
        vertices=[
            Vec3(
                cos(radians(a)) * orbit_radius,
                0,
                sin(radians(a)) * orbit_radius
            )
            for a in range(361)
        ],
        mode='line'
    ),
    color=color.rgba(255, 255, 255, 80)
)
# -------------------------------------------------
# MOON
# -------------------------------------------------

class Moon(Entity):

    def __init__(self,parent_planet,radius,orbit_radius,orbit_speed,moon_color):

        super().__init__(
            model='sphere',
            color=moon_color,
            scale=radius
        )

        self.parent_planet=parent_planet
        self.orbit_radius=orbit_radius
        self.orbit_speed=orbit_speed
        self.angle=0

# -------------------------------------------------
# PLANETS
# -------------------------------------------------

mercury=Planet("Mercury",0.4,6,95,color.gray)

venus=Planet("Venus",0.7,9,70,color.orange)

earth=Planet("Earth",0.8,13,55,color.azure)

mars=Planet("Mars",0.6,17,45,color.red)

jupiter=Planet("Jupiter",1.8,24,25,color.orange)

saturn=Planet("Saturn",1.5,32,18,color.gold)

uranus=Planet("Uranus",1.2,40,13,color.cyan)

neptune=Planet("Neptune",1.2,48,10,color.blue)

planets=[
    mercury,
    venus,
    earth,
    mars,
    jupiter,
    saturn,
    uranus,
    neptune
]

# -------------------------------------------------
# SATURN RING
# -------------------------------------------------

Entity(
    parent=saturn,
    model='circle',
    color=color.rgba(220,220,180,180),
    scale=(2.8,2.8),
    rotation_x=90
)

# -------------------------------------------------
# MOONS
# -------------------------------------------------

moons=[

Moon(earth,.18,1.6,180,color.white),

Moon(mars,.12,1.0,240,color.gray),

Moon(mars,.10,1.6,180,color.light_gray),

Moon(jupiter,.25,2.4,150,color.white),

Moon(jupiter,.22,3.2,120,color.gray),

Moon(jupiter,.20,4.0,100,color.azure),

Moon(jupiter,.18,5.0,80,color.light_gray),

Moon(saturn,.22,2.8,90,color.orange),

Moon(uranus,.18,2.2,80,color.cyan),

Moon(neptune,.18,2.0,90,color.white)

]

# -------------------------------------------------
# UPDATE
# -------------------------------------------------

def update():

    sun.rotation_y += 5*time.dt

    for planet in planets:

        planet.angle += planet.orbit_speed*time.dt

        planet.x = cos(radians(planet.angle))*planet.orbit_radius
        planet.z = sin(radians(planet.angle))*planet.orbit_radius

        planet.rotation_y += 60*time.dt

    for moon in moons:

        moon.angle += moon.orbit_speed*time.dt

        moon.x = moon.parent_planet.x + cos(radians(moon.angle))*moon.orbit_radius
        moon.z = moon.parent_planet.z + sin(radians(moon.angle))*moon.orbit_radius

        moon.rotation_y += 180*time.dt

app.run()