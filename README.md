# Create GatherTown Poster Session for a Class run in Courseworks

This repo was based on https://github.com/davidaknowles/Mini-Conf/tree/master/gather, thanks to Y-Lan for making that public. 

### Install Node & Dependencies

- Install NodeJS
- ```npm install axios canvas``` to install axios library for NodeJS, and canvas for text generation.
  
### Obtain Credentials for Gather Town API

- Get an API key from Gather Town here:
https://gather.town/apiKeys <br/> 
  (OR iff using SSO with NeurIPS [replace with appropriate domain]  https://neurips.gather.town/apiKeys) 
  
- Replace the placeholder API Key in `config.json`

FYI: [official GatherTown API documentation,](https://www.notion.so/EXTERNAL-Gather-http-API-3bbf6c59325f40aca7ef5ce14c677444)
with their original poster upload example.

### Update Configuration

- Set "EXAMPLE_TO_RUN" to 2 in `config.json`, to build an example poster session.

MAX_TOWN in `config.json` determines how many towns are created (up to 25. Lower will run faster). 

### Get final reports, project groups and video links from Courseworks

These should go in `final project reports` (pdfs), `Project groups.csv` and `video_links` (html files) respectively. 

### Extract poster information

`python3 prep_posters.py`
Then check the extracted pdf titles in `data/posterData.json` are ok. Fix using the hard coding in `prep_posters.py` and try again...

### Run the setup
   
- In a shell, from the folder where this README is, run:
`node run.js`
  
This will create the poster session on Gather Town, with URLs printed out in the terminal. 
This will also create two files:

- `data/outPosterTownUrls.json` containing the base url addresses of the towns being created (the variable part at the end of the Gather Town URL)
- `data/outPosterSpawns.json` containing the list of all posters, with links to spawn right at the poster.

The paths of the files being created can be changed in `config.json`:
```
"POSTER_TOWN_URLS_FNAME": "data/outPosterTownUrls.json"
"POSTER_JSON_FILLED_FNAME": "data/outPosterSpawns.json"

