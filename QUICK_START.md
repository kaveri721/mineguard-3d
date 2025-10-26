# MineGuard 3D - Quick Setup Guide

## 🚀 Fastest Way to Get Started

### Step 1: Download the Project Files
- Download all project files to a folder on your computer
- Ensure you have Python 3.10 or higher installed

### Step 2: One-Click Setup (Recommended)

**For Windows Users:**
```cmd
double-click setup_windows.bat
```

**For Mac/Linux Users:**
```bash
chmod +x setup_unix.sh
./setup_unix.sh
```

**Manual Setup (Alternative):**
```bash
python setup.py
```

### Step 3: Launch the Application
After setup completes, the application will start automatically at:
**http://localhost:8501**

## ⚡ Manual Setup (If Automated Setup Fails)

1. **Create Virtual Environment:**
   ```bash
   python -m venv mineguard_env
   ```

2. **Activate Environment:**
   ```bash
   # Windows
   mineguard_env\Scripts\activate

   # Mac/Linux
   source mineguard_env/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate Data & Train Models:**
   ```bash
   python models.py
   ```

5. **Launch Application:**
   ```bash
   streamlit run app.py
   ```

## 🌐 Application Features

### Dashboard Tabs:
- **Time Series**: Historical sensor data visualization
- **Sensor Dashboard**: Current readings and metrics  
- **3D Mine View**: Interactive mine digital twin
- **Historical Analysis**: Hazard trends and statistics

### Controls:
- **Real-time Mode**: Auto-refresh for live monitoring
- **Manual Inputs**: Test "what-if" scenarios with custom sensor values
- **Time Range**: Select data viewing period (1 hour to 7 days)

## 🚨 Alert System

The system monitors 4 hazard types:
- 🪨 **Rockfall**: Based on displacement, strain, vibration
- 💨 **Gas Emissions**: Methane and CO monitoring  
- 🌍 **Seismic Events**: Earthquake detection
- 💧 **Groundwater**: Water level and pressure monitoring

## 📱 Access URLs
- **Main Application**: http://localhost:8501
- **Mobile Access**: Use your computer's IP address on mobile devices

## 🛠️ Troubleshooting

**Port Already in Use:**
```bash
streamlit run app.py --server.port 8502
```

**Dependencies Issues:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Model Files Missing:**
```bash
python models.py
```

## 📞 Need Help?
Check the main README.md file for detailed documentation.

---
**MineGuard 3D** - Ready to deploy in under 5 minutes! 🚀
