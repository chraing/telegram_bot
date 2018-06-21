import requests  
import datetime
import hmac
import hashlib
import urllib.parse

hiveos_secret_key=b'8e125cd939a3a47bf5b4dfcf535a41d37a3c555a7baf1748a3a523fda6506a42'
hiveos_public_key=b'93e0855529a2239786b6a30337e984ba71e4a2544d933a4ddb3dd8eaa43abcb9'

def hiveos_api(params):
    params["public_key"] = hiveos_public_key
    url = 'https://api.hiveos.farm/worker/eypiay.php'
    hmac_ = hmac.new(hiveos_secret_key,urllib.parse.urlencode(params).encode('utf-8'),hashlib.sha256).hexdigest()
    response = requests.post(url,data=params,headers={'HMAC': hmac_}).json()
    return response

def need_stroka(lst,delit=1,okrug=1):
    n = len(lst)
    s = ""
    for i in range(n):
        if delit>1:
            s = s + str(round((lst[i]) / delit, okrug)).center(6)
        else:
            s = s + (lst[i]).center(6)
    return s
class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

greet_bot = BotHandler("607744530:AAEEf0rq76FRTJsoLZp-EX_aFs0kbVts4e4")  
greetings = ('hiveos')  
now = datetime.datetime.now()


def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings:
            s=""
            a = (hiveos_api({'method': 'getCurrentStats'}))

            hash_hiveos = (str(a.get("result").get("rigs").get("10256").get("stats").get("hash") // 1000) + ' MH/s')
            power_hiveos = (str(a.get("result").get("rigs").get("10256").get("stats").get("power")) + "W")

            s=s+hash_hiveos+" "+power_hiveos+"\n"

            temp_hiveos = (a.get("result").get("rigs").get("10256").get("stats").get("temp"))
            s=s+"Temp    ="+need_stroka(temp_hiveos)+"\n"
            fan_hiveos = (a.get("result").get("rigs").get("10256").get("stats").get("fan"))
            s = s +"Fan       ="+need_stroka(fan_hiveos)+"\n"

            hashes_hiveos = ((a.get("result").get("rigs").get("10256").get("stats").get("hashes")))
            s = s +"Hashes="+need_stroka(hashes_hiveos, 1000, 2)+"\n"

            #print(a.get("result").get("rigs").get("10256"))

            greet_bot.send_message(last_chat_id, s)
            today += 1

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
