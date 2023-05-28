

'''
Converts 'duration_ms' value to minutes:seconds
Replaces 'added_by' with that user's 'display_name' if non-empty 
'''
def process_data(spotify, items):
    for item in items:
        duration_ms = item['track']['duration_ms']
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        item['track']['duration_ms'] = f"{minutes}:{seconds:02d}"

        if (len(item['added_by']['id']) < 1):
            item['added_by']['id'] = '' #  No user id was provided in 'added_by'
        else:
            item['added_by']['id'] = spotify.user(item['added_by']['id'])['display_name']

    return items
    