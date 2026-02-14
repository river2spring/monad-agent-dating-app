"""
Quick start script - Run simulation locally without blockchain
"""
import subprocess
import sys

def main():
    print("🚀 Starting AI Agent Dating Economy Simulation")
    print("=" * 60)
    print()
    print("This will launch the Streamlit dashboard where you can:")
    print("  • View 10 autonomous agents with different personalities")
    print("  • Watch them form bonds and play Prisoner's Dilemma")
    print("  • See relationship networks evolve in real-time")
    print("  • Track earnings and reputation")
    print()
    print("Dashboard will open in your browser...")
    print("=" * 60)
    print()
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'src/dashboard.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n✅ Simulation stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you've installed requirements:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
