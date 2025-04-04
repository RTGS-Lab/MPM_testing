#!/usr/bin/env python
"""
Utility script to verify that the MPM package has been installed correctly.
This script attempts to import the main classes and prints success or error messages.
"""

def check_installation():
    """Check that the MPM package can be imported correctly."""
    try:
        # Try to import the main module
        import mpm
        print("✅ Successfully imported mpm package")
        
        # Try to import the main classes
        from mpm import ModelHandler, Plant, Atmosphere, Environment, AbovegroundEnvironment, CarbonAssimilation, ResourcePool
        print("✅ Successfully imported all core classes")
        
        # Print the installed version
        print(f"✅ Installed version: {mpm.__version__}")
        
        # Check if examples are available
        import os
        try:
            example_files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'examples'))
            print(f"✅ Found example files: {', '.join(example_files)}")
        except Exception as e:
            print(f"⚠️  Could not find example files: {str(e)}")
        
        print("\nInstallation appears to be working correctly! 🎉")
        print("To run a basic simulation, try:\n  python examples/basic_simulation.py")
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("\nThe installation may not be complete. Try reinstalling the package:")
        print("  pip install -e .")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nAn unexpected error occurred. Please check your installation.")

if __name__ == "__main__":
    check_installation()