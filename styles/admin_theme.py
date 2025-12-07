"""Admin Dashboard Theme Configuration"""

# PRIMARY COLORS
PRIMARY_PURPLE = "#4B0082"
PRIMARY_PURPLE_DARK = "#3A0066"
PRIMARY_PURPLE_LIGHT = "#6A0DAD"

# PURPLE GRADIENTS
GRADIENT_PURPLE_1 = "#7A3BA3"
GRADIENT_PURPLE_2 = "#A67AC7"
GRADIENT_PURPLE_3 = "#D4B8E8"

# NEUTRALS
BLACK = "#000000"
DARK_GRAY = "#1A1A1A"
MEDIUM_GRAY = "#333333"
LIGHT_GRAY = "#BFBFBF"
WHITE = "#FFFFFF"

# SEMANTIC COLORS
SUCCESS = "#10B981"
WARNING = "#F59E0B"
ERROR = "#EF4444"
INFO = "#3B82F6"

# TRANSPARENCY LAYERS
BLACK_OVERLAY_30 = "rgba(0, 0, 0, 0.3)"
PURPLE_OVERLAY_20 = "rgba(75, 0, 130, 0.2)"
PURPLE_OVERLAY_50 = "rgba(75, 0, 130, 0.5)"

# TYPOGRAPHY SIZES
H1_SIZE = 32
H2_SIZE = 24
H3_SIZE = 20
H4_SIZE = 18
BODY_LARGE = 16
BODY_REGULAR = 14
BODY_SMALL = 12
DISPLAY = 48
CODE = 14

# FONT WEIGHTS
WEIGHT_LIGHT = 300
WEIGHT_REGULAR = 400
WEIGHT_MEDIUM = 500
WEIGHT_SEMIBOLD = 600
WEIGHT_BOLD = 700

# SPACING
SPACING_4 = 4
SPACING_8 = 8
SPACING_12 = 12
SPACING_16 = 16
SPACING_20 = 20
SPACING_24 = 24
SPACING_32 = 32
SPACING_48 = 48

# BORDER RADIUS
RADIUS_SMALL = 6
RADIUS_MEDIUM = 8
RADIUS_LARGE = 12

# SHADOW
SHADOW_SMALL = "0 2px 4px rgba(75, 0, 130, 0.1)"
SHADOW_MEDIUM = "0 4px 12px rgba(75, 0, 130, 0.3)"
SHADOW_LARGE = "0 8px 24px rgba(75, 0, 130, 0.4)"

# DIMENSIONS
HEADER_HEIGHT = 72
MAX_WIDTH = 1280
TAB_HEIGHT = 48
CARD_MIN_HEIGHT = 140

ADMIN_THEME = {
    "colors": {
        "primary": PRIMARY_PURPLE,
        "primary_dark": PRIMARY_PURPLE_DARK,
        "primary_light": PRIMARY_PURPLE_LIGHT,
        "background": BLACK,
        "surface": DARK_GRAY,
        "border": MEDIUM_GRAY,
        "text_primary": WHITE,
        "text_secondary": LIGHT_GRAY,
        "success": SUCCESS,
        "warning": WARNING,
        "error": ERROR,
        "info": INFO,
    },
    "typography": {
        "sizes": {
            "h1": H1_SIZE,
            "h2": H2_SIZE,
            "h3": H3_SIZE,
            "h4": H4_SIZE,
            "body_large": BODY_LARGE,
            "body_regular": BODY_REGULAR,
            "body_small": BODY_SMALL,
        },
        "weights": {
            "light": WEIGHT_LIGHT,
            "regular": WEIGHT_REGULAR,
            "medium": WEIGHT_MEDIUM,
            "semibold": WEIGHT_SEMIBOLD,
            "bold": WEIGHT_BOLD,
        },
    },
    "spacing": {
        "xs": SPACING_4,
        "sm": SPACING_8,
        "md": SPACING_12,
        "lg": SPACING_16,
        "xl": SPACING_24,
        "2xl": SPACING_32,
    },
}