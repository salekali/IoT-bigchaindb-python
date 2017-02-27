import os
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit
from time import strftime


#script to read system temperature from RPi and save to file
os.system("/opt/vc/bin/vcgencmd measure_temp > sysTemp")

#script to read sensor data from saved file

fo = open("sysTemp") # Open a file
str = fo.read(); #read characters in sysTemp and hold them as 'str'
fo.close() #close opened file
print(str) # print string to check
temp1=str[5:9] #chop out required characters
temp=eval(temp1) #convert string into number
print("system temp = ", temp) # print value to check


#Use this specific keypair for this transaction
salek_pub = '6SwERTYXbqF9EB2YLqv3jUxJX1fW5VM1DZEpPzzj91Br'
salek_pri = 'CpaRDpDhNSjMm39JwjwRw6taqB8wTK4m8fk9hgHbzfJY'


#Connect to bigchaindb node in LAN
bdb = BigchainDB('http://10.42.0.1:9984')


#Create digital asset
reading_asset = {
 'data': {
  'reading':{
   'serial number': 'pi01',
   'manufacturer' : 'arm'    'temperature': temp,
   'day': strftime("%D"),
   'time': strftime("%X")
  },
 },
}

#Add metadata
reading_metadata = {
 'message': 'Here is the temperature of the Raspberry Pi!',
}

#Prepare a 'create' transaction
prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=salek_pub,
    asset=reading_asset,
    metadata=reading_metadata
)

#Add digital signatures to prepared 'create' transaction
fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx,
    private_keys=salek_pri
)

#Send signed transaction to the bigchaindb node
sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)

#Get transaction id from signed transaction
txid = fulfilled_creation_tx['id']
print txid

# (OPTIONAL) code to check if transaction was voted valid
trials = 0
while trials < 60:
    try:
        if bdb.transactions.status(txid).get('status') == 'valid':
            print('Tx valid in:', trials, 'secs')
            break
    except bigchaindb_driver.exceptions.NotFoundError:
        trials += 1
        sleep(1)

if trials == 60:
    print('Tx is still being processed... Bye!')
    exit(0)
