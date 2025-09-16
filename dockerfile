FROM ubuntu:22.04

# Install basic tools
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    python3.11 \
    python3.11-venv \
    python3-pip \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install .NET 8 SDK
RUN wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
    && bash dotnet-install.sh --channel 8.0 \
    && rm dotnet-install.sh

ENV DOTNET_ROOT=/root/.dotnet
ENV PATH=$DOTNET_ROOT:$PATH

# Install PythonNet 3.0.5
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pythonnet==3.0.5
RUN python3 -m pip install watchdog

# Install PowerShell 7 tarball (non-snap)
RUN wget https://github.com/PowerShell/PowerShell/releases/download/v7.5.3/powershell-7.5.3-linux-x64.tar.gz \
    && mkdir -v -p /opt/microsoft/powershell \
    && tar -xzf powershell-7.5.3-linux-x64.tar.gz -C /opt/microsoft/powershell \
    && rm powershell-7.5.3-linux-x64.tar.gz

ENV PATH=$PATH:/opt/microsoft/powershell
ENV PS_HOME=/opt/microsoft/powershell

# Copy your Python scripts
WORKDIR /app
COPY src/ /app/

# Default command
CMD ["python3", "main.py"]
