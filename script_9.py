# Install the missing packages in the current environment so we can complete the test
import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("📦 Installing missing packages...")
try:
    install_package("streamlit==1.29.0")
    print("✅ Streamlit installed")
    install_package("plotly==5.17.0") 
    print("✅ Plotly installed")
    install_package("pydeck==0.8.1b0")
    print("✅ PyDeck installed")
    print("\n🎉 All packages installed successfully!")
except Exception as e:
    print(f"❌ Error installing packages: {e}")