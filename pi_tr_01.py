import os
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit

os.system("/opt/vc/bin/vcgencmd measure_temp > sysTemp")
#script to read a file and extract a number

fo = open("sysTemp") # Open a file
str = fo.read(); #read characters in sysTemp and hold them as 'str'
fo.close() #close opened file
print(str) # print string to check
temp1=str[5:9] #chop out required characters
temp2=eval(temp1) #convert string into number
print("system temp = ", temp2) # print value to check
temp=temp2*2 # multiply by 2 to check for mathematical useability




#Use this specific keypair for this transaction

salek_pub = '6SwERTYXbqF9EB2YLqv3jUxJX1fW5VM1DZEpPzzj91Br'
salek_pri = 'CpaRDpDhNSjMm39JwjwRw6taqB8wTK4m8fk9hgHbzfJY'


bdb = BigchainDB('http://10.42.0.1:9984')

reading_asset = {
 'data': {
  'reading':{
   'serial number': 'pi01',
   'manufacturer' : 'arm' 
  },
 },
}


reading_metadata = {
 'message': 'Here is the temperature of the Raspberry Pi!',
 'temperature': temp
}



prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=salek_pub,
    asset=reading_asset,
    metadata=reading_metadata
)

fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx,
    private_keys=salek_pri
)

sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)

txid = fulfilled_creation_tx['id']

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
