import pandas as pd
import datetime

def calculate_drip(investment_period, current_price, current_yield, dividend_growth_rate, historic_yield):
    # Get the current year
    current_year = datetime.datetime.now().year
    
    # Initial calculations
    initial_annual_dividend = round(current_price * current_yield, 2)
    shares_owned = [1000]  # Start with 1000 shares
    annual_dividend = [initial_annual_dividend]  # Initial annual dividend
    future_share_price = []  # Future share prices
    annual_income = []  # Annual income from dividends

    # Calculate each year
    for year in range(current_year, current_year + investment_period):
        # Calculate new dividend based on growth rate
        new_annual_dividend = annual_dividend[-1] * (1 + dividend_growth_rate)
        annual_dividend.append(round(new_annual_dividend, 2))
        
        # Calculate dividends received for the year, used to buy new shares at current price
        dividends_received = new_annual_dividend * shares_owned[-1]
        annual_income.append(round(dividends_received, 2))  # Track annual income from dividends
        new_shares_bought = dividends_received / current_price
        new_shares_owned = shares_owned[-1] + new_shares_bought
        shares_owned.append(round(new_shares_owned, 0))
        
        # Calculate future share price based on historic yield and new annual dividend
        new_share_price = new_annual_dividend / historic_yield
        future_share_price.append(round(new_share_price, 2))
        
        # Update current price for next cycle
        current_price = new_share_price

    # Create a DataFrame to return results
    results_df = pd.DataFrame({
        'Year': range(current_year, current_year + investment_period),
        'Shares Owned': shares_owned[1:],  # Exclude initial shares for year calculations
        'Annual Dividend': annual_dividend[1:],  # Exclude initial dividend for year calculations
        'Future Share Price': future_share_price,
        'Annual Income': annual_income,
    })

    return results_df

def main():
    # Example usage with values for ENB.TO
    investment_period = 10  # years
    current_price = 45.53  # CAD
    current_yield = .0811  # Decimal
    dividend_growth_rate = .04733  # Decimal
    historic_yield = .06733  # Decimal

    results_df = calculate_drip(investment_period, current_price, current_yield, dividend_growth_rate, historic_yield)

    print(results_df)

if __name__ == "__main__":
    main()
