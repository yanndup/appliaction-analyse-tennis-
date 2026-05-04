import sys
import os
import base64

from dotenv import load_dotenv
import anthropic

from extract_frames import extract_frames

PROMPT = """You are an expert tennis coach with 20+ years of experience.
Analyse the tennis swing shown in these images and provide structured feedback.

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
        print("Usage: python analyse_claude.py <video.mp4>")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Erreur : ANTHROPIC_API_KEY manquant. Copie .env.example en .env et remplis ta clé.")
        sys.exit(1)

    video_path = sys.argv[1]
    print(f"\n=== ANALYSE CLAUDE — {video_path} ===\n")
    print("Extraction des frames...")
    frames = extract_frames(video_path)

    print("\nEnvoi à Claude (claude-sonnet-4-6)...")
    content = []
    for frame_bytes in frames:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": base64.standard_b64encode(frame_bytes).decode("utf-8"),
            },
        })
    content.append({"type": "text", "text": PROMPT})

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": content}],
    )

    print("\n" + "=" * 60)
    print("FEEDBACK CLAUDE")
    print("=" * 60)
    print(response.content[0].text)
    print("=" * 60)
    print(f"Modèle : {response.model}")
    print(f"Tokens — entrée : {response.usage.input_tokens}  sortie : {response.usage.output_tokens}")


if __name__ == "__main__":
    main()
