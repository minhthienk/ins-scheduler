

import requests

cookies = {
    '_ga': 'GA1.1.1585282442.1605495004',
    '_ga_S33MGBEV0G': 'GS1.1.1606723568.39.1.1606724084.0',
    '_ga_6LBTR78SZX': 'GS1.1.1615122483.154.0.1615122498.0',
    'XSRF-TOKEN': 'eyJpdiI6Im9ERkh3WUEweG9oRDAyRW5FU0psdkE9PSIsInZhbHVlIjoiK2FSK0dDK1JvWU1Nd0xtQ0JqNkVmQT09IiwibWFjIjoiMTQ3NDUxMWI3YWM1OGExNTlmNmM2ZDQ2OTVkOGIyNzE4ZjBlYjc5Y2Y5ZTE2ZjE1MThhMTE3MzczNjM4YTk2YSJ9',
    'centeronline_session': 'eyJpdiI6ImtZM2FhQ2tYcXM1UytFYmtoZGZuUnc9PSIsInZhbHVlIjoiMGg2YUp6TTRETERiYldkWlpKT1N4VGVWOUpsR1d0dUNkaDgzNmFOQkpucmIxa0JZelB4OHdtTDVKR20rYVhTVSIsIm1hYyI6IjE5ZTdmMmZiYmRiYjdkZDMwMDJkZTM3ODU3NDRjYTdiNTkzNGJhZjVmMDJhNTAxNDJjNmM1MzE2YzFiOWIyMjYifQ%3D%3D',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://ins.center.edu.vn/login',
    'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
}

response = requests.get('https://ins.center.edu.vn/', headers=headers, cookies=cookies)
print(response.text)


response = requests.get('https://ins.center.edu.vn/training/class', headers=headers, cookies=cookies)
print(response.text)

