import requests
from bs4 import BeautifulSoup
import re
from subprocess import run

def get_contributions_data_per_day(username: str, year: int):
    url = f"https://github.com/users/{username}/contributions?tab=overview&from={year}-01-01&to={year}-12-31"
    # backup_url = f"https://github.com/{username}?tab=overview&from={year}-01-01&to={year}-12-31"

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


def generate_bash_script_linux_macos(contributions_list: list):
    bash_script = open('script.sh', 'w')
    for each_day_data in contributions_list:
        script = f"""GIT_AUTHOR_DATE={each_day_data['date']}T12:00:00 GIT_COMMITER_DATE={each_day_data['date']}T12:00:00 git commit --allow-empty -m "Rewriting History!" > /dev/null\n"""
        for each_contribution in range(each_day_data['contributions']):
            bash_script.write(script)
    bash_script.write("git pull origin main\n") 
    bash_script.write("git push -f origin main")
    bash_script.close()


if __name__ == "__main__":

    username = str(input("Enter Github username for which you'd like to sync contributions: "))
    year = int(input("Enter year for which you'd like to sync contributions: "))

    contributions_list, total_contributions = get_contributions_data_per_day(username=username, year=year)
    print(f"Total Contribution to be synced: {total_contributions}")

    generate_bash_script_linux_macos(contributions_list=contributions_list)
    print("Script successfully generated!!!!")

    is_execute = input("Do you want to execute the generated script ? (Y/n): ")
    if is_execute == 'Y' or is_execute == 'y':
        run(['sh', 'script.sh'])
