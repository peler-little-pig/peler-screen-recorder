import cv2
import time
import os

if __name__ == '__main__':
    my_camera = cv2.VideoCapture(0)
    my_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    my_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    frame_size = (int(my_camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(my_camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frame_fps = 25
    video_format = cv2.VideoWriter_fourcc(*'mpeg')

    video_file_fp = cv2.VideoWriter()
    video_file_fp.open('camera_video.mp4', video_format, frame_fps, frame_size, True)

    start_time = time.time()
    video_time_length = 10
    print('Start to record video')

    while True:
        success, video_frame = my_camera.read()
        video_file_fp.write(video_frame)
        cv2.imshow('frame', video_frame)

        cur_time = time.time()
        if cv2.waitKey(1) & 0xff == 27:  # esc key
            break

    video_file_fp.release()
    my_camera.release()
    cv2.destroyAllWindows()

    mp4_file_size = os.path.getsize('camera_video.mp4')
    print(int(mp4_file_size / 1024), 'KBytes')
