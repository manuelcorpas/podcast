#!/bin/bash
# Download existing podcast audio files from WordPress
# Run from repo root: bash scripts/download_episodes.sh

set -e
cd "$(dirname "$0")/.."

echo "Downloading podcast audio from WordPress..."
echo "Note: Some files are large WAV files (up to 1.6GB). This may take a while."
echo ""

# Episode 1 (Jan 2026) - MP3 ~8MB
echo "[1/10] Why LLMs Can Hurt Your Academic Writing..."
curl -L -o audio/2026-01-25-llms-academic-writing.mp3 \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2026/01/podcast_episode.mp3"

# Episode 2 (Dec 2025) - WAV ~183MB
echo "[2/10] Missing Pieces: Genomic Diversity..."
curl -L -o audio/2025-12-10-missing-pieces-genomic-diversity.wav \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2025/12/indonesia-uk.wav"

# Episode 3 (Dec 2025) - WAV ~1.3GB
echo "[3/10] The Precision Medicine Paradox..."
curl -L -o audio/2025-12-01-precision-medicine-paradox.wav \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2025/12/geneediting.wav"

# Episode 4 (Oct 2025) - WAV ~645MB
echo "[4/10] Health Data Equity in Latin America..."
curl -L -o audio/2025-10-07-health-data-equity-latin-america.wav \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2025/10/webinar-britcham-health-data-equity-in-latin-america-in-the-age-of-ai-and-genomics.wav"

# Episode 5 (Sep 2025) - WAV ~1.6GB
echo "[5/10] Biobanking Meets AI..."
curl -L -o audio/2025-09-25-biobanking-meets-ai.wav \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2025/09/00-biobanking.wav"

# Episode 6 (Aug 2025) - WAV ~538MB
echo "[6/10] My Journey to Health Equity..."
curl -L -o audio/2025-08-13-journey-health-equity-genomics.wav \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2025/08/paicon.wav"

# Episode 7 (Jul 2025) - WAV ~370MB
echo "[7/10] Why Diversity Must Be at the Heart..."
curl -L -o audio/2025-07-13-diversity-precision-medicine.wav \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2025/07/kingston-diversity.wav"

# Episode 8 (Jun 2025) - WAV ~155MB
echo "[8/10] Bridging the Diversity Gap..."
curl -L -o audio/2025-06-24-bridging-diversity-gap.wav \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2025/06/bridging.wav"

# Episode 9 (May 2025) - WAV ~968MB
echo "[9/10] Fireside Chat with Yves Moreau..."
curl -L -o audio/2025-05-10-fireside-chat-yves-moreau.wav \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2025/05/manny-yves.wav"

# Episode 10 (May 2025) - WAV ~984MB
echo "[10/10] A ChatGPT Moment for Genomics..."
curl -L -o audio/2025-05-08-chatgpt-moment-genomics.wav \
  "https://corpasfoo.wordpress.com/wp-content/uploads/2025/05/drugdiaries.wav"

echo ""
echo "All downloads complete."
echo "Total estimated size: ~5.8 GB"
echo ""
echo "IMPORTANT: GitHub has a 100MB file size limit."
echo "You will need Git LFS for the WAV files, or convert them to MP3 first."
echo ""
echo "To convert all WAV to MP3 (recommended):"
echo "  for f in audio/*.wav; do"
echo '    ffmpeg -i "$f" -codec:a libmp3lame -qscale:a 2 "${f%.wav}.mp3"'
echo '    rm "$f"'
echo "  done"
echo ""
echo "Then update feed.xml enclosure URLs and types accordingly."
