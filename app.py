import av
import cv2
import time
import threading
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
from drowsy_detection import VideoFrameHandler
from seat_belt import detect_seatbelt

# Page configuration
st.set_page_config(
    page_title="Driver Safety Monitor🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }
.stApp { background: #0a0e1a; color: #e0e8f0; }

.main-header {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    border-bottom: 1px solid #1e3a5f;
    margin-bottom: 1.5rem;
}
.main-header h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #00cfff;
    text-transform: uppercase;
    margin: 0;
    text-shadow: 0 0 18px rgba(0,207,255,0.35);
}
.main-header p {
    color: #5a7a9a;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.2em;
    margin-top: 0.3rem;
}

.status-card {
    background: #0d1526;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.status-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    color: #4a6a8a;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.status-value { font-size: 1.3rem; font-weight: 700; letter-spacing: 0.06em; }
.status-idle  { color: #5a7a9a; }

.alert-banner {
    background: linear-gradient(135deg, #3a0000 0%, #1a0000 100%);
    border: 2px solid #ff3333;
    border-radius: 6px;
    padding: 0.9rem 1.2rem;
    text-align: center;
    animation: pulseBorder 0.8s ease-in-out infinite alternate;
    margin-bottom: 1rem;
}
.alert-banner span {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ff4444;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
@keyframes pulseBorder {
    from { border-color: #ff3333; box-shadow: 0 0 6px #ff3333; }
    to   { border-color: #ff8888; box-shadow: 0 0 18px #ff4444; }
}

section[data-testid="stSidebar"] {
    background: #080c18 !important;
    border-right: 1px solid #1e3a5f;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

.stSlider > div > div > div { background: #00cfff !important; }

.footer {
    text-align: center;
    color: #2a4a6a;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid #1e3a5f;
    margin-top: 2rem;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Session state

for key, default in {
    "alert_active": False,
    "alert_last_triggered": 0.0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# Shared state

_shared = {"alert_active": False}
_lock = threading.Lock()

# Alert sound

_alert_thread_active = False
_alert_thread_lock = threading.Lock()


def _alert_worker():
    global _alert_thread_active
    try:
        import platform
        system = platform.system()
        for _ in range(4):
            if system == "Windows":
                import winsound
                winsound.Beep(1000, 250)
            else:
                try:
                    import subprocess
                    subprocess.run(
                        ["play", "-n", "synth", "0.25", "sine", "880"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=1,
                    )
                except Exception:
                    pass
            time.sleep(0.1)
    finally:
        with _alert_thread_lock:
            _alert_thread_active = False


def trigger_alert_sound():
    global _alert_thread_active
    with _alert_thread_lock:
        if not _alert_thread_active:
            _alert_thread_active = True
            t = threading.Thread(target=_alert_worker, daemon=True)
            t.start()


# VideoProcessor

class VideoProcessor:
    def __init__(self):
        self.handler = VideoFrameHandler()
        self._alert_cooldown = 5.0
        self._last_alert_time = 0.0
        self._thresholds = {"EAR_THRESH": 0.25, "WAIT_TIME": 2.0}

    def update_thresholds(self, ear_thresh: float, wait_time: float):
        self._thresholds = {"EAR_THRESH": ear_thresh, "WAIT_TIME": wait_time}

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        processed, play_alarm = self.handler.process(rgb, self._thresholds)

        processed = detect_seatbelt(processed)

        now = time.time()
        alert_active = bool(play_alarm)
        if alert_active and (now - self._last_alert_time) > self._alert_cooldown:
            self._last_alert_time = now
            trigger_alert_sound()

        with _lock:
            _shared["alert_active"] = alert_active

        return av.VideoFrame.from_ndarray(processed, format="bgr24")



# UI Layout

st.markdown("""
<div class="main-header">
    <h1> Driver Safety Monitoring System</h1>
    <p>REAL-TIME DROWSINESS &amp; SEATBELT DETECTION SYSTEM</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Detection Parameters ⚙️")
    ear_thresh = st.slider(
        "EAR Threshold",
        min_value=0.10, max_value=0.40, value=0.25, step=0.01,
        help="Eye Aspect Ratio below this value is considered drowsy.",
    )
    wait_time = st.slider(
        "Drowsy Wait Time (s)",
        min_value=0.5, max_value=5.0, value=2.0, step=0.5,
        help="Seconds of low EAR before alarm triggers.",
    )
    st.divider()
    st.markdown("### Legend 📋")
    st.markdown("""
- 🟢 **Green** landmarks → Eyes open  
- 🔴 **Red** landmarks → Eyes closing  
- **EAR** = Eye Aspect Ratio  
- **DROWSY** = Cumulative closed-eye time  
""")

col_video, col_status = st.columns([3, 1], gap="medium")

with col_video:
    RTC_CONFIG = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )
    ctx = webrtc_streamer(
        key="driver-safety",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIG,
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
    if ctx.video_processor:
        ctx.video_processor.update_thresholds(ear_thresh, wait_time)

with col_status:
    st.markdown("#### Parameters ⚙️")

    with _lock:
        alert_active = _shared["alert_active"]

    if alert_active:
        st.markdown("""
        <div class="alert-banner">
            <span>⚠️ DROWSY ALERT! ⚠️<br>WAKE UP!</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="status-card">
        <div class="status-label">EAR Threshold</div>
        <div class="status-value status-idle">{ear_thresh}</div>
    </div>
    <div class="status-card">
        <div class="status-label">Wait Time</div>
        <div class="status-value status-idle">{wait_time}s</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    DRIVER SAFETY MONITORING SYSTEM &nbsp;|&nbsp; REAL-TIME CV PIPELINE &nbsp;|&nbsp; v1.0
</div>
""", unsafe_allow_html=True)