

'''
Converts 'duration_ms' value to minutes:seconds
Removes time from 'added_at'
'''
def process_data(items):
    for item in items:
        duration_ms = item['track']['duration_ms']
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        item['track']['duration_ms'] = f"{minutes}:{seconds:02d}"

        # Removes time from 'added_at'
        item['added_at'] = item['added_at'][:10]
        
    return items

