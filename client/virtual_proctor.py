import cv2
import temphead as th
import tempeye as te
import module as m
import time
import datetime
import easygui
import threading
import pyaudio
import wave
import keyboard
from ultralytics import YOLO
import cvzone
import pandas as pd
import speech_recognition as sr
from pydub import AudioSegment
import socket,pickle,struct
import pyshine as ps 
import imutils


model = YOLO('yolov8s.pt')

def read_classes_from_file(file_path):
    with open(file_path, 'r') as file:
        classes = [line.strip() for line in file]
    return classes
class_list = read_classes_from_file('coco.txt')

def convert_audio_to_text(audio_file):
    audio = AudioSegment.from_wav(audio_file)
    audio.export("temp.wav", format="wav")
    r = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language="ar")  # يمكنك تغيير اللهجة حسب احتياجاتك
    return text


def show_message1():
       easygui.msgbox("Don't move your head or your eyes",title="")
      
def show_message_thread1():
    t=threading.Thread(target=show_message1)
    t.start()
  
def show_message2():
       easygui.msgbox("Don't use a cell phone",title="")
def show_message_thread2():
    t=threading.Thread(target=show_message2)
    t.start()
def show_message3():
       easygui.msgbox("Don't use a book",title="")
def show_message_thread3():
    t=threading.Thread(target=show_message3)
    t.start()
   
def convert_seconds(seconds):
    seconds=int(seconds)
    minutes=seconds//60
    hours=minutes//60
    remaining_minutes=minutes%60
    remaining_seconds=seconds%60
    hours=int(hours)
    remaining_minutes=int(remaining_minutes)
    remaining_seconds=int(remaining_seconds)
    s=str(hours)+":"+str(remaining_minutes)+":"+str(remaining_seconds)
    return s
def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

audio_format = pyaudio.paInt16
channels = 1
sample_rate = 44100
chunk_size = 1024
record_seconds = 1000 # عدد الثواني المراد تسجيلها

frames_list = []
audio = pyaudio.PyAudio()
stream = audio.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)


# دالة لتسجيل الصوت
def record_audio():
    global frames_list

    frames_list = []
    record_frames = int(sample_rate / chunk_size * record_seconds)

    while True:
        audio_data = stream.read(chunk_size)
        frames_list.append(audio_data)
        if len(frames_list) >= record_frames or keyboard.is_pressed('q'):
            break
    

