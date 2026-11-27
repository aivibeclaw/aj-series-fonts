FROM python:3.12-slim

LABEL org.opencontainers.image.title="AJ Series & Aaahhh Fonts Vibe Enterprise CDN (v3.1.0)" \
      org.opencontainers.image.vendor="Aivibe Software Services Private Limited" \
      org.opencontainers.image.authors="Aravind Jayamohan, India" \
      org.opencontainers.image.version="3.1.0" \
      org.opencontainers.image.licenses="LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1"

# PLACEHOLDER: Mount or bake unmodified canonical `dist/` binaries into `/var/www/fonts/dist`
RUN apt-get update && apt-get install -y --no-install-recommends fontconfig && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/www/fonts/dist /usr/share/fonts/aj-series \
    && printf '{"status":"ok","suite":"AJ Series & Aaahhh Fonts Vibe","version":"3.1.0"}\n' > /var/www/fonts/healthz

WORKDIR /var/www/fonts
COPY dist/ /var/www/fonts/dist/
COPY dist/ /usr/share/fonts/aj-series/
COPY distributions/linux/65-aj-series.conf /etc/fonts/conf.d/65-aj-series.conf
COPY AIVIBE_ECOSYSTEM_FONT_LICENSE.md LICENSE.md COPYRIGHT_NOTICE.md /var/www/fonts/

RUN find /var/www/fonts/dist /usr/share/fonts/aj-series -type f \( -name '*.ttf' -o -name '*.otf' -o -name '*.woff' -o -name '*.woff2' \) -exec chmod 0444 {} + \
    && fc-cache -rf

EXPOSE 8080
CMD ["python3", "-m", "http.server", "8080", "--directory", "/var/www/fonts"]
