import time

fps = 0
frame_time = 9999
last_time = 0
text = "0 FPS (9999 ms)"

def update():
    global fps, frame_time, last_time, text

    curr_time = time.time() * 1000
    dt = curr_time - last_time
    last_time = curr_time

    frame_time = round(dt, 2)
    fps = round(1000 / dt, 2)
    text = f"{fps} FPS ({frame_time} ms)"