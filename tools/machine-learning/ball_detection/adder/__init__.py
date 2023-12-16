import copy
import imghdr
import json
import struct
import click
import cv2
import flask
import numpy as np
import image as img

app = flask.Flask(__name__, static_folder='static',
                  static_url_path='/adder/static')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/config.json')
def config_json():
    return flask.jsonify({
        'gridImageSize': app.config['arguments']['grid_image_size'],
        'existingAnnotationColor': app.config['arguments']['existing_annotation_color'],
        'addedAnnotationColor': app.config['arguments']['added_annotation_color'],
    })


@app.route('/existing-annotations.json')
def existing_annotations_json():
    return flask.jsonify(app.config['existing_annotations'])


@app.route('/added-annotations.json')
def added_annotations_json():
    return flask.jsonify(app.config['added_annotations'])


@app.route('/image_size/<int:index>')
def image_size(index):
    if index < 0:
        return flask.make_response('index cannot be negative', 404)
    if index >= len(app.config['existing_annotations'].keys()):
        return flask.make_response('index cannot be larger than amount of paths', 404)

    image = sorted(app.config['existing_annotations'].keys())[index]

    width, height = img.size(image)

    return flask.jsonify({
        'width': width,
        'height': height,
    })


@app.route('/image/<int:index>')
def image(index):
    if index < 0:
        return flask.make_response('index cannot be negative', 404)
    if index >= len(app.config['existing_annotations'].keys()):
        return flask.make_response('index cannot be larger than amount of images', 404)

    image = sorted(app.config['existing_annotations'].keys())[index]

    image = img.read(image)
    image = img.convert_color_space(
        image,
        source_color_space=app.config['arguments']['color_space'],
        target_color_space='RGB',
    )

    if 'crop' in flask.request.args:
        try:
            center_x = float(flask.request.args['centerX'])
            center_y = float(flask.request.args['centerY'])
            radius = float(flask.request.args['radius'])
        except (KeyError, ValueError):
            return flask.make_response('centerX, centerY, or radius missing or malformed', 404)

        upper_left = np.array([[center_x - radius],
                               [center_y - radius]])
        lower_right = np.array([[center_x + radius],
                                [center_y + radius]])

        image = img.crop(
            image,
            upper_left,
            lower_right,
            [
                app.config['arguments']['default_gray'],
                app.config['arguments']['default_gray'],
                app.config['arguments']['default_gray'],
            ],
        )

    if 'scale' in flask.request.args:
        try:
            scale_width = int(
                flask.request.args['width']) if 'width' in flask.request.args else None
            scale_height = int(
                flask.request.args['height']) if 'height' in flask.request.args else None
        except ValueError:
            return flask.make_response('width or height malformed', 404)

        if scale_width is None and scale_height is None:
            return flask.make_response('width and height missing', 404)

        if scale_width is None:
            scale_width = int(scale_height / image.shape[0] * image.shape[1])
        if scale_height is None:
            scale_height = int(scale_width / image.shape[1] * image.shape[0])

        size = np.array([[scale_width],
                         [scale_height]])

        image = img.resize(image, size)

    response = flask.make_response(img.encode(image, 'png'))
    response.headers['Content-Type'] = 'image/png'
    return response


def write_output_annotation_files():
    with open(app.config['arguments']['output_annotations_file'], 'w') as f:
        json.dump(app.config['added_annotations'], f, sort_keys=True, indent=4)
        f.write('\n')


@app.route('/set_added/<int:index>', methods=['POST'])
def set_added(index):
    if index < 0:
        return flask.make_response('index cannot be negative', 404)
    if index >= len(app.config['added_annotations'].keys()):
        return flask.make_response('index cannot be larger than amount of images', 404)

    image = sorted(app.config['added_annotations'].keys())[index]

    # set added circles
    app.config['added_annotations'][image] = flask.request.json

    write_output_annotation_files()

    return flask.jsonify({'ok': True})


@app.route('/telemetry/<string:id>', methods=['POST'])
def telemetry(id):
    if not id.isalnum():
        return flask.make_response('Malformed ID', 400)
    with open(f'{app.config["arguments"]["output_annotations_file"]}.{id}.telemetry', 'a') as f:
        for message in flask.request.json:
            json.dump(message, f)
            f.write('\n')

    return flask.make_response('Ok', 200)


@click.command()
@click.option('--debug', is_flag=True, help='Run server in debug/development mode which enables hot reloading of the application')
@click.option('--host', default='localhost', help='Hostname to listen on, set this to \'0.0.0.0\' to have the server available externally as well', show_default=True)
@click.option('--port', default=5000, help='Port of the webserver', show_default=True)
@click.option('--crop-scale-factor', default=1.5, help='Scale factor when cropping annotations', show_default=True)
@click.option('--color-space', type=click.Choice(['YCbCr', 'RGB', 'Grayscale'], case_sensitive=False), default='YCbCr', help='Color space of raw images', show_default=True)
@click.option('--grid-image-size', default=200, help='Size of scaled images in grid', show_default=True)
@click.option('--existing-annotation-color', default=(0, 0, 0), help='Color of existing annotations (three uint8 color components in [0,255] in RGB)', show_default=True)
@click.option('--added-annotation-color', default=(0, 255, 0), help='Color of added annotations by this tool (three uint8 color components in [0,255] in RGB)', show_default=True)
@click.argument('input_annotations_file', type=click.File('r'))
@click.argument('output_annotations_file', type=click.Path(dir_okay=False))
def server(*args, **kwargs):
    app.config['arguments'] = kwargs
    app.config['existing_annotations'] = json.load(
        app.config['arguments']['input_annotations_file'])

    try:
        with open(app.config['arguments']['output_annotations_file']) as f:
            app.config['added_annotations'] = json.load(f)
    except FileNotFoundError:
        # allow missing output file
        app.config['added_annotations'] = copy.deepcopy(
            app.config['existing_annotations'])

    write_output_annotation_files()

    app.run(debug=app.config['arguments']['debug'], host=app.config['arguments']
            ['host'], port=app.config['arguments']['port'])
