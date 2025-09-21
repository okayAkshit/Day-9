import requests
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

API_KEY = "41752acdca7e644e9fbcd752"
conversion_history = []
last_from = None
last_to = None

print(Fore.CYAN + "==============================")
print(Fore.CYAN + "        CLI Currency Converter")
print(Fore.CYAN + "==============================\n")

def get_exchange_rate(from_currency, to_currency):
    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()
    
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("result") != "success":
            print(Fore.RED + "Error: Failed to retrieve data from the API.")
            return None
        
        rates = data.get("conversion_rates")
        if not rates or to_currency not in rates:
            print(Fore.RED + f"Error: '{to_currency}' is not a valid currency code.")
            print(Fore.YELLOW + "Tip: Use standard ISO currency codes like USD, INR, EUR.")
            return None
        
        return rates[to_currency]
    
    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"Network/API error: {e}")
        return None

while True:
    # Amount input
    try:
        amount = float(input(Fore.MAGENTA + "Please enter the amount to convert: "))
        if amount <= 0:
            print(Fore.YELLOW + "Amount must be greater than zero. Please try again.")
            continue
    except ValueError:
        print(Fore.YELLOW + "Invalid input. Please enter a numerical value.")
        continue

    # Currency input
    print(Fore.CYAN + "\nOptions: type 'S' to swap last currencies, 'H' to view history.")
    fromm = input(Fore.MAGENTA + "From currency (e.g., USD): ").upper().strip()
    if fromm == 'S' and last_from and last_to:
        fromm, target = last_to, last_from
        print(Fore.GREEN + f"Currencies swapped. Converting from {fromm} to {target}.")
    elif fromm == 'H':
        print(Fore.CYAN + "\nConversion History:")
        for entry in conversion_history:
            print(entry)
        print(Fore.CYAN + "="*40)
        continue
    else:
        target = input(Fore.MAGENTA + "To currency (e.g., INR): ").upper().strip()
    
    rate = get_exchange_rate(fromm, target)
    if rate is None:
        continue
    
    converted = round(amount * rate, 2)
    
    # Display result
    print(Fore.GREEN + "\nConversion Result:")
    print(Fore.GREEN + f"{amount:,.2f} {fromm} = {converted:,.2f} {target}")
    print(Fore.CYAN + f"Exchange Rate: 1 {fromm} = {rate:,.4f} {target}")
    
    # Save to history
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conversion_history.append(f"{timestamp} | {amount:,.2f} {fromm} → {converted:,.2f} {target}")
    
    last_from, last_to = fromm, target
    
    # Next action
    next_step = input(Fore.CYAN + "\nWould you like to convert another amount? (y/n): ").lower().strip()
    if next_step != 'y':
        print(Fore.CYAN + "\nThank you for using the CLI Currency Converter.")
        break
