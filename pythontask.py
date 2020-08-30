import pandas as pd
import json
import requests
import datetime
from math import floor


###### <><><><><><><><><><><><><><><><><><><><><> Task 1 <><><><><><><><><><><><><><><><><><><><> ######


##### Collect the url for the month of July-2020 and store into list
url_list = ["https://rata.digitraffic.fi/api/v1/trains/2020-07-" + ("0" + str(i)) + "/4" 
            if len(str(i)) == 1
            else "https://rata.digitraffic.fi/api/v1/trains/2020-07-" +  str(i) + "/4"
            for i in range(1,32)]
##print(url_list)


#### collect the json data from each url of list
#### normlize the each json data into dataframe
#### store each dataframe into list
data_list = [pd.DataFrame(pd.json_normalize(data=requests.get(url).json(),
                                            record_path=['timeTableRows'],
                                            meta=['trainNumber', 'departureDate', 'operatorUICCode',
                                                  'operatorShortCode','trainType', 'trainCategory',
                                                  'commuterLineID', 'runningCurrently','cancelled',
                                                  'version', 'timetableType', 'timetableAcceptanceDate'],
                                            record_prefix=' ',
                                            max_level=1))
    for url in (url_list)]
##print(data_list)


#### add each dataframe from the list into final dataframe
finaldf = pd.DataFrame()
for i in data_list:
    finaldf = finaldf.append(i).reset_index(drop=True)


#### trim the spaces from the column names of final dataframe
finaldf.columns = finaldf.columns.str.replace(' ', '')
##print(finaldf)


#### export the dataframe in csv format    
finaldf.to_csv('D:/Personal/DreamLand/Resume/Accenture Latvia/output/output.csv')


###### <><><><><><><><><><><><><><><><><><><><><> Task 2 <><><><><><><><><><><><><><><><><><><><> ######


#### filter dataframe with destination code and type
#### extract the time from actualTime column and store it in list
act_time = [i for i in finaldf[(finaldf['stationUICCode']==1) & (finaldf['type']=='ARRIVAL')]['actualTime'].apply(lambda x: x[11:-5])]
##print(act_time)


#### convert each time into seconds and sum it
sum_seconds = sum(map(lambda i: int(i[0])*3600 + int(i[1])*60 + int(i[2]), map(lambda x: x.split(':'), act_time)))


#### average of total time in seconds
avg_seconds = sum_seconds / len(act_time)


#### convert seconds into hours, minutes and socond
avg_time = str(floor(avg_seconds/3600)) + ' ' + str(floor((avg_seconds%3600)/60)) + ' ' + str(floor(avg_seconds%60))


#### convert avg_time into proper time format
act_avg_time = datetime.datetime.strptime(avg_time, "%H %M %S").time()

print("The average actual arrival time of train number 4 for the month of July-2020 is ", act_avg_time)
