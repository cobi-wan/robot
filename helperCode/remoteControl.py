import paho.mqtt.client as mqtt
import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent, client):
        tk.Frame.__init__(self, parent, width=400,  height=400)

        self.label = tk.Label(self, text="last key pressed:  ", width=20)
        self.label.pack(fill="both", padx=100, pady=100)

        self.label.bind("<w>", self.on_w)
        self.label.bind("<a>", self.on_a)
        self.label.bind("<s>", self.on_s)
        self.label.bind("<d>", self.on_d)

        # give keyboard focus to the label by default, and wheneverawd
        # the user clicks on it
        self.label.focus_set()
        self.label.bind("<1>", lambda event: self.label.focus_set())
        self.client = client

    # def on_wasd(self, event):
    #     self.label.configure(text="last key pressed: " + event.keysym);
    
    def on_w(self, event):
        self.label.configure(text="last key pressed: " + event.keysym);
        self.client.publish("Control", payload="Fwd", qos=1)

    def on_s(self, event):
        self.label.configure(text="last key pressed: " + event.keysym);
        self.client.publish("Control", payload="Bck", qos=1)

    def on_a(self, event):
        self.label.configure(text="last key pressed: " + event.keysym);
        self.client.publish("Control", payload="Lft", qos=1)
    
    def on_d(self, event):
        self.label.configure(text="last key pressed: " + event.keysym);
        self.client.publish("Control", payload="Rgt", qos=1)
        



if __name__ == "__main__":
    root = tk.Tk()
    client = mqtt.Client("RemoteControl")
    client.connect("192.168.20.68", 1883)

    Example(root, client).pack(fill="both", expand=True)
    root.mainloop()

    