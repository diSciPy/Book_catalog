# syntax=docker/dockerfile:1

FROM python:3.9-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv

# Install python dependencies in /.venv
COPY Pipfile ./
COPY Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --system --create-home appuser
WORKDIR /home/appuser

# Install application into container
COPY . .

#Grant permissions to static and gunicorn
RUN chown -R appuser /home/appuser/app/static/img

#Switch to user
USER appuser

CMD ["/bin/bash"]

#start gunicorn web-server
ENTRYPOINT gunicorn --workers=1 --threads=3 -b 0.0.0.0:5001 run:flask_app

# Run the application
# CMD ["python3.9", "-m", "pipenv", "run", "python3.9", "run.py", "--host=0.0.0.0"]
# CMD ["python", "run.py", "--host=0.0.0.0"]
