import argparse
import asyncio
import logging
from aiopath import AsyncPath
from aioshutil import copyfile

parser = argparse.ArgumentParser(description="Sorting files")
parser.add_argument("--source", "-s", required=True, help="Source dir")
parser.add_argument("--output", "-o", required=True, help="Output dir")
args = vars(parser.parse_args())

source = AsyncPath(args["source"])
output = AsyncPath(args["output"])


async def read_folder(path: AsyncPath):
    try:
        async for file in path.iterdir():
            if await file.is_dir():
                await read_folder(file)
            else:
                await copy_file(file)
    except Exception as e:
        logging.error(f"Error while reading folder {path}: {e}")


async def copy_file(file: AsyncPath):
    folder = output / file.suffix[1:]
    try:
        await folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, folder / file.name)
    except OSError as e:
        logging.error(f"Error while copying file {file}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while copying file {file}: {e}")

if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    try:
        asyncio.run(read_folder(source))
        print(f"All files copied to {output} and sorted.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
