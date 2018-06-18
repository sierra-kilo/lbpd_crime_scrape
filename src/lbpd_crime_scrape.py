# lbpd_crime_scrape.py
# software built to scrape the Long Beach Police Dept Crime map
# with a user input date range

from urllib.request import urlopen as uReq
import json, time

def create_export_file():
    ts = str(time.time()).replace('.', '_')
    filename = ts + '.csv'
    f = open(filename, 'w')
    headers = 'CRIME, TIME, LOCATION, CITY\n'
    f.write(headers)
    print('Your file: ' + filename + ' is ready!')
    return f

def export_data(f, crime, time, location, city):
    f.write(crime + ',' + time + ',' + location + ',' + city + '\n')

def intro():
    print()
    print('Crime Scrape: enter start and end date to get data')
    print('on crime stats for the city of Long Beach')
    print()

def get_year():
    year = input("Enter 4 digit year ex 2018: ")
    return year

def get_month():
    month = input('Enter 2 digit month ex 01: ')
    return month

def get_day():
    day = input('Enter 2 digit date ex 01: ')
    return day

def start_date():
    print("---START DATE---")
    year = get_year()
    month = get_month()
    day = get_day()
    start_date = year + '-' + month + '-' + day
    return start_date

def end_date():
    print("---END DATE---")
    year = get_year()
    month = get_month()
    day = get_day()
    end_date = year + '-' + month + '-' + day
    return end_date

def get_url():
    start = start_date()
    end = end_date()
    #ajax url found in developer tools under network tab
    my_url = 'https://services6.arcgis.com/yCArG7wGXGyWLqav/arcgis/rest/services/Police_Crime_Mapping/FeatureServer/0/query?f=json&where=((REPORTED_DATE_TIME%20BETWEEN%20%27' + start + '%2008%3A00%3A00%27%20AND%20%27' + end + '%2007%3A59%3A59%27))&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A-20037508.342788905%2C%22ymin%22%3A-1199589.7175994702%2C%22xmax%22%3A20037508.342788905%2C%22ymax%22%3A12263111.200208541%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=UCR_LABEL%2CREPORTED_DATE_TIME%2CDR%2CLOCATION%2CCITY%2CDIVISION%2CBEAT%2CRD%2COBJECTID&orderByFields=OBJECTID%20ASC&outSR=102100'
    return my_url

# get data and write to file
def guts(f, crime_data_all):
        # loop through and print crime type
        for index in range(len(crime_data_all)):
            crime = crime_data_all[index]['attributes']['UCR_LABEL']
            time =str( crime_data_all[index]['attributes']['REPORTED_DATE_TIME'])
            location = crime_data_all[index]['attributes']['LOCATION']
            city = crime_data_all[index]['attributes']['CITY']
            # print(crime, time, location, city)
            # export data duh
            export_data(f, crime, time, location, city)

def main():
    intro()
    my_url = get_url()
    # connect to url
    u_client = uReq(my_url)
    # get all data from url
    raw_total_data = u_client.read()
    # close file
    u_client.close()
    # extract crime data
    parsed_total_data = json.loads(raw_total_data)
    crime_data_all = parsed_total_data['features']
    # create csv file
    f = create_export_file()
    # get data and export
    guts(f, crime_data_all)
    # close file
    f.close()

main()
