from datetime import datetime


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

'''
Sorts the objects by 'release_date'
Valid for ascending or descending order
'''
def sort_by_rel(response, reverse):
    def get_date_key(obj):
        date_str = obj['track']['album']['release_date']
        # Contains full date (Year-Month-Day)
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            pass
        # Contains partial date (Year-Month)
        try:
            return datetime.strptime(date_str, '%Y-%m')
        except ValueError:
            pass
        # Contains partial date (Year)
        try:
            return datetime.strptime(date_str, '%Y')
        except ValueError:
            pass

        raise ValueError("Invalid date format: {}".format(date_str))

    if not reverse:
        return sorted(response, key=get_date_key)
    else:
        return sorted(response, key=get_date_key, reverse=True)
