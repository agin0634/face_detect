import cv2

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

    while True:

        # capture frame
        ret, frame = cap.read()
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # release capture
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":

    main()