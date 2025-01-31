from googlesearch import search

def get_relavant_links(query: str):
    return list(search(query,  num_results=3, unique=True, lang="ru"))