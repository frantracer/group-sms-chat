# Group SMS Chat

This is a simple group SMS chat application that allows users to send and receive messages in a group chat format. 

The application uses FastAPI for the backend and SQLite for the database.


# Features

This application allow users to register using a mobile phone number, create groups, and send SMS to all the users that joined a group.

Users can join groups using a unique group name, and they can leave groups at any time.

When a user sends a message to a group using their mobile phone, all members of that group receive the message via SMS.

The messages are sent via Twilio's SMS service.

# Restrictions

The number of groups a user can join is limited to the number of Twilio phone numbers you have.

If all the users leave a group, the group will be automatically deleted.

# Run the Application

1. Get the authentication token and account SID from Twilio:
   https://console.twilio.com/us1/account/keys-credentials/api-keys

2. Create Twilio phone numbers:
   https://www.twilio.com/console/phone-numbers/incoming

3. Create .env file with the following content:
   ```
   TWILIO_ACCOUNT_SID=<your_account_sid>
   TWILIO_AUTH_TOKEN=<your_auth_token>
   TWILIO_PHONE_NUMBERS=<your_twilio_phone_numbers>
   ```

4. Build the Docker image:
   ```bash
   make docker-build
   ```

5. Run the Docker container:
   ```bash
   make docker-run
   ```

6. Run ngrok to expose the application:
   ```bash
    ngrok http http://localhost:9022
   ```

7. Configure Twilio to use the ngrok URL for incoming messages.
https://console.twilio.com/us1/develop/phone-numbers/manage/incoming

8. The API documentation is available at:
   ```
   http://localhost:9022/docs
   ```

# Development

1. Install the dependencies:
   ```bash
   make install
   ```

2. Run the linter:
   ```bash
   make format
   make lint
   ```

3. Run the tests:
   ```bash
    make test
    ```

4. Run the application locally:
   ```bash
   make run
   ```

# Future Improvements

- Make the project fully async: database calls and Twilio API calls
- Authentication using a session token instead of using a password in every endpoint
- Add salt to the password before hashing
- Error handling for Twilio API calls and database operations
- Add tests for the handlers
- Add queue for sending SMS messages
- Add logging for better debugging and monitoring