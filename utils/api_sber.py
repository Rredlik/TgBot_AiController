import requests

from config import Env

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload='scope=GIGACHAT_API_PERS'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': 'c0721e34-85ab-437c-981f-c325ed34cc48',
  'Authorization': f'Basic {Env.SBER_AUTH_DATA}'
}

def test_req():
  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)


if __name__ == '__main__':
  test_req()