import cv2
import telebot
import io

token = 'token'
bot = telebot.TeleBot(token)

if __name__ == "__main__":
    video = cv2.VideoCapture(0)
    success, frame = video.read()

    if success:
        ret, buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(buffer)
        bot.send_photo(chat_id="your_chat_id", photo=io_buf)
    else:
        bot.send_message(chat_id="your_chat_id", text="Не получилось получить фото")

    video.release()
    cv2.destroyAllWindows()
