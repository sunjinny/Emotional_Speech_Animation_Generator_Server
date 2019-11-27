# Emotional Facial Animation Server
This is the part of Emotional Facial Animation module for Flagship project by [Visual Media Lab, KAIST](http://vml.kaist.ac.kr).

## Authors
 - Project Manager: Sunjin Jung (<sunjin225@kaist.ac.kr>)
 - Server codes written by Minjung Jang(<joyful8296@kaist.ac.kr>)


## Tested Environment
 - Ubuntu 18.04.1 LTS on Windows Subsystems for Linux
 - Docker Server 19.03.4 on Docker for Windows


## Quickstart

### Building the Docker image
Clone this repo first. Then run this command on the bash prompt (INCLUDE THE PERIOD AT THE END):
```
$ docker build -t flagship-emotional-facial-animation-server .
```

### Running the server from the Docker image
After building the image, run this command:
```
$ docker run -d -p 3456:5000 flagship-emotional-facial-animation-server
```
Now the server runs on port 3456. Check http://localhost:3456/emotional-facial-animation/interactive by your web browser for assuring everything are working.


## API Specification
All APIs are RESTful.

### Generating Animation Data
 - URI: /emotional-facial-animation/rest/generate-animation
 - Input
   - Method: `post`
   - MIME type: `multpart/form-data`
   - Parameters:
     - `sentence_jaso` (type=`file`, *mandatory*): The `.txt` file that contains the sentence to speech. The encoding of the text should be `utf-8` and should not contain BOM character.
     - `sentence_neural_timing` (type=`file`, *mandatory*): The `.npy` file that contains the neural activation timing matrix of Korean TTS module.
     - `sentence_audio_wav` (type=`file`, *mandatory*): The `.wav` audio file that is made by the Korean TTS module.
     - `speaker_gender` (type=`number`, *mandatory*): The gender of the speeching character. `30001` is the man, `30002` is the woman.
     - `hair_model` (type=`number`, optional): The hair model type of the girl character. `0` is the basic hair, `1` is the hair with a hat.
     - `emotion_strength[10001]` (type=`number`, optional): Emotion strength of *happiness*.
     - `emotion_strength[10002]` (type=`number`, optional): Emotion strength of *anger*.
     - `emotion_strength[10003]` (type=`number`, optional): Emotion strength of *disgust*.
     - `emotion_strength[10004]` (type=`number`, optional): Emotion strength of *fear*.
     - `emotion_strength[10006]` (type=`number`, optional): Emotion strength of *sadness*.
     - `emotion_strength[10007]` (type=`number`, optional): Emotion strength of *surprise*.
 - Output
   - MIME type: `application/xml`
   - Encoding: `utf-8`
   - The content of `.xml` file of the generated animation data will be returned. Save it and pass the content to our Android module part.
