# File: src/06_web_interface/app.py

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add the ensemble module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../05_ensemble_learning'))
from full_pipeline import CompleteDetectionPipeline

class WebInterface:
    """
    User-friendly web interface
    """
    
    def __init__(self):
        st.set_page_config(
            page_title="Adversarial-Resilient Cybersecurity Analyzer",
            page_icon="🛡️",
            layout="wide"
        )
        
        # Load pipeline
        self.pipeline = CompleteDetectionPipeline()
    
    def run(self):
        """Run the web application"""
        st.title("🛡️ Adversarial-Resilient Cybersecurity Log Analyzer")
        st.markdown("""
        ### Detect cyber threats that try to evade AI systems
        *Upload log files or enter log details manually*
        """)
        
        # Sidebar
        with st.sidebar:
            st.header("Settings")
            detection_mode = st.selectbox(
                "Detection Mode",
                ["Standard", "High Sensitivity", "Adversarial Focus"]
            )
            
            st.header("Upload Logs")
            uploaded_file = st.file_uploader(
                "Choose CSV or JSON file",
                type=['csv', 'json']
            )
        
        # Main area
        tab1, tab2, tab3 = st.tabs(["📁 Upload & Analyze", "🔍 Single Log Test", "📊 Dashboard"])
        
        with tab1:
            self.file_upload_tab(uploaded_file)
        
        with tab2:
            self.single_log_tab()
        
        with tab3:
            self.dashboard_tab()
    
    def file_upload_tab(self, uploaded_file):
        """Handle file uploads"""
        if uploaded_file is not None:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_json(uploaded_file)
            
            st.write(f"Uploaded {len(df)} logs")
            st.dataframe(df.head())
            
            # Analyze button
            if st.button("Analyze Logs", type="primary"):
                with st.spinner("Analyzing for threats and adversarial attacks..."):
                    results = []
                    for _, row in df.iterrows():
                        result = self.pipeline.process_log(row.to_dict())
                        results.append(result)
                    
                    # Display summary
                    self.display_summary(results)
        
        else:
            st.info("Please upload a log file to begin analysis")
    
    def single_log_tab(self):
        """Manual log entry"""
        st.header("Test Single Log Entry")
        
        col1, col2 = st.columns(2)
        
        with col1:
            src_ip = st.text_input("Source IP", "192.168.1.100")
            dst_ip = st.text_input("Destination IP", "10.0.0.5")
            src_port = st.number_input("Source Port", 1024, 65535, 54321)
            dst_port = st.number_input("Destination Port", 1, 65535, 22)
        
        with col2:
            duration = st.number_input("Duration (seconds)", 1, 3600, 30)
            bytes_sent = st.number_input("Bytes Sent", 0, 1000000, 5000)
            bytes_received = st.number_input("Bytes Received", 0, 1000000, 1000)
            protocol = st.selectbox("Protocol", ["TCP", "UDP", "ICMP"])
        
        if st.button("Analyze This Log", type="primary"):
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': src_port,
                'dst_port': dst_port,
                'duration': duration,
                'bytes_sent': bytes_sent,
                'bytes_received': bytes_received,
                'protocol': protocol
            }
            
            result = self.pipeline.process_log(log_entry)
            
            # Display in nice format
            st.subheader("Analysis Result")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Threat Type", result['threat_detection']['prediction'])
            
            with col2:
                st.metric("Confidence", result['threat_detection']['confidence'])
            
            with col3:
                risk_color = {
                    'CRITICAL': 'red',
                    'HIGH': 'orange',
                    'MEDIUM': 'yellow',
                    'LOW': 'green'
                }.get(result['risk_assessment']['risk_level'], 'gray')
                
                st.metric(
                    "Risk Level",
                    result['risk_assessment']['risk_level'],
                    delta=f"Score: {result['risk_assessment']['risk_score']}",
                    delta_color=risk_color
                )
    
    def dashboard_tab(self):
        """Display system dashboard"""
        st.header("System Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("System Status", "🟢 Active")
        
        with col2:
            st.metric("Detection Mode", "Standard")
        
        with col3:
            st.metric("Models Loaded", len(self.pipeline.models))
        
        with col4:
            st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
        
        st.markdown("---")
        
        st.subheader("Model Information")
        st.info("""
        **Ensemble Detection System:**
        - Combines multiple ML models (Decision Trees, Random Forests, etc.)
        - Detects standard cyber threats
        - Identifies adversarial attack patterns
        - Provides risk scoring and confidence metrics
        """)
        
        if self.pipeline.models:
            st.subheader("Loaded Models")
            model_names = list(self.pipeline.models.keys())
            for model_name in model_names:
                st.write(f"✓ {model_name}")
        else:
            st.warning("⚠️ No models currently loaded. Please train models first.")
        
        st.markdown("---")
        
        st.subheader("System Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("""
            **Capabilities:**
            - Real-time log analysis
            - Batch file processing
            - Adversarial robustness
            - Risk assessment
            """)
        
        with col2:
            st.write("""
            **Supported Formats:**
            - CSV files
            - JSON files
            - Manual entry
            - Network flows
            """)
    
    def display_summary(self, results):
        """Display analysis summary"""
        # Count threats
        threat_counts = {}
        risk_scores = []
        
        for r in results:
            threat = r['threat_detection']['prediction']
            threat_counts[threat] = threat_counts.get(threat, 0) + 1
            risk_scores.append(r['risk_assessment']['risk_score'])
        
        # Create summary
        st.subheader("📈 Analysis Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_logs = len(results)
            st.metric("Total Logs Analyzed", total_logs)
        
        with col2:
            threats = sum([c for t, c in threat_counts.items() if t != 'normal'])
            st.metric("Threats Detected", threats)
        
        with col3:
            avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
            st.metric("Average Risk Score", f"{avg_risk:.1f}")
        
        # Threat distribution
        st.subheader("Threat Distribution")
        threat_df = pd.DataFrame({
            'Threat Type': list(threat_counts.keys()),
            'Count': list(threat_counts.values())
        })
        st.bar_chart(threat_df.set_index('Threat Type'))
        
        # Show high-risk logs
        st.subheader("🚨 High-Risk Logs (Risk > 70)")
        high_risk = [r for r in results if r['risk_assessment']['risk_score'] > 70]
        
        if high_risk:
            for hr in high_risk[:5]:  # Show top 5
                with st.expander(f"{hr['source_ip']} → {hr['destination']} "
                               f"(Risk: {hr['risk_assessment']['risk_score']})"):
                    st.json(hr)
        else:
            st.success("No high-risk logs detected!")

# Run the app
if __name__ == "__main__":
    app = WebInterface()
    app.run()