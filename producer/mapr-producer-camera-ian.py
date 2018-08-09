from mapr_streams_python import Producer
import numpy as np
import sys, cv2, time, pickle

p = Producer({'streams.producer.default.stream': '/mapr/gcloud.cluster.com/tmp/rawvideostream'})
if len(sys.argv) > 1:
    fps = float(sys.argv[1])
else:
    print("USAGE: Frames-per-second must be specified as a command line argument")
    exit(1)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,360)

frame_counter = 0
while (cap.isOpened):
    frame_counter += 1
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    ret, jpeg = cv2.imencode('.png', image)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    p.produce('topic1', jpeg.tostring(), str(frame_counter))
    print("frame: "+str(frame_counter))
    time.sleep(1/fps)

p.flush()
cap.release()
cv2.destroyAllWindows()
