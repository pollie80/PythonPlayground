from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

def classify_color(rgb):
    r, g, b = rgb
    if g > b:
        return 'green'
    else:
        return 'blue'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify_color', methods=['POST'])
def color_classify():
    data = request.json
    hex_color = data['hexColor']
    rgb = hex_to_rgb(hex_color)
    result = classify_color(rgb)
    return jsonify({'color': result})

if __name__ == '__main__':
    app.run(debug=True)
