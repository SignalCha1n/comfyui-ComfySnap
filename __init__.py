# File: __init__.py (in your node package directory, e.g., MySnapNodes)
import importlib
import traceback
import os
import logging

# Add a base node class for standardizing input/output handling
class BaseNode:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_info(self, message):
        self.logger.info(message)

# --- Define the filenames for remaining node files ---
NODE_FILES = [
    "snap_text",
    "face_avoid",
    "snap_filters",
    "snap_effects"
]

NODE_CLASS_MAPPINGS = {
    "SnapTextOverlay": SnapTextOverlay,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SnapTextOverlay": "Snap Text",
}
current_dir = os.path.dirname(__file__); package_name = os.path.basename(current_dir)

def load_mappings_from_module(module_name, package_name):
    classes = {}; names = {};
    try:
        module_path = os.path.join(current_dir, f"{module_name}.py")
        if not os.path.exists(module_path): print(f"--- Info: Skipping import, file not found: {module_name}.py"); return classes, names
        module = importlib.import_module(f".{module_name}", package=__package__)
        classes = getattr(module, "NODE_CLASS_MAPPINGS", {}); names = getattr(module, "NODE_DISPLAY_NAME_MAPPINGS", {})
        if classes: print(f"+++ Imported '{module_name}' ({len(classes)} nodes) +++")
    except ImportError as e: print(f"### Warning: Could not import nodes from {module_name}.py - {e}")
    except AttributeError: print(f"### Warning: Mappings not found or improperly defined in {module_name}.py")
    except Exception as e: print(f"### Error loading module {module_name}:"); traceback.print_exc()
    return classes, names

print(f"### Loading nodes from package: {package_name} ###")
for module_name in NODE_FILES:
    module_classes, module_names = load_mappings_from_module(module_name, __package__)
    NODE_CLASS_MAPPINGS.update(module_classes); NODE_DISPLAY_NAME_MAPPINGS.update(module_names)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
print(f"### Finished loading {package_name} ({len(NODE_CLASS_MAPPINGS)} nodes total) ###")