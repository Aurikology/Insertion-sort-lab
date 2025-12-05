"""
Script to deploy the Insertion Sort Lab to Hugging Face Spaces
"""
from huggingface_hub import HfApi, create_repo, upload_folder
import os
import sys

def deploy_to_hf(space_name="Insertion-Sort-Lab", username="Aurikology"):
    """
    Deploy the app to Hugging Face Spaces
    """
    try:
        # Check if token is available
        token = os.getenv("HF_TOKEN")
        if not token:
            print("⚠️  HF_TOKEN environment variable not found.")
            print("Please set it with your Hugging Face token:")
            print("  $env:HF_TOKEN='your_token_here'  (PowerShell)")
            print("\nYou can create a token at: https://huggingface.co/settings/tokens")
            return False
        
        # Initialize the API
        api = HfApi(token=token)
        
        # Space details
        repo_id = f"{username}/{space_name}"
        
        # Try to create the space (will skip if already exists)
        try:
            print(f"Creating Hugging Face Space: {repo_id}...")
            create_repo(
                repo_id=repo_id,
                repo_type="space",
                space_sdk="gradio",
                token=token,
                exist_ok=True
            )
            print("✓ Space repository ready")
        except Exception as e:
            print(f"Note: {e}")
        
        # Upload files
        print(f"\nUploading files to {repo_id}...")
        
        files_to_upload = [
            ("app.py", "Main application file"),
            ("requirements.txt", "Dependencies"),
            ("README.md", "Documentation")
        ]
        
        for filename, description in files_to_upload:
            if os.path.exists(filename):
                try:
                    api.upload_file(
                        path_or_fileobj=filename,
                        path_in_repo=filename,
                        repo_id=repo_id,
                        repo_type="space",
                        token=token,
                        commit_message=f"Update {filename}: Fix error when analyzing without algorithm comparisons"
                    )
                    print(f"✓ Uploaded {filename} ({description})")
                except Exception as e:
                    print(f"✗ Error uploading {filename}: {e}")
            else:
                print(f"⚠️  {filename} not found, skipping...")
        
        print("\n✅ Deployment complete!")
        print(f"\n🚀 Your Space is live at: https://huggingface.co/spaces/{repo_id}")
        print("\n📝 Note: It may take 1-2 minutes for the Space to rebuild and restart.")
        return True
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        print("\nMake sure you have:")
        print("1. Set HF_TOKEN environment variable with your Hugging Face token")
        print("2. Your token has write permissions")
        return False

if __name__ == "__main__":
    success = deploy_to_hf()
    sys.exit(0 if success else 1)
