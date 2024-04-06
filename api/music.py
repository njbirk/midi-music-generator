"""REST API for likes."""
import flask
from flask_cors import CORS
import os
from midi_app.main import generate_midi

app = flask.Flask(__name__)
CORS(app)


@app.route('/get-song-file/', methods=['POST'])
def get_midi():

    directory = "../out/"  # Change this to your actual folder path
    try:
        # get song name to use as input to generator + output file name
        song_name = flask.request.args.get("title", default='song', type=str)
        context = request.get_json()

        generate_midi(song_name, [data.get('Speed'),
        data.get('Tone'),
        data.get('Volume'),
        data.get('Instrument'),
        data.get('Repeatability'),
        data.get('Structuredness'),
        ]); 

        @flask.after_this_request
        def remove_file(response):
            try:
                os.remove(os.path.join(directory, f"{song_name}.wav"))
            except Exception as error:
                app.logger.error("Error removing file: %s", error)
            return response

        # Assuming your file creation logic is here and it saves the file in `directory`
        return flask.send_from_directory(directory, f'{song_name}.wav', as_attachment=True)
    except Exception as e:
        return str(e), 404

if __name__ == ('__main__'):
    app.run()
