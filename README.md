# TelegramClientPython
This is a simple Telegram client to capture messages from channels using Telethon package.

##  Set Up
Follow the steps below to complete your telegram setup.

## Telegram App
1. Go to  https://my.telegram.org/auth?to=apps
2. Create your App and save it.


## In AWS IAM
1. create an access key for the application with programmatic access and DynamoDb permisssion
2. Copy "aws_access_key_id" and "aws_secret_access_key" to the config.json file.

## In EC2
1. Copy the App id and app has from above to the config.json file.
2. Make sure the region is mentioned correctly in config.json file.
3. Make sure the channel list is appropriate in config.json file.
4. Make sure you have the `telegram_scrapping_client.pem` key file in the folder.
5. Make sure key file has permission `chmod 400 telegram_scrapping_client.pem`.


#### Starting the telegram scraper in EC2 from your computer.
1. Now connect with the EC2 scraper 
	`ssh -i "telegram_scrapping_client.pem" ubuntu@your-public-ip`
2. start tmux session `tmux new -s telegramscrapping`
3. Run the application
	`cd TelegramClientPython`
	`python3 index.py`
4. Enter the complete mobile no with code. Example - "+919898989898"
5. Enter the access code sent on your Telegram app in the cli.
6. Now the application is running
7. Dettach from the tmux session `(ctrl + B, D)`out of there and let it run.
8. To access the tmux session `tmux attach -t telegramscrapping`


**NOTE:** There is a login limit of 5 times for each User number.
Also make sure to delete the session file `main.session` before every fresh login.
