<h1 align="center">SAP Brute</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/y0k4i-1337/sap-brute?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/y0k4i-1337/sap-brute?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/y0k4i-1337/sap-brute?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/y0k4i-1337/sap-brute?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/y0k4i-1337/sap-brute?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/y0k4i-1337/sap-brute?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/y0k4i-1337/sap-brute?color=56BEB8" /> -->
</p>

<!-- Status -->


<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0;
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/y0k4i-1337" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

A simple tool to assess credential strength of SAP systems.

Tested systems:
  - SAP Fiori
  - SAP NetWeaver

*This tool is intended for legal purposes only. Users are responsible for ensuring that their use of this tool complies with all applicable laws and regulations.*

## :sparkles: Features ##

:heavy_check_mark: Password spray and/or brute force on SAP login pages;\
:heavy_check_mark: Anti-CSRF token retrieval;\
:heavy_check_mark: Customizable multi-step target URLs;

## :rocket: Technologies ##

The following tools were used in this project:

- [Python](https://www.python.org)
- [aiohttp](https://docs.aiohttp.org/en/stable/index.html)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com)
and [Python](https://www.python.org) (tested with 3.11.2) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/y0k4i-1337/sap-brute

# Access
$ cd sap-brute

# Install dependencies
$ pip install -r requirements.txt

# Run the project
$ ./sapbrute.py -h

```

### Usage ###

```bash
usage: sapbrute.py [-h] [--login-url LOGIN_URL] [--referer-url REFERER_URL]
                   [--max-concurrency MAX_CONCURRENCY] [--http-proxy HTTP_PROXY]
                   [--disable-ssl-verification]
                   usernames_file passwords_file client_ids_file token_url

SAP password spraying tool

positional arguments:
  usernames_file        File containing usernames
  passwords_file        File containing passwords
  client_ids_file       File containing client IDs
  token_url             URL to obtain the anti-CSRF token

options:
  -h, --help            show this help message and exit
  --login-url LOGIN_URL
                        URL for the login attempt (default: same as token URL)
  --referer-url REFERER_URL
                        Referer URL for the login attempt (default: same as token URL)
  --max-concurrency MAX_CONCURRENCY
                        Maximum number of concurrent tasks (default: 10)
  --http-proxy HTTP_PROXY
                        HTTP proxy to use for requests (e.g., http://proxy.example.com:8080)
  --disable-ssl-verification
                        Disable SSL certificate verification
```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/y0k4i-1337" target="_blank">y0k4i</a>

&#xa0;

<a href="#top">Back to top</a>
