import sys
import cv2


def extract_frames(video_path: str, num_frames: int = 6) -> list:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Impossible d'ouvrir la vidéo : {video_path}")

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total == 0:
        raise ValueError(f"La vidéo ne contient aucune frame : {video_path}")

    indices = [int(i * total / num_frames) for i in range(num_frames)]
    frames = []
    for i, idx in enumerate(indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError(f"Impossible de lire la frame {idx}")
        success, buffer = cv2.imencode(".jpg", frame)
        if not success:
            raise RuntimeError(f"Impossible d'encoder la frame {idx} en JPEG")
        frames.append(bytes(buffer))
        print(f"  Frame {i + 1}/{num_frames} extraite (position {idx}/{total})")

    cap.release()
    return frames


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_frames.py <video.mp4>")
        sys.exit(1)

    video = sys.argv[1]
    print(f"Extraction de {6} frames depuis : {video}")
    extracted = extract_frames(video)
    print(f"\n{len(extracted)} frames extraites avec succès.")

    import os
    base = os.path.splitext(os.path.basename(video))[0]
    for i, frame_bytes in enumerate(extracted):
        out_path = f"{base}_frame_{i + 1}.jpg"
        with open(out_path, "wb") as f:
            f.write(frame_bytes)
        print(f"  Sauvegardée : {out_path}")
