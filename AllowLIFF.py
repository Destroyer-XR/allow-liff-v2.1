import httpx, uuid
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def string_to_byte(lst):
    return [ord(num) for num in lst]

authToken = 'YOU_TOKEN'
liff_id = 'YOU_LIFF_ID'

def FixFLEX(title, data):
    return {"type": "flex","altText": title,"contents": data}

def issueLiffView(to):
    user_agent_line = 'Line/14.10.0'
    x_line_application = 'ANDROID\t14.10.0\tAndroid OS\t13'
    Bytes_liff = [130, 33, 1, 13, 105, 115, 115, 117, 101, 76, 105, 102, 102, 86, 105, 101, 119, 28, 24, 19] + string_to_byte(liff_id)
    Bytes_liff += [28, 44, 24] + string_to_byte(f'!{to}')
    Bytes_liff += [0, 0, 44, 17, 28, 24] + string_to_byte(f'${uuid.uuid4()}')
    Bytes_liff += [17, 0, 0, 34, 24, 12, 108, 105, 102, 102, 46, 108, 105, 110, 101, 46, 109, 101, 0, 0]
    with httpx.Client(http2=True) as client:
        headers = {
            'user-agent': user_agent_line,
            'x-lal':'th_TH',
            'x-line-access': authToken,
            'x-line-application': x_line_application,
            'X-Line-Liff-Id':liff_id,
            'x-lpv': '1',
            'Content-Type': 'application/x-thrift'
        }
        r = client.post('https://legy-backup.line-apps.com/LIFF1', headers=headers, data=bytes(Bytes_liff))
        if to.startswith('u'):
            return r.content[2777:2970].decode('raw_unicode_escape')
        else:
            return r.content[2780:2973].decode('raw_unicode_escape')

def AllowLIFF():
    try:
        user_agent = 'Mozilla/5.0 (Linux; Android 13; SM-A045F Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.133 Mobile Safari/537.36 Line/14.10.0'
        user_agent_line = 'Line/14.10.0'
        x_line_application = 'ANDROID\t14.10.0\tAndroid OS\t13'
        Bytes_liff = [130, 33, 1, 13, 105, 115, 115, 117, 101, 76, 105, 102, 102, 86, 105, 101, 119, 28, 24, 19] + string_to_byte(liff_id)
        Bytes_liff += [28, 44, 24] + string_to_byte('!u23ab8d51ab1f3e99b8180ecd48b57ad5')
        Bytes_liff += [0, 0, 44, 17, 28, 24] + string_to_byte(f'$a9938082-9da8-4019-89a7-ff1cb4c13296')
        Bytes_liff += [17, 0, 0, 34, 24, 12, 108, 105, 102, 102, 46, 108, 105, 110, 101, 46, 109, 101, 0, 0]
        with httpx.Client(http2=True) as client:
            headers = {
                'user-agent': user_agent_line,
                'x-lal':'th_TH',
                'x-line-access': authToken,
                'x-line-application': x_line_application,
                'X-Line-Liff-Id':liff_id,
                'x-lpv': '1',
                'Content-Type': 'application/x-thrift'
            }
            r = client.post('https://legy-backup.line-apps.com/LIFF1', headers=headers, data=bytes(Bytes_liff))
            decoded_string = r.content.decode('raw_unicode_escape')
            start = decoded_string.find("https://")
            end = decoded_string.find("\x00", start)
            url = decoded_string[start:end]
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            session_string = query_params.get('sessionString', [None])[0]
            headers = {
                'user-agent': user_agent,
                'x-line-access': authToken,
                'x-line-application': x_line_application,
            }
            r = client.get(url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            hidden_inputs = soup.find_all('input', {'type': 'hidden'})
            hidden_values = {input_tag['name']: input_tag.get('value', '') for input_tag in hidden_inputs}
            cookiex = {}
            for name, value in hidden_values.items():
                cookiex[name] = value
            cookies = {
                'X-SCGW-CSRF-Token': cookiex['__csrf'],
                'sessionString': session_string,
            }
            data = {
                'allPermission': ['P', 'CM', 'OC'],
                'approvedPermission': ['P', 'CM', 'OC'],
                '__WLS': cookiex['__WLS'],
                'channelId': cookiex['channelId'],
                '__csrf': cookiex['__csrf'],
                'addFriendInAggressiveMode': True,
                'allow': True
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'user-agent': user_agent,
                'X-Requested-With': 'jp.naver.line.android',
                'Upgrade-Insecure-Requests': '1'
            }
            client.post('https://access.line.me/oauth2/v2.1/authorize/consent', headers=headers, data=data, cookies=cookies)
    except:
        pass
    print(">> Allow Login.")

AllowLIFF()

def sendFlex(to, data):
    with httpx.Client(http2=True) as client:
        token = issueLiffView(to)
        print(token)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        json_data = {
            'messages': [data]
        }
        response = client.post('https://api.line.me/message/v3/share', headers=headers, json=json_data)
        print(response.status_code, response.text)

flex = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": f"Flex Message",
            "weight": "bold",
            "align": "center"
        }
        ]
    }
}
sendFlex("c052c976d2c2e25714a1254bba535ba97", FixFLEX(f"TEST MESSAGE FLEX", flex))
