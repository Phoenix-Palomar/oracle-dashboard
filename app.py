import streamlit as st

# ===== Dynamic imports per evitare errori Pylance =====
# I moduli vengono importati dinamicamente quando necessario

# ===== ORACLE DASHBOARD - MULTIPAGE CONFIG =====
# Configurazione multi-pagina per Streamlit

st.set_page_config(
    page_title="Oracle Dashboard",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.sidebar.title("🔱 Oracle Dashboard")
    st.sidebar.markdown("---")
    
    # Navigation
    pages = {
        "🏠 Main Dashboard": "oracle_dashboard.py",
        "📊 Advanced Charts": "oracle_charts.py",
        "⚙️ System Config": "system_config.py",
        "📋 Reports": "reports.py"
    }
    
    selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))
    
    # === PAGE ROUTING ===
    if selected_page == "🏠 Main Dashboard":
        try:
            import oracle_dashboard
            oracle_dashboard.main()  # type: ignore
        except (ImportError, AttributeError) as e:
            st.error(f"Error loading Oracle Dashboard: {e}")
        return
    elif selected_page == "📊 Advanced Charts":
        try:
            import oracle_charts
            oracle_charts.main()  # type: ignore
        except (ImportError, AttributeError) as e:
            st.error(f"Error loading Oracle Charts: {e}")
        return
    elif selected_page == "⚙️ System Config":
        try:
            import system_config
            system_config.main()  # type: ignore
        except (ImportError, AttributeError) as e:
            st.error(f"Error loading System Config: {e}")
        return
    elif selected_page == "📋 Reports":
        try:
            import reports
            reports.main()  # type: ignore
        except (ImportError, AttributeError) as e:
            st.error(f"Error loading Reports: {e}")
        return
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Oracle Autonomous System v1.0**")
    st.sidebar.markdown("[GitHub Repository](https://github.com/Phoenix-Palomar/progetto_python)")
    
    # Welcome page
    st.title("🔱 Oracle Autonomous Trading System")
    st.markdown("## Welcome to Oracle Dashboard")
    
    st.info("""
    **Oracle Dashboard** è l'interfaccia web real-time per il sistema di trading autonomo Oracle.
    
    **Features:**
    - 🏠 **Main Dashboard**: Monitoring real-time sistema e performance
    - 📊 **Advanced Charts**: Analisi grafiche avanzate con Plotly
    - ⚙️ **System Config**: Configurazione parametri sistema
    - 📋 **Reports**: Report e analytics dettagliati
    
    **Navigation:** Usa la sidebar per navigare tra le sezioni.
    """)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Status", "🟢 ACTIVE", "Healthy")
    
    with col2:
        st.metric("Dashboard Version", "v1.0", "Latest")
    
    with col3:
        st.metric("Last Update", "2024-11-15", "Today")
    
    # Getting started
    st.markdown("## Quick Start")
    
    st.markdown("""
    1. **Verifica System Status** - Vai al Main Dashboard per monitorare lo stato del sistema
    2. **Analizza Performance** - Usa Advanced Charts per analytics dettagliate
    3. **Configura Parametri** - Accedi a System Config per personalizzazioni
    4. **Scarica Reports** - Vai alla sezione Reports per dati dettagliati
    """)
    
    # Instructions per deployment
    st.markdown("## Deployment Instructions")
    
    with st.expander("🚀 Come deployare su Streamlit Cloud"):
        st.markdown("""
        ### Setup GitHub Repository
        
        1. **Commit Dashboard Files:**
        ```bash
        git add oracle_dashboard/
        git commit -m "Add Oracle Dashboard v1.0"
        git push origin main
        ```
        
        2. **Create requirements.txt:**
        ```
        streamlit>=1.28.0
        plotly>=5.17.0
        pandas>=2.1.0
        requests>=2.31.0
        ```
        
        3. **Deploy su Streamlit Cloud:**
        - Vai su https://share.streamlit.io
        - Connect GitHub repository
        - Seleziona `oracle_dashboard/app.py` come main file
        - Deploy!
        
        4. **Environment Variables (opzionali):**
        - `WORKSPACE_PATH`: Path al workspace Oracle
        - `AUTO_REFRESH`: Abilita auto-refresh (default: true)
        """)
    
    with st.expander("🔧 Configurazione Locale"):
        st.markdown("""
        ### Run Locale
        
        ```bash
        # Install dependencies
        pip install streamlit plotly pandas requests
        
        # Run dashboard
        cd oracle_dashboard
        streamlit run app.py
        
        # Browse to http://localhost:8501
        ```
        
        ### Struttura Files
        ```
        oracle_dashboard/
        ├── app.py              # Main app (questo file)
        ├── oracle_dashboard.py # Main dashboard
        ├── oracle_charts.py    # Advanced charts
        ├── system_config.py    # System configuration
        ├── reports.py          # Reports page
        └── requirements.txt    # Dependencies
        ```
        """)

if __name__ == "__main__":
    main()