def record_video():
    global note
    note=""
    count=0
    last_text=new_text="Forward"
    check=0
    check_phone=0
    check_left=0
    threshold=5
    check_right=0
    last_text_left=new_text_left="Center"
    last_text_right=new_text_right="Center"
    check1=0
    pos=""
    leftPos=""
    phone=0
    start_time=0
    end_time=0
    start_time_phone=0
    end_time_phone=0
    start_time_phone1=0
    start_time_left=0
    end_time_left=0
    start_time_right=0
    end_time_right=0
    show_message_phone=0
    show_message_book=0
    new_phone_found_time=0
    last_phone_found_time=0
    new_book_found_time=0
    last_book_found_time=0
    check_person=0
    start_time_person=0
    end_time_person=0
    time_person=0
    last_person_count_time=0
    new_person_count_time=0
    phone_found="No"
    book_found="No"
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28'
    port = 9999
    client_socket.connect((host_ip,port))
    
    if client_socket:
        procrss_type="view_client"
        client_socket.sendall(procrss_type.encode())
        video = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        output_file = "output_video.avi"
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        output_video = cv2.VideoWriter(output_file, fourcc, 2.0, (frame_width, frame_height))
        start_timer=datetime.datetime.now()
        while video.isOpened():
            success, frame = video.read()
            if success == False:
                break

            move_head=0
            move_right_eye=0
            move_left_eye=0
            
            frame,text=th.headPos(frame)
            frame,pos,leftPos,person_count=te.eyePos(frame)
            results = model.predict(frame)
            elapsed_time=(datetime.datetime.now()-start_timer).seconds
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")
            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]
                #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                #cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)
                if c=="cell phone":
                    phone_found="Yes"
                    if show_message_phone==0:
                        show_message_phone=1
                        show_message_thread2()
                    new_phone_found_time=elapsed_time
                    if (new_phone_found_time-last_phone_found_time)>=10 or last_phone_found_time==0:
                        note+="Detect a phone at time "+convert_seconds(elapsed_time)+"\n"
                        print("Detect a phone at time"+convert_seconds(elapsed_time))
                    last_phone_found_time=new_phone_found_time
                else:
                    phone_found="No"
                if c=="book":
                    book_found="Yes"
                    if show_message_book==0:
                        show_message_book=1
                        show_message_thread3()
                    new_book_found_time=elapsed_time
                    if (new_book_found_time-last_book_found_time)>=10 or last_book_found_time==0:
                        note+="Detect a book at time "+convert_seconds(elapsed_time)+"\n"
                        print("Detect a book at time"+convert_seconds(elapsed_time))
                    last_book_found_time=new_book_found_time
                else:
                    book_found="No"
            
            if person_count>1:
                new_person_count_time=elapsed_time
                if(new_person_count_time-last_person_count_time)>=10 or last_person_count_time==0:
                    print("Detect moer than one person for "+str(time_person)+" from "+convert_seconds(start_time_person)+" to "+convert_seconds(end_time_person))
                    note+="Detect moer than one person for "+str(time_person)+" from "+convert_seconds(start_time_person)+" to "+convert_seconds(end_time_person)+"\n"
                last_person_count_time=new_person_count_time       
            new_text=text
            if new_text!="Forward":
                if check==0:
                    check=1
                    start_time=elapsed_time
                if last_text==new_text:
                    end_time=elapsed_time
            if last_text != new_text and last_text !="Forward" and last_text!="":
                time=end_time-start_time
                check=0
        
                if time>=threshold:  
                    print("the student is "+last_text+" for "+str(time)+" second "+"from "+convert_seconds(start_time)+" to "+convert_seconds(end_time))
                    note+="the student is "+last_text+" for "+str(time)+" second "+"from "+convert_seconds(start_time)+" to "+convert_seconds(end_time)+"\n"  
            
                    move_head=1
            if last_text != new_text and last_text=="":
                time=end_time-start_time
                check=0
                if time>=threshold:  
                    print("can't detected poes"+" for "+str(time)+" second "+"from "+convert_seconds(start_time)+" to "+convert_seconds(end_time))
                    note+="can't detected poes"+" for "+str(time)+" second "+"from "+convert_seconds(start_time)+" to "+convert_seconds(end_time)+"\n"
                
            last_text=new_text

            new_text_right=pos


            if new_text_right!="Center":
                if check_right==0:
                    check_right=1
                    start_time_right=elapsed_time
                    
                if last_text_right==new_text_right:
                    end_time_right=elapsed_time
                    
            if last_text_right != new_text_right and last_text_right!='Center' and last_text_right!="":
                time_right=end_time_right-start_time_right
                check_right=0
                if time_right>=threshold:
                    print("the student is "+last_text_right+" for "+str(time_right)+" second "+"from "+convert_seconds(start_time_right)+" to "+convert_seconds(end_time_right)+" in his right eye")
                    move_right_eye=1
                    note+="the student is "+last_text_right+" for "+str(time_right)+" second "+"from "+convert_seconds(start_time_right)+" to "+convert_seconds(end_time_right)+" in his right eye"+"\n"
            if last_text_right != new_text_right and last_text_right !="Center" and last_text_right=="":
                time_right=end_time_right-start_time_right
                check_right=0
                if time_right>=threshold:
                    print("can't detecte eye pos"+ "for "+str(time_right)+" second "+"from "+convert_seconds(start_time_right)+" to "+convert_seconds(end_time_right)+" in his right eye")
                    note+="can't detecte eye pos"+" for "+str(time_right)+" second "+"from "+convert_seconds(start_time_right)+" to "+convert_seconds(end_time_right)+" in his right eye"+"\n"
            
            last_text_right=new_text_right

            new_text_left=leftPos
        
            if new_text_left!="Center":
                if check_left==0:
                    check_left=1
                    start_time_left=elapsed_time
                
                if last_text_left==new_text_left:
                    end_time_left=elapsed_time
                    
            if last_text_left != new_text_left and last_text_left!='Center' and last_text_left!="":
                time_left=end_time_left-start_time_left
                check_left=0
                if time_left>=threshold:
                    print("the student is "+last_text_left+" for "+str(time_left)+" second "+"from "+convert_seconds(start_time_left)+" to "+convert_seconds(end_time_left)+" in his left eye")
                    note+="the student is "+last_text_left+" for "+str(time_left)+" second "+"from "+convert_seconds(start_time_left)+" to "+convert_seconds(end_time_left)+" in his left eye"+"\n"
            if last_text_left != new_text_left and last_text_left !="Center" and last_text_left=="":
                time_left=end_time_left-start_time_left
                check_left=0
                if time_left>=threshold:
                    print("can't detecte eye pos"+ "for "+str(time_left)+" second "+"from "+convert_seconds(start_time_left)+" to "+convert_seconds(end_time_left)+" in his left eye")
                    note+="can't detecte eye pos"+" for "+str(time_left)+" second "+"from "+convert_seconds(start_time_left)+" to "+convert_seconds(end_time_left)+" in his left eye"+"\n"
            
            last_text_left=new_text_left
            if move_head==1 or move_right_eye==1 or move_left_eye==1:
                count=count+1
            if move_head==1 or move_right_eye==1 or move_left_eye==1:
                if count<=3:
                    show_message_thread1()
            
            output_video.write(frame)
            cv2.putText(frame, "head:"+text, (10, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(frame, "right eye:"+pos, (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(frame, "left eye:"+leftPos, (10, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(frame, "Number of person:"+str(person_count), (10, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(frame, "Detecte cell phone:"+phone_found, (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(frame, "Detecte book:"+book_found, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            frame = imutils.resize(frame,width=500)
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            

            cv2.imshow('Frame',frame )
            
        
            key = cv2.waitKey(1)
            
            # إيقاف الكاميرا بالضغط على حرف "q"
            if key == ord('q'):
                break
        if count>3:
            print("this student is a cheater")
            note+="this student is a cheater"+"\n"
        else:
            print("this student is not a cheater")
            note+="this student is not a cheater"+"\n"
        
        cv2.destroyAllWindows()
        video.release()
        client_socket.close()  

def start_exam():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28'
    port = 9999
    client_socket.connect((host_ip,port))
   
    audio_thread = threading.Thread(target=record_audio)
    video_thread = threading.Thread(target=record_video)
    audio_thread.start()
    video_thread.start()
    audio_thread.join()
    video_thread.join()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wave_output_file = "output_audio1.wav"
    wf = wave.open(wave_output_file, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(audio_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames_list))
    wf.close()
    audio_text=""
    r = sr.Recognizer()
    with sr.AudioFile(wave_output_file) as src:
        audio_d = r.record(src)
        try:
            audio_text= r.recognize_google(audio_d, language='ar-AR')
            print(audio_text)
        except sr.UnknownValueError as u:
            print(u)
        except sr.RequestError as r:
            print(r)
    print(audio_text)
    file_path = 'note.txt'     # تحديد مسار الملف النص
    write_to_file(file_path,note)
    if client_socket:
            procrss_type="send_notes"
            client_socket.sendall(procrss_type.encode())
            data_size=struct.pack('!I',len(note))
            client_socket.send(data_size)
            client_socket.send(note.encode('utf-8'))
            print(note)
            data_size=struct.pack('!I',len(audio_text)) 
            client_socket.send(data_size)
            client_socket.send(audio_text.encode('utf-16'))
            print(audio_text)
            print("تم ارسال البيانات بنجاح") 
    client_socket.close()
