"""KPI Statistics Cards for Admin Dashboard"""
import tkinter as tk
from tkinter import font
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from styles.admin_theme import (
        DARK_GRAY, BLACK, PRIMARY_PURPLE, PRIMARY_PURPLE_LIGHT, 
        GRADIENT_PURPLE_1, GRADIENT_PURPLE_2, GRADIENT_PURPLE_3,
        WHITE, LIGHT_GRAY, SPACING_24, SPACING_12, SPACING_32, SPACING_8,
        BODY_SMALL
    )
except ImportError:
    BLACK = "#000000"
    DARK_GRAY = "#1A1A1A"
    PRIMARY_PURPLE = "#4B0082"
    PRIMARY_PURPLE_LIGHT = "#6A0DAD"
    GRADIENT_PURPLE_1 = "#7A3BA3"
    GRADIENT_PURPLE_2 = "#A67AC7"
    GRADIENT_PURPLE_3 = "#D4B8E8"
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#BFBFBF"
    SPACING_24 = 24
    SPACING_12 = 12
    SPACING_32 = 32
    SPACING_8 = 8
    BODY_SMALL = 12


class KPICard(tk.Frame):
    def __init__(self, parent, label, value, description, icon="📊", gradient_colors=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.label = label
        self.value = value
        self.description = description
        self.icon = icon
        self.gradient_colors = gradient_colors or [PRIMARY_PURPLE, PRIMARY_PURPLE_LIGHT]
        
        self._create_card()
        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)
    
    def _create_card(self):
        """Create card structure"""
        # Card background with gradient effect (using first color as base)
        self.config(bg=self.gradient_colors[0], relief=tk.FLAT, bd=0, 
                   padx=SPACING_24, pady=SPACING_24)
        
        # Label
        try:
            label_font = font.Font(family="Segoe UI", size=BODY_SMALL)
            label_widget = tk.Label(self, text=self.label, font=label_font, 
                                   fg=GRADIENT_PURPLE_3, bg=self.gradient_colors[0])
            label_widget.pack(anchor="w", pady=(0, SPACING_8))
        except Exception as e:
            print(f"Error creating label: {e}")
        
        # Value
        try:
            value_font = font.Font(family="Segoe UI", size=32, weight="bold")
            value_widget = tk.Label(self, text=str(self.value), font=value_font, 
                                   fg=WHITE, bg=self.gradient_colors[0])
            value_widget.pack(anchor="w", pady=(0, SPACING_12))
        except Exception as e:
            print(f"Error creating value: {e}")
        
        # Divider
        try:
            divider = tk.Frame(self, bg=GRADIENT_PURPLE_2, height=1)
            divider.pack(fill=tk.X, pady=(0, SPACING_8))
        except Exception as e:
            print(f"Error creating divider: {e}")
        
        # Description with icon - ensure fonts are Font objects
        try:
            desc_frame = tk.Frame(self, bg=self.gradient_colors[0])
            desc_frame.pack(anchor="w", fill=tk.X)
            
            icon_font = font.Font(family="Segoe UI", size=14)
            icon_label = tk.Label(desc_frame, text=self.icon, font=icon_font, bg=self.gradient_colors[0])
            icon_label.pack(side=tk.LEFT, padx=(0, SPACING_8))
            
            desc_font = font.Font(family="Segoe UI", size=BODY_SMALL)
            desc_widget = tk.Label(desc_frame, text=self.description, font=desc_font, 
                                  fg=LIGHT_GRAY, bg=self.gradient_colors[0])
            desc_widget.pack(side=tk.LEFT)
        except Exception as e:
            print(f"Error creating description: {e}")
    
    def _on_hover_enter(self, event):
        """Handle hover enter"""
        self.config(relief=tk.RAISED, bd=2)
    
    def _on_hover_leave(self, event):
        """Handle hover leave"""
        self.config(relief=tk.FLAT, bd=0)


class KPICardsGrid(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BLACK, **kwargs)
        
        self.cards = []
        self._create_grid()
    
    def _create_grid(self):
        """Create 4-column grid layout"""
        # Container frame
        container = tk.Frame(self, bg=BLACK)
        container.pack(fill=tk.BOTH, padx=SPACING_32, pady=SPACING_32)
        
        # Configure grid columns (4 equal columns)
        for i in range(4):
            container.grid_columnconfigure(i, weight=1)
        
        # Sample data
        kpi_data = [
            {
                "label": "Total Books",
                "value": 2547,
                "description": "Total library items",
                "icon": "📚",
                "colors": [PRIMARY_PURPLE, PRIMARY_PURPLE_LIGHT]
            },
            {
                "label": "Available",
                "value": 1834,
                "description": "Ready to borrow",
                "icon": "✓",
                "colors": [GRADIENT_PURPLE_1, GRADIENT_PURPLE_2]
            },
            {
                "label": "Borrowed",
                "value": 713,
                "description": "Currently checked out",
                "icon": "📤",
                "colors": [GRADIENT_PURPLE_2, GRADIENT_PURPLE_3]
            },
            {
                "label": "Overdue",
                "value": 24,
                "description": "Past due date",
                "icon": "⚠️",
                "colors": ["#DC2626", "#EF4444"]
            },
        ]
        
        # Create cards
        for idx, data in enumerate(kpi_data):
            try:
                card = KPICard(
                    container,
                    label=data["label"],
                    value=data["value"],
                    description=data["description"],
                    icon=data["icon"],
                    gradient_colors=data["colors"]
                )
                card.grid(row=0, column=idx, padx=SPACING_12, pady=SPACING_12, sticky="nsew")
                self.cards.append(card)
            except Exception as e:
                print(f"Error creating KPI card {idx}: {e}")