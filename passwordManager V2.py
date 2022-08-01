from ast import Pass
from posixpath import split
from sysconfig import get_path
from telnetlib import ENCRYPT
from cryptography.fernet import Fernet

class passwordManager():
    def __init__(self):
        self.key = None
        self.password = None
        self.password_dict = {}
        self.email = None
        self.path_key = None
        self.path_pass = None
        
    def changeEmail(self):
        self.email = input("Please enter your email address: ")    
    
    def setPath_key(self):
        #filename = "yourKey"
        #self.path_key = "%s.key" % filename
        self.path_key = "yourKey.key"
    
    def setPath_pass(self):
        filename = self.email.split("@")[0]
        self.path_pass = "%s.pass" % filename
    
        
    
    def create_key(self):
        self.key = Fernet.generate_key()
        self.setPath_key()
        path = self.path_key
        with open(path, 'wb') as f:
            f.write(self.key)
    
    def load_key(self):
        with open(self.path_key, 'rb') as f:
            self.key =f.read()

   
    def create_password_file(self,init_value=None):
        self.setPath_pass()
        self.password_file = self.path_pass
        if init_value is not None:
            for key, value in init_value.items():
                self.add_password(key,value)
                
    def load_password_file(self):
        self.password_file = self.path_pass
        with open(self.path_pass, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self,site,password):
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")
    
    def get_password(self,site):
        return self.password_dict[site]
    

def main():
    password = {
        "emailExample": "name@domain.com",
        "facebookExample" : "facebookPass",
        "youtubeExample" : "youtubePass"
    }
    pm = passwordManager()
    Quit = False
    while not Quit:
        print("""
                Welcome,
                1.create a new account
                2.Access your account
                0.Quit the program
                """)
        choice = input("Enter your choice : ")
        if choice == "1":
            print("\nCreating your new account...")
            pm.create_key()
            print("\nKey created successfully")
            pm.changeEmail()
            print("\nEmail operation is successful")
            pm.create_password_file(password)
            print("\nPassword File created successfully!")
            print("\n Your account is all set-up!! \n")
        elif choice == "2":
            pm.changeEmail()
            Back = False
            while not Back:
                print("""
                        Welcome,
                        1.Load Key
                        2.Create new password File
                        3.Load password file
                        4.Add a new password
                        5.Access Password
                        6.show all passwords
                        7.Settings
                        8.back
                        0.Quit
                    """)
                
                choice = input("enter your choice : ")
                if pm.path_key == None:
                    print("\nkey was not available,setting new key...")
                    pm.setPath_key()
                if pm.path_pass == None:
                    print("\password file was not available,creating a new password...")
                    pm.setPath_pass()
                    
                if choice == "1":
                    
                    pm.load_key()

                elif choice == "2":
                    
                    pm.create_password_file() #pm.create_password_file(password)
                    
                elif choice == "3":
                    pm.load_password_file()
                    
                elif choice == "4":
                    site= input("Enter the site : ")
                    password = input("Please enter your password : ")
                    pm.add_password(site, password)
                    
                elif choice == "5":
                    site= input("what site do you want : ")
                    print(f'password for {site} is {pm.get_password(site)}')
                    
                elif choice == "6":
                    print("\nThis operation is still Unreleased")
                    
                elif choice == "7":
                    print("\nThis operation is still Unreleased")
                    #Settings
                    
                elif choice == "8":
                    Back = True
                    print("\nRedirecting you to Previous Menu")
                    
                elif choice == "0":
                    Back = True
                    Quit = True
                    print("\Exiting Program...")
                    print("\nTake care")
                    pass
                else:
                    print("\n\n\nERROR: unknown input")
        elif choice == "0":
            Quit = True
            print("\nQuitting Program...")
        else:
            print("Invalid choice !!")
                
if __name__ == "__main__":
    main()