# Application Analyse Tennis

Prototype de test pour valider l'analyse de swing tennis par IA.

**Objectif** : comparer deux approches et choisir la meilleure avant de construire le vrai produit.

---

## Deux approches testées

| Approche | Script | Entrée | Modèle |
|---|---|---|---|
| Claude (frames) | `analyse_claude.py` | 6 frames extraites automatiquement | claude-sonnet-4-6 |
| Gemini (vidéo brute) | `analyse_gemini.py` | Vidéo MP4 complète | gemini-1.5-pro |

---

## Installation (une seule fois)

**Prérequis : Python 3.9+**

```bash
pip install -r requirements.txt
```

## Configuration des clés API

```bash
cp .env.example .env
```

Ouvre `.env` et remplis tes deux clés :
- `ANTHROPIC_API_KEY` → depuis console.anthropic.com
- `GOOGLE_API_KEY` → depuis aistudio.google.com

---

## Utilisation

### Approche 1 — Claude avec frames extraites automatiquement

```bash
python analyse_claude.py ma_video.mp4
```

Le script extrait 6 frames de la vidéo (début → fin du geste) et les envoie à Claude.

### Approche 2 — Gemini avec vidéo brute

```bash
python analyse_gemini.py ma_video.mp4
```

Le script envoie la vidéo complète à Gemini 1.5 Pro qui l'analyse directement.

### Optionnel — Extraire et sauvegarder les frames seules

```bash
python extract_frames.py ma_video.mp4
```

Sauvegarde 6 frames JPEG dans le dossier courant (utile pour vérifier ce que Claude reçoit).

---

## Format du feedback produit

Les deux scripts retournent un feedback structuré :

```
SHOT TYPE
TECHNIQUE BREAKDOWN (grip, stance, backswing, contact point, follow-through)
KEY ERRORS (2-3 erreurs principales)
ACTIONABLE ADVICE (un drill concret par erreur)
OVERALL LEVEL (Beginner / Intermediate / Advanced)
```

---

## Formats vidéo supportés

- Claude : MP4, MOV, AVI (tout format lisible par OpenCV)
- Gemini : MP4 ou MOV recommandés

Durée recommandée : 5 à 30 secondes, un seul geste par vidéo.
