import pandas as pd
import datetime
import json
import glob
import os

def fetch_stock_data(csv_url):
    df = pd.read_csv(csv_url, keep_default_na=False)
    stock_data = df.set_index('Symbol')[['Current', 'DivGr', 'DY', 'DIV']].to_dict('index')
    return {symbol: (data['Current'], data['DivGr'], data['DY'], data['DIV']) for symbol, data in stock_data.items()}

def update_portfolio(portfolio, stock_data):
    for stock in portfolio:
        symbol = stock['symbol']
        if symbol in stock_data:
            current_price, dividend_growth_rate, current_yield, current_dividend = stock_data[symbol]
            current_price = float(current_price.replace('$', '').replace(',', ''))
            current_dividend = float(current_dividend.replace('$', '').replace(',', ''))
            dividend_growth_rate = float(dividend_growth_rate.replace('%', '')) / 100
            current_yield = float(current_yield.replace('%', '')) / 100  # Fixed to use current_yield correctly
            stock['current_price'] = current_price
            stock['dividend_growth_rate'] = min(dividend_growth_rate, 0.15)
            stock['current_yield'] = current_yield
            stock['current_dividend_rate'] = current_dividend
    return portfolio

def load_portfolio(file_path):
    with open(file_path, 'r') as file:
        portfolio = json.load(file)
    return portfolio

def forecast_stock_income_with_DRIP(stock_details, investment_period=15):
    current_dividend_rate = stock_details['current_dividend_rate']
    dividend_growth_rate = stock_details['dividend_growth_rate']
    shares_owned = stock_details['shares']
    current_price = stock_details['current_price']
    annual_income = []
    shares_owned_each_year = []
    for year in range(investment_period):
        annual_dividend_per_share = current_dividend_rate * (1 + dividend_growth_rate) ** year
        total_dividend_income = annual_dividend_per_share * shares_owned
        share_price_this_year = current_price * (1 + dividend_growth_rate) ** year
        shares_bought = round(total_dividend_income / share_price_this_year)
        shares_owned += shares_bought
        annual_income.append(round(total_dividend_income, 2))
        shares_owned_each_year.append(shares_owned)
    stock_details['shares'] = shares_owned
    return annual_income, shares_owned_each_year

def generate_combined_portfolio(portfolios):
    combined_portfolio = {}
    for portfolio in portfolios:
        for stock in portfolio:
            if stock['name'] in combined_portfolio:
                combined_portfolio[stock['name']]['shares'] += stock['shares']
            else:
                combined_portfolio[stock['name']] = stock
    return list(combined_portfolio.values())

def forecast_portfolio_income(portfolio):
    investment_period = 15
    current_year = datetime.datetime.now().year
    years = [current_year + i for i in range(investment_period)]
    forecast_df = pd.DataFrame(index=years)
    shares_df = pd.DataFrame(index=years)
    for stock in portfolio:
        stock_income, shares_owned_each_year = forecast_stock_income_with_DRIP(stock, investment_period)
        forecast_df[stock['name']] = stock_income
        shares_df[stock['name']] = shares_owned_each_year
    forecast_df.reset_index(inplace=True)
    forecast_df.rename(columns={'index': 'Year'}, inplace=True)
    shares_df.reset_index(inplace=True)
    shares_df.rename(columns={'index': 'Year'}, inplace=True)
    forecast_df['Total'] = forecast_df.drop('Year', axis=1).sum(axis=1)
    return forecast_df, shares_df

def print_portfolio_report(portfolio_name, forecast_df, shares_df=None):
    print(f"Portfolio Report for {portfolio_name}:")
    forecast_df.columns = ['Year'] + [f"${col}" for col in forecast_df.columns if col != 'Year']
    print(forecast_df.to_string(index=False))
    if shares_df is not None:
        print("\nShares Owned Each Year:")
        print(shares_df.to_string(index=False))
    print("\n")

def main():
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQrnYXKxB4450shcOBxz5PJeyivQIWbQRerHIjPZYkDQloDUopMreujOSPFulROXaCKPCRLqyVITS_A/pub?gid=831015118&single=true&output=csv'
    stock_data = fetch_stock_data(csv_url)
    portfolio_files = glob.glob('portfolios/*.json')
    all_portfolios = []
    for file_path in portfolio_files:
        portfolio_name = os.path.splitext(os.path.basename(file_path))[0]
        portfolio = load_portfolio(file_path)
        updated_portfolio = update_portfolio(portfolio, stock_data)
        all_portfolios.append(updated_portfolio)  # This line is crucial
        forecast_df, shares_df = forecast_portfolio_income(updated_portfolio)
        print_portfolio_report(portfolio_name, forecast_df, shares_df)

    # Now, all_portfolios correctly contains all updated individual portfolios
    if len(all_portfolios) > 1:
        combined_portfolio = generate_combined_portfolio(all_portfolios)
        forecast_combined, shares_combined = forecast_portfolio_income(combined_portfolio)
        print_portfolio_report("Combined Portfolio", forecast_combined, shares_combined)

if __name__ == "__main__":
    main()

