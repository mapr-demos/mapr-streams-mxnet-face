from mapr_streams_python import Producer
import numpy as np
import cv2,time
import sys

p = Producer({'streams.producer.default.stream': '/mapr/gcloud.cluster.com/tmp/rawvideostream'})
if len(sys.argv) > 1:
    video_file = str(sys.argv[1])
else:
    print("USAGE: Video file must be specified as a command line argument") 
    exit(1) 
cap = cv2.VideoCapture(video_file)

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

p.flush()
cap.release()
cv2.destroyAllWindows()
