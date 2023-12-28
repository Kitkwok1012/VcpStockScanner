import yfinance as yf
import pandas as pd

def check_stock_conditions(data):
    condition_1 = data['Close'] > data['200MA']
    condition_1 = condition_1 & (data['Close'] >= data['30MA']) & (data['Close'] >= data['40MA'])
    condition_1 = condition_1 & (data['30MA'] > data['40MA'])

    condition_2 = data['150MA'] > data['200MA']

    condition_3 = data['200MA'].diff(20).gt(0) | data['200MA'].diff(120).gt(0)
  
    condition_4 = (data['Close'].shift(1) < data['50MA'].shift(1)) & (data['Close'] > data['50MA'])

    condition_5 = data['RS-Ranking'] >= 70

    condition_6 = data['Volume'].diff().lt(0).rolling(window=5).sum() > 0

    condition_7 = data['Volume'].rolling(window=10).mean().diff().lt(0)

    final_condition = condition_1 & condition_2 & condition_3 & condition_4 & condition_5 & condition_6 & condition_7

    return final_condition

all_tickers = yf.Tickers('^IXIC')
tickers_list = all_tickers.tickers

current_date = date.today().strftime("%Y-%m-%d")

good_stocks = []

for ticker in tickers_list:
    try:
        stock_data = ticker.history(start=start_date, end=end_date)

        stock_data['30MA'] = stock_data['Close'].rolling(window=30).mean()
        stock_data['40MA'] = stock_data['Close'].rolling(window=40).mean()
        stock_data['50MA'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['150MA'] = stock_data['Close'].rolling(window=150).mean()
        stock_data['200MA'] = stock_data['Close'].rolling(window=200).mean()

        stock_data['RS-Ranking'] = stock_data['Close'].rank(ascending=False, pct=True) * 100

        is_good_stock = check_stock_conditions(stock_data)

        if is_good_stock.any():
            good_stocks.append((ticker.ticker, stock_data[is_good_stock]))

    except Exception as e:
        print(f"Failed to fetch stock data for {ticker.ticker}. Error: {e}")

if len(good_stocks) > 0:
    file_name = "result.txt"

    with open(file_name, 'w') as file:
        file.write("The following stocks meet the conditions:\n")
        for stock in good_stocks:
            file.write(f"\nStock: {stock[0]}\n")
            file.write(stock[1].to_string(index=False))
            file.write("\n")

    print(f"Data exported to {file_name} successfully.")
else:
    print("No stocks meet the conditions today.")
