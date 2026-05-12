#!/usr/bin/env python3
"""
Generate optimized <picture> element HTML with AVIF → WebP → JPEG fallbacks.
"""

from pathlib import Path

def generate_picture_html(base_name: str, alt_text: str, sizes: str = "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw", loading: str = "lazy", class_name: str = "") -> str:
    """
    Generate a <picture> element with AVIF, WebP, and JPEG fallbacks.
    
    Args:
        base_name: Base filename without extension (e.g., "spain-france-tra03804")
        alt_text: Alt text for the image
        sizes: Sizes attribute for responsive images
        loading: Loading attribute (lazy/eager)
        class_name: CSS class name for the img tag
    
    Returns:
        HTML string with <picture> element
    """
    breakpoints = [320, 640, 768, 1024, 1280]
    
    # Generate AVIF srcset
    avif_srcset = []
    for bp in breakpoints:
        avif_srcset.append(f"/assets/img/{base_name}-{bp}w.avif {bp}w")
    avif_srcset_str = ",\n        ".join(avif_srcset)
    
    # Generate WebP srcset
    webp_srcset = []
    for bp in breakpoints:
        webp_srcset.append(f"/assets/img/{base_name}-{bp}w.webp {bp}w")
    webp_srcset_str = ",\n        ".join(webp_srcset)
    
    class_attr = f' class="{class_name}"' if class_name else ""
    loading_attr = f' loading="{loading}"' if loading else ""
    
    html = f'''<picture>
      <source
        type="image/avif"
        srcset="{avif_srcset_str}"
        sizes="{sizes}">
      <source
        type="image/webp"
        srcset="{webp_srcset_str}"
        sizes="{sizes}">
      <img
        src="/assets/img/{base_name}.jpeg"
        alt="{alt_text}"{class_attr}{loading_attr}>
    </picture>'''
    
    return html

if __name__ == "__main__":
    # Example usage
    print(generate_picture_html("spain-france-tra03804", "Spain & France Motorcycle Tour"))
