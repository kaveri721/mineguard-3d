#!/usr/bin/env python
"""
MineGuard 3D Deployment Script
Automated setup for the mining safety AI system
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ Error in {description}:")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ Exception during {description}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please install Python 3.10 or higher")
        return False

def create_virtual_environment():
    """Create and activate virtual environment"""
    system = platform.system().lower()

    if not run_command("python -m venv mineguard_env", "Creating virtual environment"):
        return False

    # Activation commands vary by OS
    if system == "windows":
        activate_cmd = "mineguard_env\\Scripts\\activate"
        pip_cmd = "mineguard_env\\Scripts\\pip"
    else:
        activate_cmd = "source mineguard_env/bin/activate"
        pip_cmd = "mineguard_env/bin/pip"

    print(f"\n📝 To activate the virtual environment manually:")
    print(f"   {activate_cmd}")

    return pip_cmd

def install_dependencies(pip_cmd):
    """Install required packages"""
    return run_command(f"{pip_cmd} install -r requirements.txt", 
                      "Installing dependencies")

def setup_models():
    """Generate data and train models"""
    system = platform.system().lower()
    if system == "windows":
        python_cmd = "mineguard_env\\Scripts\\python"
    else:
        python_cmd = "mineguard_env/bin/python"

    return run_command(f"{python_cmd} models.py", 
                      "Generating data and training models")

def launch_application():
    """Launch the Streamlit application"""
    system = platform.system().lower()
    if system == "windows":
        streamlit_cmd = "mineguard_env\\Scripts\\streamlit"
    else:
        streamlit_cmd = "mineguard_env/bin/streamlit"

    print(f"\n🚀 Launching MineGuard 3D Application...")
    print(f"📱 The application will open in your default web browser")
    print(f"🌐 URL: http://localhost:8501")
    print(f"\n⏹️  To stop the application, press Ctrl+C in this terminal")
    print(f"\n" + "="*60)

    # Launch the application
    os.system(f"{streamlit_cmd} run app.py")

def main():
    """Main deployment function"""
    print("=" * 60)
    print("🛠️  MineGuard 3D - Automated Setup Script")
    print("⛏️  AI-Powered Mining Safety System")
    print("=" * 60)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Create virtual environment
    pip_cmd = create_virtual_environment()
    if not pip_cmd:
        sys.exit(1)

    # Install dependencies
    if not install_dependencies(pip_cmd):
        sys.exit(1)

    # Setup models and data
    if not setup_models():
        sys.exit(1)

    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)

    # Ask user if they want to launch the app
    launch_choice = input("\n🚀 Would you like to launch the application now? (y/n): ").lower().strip()

    if launch_choice in ['y', 'yes']:
        launch_application()
    else:
        system = platform.system().lower()
        if system == "windows":
            activate_cmd = "mineguard_env\\Scripts\\activate"
            streamlit_cmd = "mineguard_env\\Scripts\\streamlit run app.py"
        else:
            activate_cmd = "source mineguard_env/bin/activate"
            streamlit_cmd = "mineguard_env/bin/streamlit run app.py"

        print("\n📝 To launch the application later:")
        print(f"   1. Activate virtual environment: {activate_cmd}")
        print(f"   2. Run the application: {streamlit_cmd}")
        print("\n🌐 The application will be available at: http://localhost:8501")

if __name__ == "__main__":
    main()
