# File: snapchat_effects.py
import torch
import numpy as np
from PIL import Image, ImageEnhance
import io
import random

class LowQualityDigitalLook:
    """
    Applies simulated low-quality digital camera/Snapchat effects.
    Uses an effect_level slider (0=off, 0.5=preset default, 1=max effect).
    Includes Gaussian noise and JPEG compression.
    """
    PRESET_MODES = ["Standard Snapchat Low Light", "Early 2000s Digital"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "preset": (s.PRESET_MODES, {"default": "Standard Snapchat Low Light"}),
                "effect_level": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "seed": ("INT", { "default": 0, "min": 0, "max": 4294967295 }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "snap"

    def execute(self, image: torch.Tensor, preset: str, effect_level: float = 0.5, seed: int = 0):
        effect_level = max(0.0, min(1.0, effect_level))
        if effect_level <= 0.001: return (image,)
        seed = max(0, min(4294967295, seed)); np.random.seed(seed)
        batch_size, img_height, img_width, channels = image.shape; output_images = []

        if preset == "Standard Snapchat Low Light": base_jpeg_quality = 70; base_noise_std_dev = 8.0; base_saturation = 0.9; base_brightness = 0.95; jpeg_subsampling = 0 # Default (often 4:4:4 or 4:2:2)
        elif preset == "Early 2000s Digital": base_jpeg_quality = 50; base_noise_std_dev = 15.0; base_saturation = 0.8; base_brightness = 1.0; jpeg_subsampling = 2 # Use 4:2:0 for more color artifacts
        else: base_jpeg_quality = 75; base_noise_std_dev = 5.0; base_saturation = 1.0; base_brightness = 1.0; jpeg_subsampling = 0

        no_effect_jpeg_q = 95; no_effect_noise = 0.0; no_effect_saturation = 1.0; no_effect_brightness = 1.0
        max_effect_jpeg_q = 15; max_effect_noise = base_noise_std_dev * 2.5
        max_effect_saturation = 1.0 + (base_saturation - 1.0) * 1.5; max_effect_brightness = 1.0 + (base_brightness - 1.0) * 1.5

        def interpolate(level, val0, val05, val1):
            if level <= 0.5: factor = level / 0.5; return val0 + factor * (val05 - val0)
            else: factor = (level - 0.5) / 0.5; return val05 + factor * (val1 - val05)

        actual_jpeg_quality = interpolate(effect_level, no_effect_jpeg_q, base_jpeg_quality, max_effect_jpeg_q)
        actual_noise_std_dev = interpolate(effect_level, no_effect_noise, base_noise_std_dev, max_effect_noise)
        actual_saturation = interpolate(effect_level, no_effect_saturation, base_saturation, max_effect_saturation)
        actual_brightness = interpolate(effect_level, no_effect_brightness, base_brightness, max_effect_brightness)

        actual_jpeg_quality = int(max(1, min(100, actual_jpeg_quality)))
        actual_noise_std_dev = max(0.0, actual_noise_std_dev)
        actual_saturation = max(0.01, actual_saturation); actual_brightness = max(0.01, actual_brightness)

        for i in range(batch_size):
            img_pil_rgb = Image.fromarray((image[i].cpu().numpy() * 255).astype(np.uint8)).convert('RGB')
            processed_pil = img_pil_rgb

            # Apply Color/Brightness First
            if abs(actual_saturation - 1.0) > 0.01: enhancer = ImageEnhance.Color(processed_pil); processed_pil = enhancer.enhance(actual_saturation)
            if abs(actual_brightness - 1.0) > 0.01: enhancer = ImageEnhance.Brightness(processed_pil); processed_pil = enhancer.enhance(actual_brightness)

            # Apply Digital Noise (Applied BEFORE JPEG now)
            if actual_noise_std_dev > 0.01:
                try:
                    img_np = np.array(processed_pil).astype(np.float32) / 255.0
                    noise = np.random.normal(loc=0.0, scale=actual_noise_std_dev / 255.0, size=img_np.shape).astype(np.float32)
                    noisy_img_np = np.clip(img_np + noise, 0.0, 1.0)
                    processed_pil = Image.fromarray((noisy_img_np * 255).astype(np.uint8)) # Noisy image before JPEG
                except Exception as e: print(f"Warning: Failed to add noise: {e}")

            # Apply JPEG Compression Artifacts (Applied AFTER noise now)
            if actual_jpeg_quality < 98:
                 try:
                      buffer = io.BytesIO()
                      # Add subsampling parameter
                      processed_pil.save(buffer, format="JPEG", quality=actual_jpeg_quality, subsampling=jpeg_subsampling)
                      buffer.seek(0); processed_pil = Image.open(buffer).convert('RGB')
                 except Exception as e: print(f"Warning: JPEG compression step failed: {e}")


            final_pil = processed_pil
            output_img_np = np.array(final_pil).astype(np.float32) / 255.0
            output_images.append(torch.from_numpy(output_img_np))
        output_tensor = torch.stack(output_images)
        return (output_tensor,)

NODE_CLASS_MAPPINGS = { "LowQualityDigitalLook": LowQualityDigitalLook }
NODE_DISPLAY_NAME_MAPPINGS = { "LowQualityDigitalLook": "Low Quality Digital Look" }