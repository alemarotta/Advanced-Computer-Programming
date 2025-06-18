from flask import Flask, request

app = Flask(__name__)


@app.post("/update_history")
def print_to_file():
    

    try:
        body = request.get_json()
        with open("history.txt", "a") as f:
            message_to_print = f"{body['operation']}-{str(body['serial_number'])}\n"
            f.write(message_to_print)

            return "ACK", 200
    except Exception as e:
        return "ERROR", 400


if __name__ == "__main__":
    app.run(debug=True, port=5001)