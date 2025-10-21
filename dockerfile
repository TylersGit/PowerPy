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
    libjpeg62 \
    && rm -rf /var/lib/apt/lists/*

# Install Mono 6.12
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF \
  && echo "deb http://download.mono-project.com/repo/ubuntu stable-focal main" > /etc/apt/sources.list.d/mono-official.list \
  && apt-get update \
  && apt-get install -y clang \
  && apt-get install -y mono-devel=6.12\* \
  && rm -rf /var/lib/apt/lists/* /tmp/*

# Install .NET 8 SDK
RUN wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
    && bash dotnet-install.sh --channel 8.0 \
    && rm dotnet-install.sh

# Install PowerShell 7 tarball (non-snap)
RUN wget https://github.com/PowerShell/PowerShell/releases/download/v7.2.8/powershell-7.2.8-linux-x64.tar.gz \
    && mkdir -v -p /opt/microsoft/powershell \
    && tar -xzf powershell-7.2.8-linux-x64.tar.gz -C /opt/microsoft/powershell \
    && rm powershell-7.2.8-linux-x64.tar.gz

ENV DOTNET_ROOT=/root/.dotnet
ENV PATH=$DOTNET_ROOT:$PATH

# Install PythonNet 3.0.5
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pythonnet==3.0.5

ENV PATH=$PATH:/opt/microsoft/powershell
ENV PS_HOME=/opt/microsoft/powershell
ENV PYTHONNET_RUNTIME=coreclr

RUN pwsh -Command "Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted" \
    && pwsh -Command "Install-Module -Name 'VMware.PowerCLI' -Force"

# Copy your Python scripts
WORKDIR /app
COPY src/ /app/

# Default command
# CMD ["python3", "main.py"]
CMD ["python3"]