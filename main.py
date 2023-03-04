import requests
from bs4 import BeautifulSoup
import re

def get_contributions_data_per_day(username: str, year: int):
    url = f"https://github.com/users/{username}/contributions?tab=overview&from={year}-01-01&to={year}-12-31"

    resp = requests.get(url).content
    data = BeautifulSoup(resp, 'html.parser')

    daily_contributions_list = []
    total_contributions = 0
    for each_day_data in data.find_all('rect'):
        if int(each_day_data['data-level']) > 0 and 'data-date' in each_day_data.attrs.keys():
            number_of_contributions = int(re.findall('^[^\d]*(\d+)', each_day_data.string)[0])
            date = each_day_data['data-date']
            daily_contributions_list.append({'date': date, 'contributions': number_of_contributions })
            total_contributions += number_of_contributions
    
    
    return daily_contributions_list, total_contributions


if __name__ == "__main__":

    username = str(input("Enter Github username for which you'd like to sync contributions: "))
    year = int(input("Enter year for which you'd like to sync contributions: "))
    contributions_list, total_contributions = get_contributions_data_per_day(username=username, year=year)

