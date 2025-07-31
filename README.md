# yasac
Yet Another Simple API Client

This Python script is a lightweight, interactive API client designed to work with Zscaler OneAPI for automating operations such as retrieving access tokens and making authenticated API calls (e.g., managing custom URL categories in ZIA).


Allows user to either:

Enter an existing bearer token, or
Dynamically request a new token using Zscaler vanity domain, client ID, and client secret

Prompts the user to enter any ZIA OneAPI endpoint and payload

Supports GET and POST methods

Keeps running in a loop for repeated API calls until the user exits
