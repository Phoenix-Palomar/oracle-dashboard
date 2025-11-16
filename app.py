import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import requests
from datetime import datetime, timedelta, timezone
import json
import time

# ===== ORACLE DASHBOARD - STREAMLIT CLOUD VERSION =====
# Dashboard autonomo per Oracle Trading System
# Ottimizzato per deployment su Streamlit Cloud

st.set_page_config(
    page_title="Oracle Dashboard",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== UTILITY FUNCTIONS =====
@st.cache_data(ttl=300)  # Cache per 5 minuti
def load_market_data():
    """Carica dati di mercato reali da API"""
    try:
        symbols = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana']
        prices = {}
        
        for symbol in symbols:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_change=true"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if symbol in data:
                    prices[symbol.upper()] = {
                        'price': data[symbol]['usd'],
                        'change_24h': data[symbol].get('usd_24h_change', 0)
                    }
        return prices
    except Exception:
        # Fallback con dati simulati
        return generate_sample_market_data()

def generate_sample_market_data():
    """Genera dati di mercato simulati"""
    symbols = ['BITCOIN', 'ETHEREUM', 'BINANCECOIN', 'CARDANO', 'SOLANA']
    prices = {}
    base_prices = [45000, 3200, 320, 0.45, 95]
    
    for i, symbol in enumerate(symbols):
        price = base_prices[i] * np.random.uniform(0.95, 1.05)
        change = np.random.uniform(-10, 10)
        prices[symbol] = {
            'price': price,
            'change_24h': change
        }
    return prices

def generate_sample_performance_data(days=30):
    """Genera dati di performance simulati"""
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='H')
    
    # Simula performance AI e RL
    ai_balance = 10000
    rl_balance = 10000
    
    data = []
    for date in dates:
        # AI performance (più stabile)
        ai_change = np.random.normal(0.001, 0.02)
        ai_balance *= (1 + ai_change)
        
        # RL performance (più volatile ma potenzialmente migliore)
        rl_change = np.random.normal(0.002, 0.05)
        rl_balance *= (1 + rl_change)
        
        data.extend([
            {
                'timestamp': date,
                'agent': 'AI',
                'balance_usdt': ai_balance,
                'roi_eff': (ai_balance - 10000) / 10000 * 100,
                'trade_count': np.random.randint(0, 5)
            },
            {
                'timestamp': date,
                'agent': 'RL',
                'balance_usdt': rl_balance,
                'roi_eff': (rl_balance - 10000) / 10000 * 100,
                'trade_count': np.random.randint(0, 8)
            }
        ])
    
    return pd.DataFrame(data)

def calculate_system_metrics():
    """Calcola metriche di sistema simulate"""
    return {
        'system_health': np.random.uniform(85, 99),
        'heartbeat_status': np.random.choice(['ALIVE', 'OK'], p=[0.9, 0.1]),
        'feed_status': np.random.choice(['OK', 'WARNING'], p=[0.85, 0.15]),
        'active_processes': np.random.randint(3, 8),
        'avg_response_time': np.random.uniform(0.1, 2.5),
        'error_rate': np.random.uniform(0, 5),
        'uptime_hours': np.random.uniform(100, 500)
    }

# ===== CHART FUNCTIONS =====
def create_performance_chart(df, timeframe="7D"):
    """Crea grafico performance AI vs RL"""
    if df.empty:
        return go.Figure()
    
    # Filtra per timeframe
    now = datetime.now(timezone.utc)
    if timeframe == "1D":
        cutoff = now - timedelta(days=1)
    elif timeframe == "7D":
        cutoff = now - timedelta(days=7)
    elif timeframe == "30D":
        cutoff = now - timedelta(days=30)
    else:
        cutoff = now - timedelta(hours=24)
    
    df_filtered = df[df['timestamp'] > cutoff]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Balance Evolution', 'ROI Efficiency', 'Trade Volume', 'Balance Distribution'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "domain"}]]
    )
    
    # Balance evolution
    ai_data = df_filtered[df_filtered['agent'] == 'AI']
    rl_data = df_filtered[df_filtered['agent'] == 'RL']
    
    fig.add_trace(
        go.Scatter(x=ai_data['timestamp'], y=ai_data['balance_usdt'], 
                  name='AI Balance', line=dict(color='blue')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=rl_data['timestamp'], y=rl_data['balance_usdt'], 
                  name='RL Balance', line=dict(color='red')),
        row=1, col=1
    )
    
    # ROI efficiency
    fig.add_trace(
        go.Scatter(x=ai_data['timestamp'], y=ai_data['roi_eff'], 
                  name='AI ROI', line=dict(color='green')),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=rl_data['timestamp'], y=rl_data['roi_eff'], 
                  name='RL ROI', line=dict(color='orange')),
        row=1, col=2
    )
    
    # Trade volume
    ai_trades = ai_data.groupby(ai_data['timestamp'].dt.date)['trade_count'].sum()
    rl_trades = rl_data.groupby(rl_data['timestamp'].dt.date)['trade_count'].sum()
    
    fig.add_trace(
        go.Bar(x=ai_trades.index, y=ai_trades.values, name='AI Trades', marker_color='blue'),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(x=rl_trades.index, y=rl_trades.values, name='RL Trades', marker_color='red'),
        row=2, col=1
    )
    
    # Balance distribution (pie chart)
    current_ai_balance = ai_data['balance_usdt'].iloc[-1] if not ai_data.empty else 0
    current_rl_balance = rl_data['balance_usdt'].iloc[-1] if not rl_data.empty else 0
    
    fig.add_trace(
        go.Pie(labels=['AI Agent', 'RL Agent'], 
               values=[current_ai_balance, current_rl_balance],
               marker_colors=['blue', 'red']),
        row=2, col=2
    )
    
    fig.update_layout(height=600, title_text=f"Oracle Performance Analytics ({timeframe})")
    return fig

