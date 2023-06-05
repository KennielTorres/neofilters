

'''
Converts 'duration_ms' value to minutes:seconds
Validates that 'release_date' contains the full date in ISO 8601, else it completes it
'isrc' is changed to uppercase
Removes time from 'added_at'
'''
def process_data(items):
    for item in items:
        duration_ms = item['track']['duration_ms']
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        item['track']['duration_ms'] = f"{minutes}:{seconds:02d}"

        # Release date has no month & day. Default to {release_year}-01-01
        if (len(item['track']['album']['release_date']) == 4 and len(item['track']['album']['release_date']) < 7):
            item['track']['album']['release_date'] = f"{item['track']['album']['release_date']}-01-01"
        
        # Release date has no day. Default to {release_year-release_month}-01
        if (len(item['track']['album']['release_date']) == 7 and len(item['track']['album']['release_date']) < 10):
            item['track']['album']['release_date'] = f"{item['track']['album']['release_date']}-01"

        # Forces 'isrc' to uppercase
        item['track']['external_ids']['isrc'] = (item['track']['external_ids']['isrc']).upper()

        # Removes time from 'added_at'
        item['added_at'] = item['added_at'][:10]
        
    return items
    