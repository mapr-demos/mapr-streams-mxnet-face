from mapr_streams_python import Producer
import numpy as np
import sys, cv2, time, pickle

def resize(im, target_size, max_size):
    """
    only resize input image to target size and return scale
    :param im: BGR image input by opencv
    :param target_size: one dimensional size (the short side)
    :param max_size: one dimensional max size (the long side)
    :return:
    """
    im_shape = im.shape
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])
    im_scale = float(target_size) / float(im_size_min)
    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)
    im = cv2.resize(im, None, None, fx=im_scale, fy=im_scale, interpolation=cv2.INTER_LINEAR)
    return im, im_scale

p = Producer({'streams.producer.default.stream': '/mapr/gcloud.cluster.com/tmp/rawvideostream'})
if len(sys.argv) > 1:
    fps = float(sys.argv[1])
else:
    print("USAGE: Frames-per-second must be specified as a command line argument")
    exit(1)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

frame_counter = 0
while (cap.isOpened):
    frame_counter += 1
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image, scale = resize(image, 240, 320)
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

