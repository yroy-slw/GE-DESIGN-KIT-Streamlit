"""
ge_design_kit.stepper
------------------------
ge_stepper - navigation "scroll-spy" verticale sticky : surligne
automatiquement la section actuellement visible pendant le scroll.
Contrairement à ge_card/ge_button/ge_checkbox, ce N'EST PAS un
composant CCv2 bidirectionnel (pas d'état renvoyé à Python) — de
simples ancres HTML natives gérées par le navigateur. st.html()
injecte directement dans le document principal (pas d'iframe/Shadow
DOM), donc `position: fixed` et `scroll-behavior: smooth` s'appliquent
à toute la page.

Prévu pour les pages longues à sections multiples (ex: gallery.py —
qui l'utilise sur lui-même, cf. son propre appel à ge_stepper en tête
de fichier).
"""

import streamlit as st


def ge_stepper(sections: list[tuple[str, str]]):
    """
    sections : liste de tuples (anchor, label) — anchor doit
    correspondre à un `anchor=...` déjà posé sur un st.header/st.title
    existant dans la page.

    Exemple :
        ge_stepper([
            ("topbar", "Topbar"),
            ("sidebar", "Sidebar"),
        ])
    """
    items_html = "".join(
        f'<a href="#{anchor}" data-anchor="{anchor}" class="ge-stepper-item">'
        f'<span class="ge-stepper-dot"></span>'
        f'<span class="ge-stepper-label">{label}</span>'
        f'</a>'
        for anchor, label in sections
    )

    st.html(f"""
    <style>
        html {{ scroll-behavior: smooth; }}

        .ge-stepper {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding: 12px 0;
        }}
        @media (max-width: 1400px) {{
            .ge-stepper {{ display: none; }}
        }}

        .ge-stepper-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 5px 8px;
            text-decoration: none;
            color: var(--md-sys-color-on-surface-variant, #6b7280);
            font-size: 12.5px;
            font-family: var(--st-font);
            border-radius: 6px;
            transition: color 0.15s, background 0.15s;
            position: relative;
        }}
        .ge-stepper-item:hover {{
            color: var(--md-sys-color-primary, #003355);
            background: var(--md-sys-color-surface-container-high, rgba(0,0,0,0.04));
        }}
        .ge-stepper-dot {{
            width: 24px;
            height: 24px;
            border-radius: 12px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--md-sys-color-on-surface-variant, #474746);
            opacity: 0.2;
            transition: background 0.2s, opacity 0.2s;
            position: relative;
        }}
        .ge-stepper-item:not(:last-child) .ge-stepper-dot::after {{
            content: "";
            position: absolute;
            left: 12px;
            top: 100%;
            width: 1px;
            height: 18px;
            background: var(--md-sys-color-on-surface-variant, #474746);
        }}
        .ge-stepper-label {{
            white-space: nowrap;
            font-size: 16px;
            font-weight: 500;
            line-height: 22px;
            color: var(--md-sys-color-on-surface, #1d242b);
            opacity: 0.4;
        }}

        .ge-stepper-item.is-active {{
            color: var(--md-sys-color-primary, #003355);
        }}
        .ge-stepper-item.is-active .ge-stepper-dot {{
            background: var(--md-sys-color-primary, #01629d);
            opacity: 1;
        }}
        .ge-stepper-item.is-active .ge-stepper-label {{
            font-weight: 600;
            opacity: 1;
        }}
    </style>

    <nav class="ge-stepper" aria-label="Navigation de section">
        {items_html}
    </nav>

    <script>
    (function() {{
        const items = document.querySelectorAll('.ge-stepper-item');
        const targets = Array.from(items)
            .map(item => document.getElementById(item.dataset.anchor))
            .filter(Boolean);

        if (!targets.length || !('IntersectionObserver' in window)) return;

        const setActive = (anchorId) => {{
            items.forEach(item => {{
                item.classList.toggle('is-active', item.dataset.anchor === anchorId);
            }});
        }};

        items.forEach(item => {{
            item.addEventListener('click', (e) => {{
                e.preventDefault();
                item.classList.add('is-active');
                const target = document.getElementById(item.dataset.anchor);
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});

        // ── Cas limites que l'IntersectionObserver ne peut PAS couvrir : ──
        // ── la bande de détection (35%-45% de la hauteur de viewport) ne ──
        // ── peut jamais atteindre le haut de la 1ère section (pas assez ──
        // ── de contenu AU-DESSUS pour la faire descendre jusque-là dès ──
        // ── scrollTop=0) ni le haut de la dernière (pas assez de contenu ──
        // ── EN DESSOUS pour la faire remonter jusque-là à scroll max) — ──
        // ── dans ces deux cas précis, l'observer ne voit juste RIEN ──
        // ── d'intersectant et ne déclenche aucun setActive. On couvre ces ──
        // ── deux bords explicitement via le scroll du VRAI conteneur ──
        // ── scrollable de Streamlit (stMain, pas window — cf. docstring du ──
        // ── module : st.html() s'injecte dans le document principal, mais ──
        // ── c'est Streamlit qui scrolle sa propre section interne). ──
        //
        // checkScrollBoundaries() est appelée EN PREMIER dans le callback de
        // l'observer lui-même (pas seulement au scroll) : son 1er batch
        // d'intersections arrive de façon ASYNCHRONE après observe() — sans
        // cette priorité, ce batch initial peut retomber juste après notre
        // appel synchrone au chargement et écraser "1ère section active" par
        // la 2ᵉ section si elle intersecte aussi la bande à ce moment-là.
        const scrollContainer = document.querySelector('[data-testid="stMain"]') || window;

        function checkScrollBoundaries() {{
            const isWindow = scrollContainer === window;
            const scrollTop = isWindow ? window.scrollY : scrollContainer.scrollTop;
            const scrollHeight = isWindow ? document.documentElement.scrollHeight : scrollContainer.scrollHeight;
            const clientHeight = isWindow ? window.innerHeight : scrollContainer.clientHeight;
            if (scrollTop <= 4) {{
                setActive(targets[0].id);
                return true;
            }}
            if (scrollTop + clientHeight >= scrollHeight - 4) {{
                setActive(targets[targets.length - 1].id);
                return true;
            }}
            return false;
        }}

        const observer = new IntersectionObserver((entries) => {{
            if (checkScrollBoundaries()) return;
            const visible = entries
                .filter(e => e.isIntersecting)
                .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
            if (visible.length) {{
                setActive(visible[0].target.id);
            }}
        }}, {{
            rootMargin: '-35% 0px -55% 0px',
            threshold: 0,
        }});

        targets.forEach(t => observer.observe(t));

        scrollContainer.addEventListener('scroll', checkScrollBoundaries, {{ passive: true }});
        checkScrollBoundaries(); // état initial (avant tout scroll/callback observer)
    }})();
    </script>
    """, unsafe_allow_javascript=True)