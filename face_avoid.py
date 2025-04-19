# File: face_avoid.py
import torch
import numpy as np
import random

class FaceAvoidRandomY:
    """
    Calculates the vertical centroid of a face mask, adjusts it,
    and optionally generates a random vertical position (0-100 scale, 100=Top)
    that avoids a zone around the adjusted centroid.
    Y Scale: 100=Top, 0=Bottom
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "centroid_threshold": ("FLOAT", {"default": 0.5, "min": 0.01, "max": 1.0, "step": 0.01}),
                "vertical_adjustment": ("FLOAT", {"default": 0.0, "min": -100.0, "max": 100.0, "step": 1.0, "round": 0.1}),
                "avoid_threshold": ("FLOAT", {"default": 15.0, "min": 0.0, "max": 50.0, "step": 0.1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "generate_random": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("vertical_pos_100_top",)
    FUNCTION = "execute"
    CATEGORY = "ComfySnap"

    def execute(self, mask: torch.Tensor, centroid_threshold: float,
                vertical_adjustment: float,
                avoid_threshold: float, seed: int, generate_random: bool):

        # Add validation for mask dimensions
        if mask.dim() != 3:
            raise ValueError("Input mask must be a 3D tensor with shape (batch_size, height, width).")

        if mask.dim() != 3: raise ValueError("FaceAvoidRandomY: Input mask must be (batch, height, width).")
        batch_size, height, width = mask.shape; scaled_center_y = 50.0

        if height <= 1: pass
        else:
            single_mask = mask[0]; binary_mask = (single_mask > centroid_threshold).float(); mask_sum = torch.sum(binary_mask)
            if mask_sum > 0:
                yy = torch.arange(height, device=mask.device, dtype=mask.dtype).unsqueeze(1).repeat(1, width)
                sum_y_weighted = torch.sum(yy * binary_mask); centroid_y_pixels = sum_y_weighted / mask_sum
                normalized_y = torch.clamp(centroid_y_pixels / (height - 1), 0.0, 1.0); scaled_center_y = (100.0 * (1.0 - normalized_y)).item()

        adjusted_center_y = max(0.0, min(100.0, scaled_center_y + vertical_adjustment))

        if not generate_random: return (adjusted_center_y,)

        random.seed(seed); min_overall = 0.0; max_overall = 100.0

        exclude_bottom = max(min_overall, adjusted_center_y - avoid_threshold)
        exclude_top = min(max_overall, adjusted_center_y + avoid_threshold)

        size1 = max(0.0, exclude_bottom - min_overall)
        size2 = max(0.0, max_overall - exclude_top)
        total_allowed_size = size1 + size2

        random_y_pos = adjusted_center_y

        if total_allowed_size > 0:
            yr = random.uniform(0, total_allowed_size)
            if yr < size1:
                random_y_pos = min_overall + yr
            else:
                range2_min = exclude_top
                random_y_pos = range2_min + (yr - size1)
        else: print("Warning: Face avoidance zone covers entire range. Returning adjusted center.")

        random_y_pos = max(min_overall, min(max_overall, random_y_pos))

        return (random_y_pos,)

NODE_CLASS_MAPPINGS = {
    "FaceAvoidRandomY": FaceAvoidRandomY
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "FaceAvoidRandomY": "Face Avoid"
}