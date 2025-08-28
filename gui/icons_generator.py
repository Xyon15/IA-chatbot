#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'icônes SVG pour NeuroBot GUI
Crée des icônes vectorielles avec la palette de couleurs
"""

import os
from typing import Dict

COLOR_PALETTE = {
    'primary_dark': '#034C36',
    'secondary_dark': '#003332', 
    'accent_orange': '#FF8128',
    'accent_light': '#F2E0DF',
    'neutral_light': '#BDCDCF'
}

ICONS = {
    'cpu': '''<svg viewBox="0 0 24 24" fill="none">
        <rect x="3" y="3" width="18" height="18" rx="2" stroke="{primary}" stroke-width="2" fill="{bg}"/>
        <rect x="7" y="7" width="10" height="10" rx="1" stroke="{accent}" stroke-width="1.5" fill="{accent}"/>
        <path d="M9 1v2m6-2v2M9 21v2m6-2v2M1 9h2m18 0h2M1 15h2m18 0h2" stroke="{primary}" stroke-width="1.5"/>
    </svg>''',
    
    'memory': '''<svg viewBox="0 0 24 24" fill="none">
        <rect x="3" y="4" width="18" height="16" rx="2" stroke="{primary}" stroke-width="2" fill="{bg}"/>
        <rect x="6" y="7" width="12" height="2" rx="1" fill="{accent}"/>
        <rect x="6" y="10" width="8" height="2" rx="1" fill="{primary}"/>
        <rect x="6" y="13" width="10" height="2" rx="1" fill="{accent}"/>
        <rect x="6" y="16" width="6" height="2" rx="1" fill="{primary}"/>
    </svg>''',
    
    'gpu': '''<svg viewBox="0 0 24 24" fill="none">
        <rect x="2" y="6" width="20" height="12" rx="3" stroke="{primary}" stroke-width="2" fill="{bg}"/>
        <rect x="5" y="9" width="4" height="6" rx="1" fill="{accent}"/>
        <rect x="10" y="9" width="4" height="6" rx="1" fill="{primary}"/>
        <rect x="15" y="9" width="4" height="6" rx="1" fill="{accent}"/>
        <circle cx="6" cy="4" r="1" fill="{primary}"/>
        <circle cx="10" cy="4" r="1" fill="{accent}"/>
        <circle cx="14" cy="4" r="1" fill="{primary}"/>
        <circle cx="18" cy="4" r="1" fill="{accent}"/>
    </svg>''',
    
    'bot': '''<svg viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="9" stroke="{primary}" stroke-width="2" fill="{bg}"/>
        <circle cx="9" cy="10" r="1.5" fill="{accent}"/>
        <circle cx="15" cy="10" r="1.5" fill="{accent}"/>
        <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke="{primary}" stroke-width="1.5" stroke-linecap="round"/>
        <rect x="10" y="3" width="4" height="3" rx="2" fill="{accent}"/>
        <rect x="4" y="8" width="3" height="2" rx="1" fill="{primary}"/>
        <rect x="17" y="8" width="3" height="2" rx="1" fill="{primary}"/>
    </svg>''',
    
    'database': '''<svg viewBox="0 0 24 24" fill="none">
        <ellipse cx="12" cy="6" rx="8" ry="3" stroke="{primary}" stroke-width="2" fill="{bg}"/>
        <path d="M4 6v12c0 1.657 3.582 3 8 3s8-1.343 8-3V6" stroke="{primary}" stroke-width="2" fill="{bg}"/>
        <ellipse cx="12" cy="12" rx="8" ry="3" stroke="{accent}" stroke-width="1.5"/>
        <ellipse cx="12" cy="18" rx="8" ry="3" stroke="{accent}" stroke-width="1.5"/>
    </svg>''',
    
    'logs': '''<svg viewBox="0 0 24 24" fill="none">
        <rect x="3" y="3" width="18" height="18" rx="2" stroke="{primary}" stroke-width="2" fill="{bg}"/>
        <path d="M7 7h10M7 10h8M7 13h6M7 16h4" stroke="{accent}" stroke-width="1.5" stroke-linecap="round"/>
        <circle cx="17" cy="16" r="2" stroke="{primary}" stroke-width="1.5" fill="{accent}"/>
    </svg>''',
    
    'settings': '''<svg viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="3" stroke="{accent}" stroke-width="2" fill="{bg}"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="{primary}" stroke-width="1.5"/>
    </svg>''',
    
    'notification': '''<svg viewBox="0 0 24 24" fill="none">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" stroke="{primary}" stroke-width="2" fill="{bg}"/>
        <path d="M13.73 21a2 2 0 0 1-3.46 0" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>
        <circle cx="18" cy="6" r="3" fill="{accent}" stroke="white" stroke-width="2"/>
    </svg>'''
}

def generate_icon(name: str, svg_template: str, size: int = 24) -> str:
    """Génère une icône SVG avec les couleurs de la palette"""
    svg = svg_template.format(
        primary=COLOR_PALETTE['primary_dark'],
        accent=COLOR_PALETTE['accent_orange'], 
        bg=COLOR_PALETTE['accent_light'],
        neutral=COLOR_PALETTE['neutral_light']
    )
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
{svg}
</svg>'''

def create_icons_directory():
    """Crée le dossier d'icônes et génère toutes les icônes"""
    icons_dir = "assets/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    for name, template in ICONS.items():
        # Icône normale (24px)
        svg_content = generate_icon(name, template, 24)
        with open(f"{icons_dir}/{name}.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        # Icône grande (48px) pour les boutons importants
        svg_content_large = generate_icon(name, template, 48)
        with open(f"{icons_dir}/{name}_large.svg", "w", encoding="utf-8") as f:
            f.write(svg_content_large)
    
    print(f"✅ {len(ICONS)} icônes générées dans {icons_dir}/")

if __name__ == "__main__":
    create_icons_directory()