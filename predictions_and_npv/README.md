# For research purposes only
The following directory is intended for experimenting with different approaches to predicting the Fund size and its NPV.
Most approaches are not reliable and, in some cases, even lack common sense when using RNWF data.

### Theoretical Basis for Prediction Models
1. [ARIMA](https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html) 
2. [Facebook Prophet](https://facebook.github.io/prophet/docs/quick_start.html)
3. [Neural Prophet](https://github.com/ourownstory/neural_prophet)

### Theoretical Basis for Calculating the NPV of a Fund

Net Present Value (NPV) represents the value of future cash flows discounted to the present time. 
For a fund consisting of multiple instruments, NPV is calculated as the sum of the present values of all cash flows generated by each instrument. 

To calculate the NPV of the fund considering its total value as a terminal value, we need to follow these steps:
1. Extract the balance of the fund in RUB at the last date.
2. Calculate the annual inflows and outflows and final net cash flow:
    - the inflows are sporadic and not consistent. We will calculate the annual inflow by summing all inflows for the previous 2024 year.
    - similarly, we will calculate the annual outflow by summing all outflows for the previous 2024 year.
    - net cash flow: the difference between inflows and outflows
3. Calculate Terminal Value. At the end of the projection period, the fund's value is:
Terminal Value = Initial Balance + (Net Cash Flow x Years)
4. Calculate NPV using the formula:
$$
NPV = \sum_{t=1}^{n} \frac{\text{Net Cash Flow}_t}{(1+r)^t} + \frac{\text{Terminal Value}}{(1+r)^n}
$$


5. (Bonus) Some considerations for discount rates:
  - Risk-free rate, typically government bonds. Represents the return on a risk-free investment. Commonly used as a baseline for discounting. For low-risk or risk-free instruments, to measure the intrinsic value of investments without accounting for additional risk. 
    - Example: The yield on a 10-year Russian government bond (OFZ). These rates reflect the creditworthiness of the Russian government and are often used as a baseline. Source: Moscow Exchange (MOEX) or Central Bank of Russia (CBR).
  - Market Interest Rate, reflects the prevailing rates in the financial markets. Often used for bank deposits or other market-driven investments. For instruments tied to current market rates, like floating-rate bonds. 
    - Example: the key rate set by the Central Bank of Russia (CBR). It can serve as a benchmark for short-term discount rates. Source: Central Bank of Russia website.
    - Example: for corporate bonds or loans - the average corporate bond yield or the interbank lending rate (RUONIA).
  - Cost of Capital, represents the return required by investors, often calculated as the Weighted Average Cost of Capital (WACC), Includes equity cost, debt cost, and their respective weights. For valuing a business or project. When analyzing investments with mixed financing sources.
    - Example: capitalization rates (cap rates) typical for Russian properties from the industry.
  - Credit-Adjusted Discount Rate, adjusts the risk-free rate to reflect the credit risk of an issuer. Often derived from credit ratings or bond yield spreads. For bonds or other instruments with significant credit risk.
    - Example: adjust the risk-free rate based on the credit rating of the issuer, e.g. add a credit spread to the OFZ yield for corporate bonds with a similar maturity. Source: Credit ratings from agencies
  - Expected Return, represents the anticipated return on an asset, based on historical or forecasted data. Often used for equity investments. For shares or assets where the expected return drives investment decisions.
    - Example: use the expected return on the Russian stock market - MOEX Russia Index average return or historical returns from blue-chip stocks like Gazprom or Sberbank. Source: Historical data from the Moscow Exchange
  - Inflation-Adjusted Rate (Real Rate) accounts for inflation by adjusting the nominal discount rate. Ensures cash flows are evaluated in real terms. For long-term investments or projects where inflation significantly impacts value.
    - Example: real rate = adjusted nominal rate for Russia’s inflation. Source: Inflation data from the Federal State Statistics Service (Rosstat).
  - Hurdle Rate, a minimum acceptable rate of return set by an investor or company. Often higher than the cost of capital to account for risk premiums. For internal project evaluations or venture investments.