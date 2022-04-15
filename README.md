# idor-vuln-app
Vulnerable App | Insecure Direct Object References (IDOR)

Installation:

1. I recommend using a virtual environment in the project directory
2. Open the directory and run the venv
3. "pip install -r requirements.txt"
4. Swap the .envexample file for the provided .env file

Good to go!

____________________________________________________________________


Using the App:

1. Register an account.
2. Sign into the account.
3. Select 'home'
4. Select 'account' tab.
5. Add a few spoof accounts so that they populate into your 'Account' tab.

____________________________________________________________________


Vulnerable App Solution:

1. The URL has an exposed query with a direct reference to an object.
2. The object the query is referencing happens to be the object that connects saved passwords to 
       the logged in user.
3. It will appear as "https://172.0.0.1:5000/account/user_id=x" <- this is horrible as exploiting an IDOR here
       is as simple as incrementing/decrementing the value without even needing a proxy catching requests.
4. Give it a try and see if anyone else's saved accounts come up.

____________________________________________________________________


Patch:

1. First of all- we swapped out the registered user_id generation from a simple += 1 increment:
(incrementing code)

to a randomly generated hex value.
(hex id code)

2. This means even if the referenced object is exposed in the URL.. 
(URL screenshot)

actually finding another user will be much more difficult to guess.

3. We also removed the endpoint from populating the query in the searchbar. 
       This effectively hides the object's name - further increasing security
       
4. If we wanted to go further we could add endpoint protection with decorators checking account priveleges to increase access control.

____________________________________________________________________


Hope you enjoyed!