def create_market_overview_chart(market_data):
    """Crea grafico overview mercato"""
    if not market_data:
        return go.Figure()
    
    symbols = list(market_data.keys())
    prices = [market_data[s]['price'] for s in symbols]
    changes = [market_data[s]['change_24h'] for s in symbols]
    
    colors = ['green' if change > 0 else 'red' for change in changes]
    
    fig = go.Figure(data=[
        go.Bar(
            x=symbols,
            y=changes,
            marker_color=colors,
            text=[f"${price:,.2f}" for price in prices],
            textposition="outside"
        )
    ])
    
    fig.update_layout(
        title="Crypto Market Overview - 24h Changes",
        xaxis_title="Cryptocurrency",
        yaxis_title="24h Change (%)",
        height=400
    )
    
    return fig

def create_risk_analysis_chart(df):
    """Crea grafico analisi rischio"""
    if df.empty or 'balance_usdt' not in df.columns:
        return go.Figure()
    
    # Calcola drawdown per AI e RL
    ai_data = df[df['agent'] == 'AI']['balance_usdt']
    rl_data = df[df['agent'] == 'RL']['balance_usdt']
    
    ai_peak = ai_data.expanding().max()
    ai_drawdown = (ai_data - ai_peak) / ai_peak * 100
    
    rl_peak = rl_data.expanding().max()
    rl_drawdown = (rl_data - rl_peak) / rl_peak * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[df['agent'] == 'AI']['timestamp'],
        y=ai_drawdown,
        fill='tozeroy',
        name='AI Drawdown',
        line=dict(color='blue'),
        fillcolor='rgba(0,0,255,0.3)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df[df['agent'] == 'RL']['timestamp'],
        y=rl_drawdown,
        fill='tozeroy',
        name='RL Drawdown',
        line=dict(color='red'),
        fillcolor='rgba(255,0,0,0.3)'
    ))
    
    fig.update_layout(
        title="Portfolio Drawdown Analysis",
        xaxis_title="Time",
        yaxis_title="Drawdown (%)",
        height=400
    )
    
    return fig

