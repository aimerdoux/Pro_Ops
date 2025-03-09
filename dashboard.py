import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Crypto Arbitrage System Optimization",
    page_icon="📈",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f9f9f9;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
    .stat-value {
        font-size: 1.75rem;
        font-weight: bold;
    }
    .green-text {
        color: #2e7d32;
    }
    .blue-text {
        color: #1976d2;
    }
    .purple-text {
        color: #7b1fa2;
    }
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<div class='main-header'>Crypto Arbitrage System Optimization</div>", unsafe_allow_html=True)
st.markdown("Optimize your cryptocurrency arbitrage between Robinhood, Coinbase, Kraken, and Binance")

# Initialize session state for parameters
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.initial_capital = 4000
    st.session_state.months = 12
    st.session_state.spread_percentage = 5.5
    st.session_state.reinvestment_rate = 100
    st.session_state.cycles_per_month = 15
    
    # Capital distribution
    st.session_state.robinhood_capital = 1000
    st.session_state.coinbase_capital = 1500
    st.session_state.kraken_capital = 1000
    st.session_state.cashapp_capital = 500
    
    # Platform data
    st.session_state.platform_data = {
        'robinhood': {'fee': 0.1, 'transfer_time': 24, 'daily_limit': 1000},
        'coinbase': {'fee': 0.4, 'transfer_time': 144, 'daily_limit': 10000},
        'kraken': {'fee': 0.26, 'transfer_time': 24, 'daily_limit': 5000},
        'cashapp_fast': {'fee': 1.7, 'transfer_time': 1, 'daily_limit': 7500},
        'cashapp_standard': {'fee': 0, 'transfer_time': 48, 'daily_limit': 7500}
    }

# Helper function to format currencies
def format_currency(value):
    return f"${value:,.2f}"

# Helper function to format percentages
def format_percentage(value):
    return f"{value:.2f}%"

# Format platform name for display
def format_platform_name(name):
    if not name:
        return ''
    name = name.replace('_', ' ')
    return ' '.join(word.capitalize() for word in name.split())

# Calculate profit for a specific platform
def calculate_platform_profit(platform_key, capital):
    if platform_key not in st.session_state.platform_data:
        return 0
    
    platform = st.session_state.platform_data[platform_key]
    fee = platform['fee']
    transfer_time = platform['transfer_time']
    daily_limit = platform['daily_limit']
    
    # Effective capital is limited by daily limit
    effective_capital = min(capital, daily_limit * 30)
    
    # Calculate cycles based on time and capital constraints
    time_based_cycles = st.session_state.cycles_per_month * (720 / (720 + transfer_time))
    capital_based_cycles = np.floor(30 * effective_capital / daily_limit)
    adjusted_cycles = min(time_based_cycles, capital_based_cycles)
    
    # Calculate profit
    cycle_profit = (st.session_state.spread_percentage - fee) / 100
    monthly_return = np.power(1 + cycle_profit, adjusted_cycles) - 1
    
    return capital * monthly_return

