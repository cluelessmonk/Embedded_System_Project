import cv2
import pygame


import serial
from twilio.rest import Client
def send_sms(account_sid, auth_token, twilio_number, recipient_number, message):
    """
    Send an SMS message using Twilio.

    Parameters:
    - account_sid: Your Twilio account SID.
    - auth_token: Your Twilio authentication token.
    - twilio_number: Your Twilio phone number (sender).
    - recipient_number: The recipient's phone number (receiver).
    - message: The message content to be sent.
    """
    client = Client(account_sid, auth_token)
    
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=recipient_number
        )
        print("Message sent successfully!")
    except Exception as e:
        print("Failed to send message:", e)


def detect_faces_and_send_email(camera_index=0, music_file_visible="./face_visible.mp3", music_file_not_visible="./face_not_visible.mp3"):
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    flag = True
    # Initialize pygame
    pygame.init()

    # Load the music files
    pygame.mixer.init()
    pygame.mixer.music.load(music_file_visible)
    # pygame.mixer.music.set_volume(0.5)  # Adjust volume if needed

    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)

        # Check if face is visible
        if len(faces) > 0:
            # If face is visible, play music_file_visible
            if pygame.mixer.music.get_busy() == 0:
                pygame.mixer.music.load(music_file_visible)
                pygame.mixer.music.play()
                print("Your face is visible!")
                
                # Capture an image
                cv2.imwrite("snapshot.jpg", frame)

                # Send email with the snapshot

                if(flag==True):
                    send_sms(account_sid='abcd', auth_token='abcd', twilio_number='abcd', recipient_number='abcd', message='A person Is Detected In Front of your House')
                flag=False   
 
        else:
            # If face is not visible, play music_file_not_visible
            if pygame.mixer.music.get_busy() == 0:
                pygame.mixer.music.load(music_file_not_visible)
                pygame.mixer.music.play()
                print("Your face is not visible!")

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('Face Detection', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()



# Example usage:
# detect_faces_and_send_email(camera_index=0, music_file_visible="path_to_your_music_file_visible.mp3", music_file_not_visible="path_to_your_music_file_not_visible.mp3", owner_email="your_email@gmail.com", owner_password="your_password", recipient_email="recipient_email@example.com")

# detect_faces_and_play_music(camera_index=0, music_file="path_to_your_music_file.mp3")

# Example usage:
# detect_faces_and_play_music(camera_index=0, music_file="path_to_your_music_file.mp3")


# Define the serial port and baud rate
ser = serial.Serial('COM5', 9600)  # Replace 'COM5' with the appropriate port name

# Read and display serial data
while True:
    # Read a line of serial data
    data = ser.readline().decode().strip()
    dataval=int(data)
    if(dataval<=44):
        detect_faces_and_send_email()
   

    
    # Display the data
   







