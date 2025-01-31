from googlesearch import search
from typing import Union, List
import re
import aiohttp
import asyncio
from markdownify import markdownify
import requests
import aiohttp

def get_relavant_links(query: str):
    return list(search(query,  num_results=3, unique=True, lang="ru"))


# async def fetch_url(url):
#   async with aiohttp.ClientSession() as session:
#     async with session.get(url) as response:
#       if response.status == 200:
#         data = await response.text()
#         markdown_content = markdownify(data).strip()

#         markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
#         return ' '.join(markdown_content.split())[:250_000]
#       else:
#         print(f"Error fetching {url}: {response.status}")
#         return None
      

# async def parse_page_content(urls: List[str]) -> Union[str, None]:
#     tasks = [asyncio.create_task(fetch_url(url)) for url in urls]
#     return await asyncio.gather(*tasks)

async def parse_page_content(url: str, session: aiohttp.ClientSession) -> Union[str, None]:
    try:
        async with session.get(url, timeout=7) as response:
            if response.status in (402, 403):
                return None
            response.raise_for_status()
            html = await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

    markdown_content = await asyncio.to_thread(
        lambda: markdownify(html).strip()
    )
    markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
    return  ' '.join(markdown_content.split())[:250_000]

async def get_sources_and_context(query, logger):
    links = get_relavant_links(query)

    await logger.info(f"{links}")

    try:
        async with aiohttp.ClientSession() as session:
            tasks = [parse_page_content(url, session) for url in links]
            contexts = await asyncio.gather(*tasks)

    except Exception as e:
         await logger.error(e)

    return [contexts, links]