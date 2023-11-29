import tensorflow as tf
import streamlit as st
from keras.preprocessing import image
import numpy as np

# Specify the full path to the saved model folder
model_path = 'mobilenet_model'
model = tf.keras.models.load_model(model_path, compile=False)

# Set image dimensions
img_width, img_height = 150, 150

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(img_width, img_height))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize pixel values to [0, 1]
    return img_array

def predict_defect(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)
    return prediction

def main():
    st.title("Metal Surface Defect Prediction App")

    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")
        st.write("Classifying...")

        # Save the uploaded image to a temporary location
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as temp_image:
            temp_image.write(uploaded_file.getvalue())

        # Get predictions
        predictions = predict_defect(temp_image_path)
        defect_classes = ['Crazing', 'Inclusion', 'Patches', 'Pitted', 'Rolled', 'Scratches']
        predicted_class = defect_classes[np.argmax(predictions)]

        st.write("Prediction:")
        st.write(f"The model predicts that the image belongs to class: {predicted_class}")

    st.markdown(
        """
        #### About
        This web app is designed to predict metal surface defects using a pre-trained MobileNetV2 model.
        Upload an image, and the app will classify it into one of the defect classes.
        """
    )

if __name__ == "__main__":
    main()
