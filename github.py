"""
This script uses GitHub API to find top 5 popular repos
"""
from typing import Dict, List, Optional

import requests

API_BASE = 'https://api.github.com/'


def search_repositories(query: str, sort_by: Optional[str]=None) -> Dict:
    """/search/repositories API request for searching repositories.

    API doc:
    https://developer.github.com/v3/search/#search-repositories

    Parameters
    ----------
    query : str
        The search keywords, as well as any GitHub qualifiers
    sort_by : {`None`, 'stars', 'forks', 'updated'}, optional
        The sort field. `None` for default best match

    Returns
    -------
    Dict
        GitHub API response
    """
    url = API_BASE + 'search/repositories'
    params = {'q': query}
    if sort_by is not None:
        params['sort'] = sort_by
    response = requests.get(url, params=params)
    return response.json()


def top_repos(keywords: str, num: int=5) -> List[str]:
    """URLs of the top popular repos by keywords.

    Top `num` GitHub repositories by GitHub *stars*.

    Parameters
    ----------
    keywords : str
        The search keywords.
    num : int, optional
        How many repositories to return

    Returns
    -------
    List[str]
        Repository URLs from the most popular, to least popular
    """
    results = search_repositories(keywords, 'stars')
    return [x['url'] for x in results['items'][:num]]


if __name__ == '__main__':
    print(top_repos('java language'))

