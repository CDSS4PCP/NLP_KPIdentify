# Use micromamba for highly optimized, pre-compiled package resolution (Conda-based)
FROM mambaorg/micromamba:1.5.8

WORKDIR /app

# Copy the platform-independent conda environment file
COPY environment.yml .

# Create base environment and install all packages (bypasses local wheel compilations entirely!)
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes

# Activate the base micromamba environment automatically in all run commands
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Pre-download NLTK stopwords and punkt collections
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt');"

# Set system environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy application files
COPY src/ ./src/
COPY data/ ./data/
COPY interim_data/ ./interim_data/

# Set root temporarily to establish output folder permissions, then drop back to non-root user
USER root
RUN mkdir -p outputs/models interim_data data && \
    chown -R mambauser:mambauser /app
USER mambauser

# Expose FastAPI API port
EXPOSE 8000

# Execute inside the micromamba activated shell entrypoint
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "python", "src/nlp/jobs/gna_pipeline.py"]
CMD ["--help"]
