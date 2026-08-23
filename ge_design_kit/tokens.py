"""
ge_design_kit.tokens
---------------------
Injecte les tokens CSS GE-DESIGN (ge.ch), répliqués fidèlement
depuis les fichiers primitives.css + light.css.

Structure à 3 couches, identique à la source :
  1. PRIMITIVES   — palette brute --md-ref-palette-* (jamais utilisée
                     directement dans les composants)
  2. SHAPE/TYPESCALE — formes et typographie --md-sys-shape-* / --md-sys-typescale-*
  3. SEMANTIC LIGHT  — mapping sémantique --md-sys-color-* 
"""

import streamlit as st

_PRIMITIVES = """
:root {
    --md-ref-palette-primary-0: rgba(0, 0, 0, 1);
    --md-ref-palette-primary-10: rgba(0, 28, 51, 1);
    --md-ref-palette-primary-20: rgba(0, 51, 85, 1);
    --md-ref-palette-primary-30: rgba(0, 74, 120, 1);
    --md-ref-palette-primary-40: rgba(1, 98, 157, 1);
    --md-ref-palette-primary-50: rgba(50, 124, 184, 1);
    --md-ref-palette-primary-60: rgba(80, 150, 212, 1);
    --md-ref-palette-primary-70: rgba(109, 176, 240, 1);
    --md-ref-palette-primary-80: rgba(153, 203, 255, 1);
    --md-ref-palette-primary-90: rgba(207, 229, 255, 1);
    --md-ref-palette-primary-95: rgba(232, 243, 255, 1);
    --md-ref-palette-primary-98: rgba(247, 249, 255, 1);
    --md-ref-palette-primary-100: rgba(255, 255, 255, 1);

    --md-ref-palette-secondary-0: rgba(0, 0, 0, 1);
    --md-ref-palette-secondary-10: rgba(16, 20, 24, 1);
    --md-ref-palette-secondary-20: rgba(27, 34, 41, 1);
    --md-ref-palette-secondary-30: rgba(54, 78, 103, 1);
    --md-ref-palette-secondary-40: rgba(78, 102, 128, 1);
    --md-ref-palette-secondary-50: rgba(102, 128, 154, 1);
    --md-ref-palette-secondary-60: rgba(128, 154, 181, 1);
    --md-ref-palette-secondary-70: rgba(154, 181, 209, 1);
    --md-ref-palette-secondary-80: rgba(181, 208, 237, 1);
    --md-ref-palette-secondary-90: rgba(206, 223, 242, 1);
    --md-ref-palette-secondary-95: rgba(235, 239, 255, 1);
    --md-ref-palette-secondary-98: rgba(251, 252, 255, 1);
    --md-ref-palette-secondary-100: rgba(255, 255, 255, 1);

    --md-ref-palette-tertiary-0: rgba(0, 0, 0, 1);
    --md-ref-palette-tertiary-10: rgba(32, 28, 0, 1);
    --md-ref-palette-tertiary-20: rgba(56, 49, 0, 1);
    --md-ref-palette-tertiary-30: rgba(81, 71, 0, 1);
    --md-ref-palette-tertiary-40: rgba(107, 95, 0, 1);
    --md-ref-palette-tertiary-50: rgba(133, 120, 27, 1);
    --md-ref-palette-tertiary-60: rgba(160, 145, 52, 1);
    --md-ref-palette-tertiary-70: rgba(188, 172, 76, 1);
    --md-ref-palette-tertiary-80: rgba(216, 200, 100, 1);
    --md-ref-palette-tertiary-90: rgba(245, 228, 126, 1);
    --md-ref-palette-tertiary-95: rgba(255, 242, 174, 1);
    --md-ref-palette-tertiary-98: rgba(255, 249, 235, 1);
    --md-ref-palette-tertiary-100: rgba(255, 255, 255, 1);

    --md-ref-palette-neutral-0: rgba(24, 31, 37, 1);
    --md-ref-palette-neutral-10: rgba(29, 36, 43, 1);
    --md-ref-palette-neutral-20: rgba(35, 46, 57, 1);
    --md-ref-palette-neutral-30: rgba(58, 72, 87, 1);
    --md-ref-palette-neutral-40: rgba(82, 96, 112, 1);
    --md-ref-palette-neutral-50: rgba(106, 120, 137, 1);
    --md-ref-palette-neutral-60: rgba(132, 146, 163, 1);
    --md-ref-palette-neutral-70: rgba(153, 169, 189, 1);
    --md-ref-palette-neutral-80: rgba(213, 228, 240, 1);
    --md-ref-palette-neutral-90: rgba(230, 241, 250, 1);
    --md-ref-palette-neutral-95: rgba(230, 240, 247, 1);
    --md-ref-palette-neutral-98: rgba(247, 250, 252, 1);
    --md-ref-palette-neutral-100: rgba(255, 255, 255, 1);

    --md-ref-palette-neutral-variant-0: rgba(0, 0, 0, 1);
    --md-ref-palette-neutral-variant-10: rgba(27, 28, 27, 1);
    --md-ref-palette-neutral-variant-20: rgba(48, 48, 47, 1);
    --md-ref-palette-neutral-variant-30: rgba(71, 71, 70, 1);
    --md-ref-palette-neutral-variant-40: rgba(95, 94, 93, 1);
    --md-ref-palette-neutral-variant-50: rgba(119, 119, 117, 1);
    --md-ref-palette-neutral-variant-60: rgba(145, 144, 143, 1);
    --md-ref-palette-neutral-variant-70: rgba(172, 171, 169, 1);
    --md-ref-palette-neutral-variant-80: rgba(212, 210, 207, 1);
    --md-ref-palette-neutral-variant-90: rgba(228, 226, 224, 1);
    --md-ref-palette-neutral-variant-95: rgba(242, 240, 238, 1);
    --md-ref-palette-neutral-variant-98: rgba(251, 249, 247, 1);
    --md-ref-palette-neutral-variant-100: rgba(255, 255, 255, 1);

    --md-ref-palette-error-0: rgba(0, 0, 0, 1);
    --md-ref-palette-error-10: rgba(65, 0, 2, 1);
    --md-ref-palette-error-20: rgba(105, 0, 5, 1);
    --md-ref-palette-error-30: rgba(147, 0, 10, 1);
    --md-ref-palette-error-40: rgba(186, 27, 27, 1);
    --md-ref-palette-error-50: rgba(222, 55, 48, 1);
    --md-ref-palette-error-60: rgba(255, 84, 73, 1);
    --md-ref-palette-error-70: rgba(255, 137, 125, 1);
    --md-ref-palette-error-80: rgba(255, 180, 171, 1);
    --md-ref-palette-error-90: rgba(255, 218, 214, 1);
    --md-ref-palette-error-95: rgba(255, 237, 234, 1);
    --md-ref-palette-error-98: rgba(255, 248, 247, 1);
    --md-ref-palette-error-100: rgba(255, 255, 255, 1);

    --md-ref-palette-warning-0: rgba(0, 0, 0, 1);
    --md-ref-palette-warning-10: rgba(38, 25, 1, 1);
    --md-ref-palette-warning-20: rgba(61, 46, 6, 1);
    --md-ref-palette-warning-30: rgba(74, 55, 7, 1);
    --md-ref-palette-warning-40: rgba(120, 90, 11, 1);
    --md-ref-palette-warning-50: rgba(171, 128, 16, 1);
    --md-ref-palette-warning-60: rgba(196, 147, 18, 1);
    --md-ref-palette-warning-70: rgba(201, 164, 89, 1);
    --md-ref-palette-warning-80: rgba(229, 193, 119, 1);
    --md-ref-palette-warning-90: rgba(255, 223, 153, 1);
    --md-ref-palette-warning-95: rgba(255, 247, 229, 1);
    --md-ref-palette-warning-98: rgba(255, 253, 250, 1);
    --md-ref-palette-warning-100: rgba(255, 255, 255, 1);

    --md-ref-palette-success-0: rgba(0, 0, 0, 1);
    --md-ref-palette-success-10: rgba(0, 32, 24, 1);
    --md-ref-palette-success-20: rgba(14, 82, 66, 1);
    --md-ref-palette-success-30: rgba(16, 94, 76, 1);
    --md-ref-palette-success-40: rgba(18, 107, 86, 1);
    --md-ref-palette-success-50: rgba(22, 133, 107, 1);
    --md-ref-palette-success-60: rgba(27, 158, 127, 1);
    --md-ref-palette-success-70: rgba(128, 191, 170, 1);
    --md-ref-palette-success-80: rgba(145, 217, 193, 1);
    --md-ref-palette-success-90: rgba(162, 242, 215, 1);
    --md-ref-palette-success-95: rgba(201, 255, 237, 1);
    --md-ref-palette-success-98: rgba(251, 254, 253, 1);
    --md-ref-palette-success-100: rgba(255, 255, 255, 1);

    --md-ref-shadow-dark-opacity-0: rgba(232, 243, 255, 0.00);
    --md-ref-shadow-dark-opacity-8: rgba(232, 243, 255, 0.08);
    --md-ref-shadow-dark-opacity-12: rgba(232, 243, 255, 0.12);
    --md-ref-shadow-dark-opacity-15: rgba(232, 243, 255, 0.15);
    --md-ref-shadow-dark-opacity-16: rgba(232, 243, 255, 0.16);
    --md-ref-shadow-dark-opacity-30: rgba(232, 243, 255, 0.30);
    --md-ref-shadow-dark-opacity-80: rgba(232, 243, 255, 0.80);
    --md-ref-shadow-light-opacity-0: rgba(0, 51, 85, 0.00);
    --md-ref-shadow-light-opacity-8: rgba(0, 51, 85, 0.08);
    --md-ref-shadow-light-opacity-12: rgba(0, 51, 85, 0.12);
    --md-ref-shadow-light-opacity-15: rgba(0, 51, 85, 0.15);
    --md-ref-shadow-light-opacity-16: rgba(0, 51, 85, 0.16);
    --md-ref-shadow-light-opacity-30: rgba(0, 51, 85, 0.30);
    --md-ref-shadow-universal-opacity-0: rgba(24, 31, 37, 0.00);
    --md-ref-shadow-universal-opacity-8: rgba(24, 31, 37, 0.08);
    --md-ref-shadow-universal-opacity-15: rgba(24, 31, 37, 0.15);
    --md-ref-shadow-universal-opacity-40: rgba(24, 31, 37, 0.40);
    --md-ref-shadow-universal-opacity-80: rgba(24, 31, 37, 0.80);

    --md-ref-spacings-0: 0px;
    --md-ref-spacings-0-5: 2px;
    --md-ref-spacings-1: 4px;
    --md-ref-spacings-1-2: 4px;
    --md-ref-spacings-1-5: 6px;
    --md-ref-spacings-2: 8px;
    --md-ref-spacings-3: 12px;
    --md-ref-spacings-4: 16px;
    --md-ref-spacings-5: 20px;
    --md-ref-spacings-6: 24px;
    --md-ref-spacings-8: 32px;
    --md-ref-spacings-10: 40px;
    --md-ref-spacings-12: 48px;
    --md-ref-spacings-16: 64px;
    --md-ref-spacings-20: 80px;
    --md-ref-spacings-24: 96px;
    --md-ref-spacings-32: 128px;
    --md-ref-spacings-40: 160px;
    --md-ref-spacings-48: 192px;
    --md-ref-spacings-56: 224px;
    --md-ref-spacings-64: 256px;
    --md-ref-spacings-80: 320px;
    --md-ref-spacings-100: 400px;
    --md-ref-spacings-120: 480px;
    --md-ref-spacings-140: 560px;
    --md-ref-spacings-160: 640px;
    --md-ref-spacings-180: 720px;
    --md-ref-spacings-192: 768px;
    --md-ref-spacings-256: 1024px;
    --md-ref-spacings-320: 1280px;
    --md-ref-spacings-360: 1440px;
    --md-ref-spacings-400: 1600px;
    --md-ref-spacings-480: 1920px;

    --md-menu-item-one-line-container-height: 28px;

    --md-ref-typeface-brand: Roboto, Arial, sans-serif;
    --md-ref-typeface-weight-regular: 400;
    --md-ref-typeface-weight-medium: 500;
    --md-ref-typeface-weight-large: 700;
}
"""

