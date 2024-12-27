import neopixel

# TODO может быть не ассинхронной библиотекой

def set_color(pixels: neopixel.NeoPixel, color):
    pixels.fill(color)

async def change_color(occupied: dict, pixels: neopixel.NeoPixel):
    if occupied:
        set_color(pixels, (255, 0, 0)) # Красный
    else:
        set_color(pixels, (0, 255, 0)) # Зеленый