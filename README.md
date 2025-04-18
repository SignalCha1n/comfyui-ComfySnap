# Snap Style Nodes for ComfyUI

A collection of custom nodes for ComfyUI designed to replicate certain visual elements and effects reminiscent of Snapchat and early digital aesthetics.

## Installation

**Recommended: Using ComfyUI Manager**

1.  Install [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) if you haven't already.
2.  Open ComfyUI Manager from the menu in ComfyUI.
3.  Click "Install Custom Nodes".
4.  Search for "[Your Package Name Here, e.g., SnapNodes]" and click "Install".
5.  Restart ComfyUI.

**Manual Installation**

1.  Navigate to your ComfyUI `custom_nodes` directory.
2.  Clone this repository:
    ```bash
    git clone [Your GitHub Repo URL]
    ```
3.  Restart ComfyUI.

## Included Nodes

This package currently includes the following nodes, which will appear under the **"snap"** category when adding nodes:

---

### 1. Snapchat Text (`SnapchatTextBarOverlay`)

Adds a Snapchat-style semi-transparent text bar overlay to an image. Supports automatic text wrapping based on pixel width and various placement options.

**Inputs:**

* `image` (IMAGE): The input image.
* `text` (STRING): The text content to display in the bar.
* `vertical_placement` (COMBO): Selects the general vertical position of the text bar.
    * Options: "top", "middle", "bottom", "custom"
    * Default: "middle"
* `custom_vertical_percentage` (FLOAT): Sets the vertical position when `vertical_placement` is "custom". Uses a 0-100 scale where 0 = Bottom edge placement, 100 = Top edge placement for the bar's top edge. Default: 0.0.
* `text_color` (COLOR): The color of the text. Default: White (#FFFFFF).
* `font_name` (STRING): The filename of the font to use (e.g., `arialbd.ttf`, `segoeui.ttf`). It will attempt to load a bold variant first if available. Default: `arialbd.ttf`.
* `font_size_ratio` (FLOAT): Sets the font size relative to the image width. Default: 0.05 (5% of width).
* `vertical_padding_ratio_of_size` (FLOAT): Defines the total vertical padding (space above + below text) relative to the calculated font size. A value of 0.7 means padding is 70% of the font size. Adjusts bar height dynamically. Default: 0.7.
* `line_spacing` (INT): Pixel spacing between lines if the text wraps. Default: 4.
* `bar_color` (COLOR): The color of the semi-transparent background bar. Default: Black (#000000).
* `bar_alpha` (FLOAT): The opacity of the background bar (0.0 = fully transparent, 1.0 = fully opaque). Default: 0.5.

**Outputs:**

* `image` (IMAGE): The image with the text bar overlay applied.

---

### 2. Face Avoid (`FaceAvoidRandomY`)

Calculates the vertical center of a face mask and generates a random vertical position (0-100 scale, 100=Top) that avoids a defined zone around the face. Optionally avoids a second user-defined vertical zone. Useful for positioning overlays like text or stamps away from faces.

**Inputs:**

* `mask` (MASK): The input face mask (white pixels indicate the face). Processes only the first mask in a batch.
* `centroid_threshold` (FLOAT): Threshold (0.01-1.0) to determine which mask pixels are considered 'active' for centroid calculation. Default: 0.5.
* `vertical_adjustment` (FLOAT): Manually shift the detected vertical face center (-100 to 100) before calculating the avoidance zone. 100=Top, 0=Bottom. Default: 0.0.
* `avoid_threshold` (FLOAT): Defines the size (+/- this value) of the zone to avoid around the adjusted face center (0-50). Default: 15.0.
* `seed` (INT): Seed for the random number generator.
* `generate_random` (BOOLEAN): If True, generates a random position outside the avoidance zone(s). If False, outputs the adjusted face center position directly. Default: True.
* `avoid_zone2_y_bottom` (FLOAT, Optional): The bottom boundary (0-100, 0=Bottom) of an optional second vertical zone to avoid (e.g., where a text bar is placed). Default: -1.0 (disabled).
* `avoid_zone2_y_top` (FLOAT, Optional): The top boundary (0-100, 100=Top) of the optional second vertical zone to avoid. Default: -1.0 (disabled).

**Outputs:**

* `vertical_pos_100_top` (FLOAT): The calculated vertical position (0-100 scale, 100=Top). Either random (if enabled) or the adjusted face center.

---

### 3. Snapchat Basic Filters (`SnapchatBasicFilters`)

Applies simple color grading filters reminiscent of basic Snapchat swipe filters. Allows randomization of filter type and strength.

**Inputs:**

* `image` (IMAGE): The input image.
* `filter_type` (COMBO): Select the desired filter effect.
    * Options: "original", "grayscale", "sepia", "vivid", "cooler", "warmer", "brighter", "darker"
    * Default: "original"
* `strength` (FLOAT): Blends the filtered image with the original (0.0 = original, 1.0 = full filter effect). Default: 1.0.
* `randomize_filter` (BOOLEAN): If True, ignores `filter_type` and randomly selects an actual filter (excludes "original"). Default: False.
* `randomize_strength` (BOOLEAN): If True, ignores `strength` slider and uses a random value between the min/max settings below. Default: False.
* `random_strength_min` (FLOAT): Minimum value for randomized strength (0.0-1.0). Default: 0.5.
* `random_strength_max` (FLOAT): Maximum value for randomized strength (0.0-1.0). Default: 1.0.
* `seed` (INT): Seed for randomization.

**Outputs:**

* `image` (IMAGE): The image with the filter applied and blended.

---

### 4. Low Quality Digital Look (`LowQualityDigitalLook`)

Simulates the artifacts and noise typical of early digital cameras or low-light photos from platforms like Snapchat. Applies JPEG compression and Gaussian noise.

**Inputs:**

* `image` (IMAGE): The input image.
* `preset` (COMBO): Choose a predefined set of parameters.
    * Options: "Standard Snapchat Low Light", "Early 2000s Digital"
    * Default: "Standard Snapchat Low Light"
* `effect_level` (FLOAT): Controls the overall intensity of the effect.
    * 0.0 = No effect (original image).
    * 0.5 = The standard effect defined by the chosen `preset`.
    * 1.0 = A stronger version of the effect (more artifacts/noise).
    * Default: 0.5
* `seed` (INT): Seed for the random noise generation.

**Outputs:**

* `image` (IMAGE): The image with low-quality effects applied.

---

## Dependencies

These nodes rely on standard Python libraries (`os`, `datetime`, `random`, `io`) and libraries typically included with ComfyUI (`torch`, `numpy`, `PIL`/`Pillow`). No external installation should be required beyond having a standard ComfyUI setup.

## License

(You should add a LICENSE file to your repository and state the license here, e.g., MIT License)

---