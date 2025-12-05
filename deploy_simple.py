"""
Simple Hugging Face Deployment Script
Run this to deploy your Insertion Sort Lab to Hugging Face Spaces
"""
from huggingface_hub import HfApi, create_repo
import getpass
import sys

def main():
    print("=" * 60)
    print("Hugging Face Space Deployment")
    print("=" * 60)
    print()
    
    # Get user input
    username = input("Enter your Hugging Face username [Aurikology]: ").strip() or "Aurikology"
    space_name = input("Enter space name [Insertion-Sort-Lab]: ").strip() or "Insertion-Sort-Lab"
    
    print("\nTo deploy, you need a Hugging Face access token.")
    print("Get one at: https://huggingface.co/settings/tokens")
    print("(Make sure to select 'Write' permission)")
    print()
    
    token = getpass.getpass("Enter your Hugging Face token: ").strip()
    
    if not token:
        print("❌ Token is required. Exiting.")
        return
    
    repo_id = f"{username}/{space_name}"
    
    try:
        # Initialize API
        api = HfApi(token=token)
        
        # Create or access space
        print(f"\n📦 Setting up space: {repo_id}...")
        create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="gradio",
            token=token,
            exist_ok=True
        )
        print("✓ Space repository ready")
        
        # Upload files
        print("\n📤 Uploading files...")
        
        files = ["app.py", "requirements.txt", "README.md"]
        for file in files:
            try:
                api.upload_file(
                    path_or_fileobj=file,
                    path_in_repo=file,
                    repo_id=repo_id,
                    repo_type="space",
                    token=token,
                    commit_message="Update: Fix error when analyzing without algorithm comparisons"
                )
                print(f"  ✓ {file}")
            except Exception as e:
                print(f"  ✗ {file}: {e}")
        
        print("\n" + "=" * 60)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("=" * 60)
        print(f"\n🚀 Your app is live at:")
        print(f"   https://huggingface.co/spaces/{repo_id}")
        print(f"\n⏳ Note: The space may take 1-2 minutes to build and start.")
        print()
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
