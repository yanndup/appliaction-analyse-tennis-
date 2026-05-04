import sys
import os
import time

from dotenv import load_dotenv
import google.generativeai as genai

PROMPT = """You are an expert tennis coach with 20+ years of experience.
Analyse the tennis swing shown in this video and provide structured feedback.

Return your analysis in the following format, using these exact section headers:

SHOT TYPE
[Identify the shot: forehand, backhand, serve, volley, smash — and whether it is topspin, flat, or slice]

TECHNIQUE BREAKDOWN
- Grip: [assessment]
- Stance: [assessment]
- Backswing: [assessment]
- Contact point: [assessment]
- Follow-through: [assessment]

KEY ERRORS (pick the 2-3 most important)
1. [Error name]: [Brief description of the problem]
2. [Error name]: [Brief description of the problem]
3. [Error name if applicable — omit if fewer than 3]

ACTIONABLE ADVICE
1. [Concrete drill or adjustment for error 1]
2. [Concrete drill or adjustment for error 2]
3. [If applicable — omit if fewer than 3]

OVERALL LEVEL
[Beginner / Intermediate / Advanced] — [one sentence justification]

Be direct and specific. Avoid generic praise. Focus on what will most improve this player's technique."""


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyse_gemini.py <video.mp4>")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Erreur : GOOGLE_API_KEY manquant. Copie .env.example en .env et remplis ta clé.")
        sys.exit(1)

    video_path = sys.argv[1]
    print(f"\n=== ANALYSE GEMINI — {video_path} ===\n")

    genai.configure(api_key=api_key)

    print("Upload de la vidéo vers Gemini Files API...")
    uploaded_file = genai.upload_file(path=video_path, mime_type="video/mp4")
    print(f"Upload terminé. Attente du traitement de la vidéo...")

    while uploaded_file.state.name == "PROCESSING":
        time.sleep(2)
        uploaded_file = genai.get_file(uploaded_file.name)
        print("  Traitement en cours...")

    if uploaded_file.state.name != "ACTIVE":
        print(f"Erreur : la vidéo n'est pas disponible (état : {uploaded_file.state.name})")
        sys.exit(1)

    print("Vidéo prête. Envoi à Gemini 1.5 Pro...\n")
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([uploaded_file, PROMPT])

    print("=" * 60)
    print("FEEDBACK GEMINI")
    print("=" * 60)
    print(response.text)
    print("=" * 60)
    print("Modèle : gemini-1.5-pro")
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        meta = response.usage_metadata
        print(f"Tokens — entrée : {meta.prompt_token_count}  sortie : {meta.candidates_token_count}")

    genai.delete_file(uploaded_file.name)
    print("Fichier vidéo supprimé de Gemini Files API.")


if __name__ == "__main__":
    main()
