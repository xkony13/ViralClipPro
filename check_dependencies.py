import sys
import subprocess
import pkg_resources

REQUIREMENTS = [
    'streamlit==1.32.0',
    'python-dotenv==1.0.0',
    'moviepy==1.0.3',
    'openai==1.12.0',
    'requests==2.31.0',
    'firebase-admin==6.2.0',
    'imageio==2.34.0',
    'imageio-ffmpeg==0.4.9'
]

def check_dependencies():
    missing = []
    wrong_version = []
    
    for req in REQUIREMENTS:
        try:
            pkg_resources.require(req)
        except pkg_resources.DistributionNotFound:
            missing.append(req.split('==')[0])
        except pkg_resources.VersionConflict as e:
            wrong_version.append(f"{req} (found {e.dist.version})")
    
    if missing or wrong_version:
        print("\n⚠️ Dependency issues found:")
        for pkg in missing:
            print(f" - Missing: {pkg}")
        for pkg in wrong_version:
            print(f" - Wrong version: {pkg}")
        
        print("\n🔧 Attempting to fix automatically...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("\n✅ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("\n❌ Failed to install dependencies. Please run:")
            print(f"   {sys.executable} -m pip install -r requirements.txt")
            return False
    
    print("✅ All dependencies are satisfied!")
    return True

if __name__ == '__main__':
    if not check_dependencies():
        sys.exit(1)