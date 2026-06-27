# Crypto Price Checker

A simple Python command-line application that fetches cryptocurrency prices using the FreeCryptoAPI.

## Features

- Get the current price of a cryptocurrency
- Display the 24-hour price change
- Handle common network and API errors
- Read API key from an environment variable

## Requirements

- Python 3.10+
- requests

Install dependencies:

```bash
pip install requests
```

## Setup

Set your API key as an environment variable.

### Linux / macOS

```bash
export FREECRYPTO_API_KEY="your_api_key"
```

### Windows (Command Prompt)

```cmd
set FREECRYPTO_API_KEY=your_api_key
```

## Usage

```bash
python main.py BTC
```

Example:

```bash
python main.py ETH
```

## Example Output

```
-----------------------------------
 Bitcoin (BTC)
 Price: $117,842.54 USD
 24h Change: ▲ +2.31%
-----------------------------------
```

## Technologies

- Python
- Requests
- REST API
- FreeCryptoAPI

## License

This project is for learning purposes.