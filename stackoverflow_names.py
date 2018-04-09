"""
This script prints user names mentioned on a specific Stackoverflow page.

Two ideas were used:
    1. Links to user pages have user names for their text
    2. Comments have @mentions in their bodies

There are some caveats:
    1. Links can have unexpected texts
    2. It is hard to find the exact end of a @mention
       since mentions can have spaces (@Xxx Yyy)
    3. Initially, some comments can be hidden (<Show X more comments> link).
       Such comments are not present in the HTML of the page and will
       require another web request to get them. The hidden comments
       can have new user names.
"""
import re
from typing import List, Set

import requests

from bs4 import BeautifulSoup


def _extract_names_from_links(document: BeautifulSoup) -> List[str]:
    """Extract Stackoverflow user names from user page links.

    Find links to user pages and try to guess user names from the links.

    Parameters
    ----------
    document : BeautifulSoup
        A `BeautifulSoup` for the whole page

    Returns
    -------
    List[str]
        Names in no particular order
    """
    ans = set()
    links = document.select('a[href^="/users/"],'
                            'a[href^="https://stackoverflow.com/users/"]')
    for link in links:
        if ((link.get('href')
             and link.get('href').startswith('/users/signup?'))
                or (link.get('class') and 'login-link' in link.get('class'))):
            continue
        if link.string:
            ans.add(link.string)
    return list(ans)


def _extract_names_from_mentions(document: BeautifulSoup) -> List[str]:
    """Extract Stackoverflow user names from comment @mentions

    Find mentions (@Person) in comments and guess user names from them.

    Parameters
    ----------
    document : BeautifulSoup
        A `BeautifulSoup` for the whole page

    Returns
    -------
    List[str]
        Names in no particular order
    """
    ans: Set[str] = set()
    comments = document.select('span.comment-copy')
    for comment in comments:
        text = ' '.join(comment.strings)
        names = re.findall(r'@(\w+(?:\s[A-Z]\w+)*)', text)
        ans.update(names)
    return list(ans)


def extract_names_from_bs(document: BeautifulSoup) -> List[str]:
    """Extract Stackoverflow user names from BeautifulSoup instance.

    Use different methods to find names in the page.

    Parameters
    ----------
    document : BeautifulSoup
        A `BeautifulSoup` for the whole page.

    Returns
    -------
    List[str]
        Names in lexicographical, case insensitive order.

    See Also
    --------
    _extract_names_from_links, _extract_names_from_mentions
    """
    ans: Set[str] = set()
    ans.update(_extract_names_from_links(document))
    ans.update(_extract_names_from_mentions(document))
    return sorted(ans, key=lambda x: x.lower())


def extract_names_from_html(html: str) -> List[str]:
    """Extract Stackoverflow user names from HTML code.

    Use different methods to find names in the page.

    Parameters
    ----------
    html : str
        HTML code of the page to find names from.

    Returns
    -------
    List[str]
        Names in lexicographical, case insensitive order.

    See Also
    --------
    _extract_names_from_links, _extract_names_from_mentions
    """
    return extract_names_from_bs(BeautifulSoup(html, 'lxml'))


def extract_names_from_url(url: str) -> List[str]:
    """Extract Stackoverflow user names by page URL.

    Use different methods to find names in the page.

    Parameters
    ----------
    url : str
        URL of the page to find names from.

    Returns
    -------
    List[str]
        Names in lexicographical, case insensitive order.

    See Also
    --------
    _extract_names_from_links, _extract_names_from_mentions
    """
    response = requests.get(url)
    return extract_names_from_html(response.text)


if __name__ == '__main__':
    STACKOVERFLOW_PAGE = ('https://stackoverflow.com/'
                          'questions/3044620/python-vs-java'
                          '-performance-runtime-speed')
    print('\n'.join(extract_names_from_url(STACKOVERFLOW_PAGE)))

