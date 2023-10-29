# RestBot

## Usage
### How to Install Miniconda

Miniconda is a minimal distribution of the Conda package manager, used for managing Python environments and packages.

Follow these steps to install Miniconda on your system:

1. **Download Miniconda Installer:**
   Go to the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html) and download the installer appropriate for your operating system. Choose the 64-bit version unless you have a specific reason to use the 32-bit version.

2. **Run the Installer:**
   On Linux/macOS, make the installer executable by running the following command in the terminal (replace the filename with the actual filename you downloaded):
   ```sh
   chmod +x Miniconda3-latest-Linux-x86_64.sh
3. **Run The installer**
   ```sh
   ./Miniconda3-latest-Linux-x86_64.sh
4. **Test the Installation:**
   ```sh
   conda --version
5. **Create a New Conda Environment **
   ```sh
   conda create --name myenv python=3.8
6. **Activate the Environment:**
   ```sh
   conda activate myenv
7. Install Packages:
   ```sh
   pip install -r requirements.txt


Modify the files in `data/` or the `domain.yml` file to play around.

### Training the bot
#### Validating the data
Before training the bot, a good practice is to check for any inconsistencies in the stories and rules, though in a project this simple, it's unlikely to occur.
```
$ rasa data validate
```

#### Training
To train the bot, we simply use the rasa train command. We'll provide a name to the model for better organization, but it's not necessary.
```
$ rasa train --config config/config-light-copy.yml --fixed-model-name RestoChatv2
```

#### Testing
To testing the bot, modify testing inside /tests folder
```
$ rasa test
```

### Chatting with the bot
To test your bot, open a new terminal window and start a rasa shell session.
```
$ rasa shell
```
This will let you chat with your bot in your terminal. If you want a more interactive UI and a little more debugging information like what intents were identified and what entities were extracted, you can use Rasa X.

### How to Run Tensorboard/Monitor Result of Training
```
$ tensorboard --logdir .tensorboard
```
This will let you monitor the result training

---
