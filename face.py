import cv2
import numpy as np
import dlib
from imutils import face_utils 

from head_pose_estimation.pose_estimator import PoseEstimator
from head_pose_estimation.stabilizer import Stabilizer

dlib_model_path = 'head_pose_estimation/assets/shape_predictor_68_face_landmarks.dat'
shape_predictor = dlib.shape_predictor(dlib_model_path)
face_detector = dlib.get_frontal_face_detector()

def get_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    try:
        box = face_detector(gray)[0]
        x1 = box.left()
        y1 = box.top()
        x2 = box.right()
        y2 = box.bottom()
        return [x1, y1, x2, y2]
    except:
        return None

def draw_facebox(image, boxes, box_color=(255, 255, 255)):
    for box in boxes:
        cv2.rectangle(image,(box[0], box[1]),(box[2], box[3]), box_color, 3)

def draw_face_landmarks(image, marks, color=(255, 255, 255)):
    for mark in marks:
        cv2.circle(image, (int(mark[0]), int(mark[1])), 1, color, -1, cv2.LINE_AA)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    _, sample_frame = cap.read()

    pose_estimator = PoseEstimator(img_size=sample_frame.shape[:2])

    # Introduce scalar stabilizers for pose.
    pose_stabilizers = [Stabilizer(
                        state_num=2,
                        measure_num=1,
                        cov_process=0.01,
                        cov_measure=0.1) for _ in range(8)]
    
    while True:
        # capture frame and flip it so it looks like a mirror.
        _, frame = cap.read()
        frame = cv2.flip(frame, 2)

        # do face detection
        facebox = get_face(frame)

        if facebox is not None:
            face = dlib.rectangle(left=facebox[0], top=facebox[1], 
                            right=facebox[2], bottom=facebox[3])
            marks = face_utils.shape_to_np(shape_predictor(frame, face))

            draw_facebox(frame,[facebox],box_color=(0,255,0))   # draw box 
            draw_face_landmarks(frame,marks,color=(0,0,255))   # draw landmarks

            error, r, t = pose_estimator.solve_pose_by_68_points(marks)
            '''
            pose = list(r) + list(t)

            steady_pose = []
            pose_np = np.array(pose).flatten()
            for value, ps_stb in zip(pose_np, pose_stabilizers):
                ps_stb.update([value])
                steady_pose.append(ps_stb.state[0])

            pose_estimator.draw_annotation_box(
                frame, np.expand_dims(steady_pose[:3],0), np.expand_dims(steady_pose[3:6],0), 
                color=(128, 255, 128))
            '''

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # release capture
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()