import importlib.util
import os
import getpass
import sys
import shutil
from rgbprint import gradient_print, rgbprint, Color
import asyncio
import aiohttp
import importlib
import subprocess
import base64
from colorama import init, Fore

init()
webH_url = None
webH_username = None

def error(e):
    print(f"{Fore.RED}[X] An error has occurred: {e}")
    os.system("pause")

def print_menu():
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    menu_text = [
        "                                                                                                           ",
        "   ▄███████▄  ▄█       ███    █▄      ███      ▄██████▄     ▄█    █▄     ▄██████▄   ▄██████▄     ▄█   ▄█▄  ",
        "   ███    ███ ███       ███    ███ ▀█████████▄ ███    ███   ███    ███   ███    ███ ███    ███   ███ ▄███▀ ", 
        "   ███    ███ ███       ███    ███    ▀███▀▀██ ███    ███   ███    ███   ███    ███ ███    ███   ███▐██▀   ", 
        "   ███    ███ ███       ███    ███     ███   ▀ ███    ███  ▄███▄▄▄▄███▄▄ ███    ███ ███    ███  ▄█████▀    ", 
        " ▀█████████▀  ███       ███    ███     ███     ███    ███ ▀▀███▀▀▀▀███▀  ███    ███ ███    ███ ▀▀█████▄    ", 
        "   ███        ███       ███    ███     ███     ███    ███   ███    ███   ███    ███ ███    ███   ███▐██▄   ", 
        "   ███        ███▌    ▄ ███    ███     ███     ███    ███   ███    ███   ███    ███ ███    ███   ███ ▀███▄ ", 
        "  ▄████▀      █████▄▄██ ████████▀     ▄████▀    ▀██████▀    ███    █▀     ▀██████▀   ▀██████▀    ███   ▀█▀ ", 
        "              ▀                                                                                  ▀         ",
        "                                       > mini version of plutonium :3                                      ",
        "                                    > again remember, use it with brain                                    ",
        "                             > contact us if you need smth: dsc.gg/plutoserver                             ",
        "                                            > version ==> v1.0                                             ",
        "" 
    ]
    
    for line in menu_text:
        padding = (terminal_width - len(line)) // 2
        gradient_print(" " * padding + line, start_color=Color.yellow, end_color=Color.brown)

def print_choices():
    terminal_width = shutil.get_terminal_size((80, 20)).columns

    choices = ["[1] Send Message", "[2] Delete Webhook", "[3] Rename Webhook", "[4] Spam Webhook", "[5] Change PFP", "[6] Log out", "[7] Exit"]
    padding = (terminal_width - max(len(choice) for choice in choices)) // 2
    gradient_print(" " * padding + "╭" + "─" * max(len(choice) for choice in choices) + "╮", start_color=Color.yellow, end_color=Color.brown)
    for choice in choices:
        gradient_print(" " * padding + "│" + choice.center(max(len(choice) for choice in choices)) + "│", start_color=Color.yellow, end_color=Color.brown)
    gradient_print(" " * padding + "╰" + "─" * max(len(choice) for choice in choices) + "╯", start_color=Color.yellow, end_color=Color.brown)

async def return_To_Menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    await asyncio.sleep(0.05)
    print_menu()
    print_choices()
    await asyncio.sleep(0.05)
    choice = input("Enter your choice: ")
    await handleChoices(choice)

async def sendMsg(url, msg):
    global webH_username
    async with aiohttp.ClientSession() as session:
        print(f"{Fore.BLUE} [?] PlutoHook is processing this task...{Fore.WHITE}")
        if webH_username == None:
            async with session.post(url=url, json={"content": msg}) as post_response:
                if post_response.status == 204:
                    print(f"{Fore.GREEN} [V] PlutoHook sent message: {msg}{Fore.WHITE}")
                    await asyncio.sleep(1.25)
                    await return_To_Menu()
                else:
                    print(f"{Fore.RED} [X] PlutoHook posting returned a non-204 status code: {post_response.status}{Fore.WHITE}")
        else:
            async with session.post(url=url, json={"content": msg, "username": webH_username}) as post_response:
                if post_response.status == 204:
                    print(f"{Fore.GREEN} [V] PlutoHook sent message: {msg}{Fore.WHITE}")
                    await asyncio.sleep(1.25)
                    await return_To_Menu()
                else:
                    print(f"{Fore.RED} [X] PlutoHook posting returned a non-204 status code: {post_response.status}{Fore.WHITE}")

        # discord usually returns 204 NO CONTENT on successful webhook post
        # if you want to perform a GET request to check the message, ensure the URL is correct and you have a reason to do so.
            
