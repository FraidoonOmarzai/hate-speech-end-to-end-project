# Run the below commands in EC2

## 1. Setup Docker and update system
sudo apt-get update
sudo apt-get upgrade -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh



## 2. Add cloud user to docker group
sudo usermod -aG docker ubuntu
sudo usermod -aG docker $USER
newgrp docker



# Start configuration of self-hosted machine
## 3. Download the launch agent binary and verify the checksum
mkdir configurations
cd configurations
curl https://raw.githubusercontent.com/CircleCI-Public/runner-installation-files/main/download-launch-agent.sh > download-launch-agent.sh
export platform=linux/amd64 && sh ./download-launch-agent.sh



## 4. Create the circleci user & working directory
id -u circleci &>/dev/null || sudo adduser --disabled-password --gecos GECOS circleci
sudo mkdir -p /var/opt/circleci
sudo chmod 0750 /var/opt/circleci
sudo chown -R circleci /var/opt/circleci /opt/circleci/circleci-launch-agent



## 5. Create a CircleCI runner configuration
sudo mkdir -p /etc/opt/circleci
sudo touch /etc/opt/circleci/launch-agent-config.yaml
sudo nano /etc/opt/circleci/launch-agent-config.yaml

### 5.1. Add API in the file and change permissions
api:
  auth_token: bad5fd4e15650e9d195e134f47f747b1dc84e57d2be326dff00f1a18c35135c49be7ecef5233de81

runner:
  name: self-hosted
  working_directory: /var/opt/circleci/workdir
  cleanup_working_directory: true


### 5.2 After saving the file, enter the below commands
sudo chown circleci: /etc/opt/circleci/launch-agent-config.yaml
sudo chmod 600 /etc/opt/circleci/launch-agent-config.yaml


## 6 Enable the systemd unit
sudo touch /usr/lib/systemd/system/circleci.service
sudo nano /usr/lib/systemd/system/circleci.service


### 6.1 Put Content in the circleci.service
[Unit]
Description=CircleCI Runner
After=network.target
[Service]
ExecStart=/opt/circleci/circleci-launch-agent --config /etc/opt/circleci/launch-agent-config.yaml
Restart=always
User=circleci
NotifyAccess=exec
TimeoutStopSec=18300
[Install]
WantedBy = multi-user.target

### 6.2 After saving the file, enter the below commands
sudo chown root: /usr/lib/systemd/system/circleci.service
sudo chmod 644 /usr/lib/systemd/system/circleci.service



## 7. Start CircleCI
sudo systemctl enable circleci.service
sudo systemctl start circleci.service



## 8. Add circleci to sudo group
sudo usermod -aG docker circleci
sudo usermod -a -G docker circleci
newgrp docker


### whether running
sudo systemctl status circleci.service



## 9. Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update