import asyncio
from utils.pixel import change_color
import board
import neopixel

async def main():
    LED_COUNT = 4
    LED_PIN = board.D12
    pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT)

    await change_color(None, pixels)

if __name__ == "__main__":
    asyncio.run(main())
