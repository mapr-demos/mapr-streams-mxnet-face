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

while (cap.isOpened):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    ret, jpeg = cv2.imencode('.png', image)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    p.produce('topic1', jpeg.tostring(), str(cap.get(cv2.CAP_PROP_POS_MSEC)))
    print("video position: "+str(cap.get(cv2.CAP_PROP_POS_MSEC))+"ms")
    time.sleep(1)

p.flush()
cap.release()
cv2.destroyAllWindows()
