import phe as paillier
import json
import pandas as pd
from tqdm import tqdm

def storeKeys():
	public_key, private_key = paillier.generate_paillier_keypair(n_length=32)
	keys={}
	keys['public_key'] = {'n': public_key.n}
	keys['private_key'] = {'p': private_key.p,'q':private_key.q}
	print(keys)
	with open('./keys/B0018.json', 'w') as file:
		json.dump(keys, file)
		
def getKeys():
	with open('./keys/B0018.json', 'r') as file:
		keys=json.load(file)
		pub_key=paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
		priv_key=paillier.PaillierPrivateKey(pub_key,keys['private_key']['p'],keys['private_key']['q'])
		return pub_key, priv_key
	
storeKeys()

def serializeData(public_key):
    encrypted_data = {}
    train_data = pd.read_csv("../preprocessed_data/B0018_preprocessed.csv")
    name = ['Vehicle_Number', 'Starting_Location', 'Destination', 'Frequent_Places', 'cycle', 'ambient_temperature', 'capacity', 'voltage_measured', 'current_measured', 'temperature_measured', 'current_load', 'voltage_load', 'time']
    df2 = pd.DataFrame(columns=name)
    for index, row in tqdm(train_data.iterrows(), total=train_data.shape[0]):
        a1 = public_key.encrypt(int(row['Vehicle_Number']))
        a3 = public_key.encrypt(int(row['Starting_Location']))
        a4 = public_key.encrypt(int(row['Destination']))
        a5 = public_key.encrypt(int(row['Frequent_Places']))
        a6 = public_key.encrypt(int(row['cycle']))
        a7 = public_key.encrypt(int(row['ambient_temperature']))
        a8 = public_key.encrypt(int(row['capacity']))
        a9 = public_key.encrypt(int(row['voltage_measured']))
        a10 = public_key.encrypt(int(row['current_measured']))
        a11 = public_key.encrypt(int(row['temperature_measured']))
        a12 = public_key.encrypt(int(row['current_load']))
        a13 = public_key.encrypt(int(row['voltage_load']))
        a14 = public_key.encrypt(int(row['time']))
        x1 = str(a1.ciphertext())
        x3 = str(a3.ciphertext())
        x4 = str(a4.ciphertext())
        x5 = str(a5.ciphertext())
        x6 = str(a6.ciphertext())
        x7 = str(a7.ciphertext())
        x8 = str(a8.ciphertext())
        x9 = str(a9.ciphertext())
        x10 = str(a10.ciphertext())
        x11 = str(a11.ciphertext())
        x12 = str(a12.ciphertext())
        x13 = str(a13.ciphertext())
        x14 = str(a14.ciphertext())
        df2.loc[len(df2)] = [x1, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14]
    df2.to_csv("B0018e.csv", index=False)

pub_key, priv_key = getKeys()
serializeData(pub_key)