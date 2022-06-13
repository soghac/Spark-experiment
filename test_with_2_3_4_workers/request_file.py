import asyncio
import datetime
import json
from datetime import timedelta

import requests

url = 'http://localhost:5001/get/'


async def main():
    loop = asyncio.get_event_loop()
    users_count = [5, 10, 20]
    response_dict = dict()
    first_time = datetime.datetime.now()
    while datetime.datetime.now() - first_time < timedelta(hours=1):
        for user_count in users_count:
            with open('user_count.txt', 'w') as user_count_file:
                user_count_file.write(str(user_count))
            start_time = datetime.datetime.now()
            counter = 0
            while datetime.datetime.now() - start_time < timedelta(minutes=10):
                request_list = list()
                tmp = user_count
                for i in range(user_count):
                    request_list.append(loop.run_in_executor(None, requests.get, url))
                for i in range(len(request_list)):
                    response = await request_list[i]
                    tmp -= 1
                    response_dict[f'users={user_count}&{datetime.datetime.now().time()}'] = {
                        "status": "Row" in response.text,
                        "text": response.text,
                        "user": user_count,
                        "time": str(datetime.datetime.now().time())
                    }
                    print(f'users={user_count}&{datetime.datetime.now().time()}')
                    print(response.status_code)
                    print(response.text)
                counter += 1
                end_time = datetime.datetime.now()
                with open('average_time.txt', 'a') as average_time_file:
                    average_time_file.write(
                        "user count: " + str(user_count) + "    " + str(
                            (int(end_time.timestamp()) - int(start_time.timestamp())) / (
                                    int(user_count) * counter)) + '\n'
                    )
    with open("result_of_each_request.json", "w") as outfile:
        json.dump(response_dict, outfile)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
