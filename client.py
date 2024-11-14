import requests

def send_request():
    resp = requests.get("http://127.0.0.1:3501/v1.0/invoke/api/method/foo")

    print(resp.status_code)
    print(resp.text)

if __name__ == "__main__":
    send_request()
