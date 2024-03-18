## Steps to Run:

1. Download Fluidsynth and the necessary songfont on your machine

2. Create a python virtual environment in the root project directory

3. In the midi_app directory, run `pip install -r requirements.txt`

4. In the api directory, run `pip install Flask`

### Running

- In the root directory, to run the generation, run `python -m midi_app.main`

- To start api on local server, run `python -m api.music`

- To send an api request from the command line, run `curl -X POST http://localhost:5000/get-song-file/`
  - You can add an optional argument to the end of the url to specify a song name

### Running the Webpage

1. Ensure node is installed, then go to react-app directory and run `npm i vite` and `npm install grommet grommet-icons styled-components --save`

2. Then, run `npm run dev` to get a url to the webpage
