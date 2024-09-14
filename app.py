from flask import Flask , render_template, Response, stream_with_context
import psutil as ps
import json
from datetime import datetime
import time

app = Flask(__name__)


@app.route('/')
def monitor():
    return render_template('monitor.html')

@app.route('/chart-data')
def chart_data():
    def generate_cpu_data():
        while True:
            file_path = "HardwareMonitoring.hml"
            # Step 1: Open the file in read mode and read all lines
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Step 2: Get the last line
            raw_data = lines[-1] if lines else None
            
            # Step 3: Open the file in write mode to truncate all but the last line
            with open(file_path, 'w') as file:
                if lines:
                    file.writelines(lines[-1])
            
            if not raw_data:
                time.sleep(1)
                continue
            
            data = [d.strip() for d in raw_data.split(',')]
            
            json_data = json.dumps(
                {
                    "frame": data[0],
                    "time": data[1].split(' ')[1],
                    "gpu_temp": data[2],
                    "cpu_temp": data[3],
                    "cpu_power": data[4],
                }
            )
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    response = Response(stream_with_context(generate_cpu_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)