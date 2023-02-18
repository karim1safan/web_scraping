import requests
from bs4 import BeautifulSoup
import csv
import termcolor

print("-" * 80)
print(termcolor.colored("Hello In My Programme", color="green"))
print(
    termcolor.colored(
        "Enter The Date Of The Match And I Will Show You The Match Game Time",
        color="green",
    )
)
print(termcolor.colored("The Follwing Formate is MM/DD/YYY", color="red"))
print("-" * 80)

date = input("Enter The Date : ")

page = requests.get(f"https://www.yallakora.com/Match-Center/?data={date}")


def main(page):

    src = page.content
    soup = BeautifulSoup(src, "lxml")
    match_details = []  # add match info

    championships = soup.find_all("div", {"class": "matchCard"})

    def get_match_info(championships):

        championship_title = championships.contents[1].find("h2").text.strip()
        all_matches = championships.contents[3].find_all("li")
        number_of_matches = len(all_matches)

        for i in range(number_of_matches):
            # get teams name
            team_a = all_matches[i].find("div", {"class": "teamA"}).text.strip()
            team_b = all_matches[i].find("div", {"class": "teamB"}).text.strip()

            # get score
            match_result = (
                all_matches[i]
                .find("div", {"class": "MResult"})
                .find_all("span", {"class": "score"})
            )
            score = f"{match_result[0].text.strip()} / {match_result[1].text.strip()}"

            # get match time
            match_time = (
                all_matches[i]
                .find("div", {"class": "MResult"})
                .find("span", {"class": "time"}).text.strip()
            )

            # add match info to matches_details
            match_details.append(
                {
                    "نوع البطولة": championship_title,
                    "الفريق الأول": team_a,
                    "الفريق الثاني": team_b,
                    "ميعاد المباراة": match_time,
                    "النتيجة": score,
                }
            )

    for i in range(len(championships)):
        get_match_info(championships[i])

    keys = match_details[0].keys()

    with open(r"C:\Users\hp\OneDrive\Desktop\python\projects\yallakora.csv", "w", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(match_details)
        print(termcolor.colored("Done! \nFile Created!", color="green"))


main(page)
