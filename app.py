from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load the Excel file once
data = pd.read_excel("Class-Schedule-Fall 2024-PRINT-Version.xlsx")


# Function to find free rooms based on day, time, floor, and room type
def find_free_rooms(day, time, floor=None, room_type=None):
    occupied = data[(data['Day'] == day) & (data['Start time'] == time)]
    all_rooms = set(data['Room'].unique())
    occupied_rooms = set(occupied['Room'].unique())
    free_rooms = list(all_rooms - occupied_rooms)

    # Filter free rooms based on floor and room type if provided
    if floor:
        free_rooms = [room for room in free_rooms if room.startswith(floor)]
    if room_type:
        room_type_letter = 'C' if room_type == "Classroom" else 'L'
        free_rooms = [room for room in free_rooms if room.endswith(room_type_letter)]

    return free_rooms


# Route to render the main page
@app.route('/')
def home():
    return render_template('index.html')


# Route to check free rooms
@app.route('/check_free_rooms', methods=['POST'])
def check_free_rooms():
    day = request.form.get('day')
    time = request.form.get('time')
    floor = request.form.get('floor')
    room_type = request.form.get('room_type')
    free_rooms = find_free_rooms(day, time, floor, room_type)
    return jsonify({"free_rooms": free_rooms})


if __name__ == '__main__':
    app.run(debug=True)
