# Odds_Endor
Odds_Endor is a project that answers the technical test given by Giskard.

## Installation
The project uses django to implement its front-end

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
