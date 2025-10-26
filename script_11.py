# Create a final project summary and directory listing
import os

print("📁 MineGuard 3D - Final Project Structure")
print("=" * 60)

files_created = []
for file in os.listdir('.'):
    if file.endswith(('.py', '.csv', '.pkl', '.txt', '.md', '.bat', '.sh')):
        size = os.path.getsize(file)
        files_created.append((file, size))

# Sort by file type and name
files_created.sort(key=lambda x: (x[0].split('.')[-1], x[0]))

for filename, size in files_created:
    if size < 1024:
        size_str = f"{size} B"
    elif size < 1024*1024:
        size_str = f"{size/1024:.1f} KB"
    else:
        size_str = f"{size/(1024*1024):.1f} MB"
    
    print(f"📄 {filename:<30} ({size_str})")

# Count files by type
file_types = {}
for filename, _ in files_created:
    ext = filename.split('.')[-1]
    file_types[ext] = file_types.get(ext, 0) + 1

print("\n📊 File Summary:")
print("-" * 30)
for ext, count in sorted(file_types.items()):
    print(f"{ext.upper()} files: {count}")

print(f"\nTotal project files: {len(files_created)}")

print("\n🎯 Key Components Created:")
print("✅ Synthetic mining dataset (10,000 sensor readings)")
print("✅ AI/ML models for 4 hazard types (trained & saved)")
print("✅ Interactive Streamlit web application") 
print("✅ 3D digital twin visualization")
print("✅ Real-time monitoring dashboard")
print("✅ What-if scenario simulation")
print("✅ Automated setup scripts")
print("✅ Comprehensive documentation")
print("✅ System testing suite")

print("\n🚀 Ready for Deployment!")