# Code from GitHub. May be useful later, but currently has no use.

def main():
    import asyncio
    import sartorius

    async def get():
        async with sartorius.Scale('scale-ip.local') as scale:
            await scale.zero()             # Zero and tare the scale
            print(await scale.get())       # Get mass, units, stability
            print(await scale.get_info())  # Get model, serial, software version

    asyncio.run(get())

if __name__ == '__main__':
    main()