FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libreoffice-writer libreoffice-impress poppler-utils python3 python3-pil fonts-liberation fonts-dejavu-core fonts-crosextra-carlito fonts-crosextra-caladea && rm -rf /var/lib/apt/lists/*
ENV HOME=/tmp LANG=C.UTF-8
USER 65534:65534
WORKDIR /tmp
