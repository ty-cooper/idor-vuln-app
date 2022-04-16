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
3. Try to add a new account to your 'Account' page. What do you notice?
4. The URL should now have a direct object reference in it.

![exposed_query](https://user-images.githubusercontent.com/91342671/163654433-296dc4a2-38fb-41b8-86f6-e6ab74b3fe7d.jpg)

5. It will appear as "https://172.0.0.1:5000/account/user_id=x" <- this is horrible as exploiting an IDOR here
       is as simple as incrementing/decrementing the value without even needing a proxy catching requests.
4. Give it a try and see if anyone else's saved accounts come up.

____________________________________________________________________


Patch:

1. First of all- we swapped out the registered user_id generation from a simple += 1 increment:

![increment_code](https://user-images.githubusercontent.com/91342671/163654412-115ed502-b399-4698-8789-76804a1ac7e8.jpg)

to a randomly generated hex value.

![better_increment](https://user-images.githubusercontent.com/91342671/163654521-77578208-7349-4469-84f8-f0d534d13f5a.jpg)

2. This means even if the referenced object is exposed in the URL,
actually finding another user will be much more difficult to guess.

3. We also removed the endpoint from populating the query in the searchbar. 
       This effectively hides the object's name - further increasing security
       
4. If we wanted to go further we could add endpoint protection with decorators checking account priveleges to increase access control.

____________________________________________________________________


Hope you enjoyed!