# Run the simulation
def run_simulation():
    sim_data = []
    comp_data = []
    
    # Initial state
    current_capital = st.session_state.initial_capital
    previous_capital = st.session_state.initial_capital
    r_capital = st.session_state.robinhood_capital
    c_capital = st.session_state.coinbase_capital
    k_capital = st.session_state.kraken_capital
    ca_capital = st.session_state.cashapp_capital
    
    # Calculate total profit from all platforms
    def calculate_multi_platform_return():
        robinhood_profit = calculate_platform_profit('robinhood', r_capital)
        coinbase_profit = calculate_platform_profit('coinbase', c_capital)
        kraken_profit = calculate_platform_profit('kraken', k_capital)
        cashapp_profit = calculate_platform_profit('cashapp_standard', ca_capital)
        
        return robinhood_profit + coinbase_profit + kraken_profit + cashapp_profit
    
    # Simulate month by month
    for month in range(st.session_state.months + 1):
        if month == 0:
            # Initial month
            sim_data.append({
                'month': month,
                'capital': st.session_state.initial_capital,
                'profit': 0,
                'robinhood_capital': st.session_state.robinhood_capital,
                'coinbase_capital': st.session_state.coinbase_capital,
                'kraken_capital': st.session_state.kraken_capital,
                'cashapp_capital': st.session_state.cashapp_capital,
                'return_rate': 0,
                'accumulated_return': 0
            })
        else:
            # Calculate profit for this month
            monthly_profit = calculate_multi_platform_return()
            monthly_return = monthly_profit / current_capital
            
            # Apply reinvestment
            reinvested_profit = monthly_profit * st.session_state.reinvestment_rate / 100
            current_capital = previous_capital + reinvested_profit
            
            # Distribute reinvested profits proportionally
            total_previous = previous_capital
            r_percent = r_capital / total_previous
            c_percent = c_capital / total_previous
            k_percent = k_capital / total_previous
            ca_percent = ca_capital / total_previous
            
            r_capital += reinvested_profit * r_percent
            c_capital += reinvested_profit * c_percent
            k_capital += reinvested_profit * k_percent
            ca_capital += reinvested_profit * ca_percent
            
            # Record data
            sim_data.append({
                'month': month,
                'capital': round(current_capital, 2),
                'profit': round(monthly_profit, 2),
                'robinhood_capital': round(r_capital, 2),
                'coinbase_capital': round(c_capital, 2),
                'kraken_capital': round(k_capital, 2),
                'cashapp_capital': round(ca_capital, 2),
                'return_rate': round(monthly_return * 100, 2),
                'accumulated_return': round((current_capital / st.session_state.initial_capital - 1) * 100, 2)
            })
            
            previous_capital = current_capital
    
    # Generate comparison data for each platform
    platform_keys = ['robinhood', 'coinbase', 'kraken', 'cashapp_fast', 'cashapp_standard']
    
    for key in platform_keys:
        platform = st.session_state.platform_data[key]
        
        adjusted_cycles = min(
            st.session_state.cycles_per_month * (720 / (720 + platform['transfer_time'])),
            np.floor(30 * st.session_state.initial_capital / platform['daily_limit'])
        )
        
        cycle_profit = (st.session_state.spread_percentage - platform['fee']) / 100
        monthly_return = np.power(1 + cycle_profit, adjusted_cycles) - 1
        yearly_return = np.power(1 + monthly_return, 12) - 1
        
        comp_data.append({
            'platform': key,
            'fee': platform['fee'],
            'transfer_time': platform['transfer_time'],
            'daily_limit': platform['daily_limit'],
            'monthly_volume': platform['daily_limit'] * 30,
            'cycles_per_month': round(adjusted_cycles, 1),
            'monthly_return': round(monthly_return * 100, 2),
            'yearly_return': round(yearly_return * 100, 2)
        })
    
    return pd.DataFrame(sim_data), pd.DataFrame(comp_data)

# Get total allocated capital
def get_total_allocated_capital():
    return (st.session_state.robinhood_capital + 
            st.session_state.coinbase_capital + 
            st.session_state.kraken_capital + 
            st.session_state.cashapp_capital)

# Create tabs for the dashboard
tab1, tab2, tab3 = st.tabs(["Simulation Parameters", "Results", "Strategy"])

