import asyncio
from core import *


async def main():
    test_peer = PunchyPeer(port=8989)
    test_peer.deploy()
    while True:
        task = input('[cli]: ')
        await test_peer.send_text(task)


if __name__ == '__main__':
    asyncio.run(main())
