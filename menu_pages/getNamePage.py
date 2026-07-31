from menu_utilities.button import Button
from menu_utilities.text import Text
from menu_utilities.text_input_box import TextInputBox
import struct
import time
import network_constants as nc


class GetNamePage:
    def __init__(self, info, socket, host, port):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100)
        self.submit_button = Button("SUBMIT", 600, 330, 150, 100)
        self.name_text = TextInputBox(300, 200, 400, 100)
        self.name_text.change_to_sysfont()
        self.instruction_text = Text("Input your nickname", 300, 150)
        self.name_taken_text = Text("THIS NAME IS ALREADY IN USE", 30, 350)
        self.socket = socket
        self.host = host
        self.port = port

        self.start_timer = 0

    def draw_page(self, screen):
        self.back_button.draw(screen)
        self.instruction_text.draw(screen)
        self.submit_button.draw(screen)
        self.name_text.draw(screen)
        if time.time() - self.start_timer < 5:
            self.name_taken_text.draw(screen)

    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            return "PLAY"
        if self.submit_button.is_clicked(event):
            name = self.name_text.get_text()
            if self.is_name_taken(name):
                self.start_timer = time.time()
            else:
                self.info.name = name
                return "ONLINE_LOBBY"
        self.name_text.handle_event(event)
        return None
    
    def is_name_taken(self, name):
        name = name.encode()
        name_length = len(name)
        message = struct.pack(
            f"BB{name_length}s", nc.VALIDATE_PLAYER_NAME, name_length, name)
        self.socket.sendto(message, (self.host, self.port))
        running = True
        while running:
            msg, _ = self.socket.recvfrom(2048)
            msg_type = int(msg[0])
            if msg_type == nc.NAME_VALIDATION_RESPONSE:
                is_taken = msg[1]
                return is_taken
                    
        return False