_SHAPE_TYPESCALE = """
:root {
    /* Shape */
    --md-sys-shape-corner-none: var(--md-ref-spacings-0);
    --md-sys-shape-corner-extra-small: var(--md-ref-spacings-1);
    --md-sys-shape-corner-small: var(--md-ref-spacings-2);
    --md-sys-shape-corner-medium: var(--md-ref-spacings-3);
    --md-sys-shape-corner-large: var(--md-ref-spacings-4);
    --md-sys-shape-corner-extra-large: var(--md-ref-spacings-6);
    --md-sys-shape-corner-full: var(--md-ref-spacings-32);

    /* Typescale */
    --md-sys-typescale-display-large-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-display-large-weight: var(--md-ref-typeface-weight-large);
    --md-sys-typescale-display-large-size: 64px;
    --md-sys-typescale-display-large-line-height: 80px;
    --md-sys-typescale-display-large-tracking: 0.25px;

    --md-sys-typescale-display-medium-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-display-medium-weight: var(--md-ref-typeface-weight-large);
    --md-sys-typescale-display-medium-size: 51px;
    --md-sys-typescale-display-medium-line-height: 64px;
    --md-sys-typescale-display-medium-tracking: 0.25px;

    --md-sys-typescale-display-small-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-display-small-weight: var(--md-ref-typeface-weight-large);
    --md-sys-typescale-display-small-size: 45px;
    --md-sys-typescale-display-small-line-height: 52px;
    --md-sys-typescale-display-small-tracking: 0px;

    --md-sys-typescale-headline-large-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-headline-large-weight: var(--md-ref-typeface-weight-large);
    --md-sys-typescale-headline-large-size: 40px;
    --md-sys-typescale-headline-large-line-height: 50px;
    --md-sys-typescale-headline-large-tracking: 0px;

    --md-sys-typescale-headline-medium-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-headline-medium-weight: var(--md-ref-typeface-weight-large);
    --md-sys-typescale-headline-medium-size: 32px;
    --md-sys-typescale-headline-medium-line-height: 40px;
    --md-sys-typescale-headline-medium-tracking: 0px;

    --md-sys-typescale-headline-small-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-headline-small-weight: var(--md-ref-typeface-weight-large);
    --md-sys-typescale-headline-small-size: 28px;
    --md-sys-typescale-headline-small-line-height: 36px;
    --md-sys-typescale-headline-small-tracking: 0px;

    --md-sys-typescale-title-large-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-title-large-weight: var(--md-ref-typeface-weight-large);
    --md-sys-typescale-title-large-size: 24px;
    --md-sys-typescale-title-large-line-height: 28px;
    --md-sys-typescale-title-large-tracking: 0px;

    --md-sys-typescale-title-medium-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-title-medium-weight: var(--md-ref-typeface-weight-large);
    --md-sys-typescale-title-medium-size: 22px;
    --md-sys-typescale-title-medium-line-height: 28px;
    --md-sys-typescale-title-medium-tracking: 0.15px;

    --md-sys-typescale-title-small-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-title-small-weight: var(--md-ref-typeface-weight-medium);
    --md-sys-typescale-title-small-size: 16px;
    --md-sys-typescale-title-small-line-height: 24px;
    --md-sys-typescale-title-small-tracking: 0.15px;

    --md-sys-typescale-label-large-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-label-large-weight: var(--md-ref-typeface-weight-medium);
    --md-sys-typescale-label-large-size: 16px;
    --md-sys-typescale-label-large-line-height: 22px;
    --md-sys-typescale-label-large-tracking: 0px;

    --md-sys-typescale-label-medium-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-label-medium-weight: var(--md-ref-typeface-weight-medium);
    --md-sys-typescale-label-medium-size: 14px;
    --md-sys-typescale-label-medium-line-height: 20px;
    --md-sys-typescale-label-medium-tracking: 0.1px;

    --md-sys-typescale-label-small-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-label-small-weight: var(--md-ref-typeface-weight-medium);
    --md-sys-typescale-label-small-size: 12px;
    --md-sys-typescale-label-small-line-height: 16px;
    --md-sys-typescale-label-small-tracking: 0.5px;

    --md-sys-typescale-body-large-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-body-large-weight: var(--md-ref-typeface-weight-regular);
    --md-sys-typescale-body-large-size: 16px;
    --md-sys-typescale-body-large-line-height: 24px;
    --md-sys-typescale-body-large-tracking: 0.5px;

    --md-sys-typescale-body-medium-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-body-medium-weight: var(--md-ref-typeface-weight-regular);
    --md-sys-typescale-body-medium-size: 14px;
    --md-sys-typescale-body-medium-line-height: 20px;
    --md-sys-typescale-body-medium-tracking: 0.25px;

    --md-sys-typescale-body-small-font: var(--md-ref-typeface-brand);
    --md-sys-typescale-body-small-weight: var(--md-ref-typeface-weight-regular);
    --md-sys-typescale-body-small-size: 12px;
    --md-sys-typescale-body-small-line-height: 16px;
    --md-sys-typescale-body-small-tracking: 0.4px;
}
"""

