# DRIP Calculator Script

## Overview

The `drip.py` script is designed to simulate the outcomes of a Dividend Reinvestment Plan (DRIP) over a specified investment period. It takes into account the current share price, dividend yield, dividend growth rate, and historic yield to calculate the increase in shares owned, annual dividend income, future share price, and annual income from dividends, all while reinvesting dividends to purchase additional shares.

## Features

-   **Initial Share Ownership**: Starts with a predefined number of shares (e.g., 1000 shares) and calculates the growth in share ownership over time through dividend reinvestment.
-   **Dividend Growth**: Incorporates a specified annual dividend growth rate to project future dividends.
-   **Share Price Adjustment**: Calculates the future share price necessary to achieve a specified historic dividend yield.
-   **Annual Income Calculation**: Provides the annual income received from dividends, taking into account the increased number of shares and dividend per share.
-   **Results in DataFrame**: Outputs the simulation results in a pandas DataFrame for easy analysis, including actual years starting with the current year.

## Prerequisites

To run this script, you will need Python installed on your system along with the pandas library. You can install pandas using pip if you haven't already:

bashCopy code

`pip install pandas` 

## Usage

To use the script, simply run it from your terminal or command prompt. The `main()` function currently uses hardcoded values as an example. You can modify these values within the script to match your specific investment scenario:

pythonCopy code
#Example usage with values for ENB.TO 

    `# Example usage with values for ENB.TO
    investment_period = 10  # years
    current_price = 45.53  # CAD
    current_yield = 8.11 / 100  # Decimal
    dividend_growth_rate = 4.73 / 100  # Decimal
    historic_yield = 6.73 / 100  # Decimal` 

To run the script:

bashCopy code

`python drip.py` 

## Customization

You can customize the script by modifying the parameters in the `main()` function to reflect different investments, dividend growth rates, yields, and investment periods.

## Output

The script prints a pandas DataFrame to the console, showing the number of shares owned, annual dividend, future share price, and annual income from dividends for each year of the investment period.

----------

This README provides a basic overview and guide on how to use the `drip.py` script. Feel free to adjust it according to your project's needs or specific details.

## Usage - pif.py

PIF is a pet project I've been messing with for a couple of years.  The idea is take dividend growth and DRIP and mash them together to calculate the potential income for the future.  

For now, you need to create a porfolios folder and put a json file in it like the one below:

    `[
        {
            "name": "Stock A",
            "shares": 1000,
            "current_price": 45.53,
            "current_yield": 0.0811,
            "dividend_growth_rate": 0.0473
        },
        {
            "name": "Stock B",
            "shares": 500,
            "current_price": 100.00,
            "current_yield": 0.045,
            "dividend_growth_rate": 0.03
        }
    ]`