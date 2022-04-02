from sollutionChallenge import app
from sollutionChallenge.utils.ObjectDetectorOptions import *


if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='localhost', port=5000)
