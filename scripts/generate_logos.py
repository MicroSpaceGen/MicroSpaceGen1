#!/usr/bin/env python3
"""
Script to generate different sizes of PNG logos from SVG
"""

import os
import subprocess
from pathlib import Path

def generate_png_logos():
    """Generate different sizes of PNG logos from SVG"""
    # Create output directory if it doesn't exist
    output_dir = Path("docs/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # SVG source file
    svg_file = output_dir / "logo.svg"
    
    # Sizes to generate
    sizes = {
        "small": 100,
        "medium": 200,
        "large": 400
    }
    
    # Generate PNG files
    for name, size in sizes.items():
        output_file = output_dir / f"logo-{name}.png"
        try:
            subprocess.run([
                "rsvg-convert",
                "-w", str(size),
                "-h", str(size),
                str(svg_file),
                "-o", str(output_file)
            ], check=True)
            print(f"Generated {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating {output_file}: {e}")
        except FileNotFoundError:
            print("Error: rsvg-convert not found. Please install librsvg first.")
            print("On macOS: brew install librsvg")
            print("On Ubuntu: sudo apt-get install librsvg2-bin")
            break

if __name__ == "__main__":
    generate_png_logos() 