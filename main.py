import threading
import asyncio
from tkinter import Tk, Text, Button, Label, Canvas, END
from gui import start_conversation, end_conversation

# GUI Setup
root = Tk()
root.title("Mosaib's Appointment Bot")

Label(root, text="Enter your first message:").pack()
user_input = Text(root, height=20, width=120)
user_input.pack()

start_button = Button(root, text="Start Conversation", command=lambda: start_conversation(user_input, canvas, circle))
start_button.pack()

end_button = Button(root, text="End Conversation", command=end_conversation)
end_button.pack()

canvas = Canvas(root, width=100, height=100)
canvas.pack()
circle = canvas.create_oval(25, 25, 75, 75, fill='red')  # Start with red indicating human speaking

root.mainloop()