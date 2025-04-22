import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# --- Classes ---
class IPAsset:
    def __init__(self, name, cash_flows, discount_rate):
        self.name = name
        self.cash_flows = cash_flows
        self.discount_rate = discount_rate

    def net_present_value(self):
        return np.sum([cf / (1 + self.discount_rate)**i for i, cf in enumerate(self.cash_flows, start=1)])

class LicensedIP(IPAsset):
    pass

class InternalIP(IPAsset):
    def __init__(self, name, sale_value, years_until_sale, discount_rate):
        super().__init__(name, [], discount_rate)
        self.sale_value = sale_value
        self.years_until_sale = years_until_sale

    def net_present_value(self):
        return self.sale_value / (1 + self.discount_rate)**self.years_until_sale

class SubscriptionIP(IPAsset):
    def __init__(self, name, total_app_cash_flows, ip_allocation_percent, discount_rate):
        allocated_flows = [cf * ip_allocation_percent for cf in total_app_cash_flows]
        super().__init__(name, allocated_flows, discount_rate)

# --- Streamlit UI ---
st.title("💸 IP Portfolio Valuation Tool")

st.sidebar.header("Input Your IP Details")

years = st.sidebar.slider("Number of forecast years", 3, 10, 5)

# Discount rate
discount_rate = st.sidebar.slider("Discount Rate (%)", 1.0, 20.0, 8.0) / 100

# Licensed IP
st.sidebar.subheader("Licensed IP")
licensed_cf = [st.sidebar.number_input(f"Year {i+1} Cash Flow", min_value=0, value=10000) for i in range(years)]

# Internal IP
st.sidebar.subheader("Internal IP")
internal_value = st.sidebar.number_input("Estimated Sale Value", min_value=0, value=50000)
sale_year = st.sidebar.slider("Years Until Sale", 1, years, 3)

# Subscription IP
st.sidebar.subheader("Subscription IP")
total_app_cf = [st.sidebar.number_input(f"App Revenue Year {i+1}", min_value=0, value=50000 + i*2000) for i in range(years)]
allocation_pct = st.sidebar.slider("Allocation to IP (%)", 0.0, 100.0, 20.0) / 100

# Create portfolio
licensed = LicensedIP("Licensed IP", licensed_cf, discount_rate)
internal = InternalIP("Internal IP", internal_value, sale_year, discount_rate)
sub_ip = SubscriptionIP("Subscription IP", total_app_cf, allocation_pct, discount_rate)

portfolio = [licensed, internal, sub_ip]

# Valuation results
st.header("📊 Valuation Summary")
total_value = sum(ip.net_present_value() for ip in portfolio)
st.metric("Total Portfolio Value", f"${total_value:,.2f}")

for ip in portfolio:
    st.write(f"**{ip.name}**: ${ip.net_present_value():,.2f}")

# Plotting
def plot_cash_flows(portfolio, years):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(1, years + 1)
    for ip in portfolio:
        if ip.cash_flows:
            ax.plot(x[:len(ip.cash_flows)], ip.cash_flows, marker='o', label=ip.name)
    ax.set_title("Cash Flows Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cash Flow ($)")
    ax.legend()
    st.pyplot(fig)

def plot_valuation_breakdown(portfolio):
    names = [ip.name for ip in portfolio]
    values = [ip.net_present_value() for ip in portfolio]
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=values, y=names, palette="coolwarm", ax=ax)
    ax.set_title("NPV by IP Asset")
    ax.set_xlabel("Value ($)")
    st.pyplot(fig)

st.header("📈 Charts")
plot_cash_flows(portfolio, years)
plot_valuation_breakdown(portfolio)