# Couche sémantique — dupliquée sur :root ET .light pour fonctionner
# immédiatement (cf. docstring du module).
_SEMANTIC_LIGHT = """
:root, .light {
    --md-sys-color-secondary-container: var(--md-ref-palette-secondary-90);
    --md-sys-color-tertiary-container: var(--md-ref-palette-tertiary-90);
    --md-sys-color-error-container: var(--md-ref-palette-error-90);
    --md-sys-color-warning-container: var(--md-ref-palette-warning-90);
    --md-sys-color-success-container: var(--md-ref-palette-success-90);
    --md-sys-color-primary-container: var(--md-ref-palette-primary-90);
    --md-sys-color-surface: var(--md-ref-palette-neutral-100);
    --md-sys-color-surface-container-lowest: var(--md-ref-palette-neutral-98);
    --md-sys-color-surface-dim: var(--md-ref-palette-neutral-80);
    --md-sys-color-surface-container-low: var(--md-ref-palette-neutral-95);
    --md-sys-color-surface-bright: var(--md-ref-palette-neutral-98);
    --md-sys-color-surface-container: var(--md-ref-palette-neutral-98);
    --md-sys-color-surface-container-high: var(--md-ref-palette-neutral-90);
    --md-sys-color-surface-container-highest: var(--md-ref-palette-neutral-80);
    --md-sys-color-surface-variant: var(--md-ref-palette-neutral-90);
    --md-sys-color-inverse-on-surface: var(--md-ref-palette-neutral-95);
    --md-sys-color-inverse-surface: var(--md-ref-palette-neutral-20);
    --md-sys-color-inverse-primary: var(--md-ref-palette-primary-80);
    --md-sys-color-on-primary: var(--md-ref-palette-primary-100);
    --md-sys-color-on-secondary: var(--md-ref-palette-secondary-100);
    --md-sys-color-on-tertiary: var(--md-ref-palette-tertiary-100);
    --md-sys-color-on-error: var(--md-ref-palette-error-100);
    --md-sys-color-on-warning: var(--md-ref-palette-warning-100);
    --md-sys-color-on-success: var(--md-ref-palette-success-100);
    --md-sys-color-on-primary-container: var(--md-ref-palette-primary-10);
    --md-sys-color-on-secondary-container: var(--md-ref-palette-secondary-10);
    --md-sys-color-on-tertiary-container: var(--md-ref-palette-tertiary-10);
    --md-sys-color-on-error-container: var(--md-ref-palette-error-10);
    --md-sys-color-on-warning-container: var(--md-ref-palette-warning-10);
    --md-sys-color-on-success-container: var(--md-ref-palette-success-10);
    --md-sys-color-on-surface: var(--md-ref-palette-neutral-10);
    --md-sys-color-on-surface-variant: var(--md-ref-palette-neutral-variant-30);
    --md-sys-color-on-background: var(--md-ref-palette-neutral-10);
    --md-sys-color-outline: var(--md-ref-palette-neutral-variant-70);
    --md-sys-color-outline-variant: var(--md-ref-palette-neutral-variant-80);
    --md-sys-color-outline-error: var(--md-ref-palette-error-40);
    --md-sys-color-outline-warning: var(--md-ref-palette-warning-40);
    --md-sys-color-primary: var(--md-ref-palette-primary-40);
    --md-sys-color-outline-success: var(--md-ref-palette-success-40);
    --md-sys-color-secondary: var(--md-ref-palette-secondary-40);
    --md-sys-color-tertiary: var(--md-ref-palette-tertiary-40);
    --md-sys-color-error: var(--md-ref-palette-error-40);
    --md-sys-color-warning: var(--md-ref-palette-warning-40);
    --md-sys-color-success: var(--md-ref-palette-success-40);
    --md-sys-color-background: var(--md-ref-palette-secondary-98);
    --md-sys-color-shadow: var(--md-ref-shadow-light-opacity-0);
    --md-sys-color-scrim: var(--md-ref-shadow-universal-opacity-40);
    --md-sys-color-state-opacity-0: var(--md-ref-shadow-light-opacity-0);
    --md-sys-color-state-opacity-8: var(--md-ref-shadow-light-opacity-8);
    --md-sys-color-state-opacity-12: var(--md-ref-shadow-light-opacity-12);
    --md-sys-color-state-opacity-16: var(--md-ref-shadow-light-opacity-16);
    --md-sys-color-shadow-opacity-15: var(--md-ref-shadow-light-opacity-15);
    --md-sys-color-shadow-opacity-30: var(--md-ref-shadow-light-opacity-30);
    --md-sys-color-gradient-grad-0: var(--md-ref-shadow-universal-opacity-0);
    --md-sys-color-gradient-grad-100: var(--md-ref-shadow-universal-opacity-80);

    /* Alias --spacing utilisé par nos composants ge_design_kit */
    --spacing: var(--md-ref-spacings-1);
}
"""


def inject_ge_tokens():
    """
    A appeler seule si tu n'utilises PAS inject_ge_styles() combiné.
    Pour minimiser le nombre de stElementContainer vides dans le DOM,
    préfère ge_design_kit.styles.inject_ge_styles() qui fusionne
    fonts + tokens + layout en un seul appel.
    """
    st.html(f"<style>{_PRIMITIVES}{_SHAPE_TYPESCALE}{_SEMANTIC_LIGHT}</style>")


# Exposé pour combinaison dans styles.py — évite un st.markdown séparé
TOKENS_CSS = _PRIMITIVES + _SHAPE_TYPESCALE + _SEMANTIC_LIGHT
