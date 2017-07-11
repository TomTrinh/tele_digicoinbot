import json
import requests
import time
import urllib
import urllib.request


def response(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

def get_coin_price(coin):
    url = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-{}'.format(coin)
    res = json.loads(response(url))
    if coin == 'btc' or coin == 'BTC' or coin == 'Btc':
        error_mess = 'No BTC-BTC price in Bittrex'
        return (error_mess)
    elif res['success'] == False:
        error_mess = 'This coin does not exist in Bittrex'
        return (error_mess)
    else:
        price = res['result'][0]
        return(price)

TOKEN = "448274854:AAENx0KErWsU41Q3emSadrj-OJRDF6b2lFI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    text = get_coin_price(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)



def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)




def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
    
