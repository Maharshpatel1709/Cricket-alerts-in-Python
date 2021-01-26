import requests
import json
from datetime import datetime
import time

send_data_copy = ""

class GetScore:
    def __init__(self):
        self.url_get_match = "https://cricapi.com/api/matches/"
        self.url_get_score = "https://cricapi.com/api/cricketScore/"
        self.apikey = "Y3W6o4z4uFgjrvfqnSxZ4hDoiGi2"
        self.unique_id = ""

    def get_unique_id(self):
        uri_params = {"apikey":self.apikey}
        response = requests.get(self.url_get_match, params=uri_params)
        response_text = response.text
        all_matches = json.loads(response_text)
        flag = 0
        for i in all_matches['matches']:
            if (i['team-1'] == "India" or i['team-2'] == "India" and i['matchStarted']):
                todays_date = datetime.today().strftime('%Y-%m-%d')
                if todays_date == i['date'].split("T")[0]:
                    self.unique_id = i['unique_id']
                    flag = 1
                    break
        if flag == 0:
            self.unique_id = -1
        send_data = self.get_live_score()
        global send_data_copy
        if not send_data_copy == send_data:
            print(send_data)
            base_url = "https://api.telegram.org/bot1597917646:AAEJ4VvGgbxcqhqpvMEofngTvxBOofgibY0/sendMessage?chat_id=-1001221461547&text={}"
            requests.get(base_url.format(send_data))
            send_data_copy = send_data

    def get_live_score(self):
        data = ""
        if self.unique_id == -1:
            data = "No India matches today"
        else:
            uri_params = {"apikey": self.apikey, "unique_id": self.unique_id}
            response = requests.get(self.url_get_score, params=uri_params)
            response_text = response.text
            match_data = json.loads((response_text))
            data = "Score : \n" + match_data['score']
        return data

if __name__ == "__main__":
    while True:
        obj = GetScore()
        obj.get_unique_id()
        time.sleep(10)