"""
Script to download an education-themed background image for the website.
This script downloads a high-quality education/learning image from Unsplash.
"""

import os
import requests
from pathlib import Path

def download_education_image():
    """Download an education-themed background image"""
    
    # Create images directory if it doesn't exist
    images_dir = Path("static/images")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    image_path = images_dir / "education-background.jpg"
    
    # Check if image already exists
    if image_path.exists():
        print(f"Image already exists at: {image_path}")
        response = input("Do you want to download a new one? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing image.")
            return
    
    print("Downloading education-themed background image...")
    print("This may take a moment...")
    
    # Education-themed image URLs from Unsplash
    image_urls = [
        # Modern education/learning images
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920&q=80&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920&q=80&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1920&q=80&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920&q=80&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80&auto=format&fit=crop",
    
    ]
    
    # Try to download from Unsplash
    for i, url in enumerate(image_urls, 1):
        try:
            print(f"Trying image source {i}/{len(image_urls)}...")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Save the image
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = image_path.stat().st_size / (1024 * 1024)  # Size in MB
            print(f"✓ Successfully downloaded education image!")
            print(f"  Location: {image_path}")
            print(f"  Size: {file_size:.2f} MB")
            print("\nThe image is now ready to use!")
            return
            
        except Exception as e:
            print(f"  Failed: {str(e)}")
            if i < len(image_urls):
                print("  Trying next source...")
            continue
    
    # If all URLs fail, provide manual instructions
    print("\n" + "="*60)
    print("Automatic download failed. Please download manually:")
    print("="*60)
    print("\n1. Visit one of these sites:")
    print("   - Unsplash: https://unsplash.com/s/photos/education")
    print("   - Pexels: https://www.pexels.com/search/education/")
    print("   - Pixabay: https://pixabay.com/images/search/education/")
    print("\n2. Search for: 'education', 'learning', 'students', or 'classroom'")
    print("\n3. Download a high-resolution image (1920x1080 or larger)")
    print("\n4. Save it as: static/images/education-background.jpg")
    print("\n5. Make sure it's a JPG or PNG file")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        download_education_image()
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease download the image manually using the instructions above.")

