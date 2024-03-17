import argparse
import sys
from datetime import datetime
import requests
from rich.console import Console
from rich.table import Table
from rich.text import Text


BASE_URL = "https://api.coingecko.com"

def get(base_url, uri, params=None):
    url = f"{base_url}{uri}"
    response = requests.get(url=url, params=params)
    return response.json()

def convert_date(date):
    date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_obj.strftime("%d-%m-%Y")

def main(args):
    parser = argparse.ArgumentParser(
        description="Use o comando `python coinanalysis.py -h` para ver as opcoes de parametros"
    )

    parser.add_argument(
        "--coin",
        "-c",
        required=True,
        default="bitcoin",
        help="Token que sera avaliado. Este valor se baseia no id do token representado no coingecko (API ID)."
    )

    args = parser.parse_args()

    data1 = get(BASE_URL, f"/api/v3/coins/{args.coin}")
    ath_price = data1['market_data']['ath']['usd']
    ath_date = data1['market_data']['ath_date']['usd']

    data2 = get(BASE_URL, f"/api/v3/coins/{args.coin}/history", params={'date':convert_date(ath_date)})
    ath_mcap=data2['market_data']['market_cap']['usd']
    ath_coins=ath_mcap/ath_price

    current_price = data1['market_data']['current_price']['usd']
    current_mcap = data1['market_data']['market_cap']['usd']
    current_coins = current_mcap/current_price

    console = Console()
    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("", style="dim", width=12)
    table.add_column("ATH", justify="right")
    table.add_column("CURRENT", justify="right")
    table.add_row(
        "PRICE",
        "${:,.2f}".format(ath_price),
        "${:,.2f}".format(current_price)
    )
    table.add_row(
        "MCAP",
        "${:,.0f}".format(ath_mcap),
        "${:,.0f}".format(current_mcap)
    )
    table.add_row(
        "COINS",
        "{:,.0f}".format(ath_coins),
        "{:,.0f}".format(current_coins)
    )
    console.print(table)

    projected_mcap = ath_price * current_coins
    projected_price = ath_mcap / current_coins

    console.print(f":pushpin: Para o token chegar no preço do ATH é necessário um MCAP de [bold yellow]${projected_mcap:,.0f}[/bold yellow].", style="bold")
    console.print(f":pushpin: Se o token chegar no MCAP do ATH o seu preço será de [bold yellow]${projected_price:,.2f}[/bold yellow].", style="bold")

if __name__ == "__main__":
    main(sys.argv[1:])
