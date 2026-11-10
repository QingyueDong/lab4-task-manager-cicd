# =============================================================================
# Lab 4 / Lecture 4 - Activity 7: Dockerfile for the task manager
#
# Build:  docker build -t task-manager:latest .
# Run  :  docker run --rm -v "$PWD:/workspace" -w /workspace task-manager:latest
#         (the -v/-w mount is what lets the container update YOUR index.html)
# =============================================================================

# Use a Python base image (slides: python:3.9-slim, end-of-life since Oct 2025).
# The slim image already includes bash, perl (used by update_index.sh) and tzdata.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# No `apt-get install git`: committing happens in the workflow, not in the container.

# Copy only the scripts (never .git - see .dockerignore)
COPY .github/scripts/ /app/.github/scripts/

# Ensure the entrypoint script exists and is executable
RUN chmod +x /app/.github/scripts/*.sh

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["/app/.github/scripts/entrypoint.sh"]