# Tab 1: Simulation Parameters
with tab1:
    # Create two columns for the main parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='sub-header'>Main Parameters</div>", unsafe_allow_html=True)
        
        st.session_state.initial_capital = st.number_input(
            "Initial Capital ($)",
            min_value=1000,
            max_value=1000000,
            value=st.session_state.initial_capital,
            step=500
        )
        
        st.session_state.spread_percentage = st.slider(
            "Spread Percentage (%)",
            min_value=0.1,
            max_value=10.0,
            value=st.session_state.spread_percentage,
            step=0.1
        )
        
        st.session_state.cycles_per_month = st.slider(
            "Cycles Per Month",
            min_value=1,
            max_value=30,
            value=st.session_state.cycles_per_month,
            step=1
        )
        
        st.session_state.months = st.slider(
            "Time Horizon (Months)",
            min_value=1,
            max_value=36,
            value=st.session_state.months,
            step=1
        )
        
        st.session_state.reinvestment_rate = st.slider(
            "Reinvestment Rate (%)",
            min_value=0,
            max_value=100,
            value=st.session_state.reinvestment_rate,
            step=5
        )
    
    with col2:
        st.markdown("<div class='sub-header'>Capital Distribution</div>", unsafe_allow_html=True)
        
        st.session_state.robinhood_capital = st.number_input(
            "Robinhood Capital ($)",
            min_value=0,
            max_value=int(st.session_state.initial_capital),
            value=min(st.session_state.robinhood_capital, st.session_state.initial_capital),
            step=100,
            help="Daily limit: $1,000"
        )
        
        st.session_state.coinbase_capital = st.number_input(
            "Coinbase Capital ($)",
            min_value=0,
            max_value=int(st.session_state.initial_capital),
            value=min(st.session_state.coinbase_capital, st.session_state.initial_capital),
            step=100,
            help="6-day holding period"
        )
        
        st.session_state.kraken_capital = st.number_input(
            "Kraken Capital ($)",
            min_value=0,
            max_value=int(st.session_state.initial_capital),
            value=min(st.session_state.kraken_capital, st.session_state.initial_capital),
            step=100,
            help="Daily limit: $5,000"
        )
        
        st.session_state.cashapp_capital = st.number_input(
            "CashApp Capital ($)",
            min_value=0,
            max_value=int(st.session_state.initial_capital),
            value=min(st.session_state.cashapp_capital, st.session_state.initial_capital),
            step=100,
            help="Instant (1.7% fee) or Standard (0% fee, 48h)"
        )
        
        total_allocated = get_total_allocated_capital()
        is_matching = total_allocated == st.session_state.initial_capital
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**Total Allocated Capital:**")
        
        if is_matching:
            st.markdown(f"<span class='stat-value green-text'>{format_currency(total_allocated)}</span> (Matches initial capital)", unsafe_allow_html=True)
        else:
            diff = total_allocated - st.session_state.initial_capital
            st.markdown(f"<span class='stat-value' style='color: red;'>{format_currency(total_allocated)}</span> (Mismatch: {format_currency(diff)})", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Run simulation and generate data
simulation_df, comparison_df = run_simulation()

# Tab 2: Results
with tab2:
    # Summary statistics in cards at the top
    st.markdown("<div class='sub-header'>Summary Statistics</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("**Ending Capital**")
        ending_capital = simulation_df.iloc[-1]['capital'] if not simulation_df.empty else st.session_state.initial_capital
        st.markdown(f"<span class='stat-value'>{format_currency(ending_capital)}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("**Total Profit**")
        total_profit = ending_capital - st.session_state.initial_capital
        st.markdown(f"<span class='stat-value green-text'>{format_currency(total_profit)}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("**Return Rate**")
        return_rate = simulation_df.iloc[-1]['accumulated_return'] if not simulation_df.empty else 0
        st.markdown(f"<span class='stat-value blue-text'>{format_percentage(return_rate)}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Capital growth chart
    st.markdown("<div class='sub-header'>Capital Growth Over Time</div>", unsafe_allow_html=True)
    
    # Create a plotly figure for capital growth
    fig1 = go.Figure()
    
    # Add traces for each capital type
    fig1.add_trace(go.Scatter(
        x=simulation_df['month'],
        y=simulation_df['capital'],
        mode='lines+markers',
        name='Total Capital ($)',
        line=dict(color='#8884d8', width=3),
        marker=dict(size=8)
    ))
    
    fig1.add_trace(go.Scatter(
        x=simulation_df['month'],
        y=simulation_df['robinhood_capital'],
        mode='lines',
        name='Robinhood Capital',
        line=dict(color='#2196F3')
    ))
    
    fig1.add_trace(go.Scatter(
        x=simulation_df['month'],
        y=simulation_df['coinbase_capital'],
        mode='lines',
        name='Coinbase Capital',
        line=dict(color='#9C27B0')
    ))
    
    fig1.add_trace(go.Scatter(
        x=simulation_df['month'],
        y=simulation_df['kraken_capital'],
        mode='lines',
        name='Kraken Capital',
        line=dict(color='#4CAF50')
    ))
    
    fig1.add_trace(go.Scatter(
        x=simulation_df['month'],
        y=simulation_df['cashapp_capital'],
        mode='lines',
        name='CashApp Capital',
        line=dict(color='#FFC107')
    ))
    
    # Update layout
    fig1.update_layout(
        title='',
        xaxis_title='Month',
        yaxis_title='Capital ($)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode="x unified"
    )
    
    fig1.update_xaxes(tickmode='linear', tick0=0, dtick=1)
    
    # Display the chart
    st.plotly_chart(fig1, use_container_width=True)
    
    # Monthly profit chart
    st.markdown("<div class='sub-header'>Monthly Profit</div>", unsafe_allow_html=True)
    
    # Filter out the initial month (0) which has no profit
    profit_data = simulation_df[simulation_df['month'] > 0]
    
    # Create a plotly bar chart for monthly profit
    fig2 = px.bar(
        profit_data,
        x='month',
        y='profit',
        labels={'month': 'Month', 'profit': 'Profit ($)'},
        color_discrete_sequence=['#82ca9d']
    )
    
    fig2.update_layout(
        title='',
        xaxis_title='Month',
        yaxis_title='Monthly Profit ($)',
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode="x unified"
    )
    
    fig2.update_xaxes(tickmode='linear', tick0=1, dtick=1)
    
    # Display the chart
    st.plotly_chart(fig2, use_container_width=True)
    
    # Platform comparison
    st.markdown("<div class='sub-header'>Platform Comparison</div>", unsafe_allow_html=True)
    
    # Format the comparison dataframe for display
    display_comparison_df = comparison_df.copy()
    display_comparison_df['platform'] = display_comparison_df['platform'].apply(format_platform_name)
    display_comparison_df.columns = [col.replace('_', ' ').title() for col in display_comparison_df.columns]
    
    # Format columns
    display_comparison_df['Fee'] = display_comparison_df['Fee'].apply(lambda x: f"{x}%")
    display_comparison_df['Daily Limit'] = display_comparison_df['Daily Limit'].apply(lambda x: f"${x:,}")
    display_comparison_df['Monthly Volume'] = display_comparison_df['Monthly Volume'].apply(lambda x: f"${x:,}")
    display_comparison_df['Monthly Return'] = display_comparison_df['Monthly Return'].apply(lambda x: f"{x}%")
    display_comparison_df['Yearly Return'] = display_comparison_df['Yearly Return'].apply(lambda x: f"{x}%")
    
    # Rename columns for better display
    display_comparison_df = display_comparison_df.rename(columns={
        'Platform': 'Platform',
        'Fee': 'Fee (%)',
        'Transfer Time': 'Transfer Time (hrs)',
        'Daily Limit': 'Daily Limit ($)',
        'Monthly Volume': 'Monthly Volume ($)',
        'Cycles Per Month': 'Cycles/Month',
        'Monthly Return': 'Monthly Return',
        'Yearly Return': 'Yearly Return'
    })
    
    # Display the table
    st.dataframe(display_comparison_df, use_container_width=True)

# Tab 3: Strategy
with tab3:
    st.markdown("<div class='sub-header'>Optimized Multi-Platform Strategy</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card' style='background-color: #fffde7;'>", unsafe_allow_html=True)
    st.markdown("### Current Capital Distribution")
    st.markdown(f"Optimized allocation of your {format_currency(st.session_state.initial_capital)} starting capital:")
    
    # Display the capital distribution as a bullet list
    st.markdown(f"""
    * **Robinhood:** {format_currency(st.session_state.robinhood_capital)} ({format_currency(min(st.session_state.platform_data['robinhood']['daily_limit'], st.session_state.robinhood_capital))}/day effective throughput)
    * **Coinbase:** {format_currency(st.session_state.coinbase_capital)} (6-day cycle, rolling deposits)
    * **Kraken:** {format_currency(st.session_state.kraken_capital)} ({format_currency(min(st.session_state.platform_data['kraken']['daily_limit'], st.session_state.kraken_capital))}/day effective throughput)
    * **CashApp:** {format_currency(st.session_state.cashapp_capital)} (reserve for opportunistic trades)
    """)
    
    st.markdown("### Daily Operational Schedule:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Monday-Friday:**")
        st.markdown("""
        * Deploy Robinhood capital ($1,000/day)
        * Deploy Kraken capital (up to $5,000/day)
        * Monitor Coinbase capital releases (after 6-day hold)
        """)
    
    with col2:
        st.markdown("**Timing Strategy:**")
        st.markdown("""
        * Morning: Initiate transfers from purchasing platforms
        * Afternoon: Execute P2P trades on Binance
        * Evening: Prepare next day's transactions
        """)
    
    st.markdown("### Maximum Monthly Throughput:")
    
    max_throughput = (
        st.session_state.platform_data['robinhood']['daily_limit'] * 30 +
        st.session_state.platform_data['kraken']['daily_limit'] * 30 +
        st.session_state.coinbase_capital / 2
    )
    
    st.markdown(f"<span class='stat-value green-text'>{format_currency(max_throughput)}</span>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <p style='font-size: 0.9rem; color: #666;'>
    (Based on Robinhood: {format_currency(st.session_state.platform_data['robinhood']['daily_limit'] * 30)}, 
    Kraken: {format_currency(st.session_state.platform_data['kraken']['daily_limit'] * 30)}, 
    Coinbase: ~{format_currency(st.session_state.coinbase_capital / 2)} with 6-day cycle)
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Add info about when the simulation was last run
st.sidebar.markdown("### Simulation Info")
st.sidebar.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.sidebar.markdown(f"Initial capital: {format_currency(st.session_state.initial_capital)}")
st.sidebar.markdown(f"Spread percentage: {format_percentage(st.session_state.spread_percentage)}")
st.sidebar.markdown(f"Time horizon: {st.session_state.months} months")

# Add a button to re-run the simulation manually if needed
if st.sidebar.button("Re-run Simulation"):
    st.experimental_rerun()
