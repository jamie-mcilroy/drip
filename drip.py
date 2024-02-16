import pandas as pd
import datetime

def calculate_drip(investment_period, current_price, current_yield, dividend_growth_rate, initial_shares):
    # Get the current year
    current_year = datetime.datetime.now().year
    
    # Initial calculations
    initial_annual_dividend_per_share = round(current_price * current_yield, 2)
    shares_owned = [initial_shares]  # Start with the passed in number of shares
    annual_dividend_per_share = [initial_annual_dividend_per_share]  # Initial annual dividend per share
    future_share_price = [current_price]  # Initialize with the current price
    annual_income = []  # Annual income from dividends
    dividend_per_share = [initial_annual_dividend_per_share / initial_shares]  # Dividend per share

    # Calculate each year
    for year in range(1, investment_period + 1):
        # Calculate new dividend per share based on growth rate
        new_annual_dividend_per_share = annual_dividend_per_share[-1] * (1 + dividend_growth_rate)
        annual_dividend_per_share.append(round(new_annual_dividend_per_share, 2))
        
        # Calculate dividends received for the year, used to buy new shares at current price
        dividends_received = new_annual_dividend_per_share * shares_owned[-1]
        annual_income.append(round(dividends_received, 2))  # Track annual income from dividends
        new_shares_bought = dividends_received / future_share_price[-1]
        new_shares_owned = shares_owned[-1] + new_shares_bought
        shares_owned.append(round(new_shares_owned, 0))
        
        # Update dividend per share for the year
        dividend_per_share.append(round(new_annual_dividend_per_share, 2))
        
        # Increase future share price annually by the current dividend yield
        new_share_price = future_share_price[-1] * (1 + current_yield)
        future_share_price.append(round(new_share_price, 2))

    # Create a DataFrame to return results
    results_df = pd.DataFrame({
        'Year': [current_year + i for i in range(investment_period)],
        'Shares Owned': shares_owned[1:],  # Exclude initial shares for year calculations
        'Annual Dividend Per Share': dividend_per_share[1:],  # Start calculations from the first year
        'Future Share Price': future_share_price[1:],  # Start calculations from the first year
        'Annual Income': annual_income
    }) 

    return results_df

def main():
    # Example usage with values for ENB.TO
    investment_period = 20  # years
    current_price = 45.53  # CAD
    current_yield = .0811  # Decimal
    dividend_growth_rate = .04733  # Decimal
    initial_shares = 9574  # Number of shares to start with

    results_df = calculate_drip(investment_period, current_price, current_yield, dividend_growth_rate, initial_shares)

    print(results_df)

if __name__ == "__main__":
    main()