async def deleteWebhook(url):
    global webH_url, webH_username
    async with aiohttp.ClientSession() as session:
        print(f"{Fore.BLUE} [?] PlutoHook is processing this task...{Fore.WHITE}")
        async with session.get(url=url) as response:
            if response.status == 200:
                response_json = await response.json()
                username = response_json.get("name")
                async with session.delete(url=url) as delete_response:
                    if delete_response.status == 204:
                        print(f"{Fore.GREEN} [V] PlutoHook deleted webhook named: {username}{Fore.WHITE}")
                        webH_url = None
                        webH_username = None
                        await asyncio.sleep(1.25)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        await asyncio.sleep(0.05)
                        await main()
                    else:
                        print(f"{Fore.RED} [X] PlutoHook deletion returned a non-204 status code: {delete_response.status}{Fore.WHITE}")
                        await asyncio.sleep(1.25)
                        await return_To_Menu()
            else:
                print(f"{Fore.RED} [X] PlutoHook failed to retrieve webhook details: {response.status}{Fore.WHITE}")
                await asyncio.sleep(1.25)
                await return_To_Menu()
    
async def renameWebhook(url, username):
    global webH_username
    async with aiohttp.ClientSession() as session:
        print(f"{Fore.BLUE} [?] PlutoHook is processing this task...{Fore.WHITE}")
        async with session.patch(url=url, json={"username": username}) as post_response:
            if post_response.status == 200:
                webH_username = username
                print(f"{Fore.GREEN} [V] PlutoHook changed webhook's username to: {webH_username}{Fore.WHITE}")
                await asyncio.sleep(1.25)
                await return_To_Menu()
            else:
                print(f"{Fore.RED} [X] PlutoHook posting returned a non-200 status code: {post_response.status}{Fore.WHITE}")
                await asyncio.sleep(1.25)
                await return_To_Menu()
                
