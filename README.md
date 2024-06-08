# ImageIdentifier

<b>Obtaining identification in terminal</b> <br>
Run in code editor terminal (i.e. Visual Studio code) using <i>predict_console.py</i> (change the results = model path to your image path) <br>
<br>

<b>Obtaining identification in another application</b> <br>
Make a POST request in another application to http://localhost:5000/identify or http://127.0.0.1:5000/identify to fetch an identification; <i>predict_postRequest.py</i> must be running. To test, run <i>postTest.py</i> in terminal. <br>
~Works with SpeciesTracker-NodeJS<br>
<br>

<b>Training custom dataset</b> <br>
1. Create dataset folder structure (i.e. mushroom_dataset). <br>
2. Optional - run <i>_webcrawler.py</i> to find images to put in train and val folders 
3. Run <i>train.py</i> <br> <br>

<b>References:</b> <br>
https://www.youtube.com/watch?v=aVKGjzAUHz0 <br>
https://github.com/computervisioneng/image-classification-yolov8 <br>
