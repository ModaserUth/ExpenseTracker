import uvicorn
from main import app
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8000")

if __name__ == "__main__":
    # تشغيل المتصفح تلقائياً بعد ثانيتين من قيام السيرفر
    Timer(2, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)