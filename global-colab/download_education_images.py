"""
Script to download education-related images for the website.
"""

import os
import requests
from pathlib import Path

def download_education_images():
    """Download education-themed images"""
    
    # Create images directory if it doesn't exist
    images_dir = Path("static/images")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # List of education images to download
    images = {
        "students-learning.jpg": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&q=80&auto=format&fit=crop",
        "online-education.jpg": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&q=80&auto=format&fit=crop",
        "collaboration.jpg": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&q=80&auto=format&fit=crop",
        "study-group.jpg": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&q=80&auto=format&fit=crop",
        "education-technology.jpg": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800&q=80&auto=format&fit=crop",
    }
    
    print("Downloading education-related images...")
    
    for filename, url in images.items():
        image_path = images_dir / filename
        
        # Skip if already exists
        if image_path.exists():
            print(f"  ✓ {filename} already exists")
            continue
        
        try:
            print(f"  Downloading {filename}...")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = image_path.stat().st_size / 1024  # Size in KB
            print(f"    ✓ Downloaded ({file_size:.1f} KB)")
            
        except Exception as e:
            print(f"    ✗ Failed: {str(e)}")
    
    print("\n✓ Image download complete!")

if __name__ == "__main__":
    try:
        download_education_images()
    except Exception as e:
        print(f"Error: {str(e)}")

