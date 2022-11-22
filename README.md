# Odds_Endor
Odds_Endor is a project that answers the technical test given by Giskard.

Hope it helps the millenium falcon to destroy the death star ! 

## Installation
The project uses django to implement its front-end, and python 3.7 to run. It was not tested on Windows, only on Linux.

### Anaconda
If you are using Anaconda as your package manager, here is how to install django.
```bash
conda install -c anaconda django
```
If you already have project that uses old version of django it is best to first create a virtual environment, and afterwards to install the latest django version.
```bash
conda create -n yourenvname python=3.7 anaconda
conda activate yourenvname
conda install -c anaconda django
```
### pip
Same as with anaconda, if you already have project that uses old version of django it is best to first create a virtual environment.
To install django with pip, here is the command.
```bash
pip3 install django
```

## Usage
There are two possibilities to get the odds for the millenium falcon : CLI or web page.

### Command Line Interface
To use the CLI, write the following command:
```bash
cd Odds_Endor
python3 get_prob.py file_hunter.json file_mission.json
```
It will return the odds that the ship make it to endor before the death star is launched.

### Web
To launch, the web interface, the following command is needed:
```bash
cd Odds_Endor
python3 manage.py runserver
```
Afterwards, open your browser, and go to http://127.0.0.1:8000/

Follow the instruction on the page in order to get the odds.

