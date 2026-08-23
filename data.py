"""
data.py
--------
Source de données mockée du POC, partagée entre les pages (views/).
"""

import pandas as pd


def load_operations_df() -> pd.DataFrame:
    df = pd.DataFrame([
        {
            "Opération": "Votation fédérale", "Date": "17.06.2025",
            "Type de scrutin": "Votation", "Canal": "Correspondance",
            "Statut analyse": "🟢 Analysée", "Clusters": 3,
            "Dernière analyse": "18.06.2025 14h32",
        },
        {
            "Opération": "Votation cantonale", "Date": "17.06.2025",
            "Type de scrutin": "Votation", "Canal": "Urne",
            "Statut analyse": "🟢 Analysée", "Clusters": 0,
            "Dernière analyse": "18.06.2025 14h00",
        },
        {
            "Opération": "Votation communale", "Date": "17.06.2025",
            "Type de scrutin": "Votation", "Canal": "Correspondance",
            "Statut analyse": "🟡 En cours", "Clusters": None,
            "Dernière analyse": None,
        },
        {
            "Opération": "Votation fédérale", "Date": "17.06.2025",
            "Type de scrutin": "Votation", "Canal": "Urne",
            "Statut analyse": "⚪ Non démarrée", "Clusters": None,
            "Dernière analyse": None,
        },
        {
            "Opération": "Élection du Conseil d'État", "Date": "09.02.2025",
            "Type de scrutin": "Élection", "Canal": "Correspondance",
            "Statut analyse": "🟢 Analysée", "Clusters": 1,
            "Dernière analyse": "10.02.2025 09h15",
        },
        {
            "Opération": "Élection du Conseil national", "Date": "09.02.2025",
            "Type de scrutin": "Élection", "Canal": "Urne",
            "Statut analyse": "🟢 Analysée", "Clusters": 5,
            "Dernière analyse": "10.02.2025 11h20",
        },
        {
            "Opération": "Votation fédérale", "Date": "09.02.2025",
            "Type de scrutin": "Votation", "Canal": "Correspondance",
            "Statut analyse": "🟡 En cours", "Clusters": None,
            "Dernière analyse": None,
        },
        {
            "Opération": "Votation cantonale", "Date": "22.10.2025",
            "Type de scrutin": "Votation", "Canal": "Urne",
            "Statut analyse": "⚪ Non démarrée", "Clusters": None,
            "Dernière analyse": None,
        },
        {
            "Opération": "Élection municipale", "Date": "22.10.2025",
            "Type de scrutin": "Élection", "Canal": "Correspondance",
            "Statut analyse": "🟢 Analysée", "Clusters": 2,
            "Dernière analyse": "23.10.2025 08h45",
        },
        {
            "Opération": "Votation communale", "Date": "22.10.2025",
            "Type de scrutin": "Votation", "Canal": "Urne",
            "Statut analyse": "🟢 Analysée", "Clusters": 0,
            "Dernière analyse": "23.10.2025 10h05",
        },
    ])
    df.insert(0, "id", range(len(df)))
    return df
