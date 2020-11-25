import requests,time
def getData(data,device):
    return {
        'iot2tangle': data,
        'device': device,
        'timestamp': int(time.time())
    }
data = [
    {
        'sensor': 'escrow',
        'data': [
            {
                'collateral': 100,
                'tool': 'hammer',
                'condition': 'rfid',
                'fee': 1,
                'start_time': time.time(),
                'esrow_address': 'A'*81,
                'deposite_address': 'B'*81,
             }
        ]
    }
]
data = getData(data,'ESCROW_PI')
r = requests.post('https://keepy.gradstudent.me/messages',json=data)
print(r.status_code, r.text)
