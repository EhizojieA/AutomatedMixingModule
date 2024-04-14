import tensorflow as tf
import numpy as np
from essentia.standard import MonoLoader

# Define the paths to the TensorFlow models
embedding_model_path = "/home/leonscott/PycharmProjects/AutomatedMixingModule/TensorFlowModels/discogs-effnet-bs64-1-savedmodel/effnetdiscogs-bs64-1-savedmodel/saved_model.pb"
classification_model_path = "/home/leonscott/PycharmProjects/AutomatedMixingModule/TensorFlowModels/classification/nsynth_instrument-discogs-effnet-1.pb"

def load_model(model_path):
    return tf.saved_model.load(model_path)

def predict_instrument(audio_file):
    try:
        # Load the audio file
        audio = MonoLoader(filename=audio_file, sampleRate=16000, resampleQuality=4)()

        # Load the embedding model
        embedding_model = load_model(embedding_model_path)
        infer_embedding = embedding_model.signatures["serving_default"]
        embeddings = infer_embedding(tf.constant(audio))['PartitionedCall']

        # Load the classification model
        classification_model = load_model(classification_model_path)
        infer_classification = classification_model.signatures["serving_default"]
        predictions = infer_classification(embeddings)['model_Softmax'][0]

        # Get the index of the predicted instrument
        predicted_instrument_index = np.argmax(predictions)
        return predicted_instrument_index, predictions[predicted_instrument_index]
    except Exception as e:
        print(f"Error processing the file {audio_file}: {e}")
        return None, None

# List of audio files to test
audio_files = [
    "/home/leonscott/PycharmProjects/AutomatedMixingModule/AudioFiles/07_Overheads.wav",
    "/home/leonscott/PycharmProjects/AutomatedMixingModule/AudioFiles/10_BassDI.wav",
    "/home/leonscott/PycharmProjects/AutomatedMixingModule/AudioFiles/11_ElecGtr1.wav",
    "/home/leonscott/PycharmProjects/AutomatedMixingModule/AudioFiles/16_Hammond.wav",
    "/home/leonscott/PycharmProjects/AutomatedMixingModule/AudioFiles/17_LeadVox.wav"
]

# Test each audio file
for idx, audio_file in enumerate(audio_files, start=1):
    print(f"\nTesting Audio File {idx}: {audio_file}")
    instrument_index, confidence = predict_instrument(audio_file)
    if instrument_index is not None:
        print(f"Predicted Instrument Index: {instrument_index}")
        print(f"Confidence: {confidence}")
    else:
        print("Failed to predict instrument.")
