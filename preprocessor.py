# we put all the preprocessing data code
import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    datetime_strings = dates

    def convert_datetime_string(datetime_string):
        # Step 1: Remove extra spaces and the trailing dash
        datetime_string = datetime_string.strip().rstrip('-')

        # Step 2: Convert to datetime object using pd.to_datetime
        datetime_obj = pd.to_datetime(datetime_string, format='%m/%d/%y, %H:%M ')
        # Step 3: Format the datetime object to the desired output format
        formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_datetime

    # Use list comprehension to apply the conversion function to all date and time strings
    converted_datetimes = [convert_datetime_string(dt_str) for dt_str in datetime_strings]

    df = pd.DataFrame({'user_message': messages, 'message_date': converted_datetimes})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%Y-%m-%d %H:%M:%S')

    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['User'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year  # .dt._is the atribute
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period']=period
    return df