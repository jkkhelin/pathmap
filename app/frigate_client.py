"""This module provides functions related to integrating with the
Frigate service. Namely, fetch_events gets retrieves event data, and
extract_detections converts it into a list of individual detections
or object path data points that we are interested in."""

import time, httpx

from detection_class import Detection

def fetch_events(url):
    """Get "person" events from Frigate from the last 24 hours.
    
    Args:
        url (str): Frigate base url (eg. http://frigate.local:5000).

    Returns:
        dict: retrieved event data.
    """
    after = int(time.time()) - 24 * 3600
    params = {
        'label': 'person',
        'limit': 1000,
        'after': after
    }
    headers = {
        'Accept': 'application/json'
    }

    r = httpx.get(url + '/api/events', params=params, headers=headers)
    return r.json()

def extract_detections(events):
    """Extract detection data from raw event data.

    Args:
        events: event data.

    Returns:
        list: list of detections related to the events.
    """
    return [
        Detection(event['camera'], step[0])
        for event in events
        for step in event['data']['path_data']
    ]
