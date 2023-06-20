from scaledrivers import scale, mettlertoledo
import asyncio

async def main():
    scale = mettlertoledo.MettlerToledo("COM5")
    cin = input()
    while cin != 'q':
        print(await scale.send_receive(cin))
        cin = input()

if __name__ == "__main__":
    asyncio.run(main())