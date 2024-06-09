import requests
import json
import os

discord_notify = False
myDiscordID = os.environ["DID"]
discordWebhook = os.environ["DWEBHOOK"]

urls = {
    "Genshin": 'https://sg-hk4e-api.hoyolab.com/event/sol/sign?lang=en-us&act_id=e202102251931481',
    "Star Rail": 'https://sg-public-api.hoyolab.com/event/luna/os/sign?lang=en-us&act_id=e202303301540311',
    "Honkai 3": 'https://sg-public-api.hoyolab.com/event/mani/sign?lang=en-us&act_id=e202110291205111'
}

def main():
    auto_sign_function()
    if discord_notify and discordWebhook:
        post_webhook("test")

def discord_ping():
    return f"<@{myDiscordID}> " if myDiscordID else ''

def auto_sign_function():
    with open("header.json") as file:
        header = json.load(file)
        header["Cookie"] = os.environ["HOYO"]

    fields = []
    for game in urls:
        if game == "Honkai 3" or game == "Star Rail":
            # skip hi3 cuz i dont play
            continue
        response_json = requests.post(urls[game], headers=header)
        check_in_result = response_json.json()["message"]
        retcode = response_json.json()["retcode"]
        if response_json.ok:
            fields.append({"name": game + f": {retcode}", "value": check_in_result, "inline": False})
        else:
            post_webhook(data=f"{discord_ping()} : {game} : {check_in_result}")
    post_webhook(embed={
        "title": "Hoyolab",
        "type": "rich",
        "fields": fields
    })

def post_webhook(data=None, embed=None):
    payload = {
        "username": "hoyo-check",
        "avatar_url": "https://cdn.discordapp.com/avatars/1098141251209023538/f04548c8dcf740167baec44ea51f4d02.png",
        "content": data,
        "embeds": [embed] if embed else []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(discordWebhook, json=payload, headers=headers)

if __name__ == "__main__":
    main()
