# UPDATE 25/05/23

I changed the api used in the original program to the latest one (previously it was using 2 apis to fetch wallet and miners data
I added a timer (on the bottom of the page) to verify the program is running
I added the Kolka trust score alongside the verified status
Slightly changed the code to make it universal for linux and windows users

Now use only the miners2.py program

I left the previous versions available if someone wants to see the initial code

# duco-miners

I modified dansinclair25 CLI dashboard to better fit my needs. Added username, staking amount, uptime of the proram, verified status and changed the daily profit calculation for more accuracy.
There are two versions, one for linux (miners.py) and one for windows (miners_win.py)

Of course change the username in the program to the one you want to monitor... (Write your username between the quotes line 37 of the program if you don't want to input it upon each start)

duco-miners is still a super simple terminal "dashboard" for you to view a list of your Duino Coin miners. The output automatically updates every 60 seconds and provides you with a break down of each of your miners (in alphabetical order) as well as an overview of all of your miners and your current balance.

![image](https://github.com/jpx13/duco-miners/assets/19504251/ce925481-a469-4086-9157-f839b8a1d50c)

The "Daily profit" method used by dansinclair25 has been changed and takes now the last ten minutes averages. So it is most accurate after ten minutes ! 

## Usage

1. Clone this repo
2. Open up a terminal and `cd` into the repo directory
3. Run `pip3 install -r requirements.txt`
4. edit the miners2.py program to fill your username
5. Once all of the dependencies have been installed run `python3 miners.py`

## Extra
Thanks to dansinclair25 for his initial work !

Feel free to fork and edit this as you see fit. 

If you like this and would like to donate some DUCO to him, his wallet username is `dansinclair25`, if you want to give some ducos to me, my wallet name is 'discopepereland'
