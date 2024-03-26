# phase-3-project
[![Python 3.7](https://img.shields.io/badge/Python-3.7-blue.svg)](http://www.python.org/download/)
![platform](https://img.shields.io/badge/Platform-Linux%7CMacOS%7CWindows-brightgreen.svg)
# install:
```bash
sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev
pyenv install 3.8.13
```
# ORM:
```bash
User -> Username
Username -> Password
```

# Usage (new user):
##### 1. In your terminal navigate to, the Classes directory then use python -i user.py to tell the python interpreter to execute the script in the user.py file and stay in interactive mode then call the create function in the User class with parameters of the new user's first and last name as shown below:
![Screenshot 2024-03-26 124305_new_user_1](https://github.com/lskervin/phase-3-project/assets/156468489/675b8eca-72fb-432f-ab2e-1107cb2b060d)
#### ***Disclaimer: Executing the create function in the User class triggers the functions generate_username() and generate_password.*** 
##### 2. After creating a user run quit() in your terminal, then use python -i main.py to tell the python interpreter to execute the script in the main.py file and stay in interactive mode, you will see the prompt to enter a username as shown below: 
![Screenshot 2024-03-26 114432_1](https://github.com/lskervin/phase-3-project/assets/156468489/e7fca5e9-4558-4358-a446-3df75e5dafba)
#### ***Disclaimer: Verify Username exists in users.db, see below:***
![Screenshot 2024-03-26 115453_2](https://github.com/lskervin/phase-3-project/assets/156468489/5586c49c-5f79-44b9-a72b-7431231418c7)
##### 3. The crack_password_for_username function will be executed until the password is cracked, see below:
![Screenshot 2024-03-26 115454_3](https://github.com/lskervin/phase-3-project/assets/156468489/e9f7b0bc-89f4-4ca6-aa93-a8fa8bdf1761)
# Usage (existing user):
##### Follow Steps 2 and 3 from above in  [Usage (new user)](#usage-new-user)
