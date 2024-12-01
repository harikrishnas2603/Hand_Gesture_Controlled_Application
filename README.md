# Hand-Gesture-Controlled-Applications
This project aims to provide a hand gesture based control systems for media apps such as image viewer, audio player, and video player.

## Prerequisites
- Python 3.10.x

## Setup Instructions
1. Clone the repo.
   
   ```bash
   git clone https://github.com/DeenuYT/Hand-Gesture-Controlled-Applications.git
   ```
3. Create a virtual environment (Optional).
   ```bash
   python -m venv <venv name>
   ```
4. Install the required python modules.
   ```bash
   pip install -r requirements.txt
   ```
5. Run the `media_apps.py`.
   ```bash
   python media_apps.py
   ```

## Supported Gestures
- Open Palm **(OP)**
- Right (Hand) Index Pointing **(RHIP)**
- Left Index Pointing **(LHIP)**
- Right Index and Middle Pointing **(RHIMP)**
- Right Index and Middle Pointing **(LHIMP)**
- Thumbs Up **(TU)**
- Zero Sign **(ZS)**
- OK sign **(OK)**
- Number Two Sign Closed **(NTC)**
- Number Two Sign Stretch **(NTS)**

## Apps and functions
1. **Image Viewer**
   - Next Image (RHIP)
   - Previous Image (LHIP)
   - Zoom In (NTS)
   - Zoom Out (NTC)
   - Zoom Reset (ZS)
2. **Audio Player**
   - Play (TU / OK)
   - Stop (OP / ZS)
   - Next Song (RHIP)
   - Previous Song (LHIP)
   - Volume Up (NTS)
   - Volume Down (NTC)
3. **Video Player**
   - Play (TU / OK)
   - Pause (OP)
   - Stop (ZS)
   - Next Video (RHIP)
   - Previous Video (LHIP)
   - Fast Forward (RHIMP)
   - Rewind (LHIMP)
   - Volume Up (NTS)
   - Volume Down (NTC)
