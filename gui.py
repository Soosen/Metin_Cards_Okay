import arcade
import pyglet
import math
#fps
UPDATE_RATE = 1/60

#chosen Monitor
MONITOR_NUM = 0
MONITORS = pyglet.canvas.Display().get_screens()
MONITOR = MONITORS[MONITOR_NUM]

class GameWindow(arcade.Window):

    def __init__(self, width, height, title, game):
        super().__init__(width, height, title)
        self.game = game
        self.game.start()
        self.personal_score = self.game.load_personal_score()
        self.width = width
        self.height = height
        self.game_counted = False


    def setup(self):
        #set fps
        self.set_update_rate(UPDATE_RATE)

        #center the window on start
        self.center_on_screen()       

        pass

    def on_draw(self):
        #draw the maze
        self.clear()
        arcade.start_render()
        self.draw_game()
        arcade.finish_render()

    def on_update(self, delta_time):
        
        pass

    def on_key_press(self, key, key_modifiers):

        if key == arcade.key.R:
            if(not self.game_counted):
                self.personal_score["resets"] += 1
                self.game.update_personal_score(self.personal_score)
            self.game = self.game.reset_game()
            self.game_counted = False
        
    def get_card_in_hand_index(self, x, y):
        space_between_cards_x = 50
        space_between_cards_y = 25
        card_width = 50
        card_height = 75
        offset_x = 200 - card_width/2
        offset_y = 385 + card_height

        if(y > offset_y + card_height or y < offset_y):
            return -1

        x_pos_in_cards = (x - offset_x)
        if(x_pos_in_cards % (card_width + space_between_cards_x) > card_width):
            return -1
        else:
            index = math.floor(
                x_pos_in_cards / (card_width + space_between_cards_x))

        if(index > 4):
            return -1

        return index

    def get_card_in_chamber_index(self, x, y):
        space_between_cards_x = 50
        space_between_cards_y = 25
        card_width = 50
        card_height = 75
        offset_x = 300 - card_width/2
        offset_y = 260 + card_height

        if(y > offset_y + card_height or y < offset_y):
            return -1

        x_pos_in_cards = (x - offset_x)
        if(x_pos_in_cards % (card_width + space_between_cards_x) > card_width):
            return -1
        else:
            index = math.floor(
                x_pos_in_cards / (card_width + space_between_cards_x))
        if(index > 2):
            return -1

        return index

    def is_reset_button(self, x, y):
        return x > 13 and x <= 88 and y > 512 and y <= 587

    def on_mouse_press(self, x, y, button, key_modifiers):
        if(self.is_reset_button(x, y)):
            if(not self.game_counted):
                self.personal_score["resets"] += 1
                self.game.update_personal_score(self.personal_score)
            self.game = self.game.reset_game()
            self.game_counted = False
            return
            
        if(len(self.game.hand) - self.game.hand.count(0) == 0):
            return

        #get index of card that has been clicked in the hand pool
        index_hand = self.get_card_in_hand_index(x, y)
        #get index of card that has been clicked in the chamber pool
        index_chamber = self.get_card_in_chamber_index(x, y)

        if(button == arcade.MOUSE_BUTTON_RIGHT):
            #delete a chosen card and save the action in the history
            if(index_hand >= 0 and index_hand < 5):
                if(self.game.hand[index_hand] != 0):
                    saved_state = self.game.state
                    if(self.game.perform_action(index_hand + 1)):
                        self.game.history.append((saved_state, index_hand + 1))
        elif(button == arcade.MOUSE_BUTTON_LEFT):
            #move a card from hand to chamber
            if(index_hand >= 0 and index_hand < 5 and self.game.hand[index_hand] != 0):
                if(-1 in self.game.chamber and index_hand not in self.game.chamber):
                    self.game.chamber[self.game.chamber.index(-1)] = index_hand
                    
            #move a card back from chamber to hand
            elif(index_chamber >= 0 and index_chamber < 3 and self.game.chamber[index_chamber] != -1):
                self.game.chamber[index_chamber] = -1
            
            #if there are three cards in the chamber try to combine them
            if(not -1 in self.game.chamber):
                saved_state = self.game.state
                #if combined save it to the history
                action = self.game.combine_indexes_to_action(self.game.chamber)
                if(self.game.perform_action(action)):
                    self.game.history.append((saved_state, action))
                    self.game.chamber = [-1, -1, -1]

        if(self.game.points >= 400 and not self.game_counted):
            self.game.save_history()
            self.personal_score["wins"] += 1
            self.game.update_personal_score(self.personal_score)
            self.game_counted = True
        
        if(self.game.is_over() and not self.game_counted):
            self.personal_score["loses"] += 1
            self.game.update_personal_score(self.personal_score)
            self.game_counted = True
        pass

    def center_on_screen(self):
        _left = MONITOR.width // 2 - self.width // 2
        _top = (MONITOR.height // 2 - self.height // 2)
        self.set_location(_left, _top)

    def draw_game(self):
        #Draw background image
        texture = arcade.load_texture("Textures/background.jpg")
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width + 20, self.height + 50, texture)

        #Draw cards pool
        offset_x = 50
        offset_y = 60
        space_between_cards_x = 50
        space_between_cards_y = 25
        card_width = 50
        card_height = 75
        for i in range(len(self.game.unused_cards_sorted)):
            card_in_hand = False
            for c in self.game.hand:
                if(c != 0 and self.game.card_to_number(c) == i + 1):
                    card_in_hand = True

            if(self.game.unused_cards_sorted[i] or card_in_hand):
                card = self.game.number_to_card(i)
                texture = arcade.load_texture(f"Textures/{card.color}_{card.number}.png")
                arcade.draw_texture_rectangle(offset_x + (i % 8) * (card_width + space_between_cards_x), offset_y + (math.floor(i / 8) * (card_height + space_between_cards_y)), card_width,
                                              card_height, texture)
            else:
                color = arcade.color.BLUE_GRAY
                arcade.draw_rectangle_filled(offset_x + (i % 8) * (card_width + space_between_cards_x), offset_y + (math.floor(i / 8) * (card_height + space_between_cards_y)), card_width,
                                             card_height, color)
               
                

        #Draw hand
        offset_x = 200
        offset_y = 425
        for i in range(5):
            if(self.game.hand[i] != 0 and i not in self.game.chamber):
                card = self.game.number_to_card(i)
                texture = arcade.load_texture(
                    f"Textures/{self.game.hand[i].color}_{self.game.hand[i].number}.png")
                arcade.draw_texture_rectangle(offset_x + i  * (card_width + space_between_cards_x), offset_y + card_height + space_between_cards_y, card_width,
                                              card_height, texture)
            else:
                color = arcade.color.BLUE_GRAY

                arcade.draw_rectangle_filled(offset_x + i  * (card_width + space_between_cards_x), offset_y + card_height + space_between_cards_y, card_width,
                                         card_height, color)

        #Draw chamber
        offset_x = 300
        offset_y = 300
        for i in range(3):
            if(self.game.chamber[i] != -1):
                texture = arcade.load_texture(
                    f"Textures/{self.game.hand[self.game.chamber[i]].color}_{self.game.hand[self.game.chamber[i]].number}.png")
                arcade.draw_texture_rectangle(offset_x + i * (card_width + space_between_cards_x), offset_y + card_height + space_between_cards_y, card_width,
                                             card_height, texture)
            else:
                color = arcade.color.BLUE_GRAY
                arcade.draw_rectangle_filled(offset_x + i  * (card_width + space_between_cards_x), offset_y + card_height + space_between_cards_y, card_width,
                                         card_height, color)
        
        arcade.draw_text("Points: " + str(self.game.points),
                         640, 315, arcade.color.WHITE, 20, bold=True, font_name="Kenney Blocks Font")

        #Draw Personal Score
        arcade.draw_text("Personal W/L/R: " + f"{self.personal_score['wins']}/{self.personal_score['loses']}/{self.personal_score['resets']}",
                         25, 315, arcade.color.WHITE, 20, bold=True, font_name="Kenney Blocks Font")
        
        #Draw by Soosen
        arcade.draw_text("By Soosen",
                         655, 600, arcade.color.WHITE, 20, bold=True, font_name="Kenney Blocks Font")

        #Draw Reset Button
        texture = arcade.load_texture("Textures/reset.png")
        arcade.draw_texture_rectangle(50, 585, 75, 75, texture)


