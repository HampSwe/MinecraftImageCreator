import keras_ocr 

pipeline = keras_ocr.pipeline.Pipeline()

images = [
  keras_ocr.tools.read(url) for url in [
      'https://storage.googleapis.com/gcptutorials.com/examples/keras-ocr-img-1.jpg',        
      'https://storage.googleapis.com/gcptutorials.com/examples/keras-ocr-img-2.png'
  ]
]

print(images[0])
print(images[1])

prediction_groups = pipeline.recognize(images)

predicted_image_1 = prediction_groups[0]
for text, box in predicted_image_1:
  print(text)

predicted_image_2 = prediction_groups[1]
for text, box in predicted_image_2:
  print(text)