async def getWebhooksName(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as post_response:
            if post_response.status == 200:
                response_json = await post_response.json()
                username = response_json.get("name")
                return username
                
async def spamWebhook(url, msg, timeout):
    try:
        global webH_username
        print(f"{Fore.BLUE} [?] PlutoHook is processing this task...{Fore.WHITE}")
        await asyncio.sleep(0.35)
        print(f"{Fore.BLUE} [?] PlutoHook is starting spamming! If you want stop this, re-launch the program.{Fore.WHITE}")
        async with aiohttp.ClientSession() as session:
            if webH_username == None:
                while True:
                    async with session.post(url=url, json={"content": msg}) as post_response:
                        if post_response.status == 204:
                            print(f"{Fore.GREEN} [V] PlutoHook sent message: {msg}{Fore.WHITE}")
                            await asyncio.sleep(float(timeout))
                        else:
                            print(f"{Fore.RED} [X] PlutoHook posting returned a non-204 status code: {post_response.status}{Fore.WHITE}")
                            await asyncio.sleep(float(timeout))
            else:
                while True:
                    async with session.post(url=url, json={"content": msg, "username": webH_username}) as post_response:
                        if post_response.status == 204:
                            print(f"{Fore.GREEN} [V] PlutoHook sent message: {msg}{Fore.WHITE}")
                            await asyncio.sleep(float(timeout))
                        else:
                            print(f"{Fore.RED} [X] PlutoHook posting returned a non-204 status code: {post_response.status}{Fore.WHITE}")
                            await asyncio.sleep(float(timeout))
    except KeyboardInterrupt as e:
        error(e)

async def changePFP(url, image_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as image_response:
            if image_response.status != 200:
                print(f"{Fore.RED} [X] Failed to fetch image. Status code: {image_response.status}{Fore.WHITE}")
                return
            image_data = await image_response.read()

    base64_image = base64.b64encode(image_data).decode('utf-8')
    payload = {
        'avatar': f'data:image/png;base64,{base64_image}'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload) as response:
            if response.status == 200:
                print(f"{Fore.GREEN} [V] Profile picture changed successfully.{Fore.WHITE}")
                await asyncio.sleep(1.25)
                await return_To_Menu()
            else:
                print(f"{Fore.RED} [X] Failed to change profile picture. Status code: {response.status}{Fore.WHITE}")
                await asyncio.sleep(1.25)
                await return_To_Menu()

async def logOut():
    global webH_url, webH_username
    usernameHHH = await getWebhooksName(webH_url)
    print(f"{Fore.BLUE} [?] PlutoHook logging out of: {usernameHHH}{Fore.WHITE}")
    webH_url = None
    webH_username = None
    await asyncio.sleep(1.75)
    os.system('cls' if os.name == 'nt' else 'clear')
    await asyncio.sleep(0.05)
    await main()
    
async def handleChoices(choice):
    global webH_url, webH_username
    if choice == '1':
        msg = input("Message: ")
        if msg:
            await sendMsg(webH_url, msg)
    elif choice == '2':
        await deleteWebhook(webH_url)
    elif choice == '3':
        username = input("Webhook Username: ")
        if username:
            await renameWebhook(webH_url, username)
    elif choice == '4':
        msg = input("Message: ")
        timeout = input("Timeout (to avoid api-ratelimit): ")
        if msg and timeout:
            await spamWebhook(webH_url, msg=msg, timeout=timeout)
    elif choice == '5':
        imageURL = input("URL to image: ")
        if imageURL:
            await changePFP(webH_url, imageURL)
    elif choice == '6':
        doYouRealWant = input("Do you really want to logout? [Y/N]: ")
        if doYouRealWant.upper() == "Y":
            await logOut()
        elif doYouRealWant.upper() == "N":
            print(f"{Fore.BLUE} [?] Uh... Okay! {Fore.WHITE}")
            await asyncio.sleep(1.75)
            await return_To_Menu()
        else:
            print(f"{Fore.BLUE} [?] Invalid option. Try again. {Fore.WHITE}")
            await asyncio.sleep(1.75)
        await return_To_Menu()
    elif choice == '7':
        print(f"{Fore.BLUE} [?] Exiting the program! Re-launch the program if you need. {Fore.WHITE}")
        await asyncio.sleep(1.75)
        exit()
    else:
        print(f"{Fore.BLUE} [?] Invalid choice!{Fore.WHITE}")
        await asyncio.sleep(1.75)
        await return_To_Menu()

async def main():
    global webH_url
    print_menu()
    webhook_url = getpass.getpass(f"Webhook URL: ")
    if webhook_url and webhook_url.startswith("https://discord.com/api/webhooks/"):
        async with aiohttp.ClientSession() as session:
            print(f"{Fore.BLUE} [?] PlutoHook is processing this task...{Fore.WHITE}")
            async with session.get(webhook_url) as response:
                if response.status == 200:
                    webH_url = webhook_url
                    print(f"{Fore.GREEN} [V] Webhook URL is valid. You may continue!{Fore.WHITE}")
                    await asyncio.sleep(1.25)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_menu()
                    print_choices()
                    await asyncio.sleep(0.05)
                    choice = input("Enter your choice: ")
                    await handleChoices(choice)
                else:
                    print(f"{Fore.RED} [X] Webhook URL returned a non-200 status code: {response.status}{Fore.WHITE}")
    else:
        print(f"{Fore.RED} [X] The webhook URL is invalid! Please ensure it starts with 'https://discord.com/api/webhooks/'!{Fore.WHITE}")

if __name__ == "__main__":
    asyncio.run(main())