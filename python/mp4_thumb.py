import os
import glob
import cv2

a = glob.glob(r'../media/video/*.mp4')
for x in a:
    name = os.path.join("../media/video/thumb", x[15:-4]);
    name += ".jpg"
    print(name)

    if False == os.path.exists(name):
        vc = cv2.VideoCapture(x)
 
        # get total frame num of mp4 file
        fps = vc.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        # print(fps)
        offset = int(fps * 0.5)
        vc.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, offset)
        # check the file exist
        if vc.isOpened():
            rval , frame = vc.read()
            h, w, x = frame.shape

            width = int(w*200/h)
            print(200, width)            
            # resize image
            frame = cv2.resize(frame, (width, 200), interpolation = cv2.INTER_CUBIC)
            cv2.imwrite(name, frame)
        # close vc
        vc.release     