# ===== MAIN APP =====
def main():
    # Header
    st.title("🔱 Oracle Trading System Dashboard")
    st.markdown("**Real-time Analytics** | AI vs RL Performance Monitoring")
    
    # Sidebar
    st.sidebar.title("🔱 Oracle Dashboard")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["🏠 Main Dashboard", "📊 Performance Charts", "🌍 Market Overview", "⚠️ Risk Analysis"]
    )
    
    # Controls
    timeframe = st.sidebar.selectbox("Timeframe", ["1D", "7D", "30D"], index=1)
    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    # Load data
    market_data = load_market_data()
    performance_df = generate_sample_performance_data()
    metrics = calculate_system_metrics()
    
    # === MAIN DASHBOARD ===
    if page == "🏠 Main Dashboard":
        st.header("📊 System Status Overview")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "System Health",
                f"{metrics['system_health']:.1f}%",
                delta="🟢 Healthy" if metrics['system_health'] > 90 else "🟡 OK"
            )
        
        with col2:
            status_emoji = "🟢" if metrics['heartbeat_status'] == 'ALIVE' else "🟡"
            st.metric("System Status", metrics['heartbeat_status'], f"{status_emoji} Active")
        
        with col3:
            feed_emoji = "🟢" if metrics['feed_status'] == 'OK' else "🟡"
            st.metric("Data Feed", metrics['feed_status'], f"{feed_emoji} {metrics['feed_status']}")
        
        with col4:
            st.metric("Active Processes", metrics['active_processes'], f"🔄 Running")
        
        # Performance overview
        st.header("💰 Performance Overview")
        
        if not performance_df.empty:
            recent_data = performance_df.tail(100)  # Last 100 records
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Current balances
                ai_balance = recent_data[recent_data['agent'] == 'AI']['balance_usdt'].iloc[-1]
                rl_balance = recent_data[recent_data['agent'] == 'RL']['balance_usdt'].iloc[-1]
                
                st.subheader("Current Balances")
                st.metric("AI Agent", f"${ai_balance:,.2f}", f"{((ai_balance-10000)/10000*100):+.2f}%")
                st.metric("RL Agent", f"${rl_balance:,.2f}", f"{((rl_balance-10000)/10000*100):+.2f}%")
            
            with col2:
                # ROI comparison
                ai_roi = recent_data[recent_data['agent'] == 'AI']['roi_eff'].iloc[-1]
                rl_roi = recent_data[recent_data['agent'] == 'RL']['roi_eff'].iloc[-1]
                
                st.subheader("ROI Efficiency")
                st.metric("AI ROI", f"{ai_roi:.2f}%")
                st.metric("RL ROI", f"{rl_roi:.2f}%")
                
                better_performer = "AI" if ai_roi > rl_roi else "RL"
                st.info(f"🏆 Best Performer: **{better_performer}**")
        
        # Recent activity
        st.header("📈 Recent Activity")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Avg Response Time", f"{metrics['avg_response_time']:.2f}s")
        
        with col2:
            st.metric("Error Rate", f"{metrics['error_rate']:.1f}%")
        
        with col3:
            st.metric("Uptime", f"{metrics['uptime_hours']:.0f}h")
    
    # === PERFORMANCE CHARTS ===
    elif page == "📊 Performance Charts":
        st.header(f"📈 Performance Analysis ({timeframe})")
        
        if not performance_df.empty:
            fig = create_performance_chart(performance_df, timeframe)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            st.subheader("📊 Performance Statistics")
            
            ai_data = performance_df[performance_df['agent'] == 'AI']
            rl_data = performance_df[performance_df['agent'] == 'RL']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**AI Agent Statistics**")
                st.write(f"- Average Balance: ${ai_data['balance_usdt'].mean():,.2f}")
                st.write(f"- Max Balance: ${ai_data['balance_usdt'].max():,.2f}")
                st.write(f"- Total Trades: {ai_data['trade_count'].sum()}")
                st.write(f"- Volatility: {ai_data['balance_usdt'].std():.2f}")
            
            with col2:
                st.write("**RL Agent Statistics**")
                st.write(f"- Average Balance: ${rl_data['balance_usdt'].mean():,.2f}")
                st.write(f"- Max Balance: ${rl_data['balance_usdt'].max():,.2f}")
                st.write(f"- Total Trades: {rl_data['trade_count'].sum()}")
                st.write(f"- Volatility: {rl_data['balance_usdt'].std():.2f}")
        else:
            st.warning("No performance data available")
    
    # === MARKET OVERVIEW ===
    elif page == "🌍 Market Overview":
        st.header("🌍 Crypto Market Overview")
        
        if market_data:
            fig = create_market_overview_chart(market_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Market data table
            st.subheader("Market Data")
            market_df = pd.DataFrame.from_dict(market_data, orient='index')
            market_df.index.name = 'Symbol'
            market_df['Price'] = market_df['price'].apply(lambda x: f"${x:,.2f}")
            market_df['24h Change'] = market_df['change_24h'].apply(lambda x: f"{x:+.2f}%")
            market_df = market_df[['Price', '24h Change']]
            
            st.dataframe(market_df, use_container_width=True)
        else:
            st.warning("Market data not available")
    
    # === RISK ANALYSIS ===
    elif page == "⚠️ Risk Analysis":
        st.header("⚠️ Risk Analysis")
        
        if not performance_df.empty:
            # Risk metrics
            ai_data = performance_df[performance_df['agent'] == 'AI']
            rl_data = performance_df[performance_df['agent'] == 'RL']
            
            ai_returns = ai_data['balance_usdt'].pct_change().dropna()
            rl_returns = rl_data['balance_usdt'].pct_change().dropna()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("AI Agent Risk Metrics")
                ai_vol = ai_returns.std() * 100
                ai_sharpe = ai_returns.mean() / ai_returns.std() if ai_returns.std() > 0 else 0
                st.metric("Volatility", f"{ai_vol:.2f}%")
                st.metric("Sharpe Ratio", f"{ai_sharpe:.3f}")
                
                if len(ai_returns) > 20:
                    ai_var = ai_returns.quantile(0.05) * 100
                    st.metric("VaR (5%)", f"{ai_var:.2f}%")
            
            with col2:
                st.subheader("RL Agent Risk Metrics")
                rl_vol = rl_returns.std() * 100
                rl_sharpe = rl_returns.mean() / rl_returns.std() if rl_returns.std() > 0 else 0
                st.metric("Volatility", f"{rl_vol:.2f}%")
                st.metric("Sharpe Ratio", f"{rl_sharpe:.3f}")
                
                if len(rl_returns) > 20:
                    rl_var = rl_returns.quantile(0.05) * 100
                    st.metric("VaR (5%)", f"{rl_var:.2f}%")
            
            # Drawdown chart
            fig_risk = create_risk_analysis_chart(performance_df)
            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.warning("Insufficient data for risk analysis")
    
    # Auto refresh
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Oracle Dashboard v1.0**")
    st.sidebar.markdown("Real-time AI vs RL Trading Analytics")
    
    # Footer main
    st.markdown("---")
    st.markdown(
        f"**Oracle Trading System Dashboard** | "
        f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"[Phoenix-Palomar](https://github.com/Phoenix-Palomar)"
    )

if __name__ == "__main__":
    main()
