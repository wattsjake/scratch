from scaledrivers import scale, mettlertoledo
import asyncio

async def print_send_receive(scale: scale.Scale, command: str):
    cin = await scale.send_receive(command)
    print(cin)

async def main():
    scale = mettlertoledo.MettlerToledo("COM5")
    cin = input()
    while cin != 'q':
        await print_send_receive(scale, cin)
        cin = input()

if __name__ == "__main__":
    asyncio.run(main())