from flask import Flask, request, jsonify, render_template
from uar import UAR
from fpid import FPID
from pid import PID

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/uar')
def json_example():
    args = request.args

    uar = UAR(
        h_0 = 0,
        h_ex = float(args.get('h', 2)),
        N = 160,
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

@app.route('/pid')
def pid():
    args = request.args

    pid = PID(
        h_0 = 0,
        h_ex = float(args.get('h', 2)),
        N = 6000,
        A = 2.5,
        beta = 0.25,
        Tp = float(args.get('p', 0.05)),
        Td = float(args.get('d', 0.05)),
        Ti = float(args.get('d', 0.75)),
        kp = 1.0,
        Qd_min = 0,
        Qd_max = float(args.get('qd', 2)),
    )
    pid.run()

    return jsonify({
        'n_axis': pid.n_axis,
        'h_axis': pid.h_axis,
        'Qd_axis': pid.valveeQd
    })

@app.route('/fpid')
def fpid():
    args = request.args

    fpid = FPID(
        h_0 = 0,
        h_ex = float(args.get('h', 2)),
        N = 1300,
        A = 2.5,
        beta = 0.25,
        Tp = float(args.get('p', 0.05)),
        Td = float(args.get('d', 0.05)),
        kp = 1.0,
        Qd_min = 0,
        Qd_max = float(args.get('qd', 2)),
    )

    return jsonify({
        'n_axis': fpid.n_axis,
        'h_axis': fpid.pid_y[1],
        'Qd_axis': fpid.pid_y[2]
    })


if __name__ == '__main__':
    app.run(debug=True, port=8080)