FROM python:3.12-slim

LABEL org.opencontainers.image.title="AJ Series & Aaahhh Fonts Vibe (Sound of Font v3.0.0)" \
      org.opencontainers.image.vendor="Aivibe Software Services Private Limited" \
      org.opencontainers.image.authors="Aravind Jayamohan <aravind.j.naidu@gmail.com>" \
      org.opencontainers.image.version="3.0.0" \
      org.opencontainers.image.licenses="LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.0"

RUN apt-get update && apt-get install -y --no-install-recommends fontconfig && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/aj-series-fonts
COPY dist/ /usr/share/fonts/aj-series/
COPY distributions/linux/65-aj-series.conf /etc/fonts/conf.d/65-aj-series.conf
COPY sound_of_font/ /opt/aj-series-fonts/sound_of_font/
COPY AIVIBE_ECOSYSTEM_FONT_LICENSE.md LICENSE.md COPYRIGHT_NOTICE.md /opt/aj-series-fonts/

RUN fc-cache -rf

EXPOSE 8080
CMD ["python3", "-m", "http.server", "8080", "--directory", "/opt/aj-series-fonts/sound_of_font/web"]
