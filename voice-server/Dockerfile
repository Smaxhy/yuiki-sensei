# Yuki's free voice server: the official VOICEVOX engine (Himari & Ryusei voices),
# ready for a free Hugging Face Space (Docker SDK, port 7860).
FROM voicevox/voicevox_engine:cpu-latest
# Hugging Face runs containers as user 1000, so skip the root-only entrypoint
# and keep the engine's settings somewhere writable.
ENV HOME=/tmp XDG_DATA_HOME=/tmp
ENTRYPOINT []
EXPOSE 7860
CMD ["/opt/voicevox_engine/run","--host","0.0.0.0","--port","7860","--cors_policy_mode","all"]
