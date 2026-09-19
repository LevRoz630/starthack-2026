#!/usr/bin/env bash
# Cuts the demo film: the advisor picking up (b-roll), then the call on screen with
# both voices over it.
#
# phone-screen.mp4 is silent -- the phone's own mic fed the app, nothing was recorded
# into the file. advisor-voice.m4a is the room recording of that same run, and it is
# already in step with it: the card at 2:00 shows the advisor's own sentence ("which
# is not -- really not risky..."), which ends at 122.4s in the audio too. So his track
# is laid down at offset zero and only the take's tail is cut.
#
# Walter's eight lines were recorded separately (walter-voice.m4a) and are placed to
# land just before the card each one produces. He is mixed on top and the advisor
# ducks under him, because the advisor answered straight through without leaving gaps
# the questions fit into.
#
# CARDS is when each of Walter's cards appears in phone-screen.mp4. Nudge a number
# and re-run; nothing else needs touching.
set -uo pipefail
cd "$(dirname "$0")"

MEDIA=media
OUT=${1:-demo.mp4}
W=1080
H=1920
LEAD=0.4          # a question ends this long before its card appears
ADVISOR_END=174   # the take carries on into the room afterwards; that is not the film
BROLL_END=4.6     # he has the phone up by 3.4s; the film moves on once he has it
KEEP=0.5          # a pause longer than this is trimmed back to it, picture and all
HUSH=-33dB        # quieter than this counts as a pause; the room is never silent
HUSH_MIN=0.6      # and it has to last this long to be one
PROTECT=176       # past here is the call note and the email: silent on purpose
FIRST_ANSWER=5.0  # nobody speaks before the advisor has answered

# Walter's eight lines: start and end in walter-voice.m4a, from silencedetect.
SEGS=(
  "1.04 5.40"    # Morning, it's Walter. How much did today cost me?
  "6.80 10.27"   # I still follow the chemistry side. How much is in pharma?
  "11.78 14.62"  # Am I too concentrated in one thing?
  "15.68 17.78"  # And how has it done over the year?
  "19.27 21.92"  # How risky is the portfolio overall?
  "23.53 26.02"  # And how much cash do I have with you?
  "27.94 30.43"  # When did we last actually change anything?
  "31.02 34.49"  # Keep it off paper where you can. I'll call you.
)
# Where each one's card appears on screen. The sign-off has no card of its own, so it
# sits in the pause before End call is pressed.
CARDS=(10.0 31.4 52.8 72.2 102.2 129.2 145.2 167.9)

# --- Walter's lines, each delayed to its place ---------------------------------
filters=""
mixes=""
for i in "${!SEGS[@]}"; do
  read -r from to <<<"${SEGS[$i]}"
  dur=$(awk -v a="$from" -v b="$to" 'BEGIN{printf "%.3f", b-a}')
  at=$(awk -v c="${CARDS[$i]}" -v d="$dur" -v l="$LEAD" -v f="$FIRST_ANSWER" \
       'BEGIN{t=c-l-d; if (t<f) t=f; printf "%.0f", t*1000}')
  filters+="[1:a]atrim=start=${from}:end=${to},asetpts=PTS-STARTPTS,adelay=${at}|${at}[w$i];"
  mixes+="[w$i]"
done

# --- part one: the advisor answers ---------------------------------------------
ffmpeg -v error -y -t "$BROLL_END" -i "$MEDIA/advisor-broll.mp4" \
  -filter_complex "[0:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},boxblur=22:2[bg];
                   [0:v]scale=${W}:-2[fg];
                   [bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p[v]" \
  -map "[v]" -map 0:a -af "loudnorm=I=-18" \
  -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 part-a.mp4 || exit 1

# --- part two: the call on screen, both voices over it -------------------------
# The mix is built first on its own, because where it falls silent is where both it
# and the picture get shortened -- cutting only the sound would walk the cards out of
# step with the voices.
ffmpeg -v error -y -i "$MEDIA/advisor-voice.m4a" -i "$MEDIA/walter-voice.m4a" \
  -filter_complex "${filters}
                   ${mixes}amix=inputs=${#SEGS[@]}:normalize=0,aresample=48000,asplit=2[wa][wb];
                   [0:a]atrim=end=${ADVISOR_END},asetpts=PTS-STARTPTS,aresample=48000[adv];
                   [adv][wb]sidechaincompress=threshold=0.03:ratio=9:attack=30:release=500[duck];
                   [duck][wa]amix=inputs=2:normalize=0,loudnorm=I=-18[a]" \
  -map "[a]" -c:a pcm_s16le mix.wav || exit 1

CALL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MEDIA/phone-screen.mp4")
KEEPS=$(ffmpeg -hide_banner -i mix.wav -af "silencedetect=noise=${HUSH}:d=${HUSH_MIN}" -f null /dev/null 2>&1 \
        | python3 gaps.py "$CALL" "$KEEP" "$PROTECT")
[ -n "$KEEPS" ] || exit 1

ffmpeg -v error -y -i "$MEDIA/phone-screen.mp4" -i mix.wav \
  -filter_complex "[0:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},boxblur=22:2[bg];
                   [0:v]scale=-2:${H}[fg];
                   [bg][fg]overlay=(W-w)/2:0[full];
                   [full]select='${KEEPS}',setpts=N/FRAME_RATE/TB,fps=30,format=yuv420p[v];
                   [1:a]aselect='${KEEPS}',asetpts=N/SR/TB[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 part-b.mp4 || exit 1
rm -f mix.wav

# --- one film ------------------------------------------------------------------
printf "file 'part-a.mp4'\nfile 'part-b.mp4'\n" > parts.txt
ffmpeg -v error -y -f concat -safe 0 -i parts.txt -c copy "$OUT" || exit 1
rm -f parts.txt part-a.mp4 part-b.mp4
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
