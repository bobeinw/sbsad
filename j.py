import aiohttp
import asyncio
import re
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl import functions
from datetime import datetime
TIMEOUT = 10  
counter = 0
semaphore = asyncio.Semaphore(5)  

api_id = 24796447
api_hash = '357f0b9aa7389298db9838d034919260'
session_string = "1BJWap1sBu1z1ME-sEFyRNy3WxIcGtpz1aEaEAg3rlkDdkin-htCr6a2sTUTS3ihHQ80HBaWzhhnd1SRfYwCQH_z1hgjy-fwG2DGSkAqldNEzuOkg55ggyHOQUgr5wtOg1aqbjjZ7n9KkuACdrqltsI04ijN6QiqydLyK4guVUfxwjpiiKi1ioiyosea_deVsxoO6ieXlCk2V5hUhvZ7ENeVp17nGwTDP2_iI74g-YfA2Pp4yYc10TC7rtaMDWOssSTBcQaguQWHcpppNHezIE7Vx2M3zxrOrbIkyB0eY36HOMLoFxMu0tQiwNfVDUolZygjTsHB41L7yxY_LCx8g-BTWJBPm3ZM="
channel = None

async def create_channel():
    global channel
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    await client.start()

    try:
        result = await client(functions.channels.CreateChannelRequest(
            title=" Failed to Claim 🦧", 
            about=" Failed to Claim 🦧", 
            megagroup=False
        ))
        channel = result.chats[0]
    except Exception as e:
        print(f"فشل إنشاء القناة: {str(e)}")
    finally:
        await client.disconnect()

async def send_video_with_description(client, current_time, user, clicks, is_flood=False, flood_time_remaining=None):
    try:
        video_url = "https://t.me/YYYYYYvY/349"
        description = "𝙱𝚛𝚘𝚝𝚑𝚎𝚛 𝚝𝚑𝚎 𝚏𝚕𝚘𝚘𝚍 𝚑𝚊𝚜 𝚊𝚛𝚛𝚒𝚟𝚎𝚍 🎢🔥" if is_flood else "The user was installed in this channel successfully"
        flood_message = f"Since: {current_time} | Ending Flood: {flood_time_remaining}" if is_flood else f"Since: {current_time}"
        video_message = f"""
ʜɪ sɪʀ ғʟᴏᴏᴅ ᴜsᴇʀɴᴀᴍᴇ
———————————————
๛ Username: @{user}
———————————————
𝖯𝖸 ↠ @x_bob
"""
        
        destination = "https://t.me/flood_kinsss"  
        await client.send_file(destination, video_url, caption=video_message)
    except Exception as e:
        print(f"فشل إرسال الفيديو: {str(e)}")

async def assign_username_to_channel(client, username, clicks):
    try:
        channel_entity = await client.get_input_entity(channel)
        await client(functions.channels.UpdateUsernameRequest(channel_entity, username))
        print(f"تم تثبيت اليوزر في القناة بنجاح\n @{username}")       
        about_text = f"@YYYYYYvY User Name here\n@YYYYYYvY معرفات داخل القناة\n@YYYYYYvY 频道内的用户名\n╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴"
        await client(functions.messages.EditChatAboutRequest(peer=channel_entity, about=about_text))        
        await send_video_with_description(client, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username, clicks)
        return True
    except Exception as e:
        if "A wait of" in str(e):
            wait_time = int(str(e).split("A wait of ")[1].split(" seconds")[0].strip())  
            print(f"Flood User -> {username} -> {wait_time}")     
            asyncio.create_task(send_video_with_description(client, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username, clicks, is_flood=True, flood_time_remaining=wait_time))
            return False
        if "Nobody is using this username, or the username is unacceptable" in str(e):
            print(f"@{username} -> banded")
        elif "The username is already taken (caused by UpdateUsernameRequest)" in str(e):
            print(f"User is Flood -> @{username}")
            await send_video_with_description(client, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username, clicks, is_flood=True, flood_time_remaining="?")
        else:
            print(f"unknown error in user @{username}:\n{str(e)}")
            return False

async def check_username(session, user, client, clicks):
    global counter
    try:
        async with semaphore:
            async with session.get(f"https://fragment.com/username/{user}", timeout=TIMEOUT) as response:
                html = await response.text()
                if '<span class="tm-section-header-status tm-status-taken">Taken</span>' in html:
                    print(f"[{counter + 1}] -> {user} -> Taken")
                elif '<span class="tm-section-header-status tm-status-unavail">Sold</span>' in html:
                    print(f"[{counter + 1}] -> {user} -> Sold")
                elif '<div class="table-cell-status-thin thin-only tm-status-unavail">Unavailable</div>' in html:
                    print(f"[{counter + 1}] -> {user} -> Unavailable")
                    success = await assign_username_to_channel(client, user, clicks)
                    if success:
                        return True  
                else:
                    print(f"[{counter + 1}] -> {user} -> Unknown")
                
        counter += 1
    except asyncio.TimeoutError:
        print(f"[{counter + 1}] -> {user} -> Timeout")
    except Exception as e:
        flood_match = re.search(r"FLOOD_WAIT_(\d+)", str(e))
        if flood_match:
            wait_time = int(flood_match.group(1))
            print(f"[{counter + 1}] -> {user} -> Flood wait. توقّف لمدة {wait_time} ثانية.")
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await send_video_with_description(client, current_time, user, clicks, flood_time_remaining=wait_time)
            await asyncio.sleep(wait_time)
        else:
            print(f"[{counter + 1}] -> {user} -> Error: {str(e)}")

async def check_usernames_from_file(filename, client):
    connector = aiohttp.TCPConnector(limit=100)  
    async with aiohttp.ClientSession(connector=connector) as session:
        with open(filename, 'r') as file:
            usernames = [user.strip() for user in file.readlines()]

        tasks = [check_username(session, user, client, clicks=counter) for user in usernames]
        await asyncio.gather(*tasks)  

async def main():
    await create_channel()
    if channel:
        client = TelegramClient(StringSession(session_string), api_id, api_hash)
        await client.start()
        filename = 'usernames.txt'
        await check_usernames_loop(filename, client)
        await client.disconnect()
async def check_usernames_loop(filename, client):
    """
ظل بالي يمك هــــم بالك وياي
لو بس كلام العــــــــــشگ دونته
صدگني على مودك ما نمت ليل
ولا طــــــعم المنام بعيني ضگته
شمالك ما تــحس ما تملك أحساس
لا تسكت حبيبي تمــــوت السكته
قانون العـــــــشگ علمني ع الشوگ
وقانــــــــون گلبي اختارك انــــــت
تدري لـــــيش احبك واريـــــد وياك
لان وصفك عجبني وبروحي صورته
راح احلف احبـــك وظل الك اشتاك
وغيرك ما احـــــب والله بس انــــت
آحبك

المبدع - @YYYYYYvY 😂

    """
    while True:
        

        connector = aiohttp.TCPConnector(limit=100)  
        async with aiohttp.ClientSession(connector=connector) as session:
            with open(filename, 'r') as file:
                usernames = [user.strip() for user in file.readlines()]
            
            tasks = [check_username(session, user, client, clicks=counter) for user in usernames]
            await asyncio.gather(*tasks)  

        
        await asyncio.sleep(5) 
asyncio.run(main());