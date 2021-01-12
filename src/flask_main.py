import time, os, shutil, numpy as np, tensorflow as tf
from flask import Flask, render_template, Response, jsonify, request 
from cv2 import cv2
from time import gmtime, strftime
from werkzeug.http import HTTP_STATUS_CODES
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from db_model import db, app, Item
from sqlalchemy import func, create_engine

# Global variables
# Initialize db
db.create_all()
engine = create_engine('sqlite:///../db/items.db')

# Load model
MODEL = load_model(filepath='./current.h5')

# Open webcam
WEBCAM = cv2.VideoCapture(0)

# Image height and width
IMG_HEIGHT, IMG_WIDTH = 256, 256

def gen_images():
    """
        Constantly read webcam video feed frame image
    """
    while True:    
        _, frame = WEBCAM.read()    
        frame = cv2.resize(frame, (1280,720))
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def check_item(item):
    """
        Check if item is in DB
    """
    with engine.connect() as con:
        query = con.execute("""SELECT * from ITEM Where item_type = ?""", item)
        res = query.fetchall()
    return res

@app.route('/')
def index():
    """
        Renders default page for index in Flask
    """
    return render_template('index.html')

@app.route('/webcam')
def display_webcam():
    """
        Load webcam frame image to html
    """
    return Response(gen_images(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_screenshot')
def take_screenshot():
    """
        Saves the current image displayed by the webcam

        Returns

    """
    # Read webcam feed
    _, frame = WEBCAM.read()  
    # Format image size
    img = cv2.resize(frame, (IMG_HEIGHT, IMG_WIDTH))
    # Save image
    img_name = f'../data/{strftime("%Y-%m-%d-%H-%M-%S", gmtime())}-image.jpg'
    cv2.imwrite(img_name, img)
    # Define return message
    payload = {'status': HTTP_STATUS_CODES.get(200, 'success')}
    payload['result'] = f'{img_name}'
    return jsonify(payload)

@app.route('/make_prediction', methods=['POST'])
def make_prediction():
    """
        Calls model to perform a prediction using the current image displayed by the webcam

        Returns

    """
    # Define class names
    class_names = ['body', 'conditioner', 'cotton', 'facial', 'sebum', 'serum', 'shampoo', 'toner']
    # Grab image name from post request
    img_name = request.form['img_name']
    # Process image for prediction    
    img = keras.preprocessing.image.load_img(path=img_name, 
                                            color_mode='rgb',
                                            target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_arr = keras.preprocessing.image.img_to_array(img)
    img_arr = tf.expand_dims(img_arr, 0)
    # Make prediction
    pred = MODEL.predict(img_arr)
    # Format prediction to return predicted class
    scores = tf.nn.softmax(pred[0])
    pred_class = np.argmax(scores)
    predicted = class_names[pred_class]
    return jsonify({'result':predicted})

@app.route('/add_to_db', methods=['POST'])
def add_to_db():
    """
        Add predicted item (Increases count by 1) to the DB

        Returns

    """
    item = request.form['item']
    num_items = request.form['number']

    with engine.connect() as con:
        if check_item(item):
            con.execute("""UPDATE Item SET num_items = Item.num_items + ? WHERE Item.item_type = ?""", num_items, item)
        else:
            con.execute("""INSERT INTO Item (item_type, num_items) VALUES (?, ?)""", item, num_items)

    # data = Item(item_type=item, num_items=num_items)
    # db.session.add(data)
    # db.session.commit()
    return jsonify({'result':f'{item} added successfully'})

@app.route('/remove_from_db', methods=['POST'])
def remove_from_db():
    """
        Removes predicted item (Decreases count by 1) from the DB

        Returns
    """
    item = request.form['item']

    with engine.connect() as con:
        if check_item(item):
            con.execute("""UPDATE Item SET num_items = Item.num_items - 1 WHERE Item.item_type = ?""", item)
    return jsonify({'result':f'{item} removed successfully'})

@app.route('/check_stock', methods=['GET'])
def check_stock():
    """
        Checks current stock amount of items in the DB

        Returns
    """
    result = []

    with engine.connect() as con:
        query = con.execute("""SELECT * FROM Item""")
        res = query.fetchall()

    for item in res:
        result.append({'item_type':item[1], 'number':item[2]})
    return jsonify({'result':result})

@app.route('/delete_file', methods=['POST'])
def delete_file():
    """
        Deletes saved image file
    """
    file_name = request.form['img_name']
    os.remove(file_name)
    return jsonify({'result':f'{file_name} deleted from folder'})

@app.route('/wrong_predictions', methods=['POST'])
def wrong_predictions():
    """
        Saves image file of wrongly predicted item
    """
    file_path = request.form['img_name']
    file_name = file_path.split('/')[-1]
    destination = os.path.join('../wrong_predictions', file_name)
    shutil.move(src=file_path, dst=destination)
    return jsonify({'result':f'{file_name} saved to wrong predictions folder'})

@app.route('/bulk_screenshots', methods=['POST'])
def bulk_screenshots():
    """
        Saves multiple iamge file
    """
    number = request.form['number']    
    for i in range(int(number)):
        take_screenshot()
        print(f'Screenshot {i+1} taken')
        time.sleep(1)
    return jsonify({'result':'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False)