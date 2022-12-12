import subprocess
import requests
from requests.exceptions import HTTPError
import json
import sys
import time
from tabulate import tabulate
from operator import itemgetter

def format_hashrate(hr):
    unit = ''
    if hr < 1000:
        unit = 'H'
    elif hr < 1000000:
        hr /= 1000
        unit = 'kH'
    else:
        hr /= 1000000
        unit = 'mH'
    return '{:.2f} {}/s'.format(hr, unit)

def sec2hms(ss):
	(hh, ss)=divmod(ss, 3600)
	(mm, ss)=divmod(ss, 60)
	sec = int (ss)
	hr = int (hh)
	mn = int (mm)
	res = "" + str(hr) +":"+str(mn)+":"+str(sec)
	return res


def main():
    subprocess.call('cls', shell = True )
    tab_moy = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    indice  = 0
    username = "discopepereland"
    while not username:
        username = input('Enter your DUCO username: ')

    print("Fetching miners list…")

    prev_balance = 0
    start_time = time.time()
    current_time = 0
    last_update = None
    first = 0

    while True:
        try:
            miners_response = requests.get(f"https://server.duinocoin.com/miners/{username}")
            miners_response.raise_for_status()
            miners_json_data = json.loads(miners_response.text)

            balances_response = requests.get(f"https://server.duinocoin.com/balances/{username}")
            balances_response.raise_for_status()
            balances_json_data = json.loads(balances_response.text)

            api_response = requests.get("https://server.duinocoin.com/api.json")
            api_response.raise_for_status()
            api_json_data = json.loads(api_response.text)

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            time.sleep(10)
            continue
        except Exception as err:
            print(f'Other error occurred: {err}')
            time.sleep(10)
            continue
        except KeyboardInterrupt:
            print('Exiting…')
            sys.exit()
        
        if miners_json_data and balances_json_data and api_json_data:
            subprocess.call('cls', shell = True )

            duco_price_usd = api_json_data.get('Duco price', 0)

            #user_miners = [v for v in miners_json_data.values() if v["User"] == username]
            user_miners = miners_json_data.get('result')
            
            if not user_miners:
                print("No miners found.")
            else:    
                miners = []
                total_hash = 0
                totalSharerate = 0
                totalAccepted = 0

                for v in user_miners:
                   hashrate = int(v.get("hashrate", 0))
                   total_hash += hashrate

                   accepted = int(v.get("accepted", 0))
                   rejected = int(v.get("rejected", 0))
                   sharerate = int(v.get("sharetime", 0))
                   
                   if sharerate < (accepted + rejected):
                           sharerate = accepted + rejected

                
                   totalSharerate += sharerate
                   totalAccepted += accepted

                   
                   successRate = f'{accepted}/{sharerate}'
                   
                   algo = v["algorithm"]
                   diff = int(v.get("diff", 0))
                   id = v["identifier"]
                   software = v["software"]
                   pool = v.get("pool")
                   ping = int(v.get("pg"))
                   miners.append([id, software, algo, successRate, format_hashrate(hashrate),pool, diff,ping])
            
            miners.sort(key=itemgetter(0))

            #user_balance_str = balances_json_data.get(username, "0 DUCO").replace(' DUCO', ' ᕲ')
            #user_balance = float(user_balance_str.replace(' ᕲ', ''))
            user_balance = balances_json_data.get('result').get('balance')

            if(first != 0):
               balance_difference = user_balance - prev_balance
            else:
               balance_difference = -1
            tab_moy[indice] = balance_difference
            indice = (indice+1)%10
            time_difference = time.time() - last_update if last_update else 0
            moy = 0.0
            val = 0
            for i in range(10):
                if(tab_moy[i]>=0):
                    val += 1
                    moy += tab_moy[i]
            if (val >0):
                moy = moy/val
            else:
                moy = 0
            daily_average = moy*60*24   # balance_difference*float((60/time_difference)*60*24) if time_difference != 0 else 0
            current_time = time.time() - start_time
            
            
            
            verified = balances_json_data.get('result').get('verified')
            stake = balances_json_data.get('result').get('stake_amount')
            total_success_pc = int((totalAccepted/totalSharerate)*100) if totalSharerate > 0 else 0
            total_success = f'{total_success_pc}% ({totalAccepted}/{totalSharerate})'
            print(tabulate([[username,user_balance,stake, len(miners), format_hashrate(total_hash), f'{total_success}', f'{daily_average:.2f} D',f'{sec2hms(current_time)}',verified]], headers=["Username","Balance","Staking", "Miners", "Total hashrate", "Total success", "Daily profit","uptime","verified"]))
            
            if miners:
                print(tabulate(miners, headers=["ID", "Software", "Algo", "Success", "Hashrate","Pool", "Diff","Ping"], tablefmt='fancy_grid'))
            
            prev_balance = user_balance
            last_update = time.time()
            first = 1
            time.sleep(60)

if __name__ == "__main__":
    main()
