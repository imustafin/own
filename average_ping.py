""" This script calculates the average time between sending and receiving
a response from a specific server.
"""
import datetime

import requests

REQUESTS_TO = 'http://188.130.155.101:9000/ping/time'


def average_time(pings_num: int=10) -> float:
    """Average request-reponse time to a specific server in milliseconds.

    Do `pings_num` requests and calculate the mean time
    between sending a request and receiving a response.

    Parameters
    ----------
    pings_num : int, optional
        How many requests to send. Should be greater than 0.

    Returns
    -------
    float
        Mean request-response time in milliseconds
    """
    sum_waited_secs: float = 0
    for request in range(pings_num):
        before = datetime.datetime.now()
        requests.get(REQUESTS_TO)
        after = datetime.datetime.now()
        sum_waited_secs += (after - before).total_seconds()
    return (sum_waited_secs * 1000) / pings_num


if __name__ == '__main__':
    print(average_time())

