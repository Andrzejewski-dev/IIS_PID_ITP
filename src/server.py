from flask import Flask, request, jsonify, render_template
from uar import UAR

app = Flask(__name__)

@app.route('/uar')
def json_example():
    # args = request.args
    # args.get('p')

    uar = UAR(
        h_0 = 0,
        h_ex = 2,
        N = 120,
        A = 4,
        beta = 1,
        Tp = 1
    )
    uar.run()

    return jsonify({
        'n_axis': uar.n_axis,
        'h_axis': uar.h_axis,
        'Qd_axis': uar.Qd_axis
    })

@app.route('/')
def homepage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)