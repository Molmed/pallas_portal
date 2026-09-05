FROM python:3.12-slim-bookworm

# Create user name and home directory variables.
# The variables are later used as $USER and $HOME.
ENV USER=deploy
ENV HOME=/home/$USER

# Add user to system
RUN useradd -m -u 1000 $USER

WORKDIR $HOME/app

# Update system and install dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common \
    git

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER $USER
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]
