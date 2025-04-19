# File: utils.py
# Common utility functions for ComfySnap nodes

def hex_to_rgb(hex_color):
    """
    Converts a hex color string (e.g., '#FFFFFF') to an RGB tuple (255, 255, 255).
    
    Args:
        hex_color (str): Hex color string, with or without '#' prefix.
        
    Returns:
        tuple: RGB color tuple with values from 0-255.
    """
    hex_color = hex_color.lstrip('#')
    l = len(hex_color)
    
    if l == 3:
        # Short form like #RGB
        return tuple(int(hex_color[i] * 2, 16) for i in range(3))
    elif l == 6:
        # Standard form like #RRGGBB
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Default fallback to white if the format is invalid
    return (255, 255, 255)