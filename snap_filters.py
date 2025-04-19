# File: snap_filters.py
import torch
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import random

class SnapBasicFilters:
    """
    Applies basic Snap-style color filters to an image,
    with options to randomize filter type and strength.
    """
    FILTER_TYPES = ["original", "grayscale", "vivid", "cooler", "warmer", "brighter", "darker"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "filter_type": (s.FILTER_TYPES, {"default": "original"}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "randomize_filter": ("BOOLEAN", {"default": False}),
                "randomize_strength": ("BOOLEAN", {"default": False}),
                "random_strength_min": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "random_strength_max": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "snap"

    def execute(self, image: torch.Tensor, filter_type: str, strength: float,
                     randomize_filter: bool, randomize_strength: bool, seed: int,
                     random_strength_min: float, random_strength_max: float):

        # Add validation for filter type
        if filter_type not in self.FILTER_TYPES:
            raise ValueError(f"Invalid filter type '{filter_type}'. Valid options are: {self.FILTER_TYPES}.")

        actual_filter_type = filter_type; actual_strength = strength
        if randomize_filter or randomize_strength: random.seed(seed)
        if randomize_filter:
            available_filters = [f for f in self.FILTER_TYPES if f != "original"]
            if available_filters: actual_filter_type = random.choice(available_filters)
            else: actual_filter_type = "original"
        if randomize_strength:
            min_s = min(random_strength_min, random_strength_max); max_s = max(random_strength_min, random_strength_max)
            actual_strength = random.uniform(min_s, max_s)
        actual_strength = max(0.0, min(1.0, actual_strength))

        if (actual_filter_type == "original" and actual_strength >= 1.0) or actual_strength <= 0.001: return (image,)

        batch_size, img_height, img_width, channels = image.shape; output_images = []
        for i in range(batch_size):
            img_pil_rgb = Image.fromarray((image[i].cpu().numpy() * 255).astype(np.uint8)).convert('RGB')
            original_img_pil = img_pil_rgb.copy(); filtered_img_pil = img_pil_rgb

            if actual_filter_type != "original":
                try:
                    if actual_filter_type == "grayscale":
                        filtered_img_pil = ImageOps.grayscale(img_pil_rgb).convert('RGB')
                    elif actual_filter_type == "vivid":
                        enhancer_c = ImageEnhance.Contrast(filtered_img_pil); filtered_img_pil = enhancer_c.enhance(1.3)
                        enhancer_s = ImageEnhance.Color(filtered_img_pil); filtered_img_pil = enhancer_s.enhance(1.3)
                    elif actual_filter_type == "cooler":
                        # Reverted to alpha blend method for a subtle tint
                        temp_rgba = filtered_img_pil.convert("RGBA")
                        # Slightly less intense blue tint (alpha 30 / 255 approx 12%)
                        blue_tint = Image.new("RGBA", filtered_img_pil.size, (120, 150, 255, 30))
                        filtered_img_pil = Image.alpha_composite(temp_rgba, blue_tint).convert("RGB")
                    elif actual_filter_type == "warmer":
                        # Reverted to alpha blend method for a subtle tint
                        temp_rgba = filtered_img_pil.convert("RGBA")
                        # Slightly less intense orange tint (alpha 30 / 255 approx 12%)
                        orange_tint = Image.new("RGBA", filtered_img_pil.size, (255, 180, 100, 30))
                        filtered_img_pil = Image.alpha_composite(temp_rgba, orange_tint).convert("RGB")
                    elif actual_filter_type == "brighter":
                        enhancer = ImageEnhance.Brightness(filtered_img_pil); filtered_img_pil = enhancer.enhance(1.25)
                    elif actual_filter_type == "darker":
                        enhancer_b = ImageEnhance.Brightness(filtered_img_pil); filtered_img_pil = enhancer_b.enhance(0.8)
                        enhancer_c = ImageEnhance.Contrast(filtered_img_pil); filtered_img_pil = enhancer_c.enhance(1.1)
                    else: filtered_img_pil = original_img_pil
                except Exception as e: print(f"Error applying filter '{actual_filter_type}': {e}"); filtered_img_pil = original_img_pil

            final_img_pil = Image.blend(original_img_pil, filtered_img_pil, actual_strength)
            output_img_np = np.array(final_img_pil).astype(np.float32) / 255.0
            output_images.append(torch.from_numpy(output_img_np))
        output_tensor = torch.stack(output_images)
        return (output_tensor,)

NODE_CLASS_MAPPINGS = { "SnapBasicFilters": SnapBasicFilters }
NODE_DISPLAY_NAME_MAPPINGS = { "SnapBasicFilters": "Snap Basic Filters" }