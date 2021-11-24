## Tomato Disease Prediction.

this is a full application with and `api` and `app` that integerates together to allow of uploading an image in order to predict what disease tomato have from it leaves.

you can download the dataset from `kaggle.
com` [Here](https://www.kaggle.com/noulam/tomato)

### Tomato Diseases
- **Bacterial spot**
- **Early blight**
- **Late blight**
- **Leaf Mold**
- **Septoria leaf spot**
- **Spider mites Two-spotted spider mite**
- **Target Spot**
- **Yellow Leaf Curl Virus**
- **mosaic virus**
- **healthy**

The **AI** model and the Image Analysis can be found in the `Jupyter Notebook` found in the repo [Here](./Tomato_Analysis.ipynb)

The last two cells in teh Notebook are for saving a new version of the model and it what will be used in the `api` calls to predict the disease.

### Bundling the Kivy App.
I had provided you with the script that will compile and build the app gor you which it in the `app/buildozer.spec`

Just run this command. which will compile and create a debug version for the app.

```sh
$ cd app/
$ buildozer -v android debug run logcat
```

### Demo and Screenshots
![Screenshot and Demo](./demo/screenshot.png)