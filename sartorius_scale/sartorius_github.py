import asyncio
import sartorius

async def get():
    async with sartorius.Scale('scale-ip.local') as scale:
        await scale.zero()             # Zero and tare the scale
        print(await scale.get())       # Get mass, units, stability
        print(await scale.get_info())  # Get model, serial, software version

asyncio.run(get())