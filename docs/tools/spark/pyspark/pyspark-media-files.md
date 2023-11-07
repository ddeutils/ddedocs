# Pyspark Handling Media Files

**Update**: `2023-05-08` |
**Type**: `Use-Cases` |
**Tag**: `Big Data` `Spark` `PySpark` `Binary File`

Pyspark provides several APIs to deal with image, audio, and video files. In this
article we will discuss some ways to handle these files in PySpark.

**Table of Contents**:

- [Basic Features](#basic-features)
- [Additional Features provided by PySpark API](#additional-features-provided-by-pyspark-api)
- [Advantages of Using PySpark](#advantages-of-using-pyspark)

## Basic Features

It just basic ways to handle these files. Depending on the specific use case,
you may need to perform additional operations such as resizing images, extracting
audio features, or processing video frames.

### Image Files

```python
from pyspark.ml.image import ImageSchema
from PIL import Image

# Read image file
image = Image.open("path/to/image.jpg")

# Convert to PySpark DataFrame
df = ImageSchema.readImages("path/to/image.jpg")
```

### Audio Files

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import BinaryType
from pydub import AudioSegment

# Define a UDF to read audio file
@udf(returnType=BinaryType())
def read_audio_file(path):
    audio = AudioSegment.from_file(path)
    return audio.export(format="wav").read()

# Read audio file and convert to PySpark DataFrame
df = (
    spark.read.format("binaryFile")
        .load("path/to/audio.mp3")
        .selectExpr("path", "read_audio_file(content) as audio_data")
)
```

### Video Files

```python
import cv2
from pyspark.sql.functions import udf
from pyspark.sql.types import BinaryType

# Define a UDF to read video file
@udf(returnType=BinaryType())
def read_video_file(path):
    cap = cv2.VideoCapture(path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

# Read video file and convert to PySpark DataFrame
df = (
    spark.read.format("binaryFile")
        .load("path/to/video.mp4")
        .selectExpr("path", "read_video_file(content) as video_data")
)
```

## Additional Features provided by PySpark API

In addition to reading and converting image, audio, and video files to PySpark
DataFrames, there are several other operations that you can perform on these files
in PySpark.

### Image Files

- **Resize images**

```python
from pyspark.ml.image import ImageSchema
from PIL import Image

# Read image file
image = Image.open("path/to/image.jpg")

# Resize image
resized_image = image.resize((224, 224))

# Convert to PySpark DataFrame
df = ImageSchema.readImages("path/to/image.jpg")
```

- **Convert images to different formats**

```python
from pyspark.ml.image import ImageSchema
from PIL import Image

# Read image file
image = Image.open("path/to/image.jpg")

# Convert to PNG format
image.save("path/to/image.png")

# Convert to PySpark DataFrame
df = ImageSchema.readImages("path/to/image.png")
```

- **Extract image features**

```python
from pyspark.ml.image import ImageSchema
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input

# Read image file
df = ImageSchema.readImages("path/to/image.jpg")

# Load pre-trained VGG16 model
model = VGG16(weights="imagenet", include_top=False)

# Preprocess input image
df = df.select("image.origin", preprocess_input("image.data").alias("features"))

# Extract image features
df = model.transform(df)
```

### Audio Files

- **Extract audio features**

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, DoubleType
from pyAudioAnalysis import audioFeatureExtraction

# Define a UDF to extract MFCC features from audio file
@udf(returnType=ArrayType(DoubleType()))
def extract_mfcc_features(audio_data):
    return audioFeatureExtraction.stFeatureExtraction(
        audio_data, 44100, 44100, 0.050*44100, 0.025*44100
    )[0].tolist()

# Read audio file and convert to PySpark DataFrame
df = (
    spark.read.format("binaryFile")
        .load("path/to/audio.wav")
        .selectExpr("path", "content")
)

# Extract MFCC features
df = df.select("path", extract_mfcc_features("content").alias("features"))
```

- **Convert audio files to different formats**

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import BinaryType
from pydub import AudioSegment

# Define a UDF to convert audio file to MP3 format
@udf(returnType=BinaryType())
def convert_to_mp3(audio_data):
    audio = AudioSegment.from_file(audio_data, format="wav")
    return audio.export(format="mp3").read()

# Read audio file and convert to PySpark DataFrame
df = spark.read.format("binaryFile").load("path/to/audio.wav").selectExpr("path", "content")

# Convert to MP3 format
df = df.select("path", convert_to_mp3("content").alias("audio_data"))
```

- **Remove noise from audio files**

  You can use techniques such as bandpass filtering, low-pass filtering, or high-pass
  filtering to remove noise from audio files.

### Video Files

- Extract video frames

```python
import cv2
import numpy as np
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, BinaryType

# Define a UDF to extract video frames from video file
@udf(returnType=ArrayType(BinaryType()))
def extract_video_frames(video_data):
    cap = cv2.VideoCapture(video_data)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.asarray(frame)
        frames.append(frame.tobytes())
    return frames

# Read video file and convert to PySpark DataFrame
df = spark.read.format("binaryFile").load("path/to/video.mp4").selectExpr("path", "content")

# Extract video frames
df = df.select("path", extract_video_frames("content").alias("frames"))
```

- Apply video filters

```python
import cv2
import numpy as np
from pyspark.sql.functions import udf
from pyspark.sql.types import BinaryType
from PIL import Image, ImageFilter

# Define a UDF to apply a Gaussian blur filter to video frames
@udf(returnType=BinaryType())
def apply_gaussian_blur(frame_data):
    # Convert bytes to NumPy array
    frame = np.frombuffer(frame_data, dtype=np.uint8).reshape((480, 640, 3))

    # Apply Gaussian blur filter
    img = Image.fromarray(frame)
    img = img.filter(ImageFilter.GaussianBlur(radius=5))
    frame = np.asarray(img)

    # Convert back to bytes
    return frame.tobytes()

# Read video file and convert to PySpark DataFrame
df = spark.read.format("binaryFile").load("path/to/video.mp4").selectExpr("path", "content")

# Apply Gaussian blur filter to video frames
df = df.select("path", apply_gaussian_blur("content").alias("frame_data"))
```

- Perform object detection

```python
import cv2
import numpy as np
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, BinaryType
from tensorflow.keras.models import load_model

# Load pre-trained object detection model
model = load_model("path/to/object_detection_model.h5")

# Define a UDF to perform object detection on video frames
@udf(returnType=ArrayType(BinaryType()))
def perform_object_detection(frame_data):
    # Convert bytes to NumPy array
    frame = np.frombuffer(frame_data, dtype=np.uint8).reshape((480, 640, 3))

    # Perform object detection
    detections = model.detect(frame)

    # Draw bounding boxes on the frame
    for detection in detections:
        x, y, w, h = detection["box"]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Convert back to bytes
    return frame.tobytes()

# Read video file and convert to PySpark DataFrame
df = spark.read.format("binaryFile").load("path/to/video.mp4").selectExpr("path", "content")

# Perform object detection on video frames
df = df.select("path", perform_object_detection("content").alias("frame_data"))
```

## Advantages of Using PySpark

Here are some advantages of using PySpark for processing image, audio, and video files:

- **Scalability**:
  PySpark is designed for distributed computing, which means that it can process
  large files and datasets much faster than traditional computing frameworks.
  This makes it an ideal choice for processing image, audio, and video files,
  which can be very large.

- **Performance**:
  PySpark is highly optimized for data processing, which means that it can perform
  complex operations on large datasets very quickly. This is especially important
  when working with image, audio, and video files, which often require computationally
  intensive operations like feature extraction and object detection.

- **Integration with other tools**:
  PySpark integrates with many popular data processing and machine learning tools,
  like TensorFlow, Keras, and OpenCV. This makes it easy to incorporate these tools
  into your data processing pipeline, and to leverage their capabilities for tasks
  like image classification, object detection, and speech recognition.

- **Flexible data sources**:
  PySpark can read data from a wide range of sources, including local files, distributed
  file systems like Hadoop Distributed File System (HDFS), and cloud storage platforms
  like Amazon S3 and Google Cloud Storage. This makes it easy to process image,
  audio, and video files regardless of where they are stored.

- **Unified API**:
  PySpark provides a unified API for processing different types of data, including
  image, audio, and video files. This means that you can use the same set of APIs
  and functions to process all of these different file types, which can simplify
  your code and reduce development time.

- **Fault tolerance**:
  PySpark is designed to be fault-tolerant, which means that it can recover from
  failures and continue processing data even if some nodes fail. This is especially
  important when processing large datasets, as the likelihood of a node failure
  increases with the size of the dataset.

- **Cost-effective**:
  PySpark is open-source and can be run on commodity hardware, which makes it a
  cost-effective option for processing image, audio, and video files. Additionally,
  PySpark can be run on cloud-based infrastructure, which allows you to scale your
  processing resources up or down as needed, and to pay only for what you use.

## References

- https://blog.devgenius.io/handling-media-files-in-pyspark-image-audio-video-files-8e3bcd7a5c4e
