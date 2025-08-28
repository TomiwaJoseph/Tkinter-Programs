from game_card import Card


class Logic:
    SUIT_TYPE = None
    TABLEAU_LISTS = []
    STOCK_PILE_LISTS = []
    STOCK_PILE_CARDS = []
    FOUNDATION_POSITION = [(60, 70), (80, 70), (100, 70),
                           (120, 70), (140, 70), (160, 70), (180, 70), (200, 70)]
    FOUNDATION_COUNT = 0
    CURRENT_BACKDROP_THEME = "Default"
    CURRENT_CARD_THEME = "Default"
    STACK_STARTING_POSITIONS = {'stack_1': (60, 180), 'stack_2': (130, 180), 'stack_3': (200, 180), 'stack_4': (270, 180), 'stack_5': (
        340, 180), 'stack_6': (410, 180), 'stack_7': (480, 180), 'stack_8': (550, 180), 'stack_9': (620, 180), 'stack_10': (690, 180)}
    STACK_COORDS = {"stack_1": [0, 100], "stack_2": [100, 170], "stack_3": [170, 240], "stack_4": [240, 310], "stack_5": [
        310, 380], "stack_6": [380, 450], "stack_7": [450, 520], "stack_8": [520, 590], "stack_9": [590, 660], "stack_10": [660, 730]}
    suit_dict = {1: "ace", 13: "king", 12: "queen", 11: "jack"}
    TABLEAU_CARDS = {}
    COVERED_CARDS_REMAINING = 5
    MOVES_COUNT = 0
    dragging = False
    start_x = None
    start_y = None
    animation_is_done = True
    shrink_speed = 5
    temp_current_theme = None
    cards_moved = []
    move_parameters = {}

    def reset_all_variables():
        Logic.TABLEAU_LISTS = []
        Logic.STOCK_PILE_LISTS = []
        Logic.STOCK_PILE_CARDS = []
        Logic.FOUNDATION_COUNT = 0
        Logic.TABLEAU_CARDS = {}
        Logic.COVERED_CARDS_REMAINING = 5
        Logic.MOVES_COUNT = 0
        Logic.dragging = False
        Logic.start_x = None
        Logic.start_y = None
        Logic.animation_is_done = True
        Logic.shrink_speed = 5
        Logic.temp_current_theme = None
        Logic.cards_moved = []
        Logic.move_parameters = {}

    def handle_tableau_card_click(self, event):
        clicked_card = self.game_canvas.gettags("current")
        if clicked_card:
            card_id = clicked_card[1].split("-")[1]
            card_stack = clicked_card[0]
            moveable = Logic.check_if_card_can_be_moved(card_id, card_stack)

            if not moveable:
                return

            Logic.dragging = self.game_canvas.find_closest(event.x, event.y)[0]
            Logic.start_x = event.x
            Logic.start_y = event.y
            Logic.move_parameters["from"] = card_stack
            Logic.move_parameters["origin"] = clicked_card[2]

    def handle_tableau_drag_card(self, event):
        """Handle mouse drag - move the card"""
        if Logic.dragging:
            # Calculate the distance moved
            dx = event.x - Logic.start_x
            dy = event.y - Logic.start_y

            # Move all cards under (including the clicked card)
            for card in Logic.cards_moved:
                self.game_canvas.move(card.id, dx, dy)
                self.game_canvas.tag_raise(card.id)

            # Update start position for next movement
            Logic.start_x = event.x
            Logic.start_y = event.y

    def handle_tableau_drop_card(self, event):
        """Handle mouse release - stop dragging"""
        Logic.dragging = False
        self.game_canvas.config(cursor="")
        x_coord = event.x

        if Logic.move_parameters:
            for key, value in Logic.STACK_COORDS.items():
                x0, x1 = value
                if x_coord >= x0 and x_coord <= x1:
                    break
                if x_coord < 0:
                    break

            # set the app's move parameter
            Logic.move_parameters["to"] = key
            # move the card
            Logic.handle_card_movement(self)

            # if move occurred:
            # check if any of the new cards complete a stack
            complete_stack = Logic.check_complete_stack()
            if complete_stack:
                Logic.remove_cards_from_tableau(self, complete_stack)

            # show cards under the moved card / completed stack
            Logic.show_underlying_cards_if_any(self)

            # check if theres no more move
            no_card_can_move = Logic.check_if_any_card_can_be_moved()
            if no_card_can_move:
                self.show_game_over_frame()

            Logic.cards_moved = []
            Logic.move_parameters = {}

    def handle_stock_pile_click(self):
        clicked_card = self.game_canvas.gettags("current")
        the_id = clicked_card[0].split("-")[1]
        if int(the_id) != Logic.COVERED_CARDS_REMAINING:
            return

        if Logic.animation_is_done:
            card_values = Logic.get_card_value(the_id)
            card_position = self.game_canvas.coords(the_id)
            positions = Logic.get_topmost_positons(self)

            for idx, value in enumerate(card_values):
                # create card on top of the pile
                initial_x, initial_y = card_position
                image = self.card_theme_image
                new_card = self.game_canvas.create_image(
                    initial_x, initial_y, image=image, tags="animated")
                target_x, target_y = positions[idx]
                # animate the card
                Logic.animate_card(self, new_card, target_x, target_y)

                # update the card image
                card_name = f"{Logic.suit_dict.get(value, value)}_of_{Logic.SUIT_TYPE}"
                image = self.card_suit_images[card_name]
                self.game_canvas.itemconfig(new_card, image=image)

                # update the card image tags
                stack_name = f"stack_{idx+1}"
                self.game_canvas.itemconfig(new_card, tags=(
                    stack_name, f"card-{new_card}", f"{target_x}-{target_y}"))

                the_card = Card(new_card, "tableau-card", value, "visible")
                Logic.TABLEAU_CARDS[stack_name].append(the_card)

                self.game_canvas.tag_bind(new_card, "<Button-1>", lambda event,
                                          instance=self: Logic.handle_tableau_card_click(instance, event))
                self.game_canvas.tag_bind(new_card, "<B1-Motion>", lambda event,
                                          instance=self: Logic.handle_tableau_drag_card(instance, event))
                self.game_canvas.tag_bind(new_card, "<ButtonRelease-1>", lambda event,
                                          instance=self: Logic.handle_tableau_drop_card(instance, event))

            # delete the card from the stock pile
            self.game_canvas.delete(the_id)
            # remove the card from the stock pile
            Logic.remove_card_from_pile(the_id)

            Logic.COVERED_CARDS_REMAINING -= 1

            # check if any of the new cards complete a stack
            complete_stack = Logic.check_complete_stack()
            if complete_stack:
                Logic.remove_cards_from_tableau(self, complete_stack)

            # check if theres no more move
            no_card_can_move = Logic.check_if_any_card_can_be_moved()
            if no_card_can_move:
                self.show_game_over_frame()

    def handle_card_movement(self):
        from_stack, to_stack, origin_coords = Logic.move_parameters[
            "from"], Logic.move_parameters["to"], Logic.move_parameters["origin"]
        float_x, float_y = origin_coords.split("-")
        dx, dy = float(float_x), float(float_y)

        # check if the card be be moved to the destination stack
        can_go_to_destination = Logic.check_if_card_can_go_to_destination(
            from_stack, to_stack, Logic.cards_moved[0])

        if can_go_to_destination:
            # movement or click from original stack to same stack
            if from_stack == to_stack:
                # if only one card is moved
                if len(Logic.cards_moved) == 1:
                    card = Logic.cards_moved[0]
                    stack_card_can_move_to = Logic.check_available_stack_card_can_move_to(
                        self, card.value, from_stack)
                    if stack_card_can_move_to != []:
                        stack_to_go = stack_card_can_move_to[0]
                        cards_on_stack = Logic.TABLEAU_CARDS[stack_to_go]
                        # if there is no card on the stack
                        if cards_on_stack == []:
                            position = Logic.STACK_STARTING_POSITIONS[stack_to_go]
                            dx, dy = position
                            self.game_canvas.coords(card.id, int(dx), int(dy))
                            # self.game_canvas.tag_raise(card.id)
                            final_coords = dx, dy
                        else:
                            last_card = cards_on_stack[-1]
                            tag = self.game_canvas.gettags(last_card.id)[2]
                            float_x, float_y = tag.split("-")
                            dx, dy = float(float_x), float(float_y)
                            self.game_canvas.coords(
                                card.id, int(dx), int(dy)+25)
                            self.game_canvas.tag_raise(card.id)
                            final_coords = dx, dy+25
                        Logic.move_parameters["to"] = stack_to_go
                        Logic.MOVES_COUNT += 1
                        Logic.update_card_lists(
                            self, from_stack, stack_to_go, card, final_coords)
                    else:
                        # no other stack to move to...
                        # drop card back on same stack
                        self.game_canvas.coords(card.id, int(dx), int(dy))
                # cascading cards are clicked
                else:
                    first_of_cascading_card = Logic.cards_moved[0]
                    stack_card_can_move_to = Logic.check_available_stack_card_can_move_to(
                        self, first_of_cascading_card.value, from_stack)
                    # there are stack(s) the card can move to
                    if stack_card_can_move_to != []:
                        # choose first available option
                        stack_to_go = stack_card_can_move_to[0]
                        cards_on_stack = Logic.TABLEAU_CARDS[stack_to_go]
                        for card in Logic.cards_moved:
                            if cards_on_stack == []:
                                position = Logic.STACK_STARTING_POSITIONS[stack_to_go]
                                dx, dy = position
                                self.game_canvas.coords(
                                    card.id, int(dx), int(dy))
                                self.game_canvas.tag_raise(card.id)
                                final_coords = dx, dy
                            else:
                                last_card_on_destination_stack = Logic.TABLEAU_CARDS[stack_to_go][-1]
                                last_card_id = last_card_on_destination_stack.id
                                tag = self.game_canvas.gettags(last_card_id)[2]
                                float_x, float_y = tag.split("-")
                                dx, dy = float(float_x), float(float_y)
                                self.game_canvas.coords(
                                    card.id, int(dx), int(dy)+25)
                                self.game_canvas.tag_raise(card.id)
                                final_coords = dx, dy+25
                            Logic.update_card_lists(
                                self, from_stack, stack_to_go, card, final_coords)
                        Logic.move_parameters["to"] = stack_to_go
                        Logic.MOVES_COUNT += 1
                    else:
                        # no other stack to move to...
                        # drop card back on same stack
                        for card in Logic.cards_moved:
                            tags = self.game_canvas.gettags(card.id)
                            card_coords = tags[2].split("-")
                            dx, dy = float(card_coords[0]), float(
                                card_coords[1])
                            self.game_canvas.coords(card.id, int(dx), int(dy))
            # movement from original stack to another stack
            else:
                # if only one card is moved
                if len(Logic.cards_moved) == 1:
                    # if empty stack
                    if Logic.TABLEAU_CARDS[to_stack] == []:
                        position = Logic.STACK_STARTING_POSITIONS[to_stack]
                        dx, dy = position
                        card = Logic.cards_moved[0]
                        self.game_canvas.coords(card.id, int(dx), int(dy))
                        final_coords = dx, dy
                    else:
                        last_card_on_destination_stack = Logic.TABLEAU_CARDS[to_stack][-1]
                        last_card_id = last_card_on_destination_stack.id
                        tag = self.game_canvas.gettags(last_card_id)[2]
                        float_x, float_y = tag.split("-")
                        dx, dy = float(float_x), float(float_y)
                        card = Logic.cards_moved[0]

                        self.game_canvas.coords(card.id, int(dx), int(dy)+25)
                        final_coords = dx, dy+25
                    Logic.update_card_lists(
                        self, from_stack, to_stack, card, final_coords)
                else:
                    for card in Logic.cards_moved:
                        # final_coords = None
                        if Logic.TABLEAU_CARDS[to_stack] == []:
                            position = Logic.STACK_STARTING_POSITIONS[to_stack]
                            dx, dy = position
                            self.game_canvas.coords(
                                card.id, int(dx), int(dy))
                            final_coords = dx, dy
                        else:
                            last_card_on_destination_stack = Logic.TABLEAU_CARDS[to_stack][-1]
                            last_card_id = last_card_on_destination_stack.id
                            tag = self.game_canvas.gettags(last_card_id)[2]
                            float_x, float_y = tag.split("-")
                            dx, dy = float(float_x), float(float_y)
                            self.game_canvas.coords(
                                card.id, int(dx), int(dy)+25)
                            final_coords = dx, dy+25
                        Logic.update_card_lists(
                            self, from_stack, to_stack, card, final_coords)
                Logic.MOVES_COUNT += 1
        else:
            # return card back to stack
            # if only one card is moved
            if len(Logic.cards_moved) == 1:
                card_id = Logic.cards_moved[0].id
                self.game_canvas.coords(card_id, int(dx), int(dy))
            else:
                for card in Logic.cards_moved:
                    tags = self.game_canvas.gettags(card.id)
                    card_coords = tags[2].split("-")
                    dx, dy = float(card_coords[0]), float(card_coords[1])
                    self.game_canvas.coords(card.id, int(dx), int(dy))

    def update_card_lists(self, from_stack, to_stack, card, new_coords):
        # change tags for the card image
        tags = self.game_canvas.gettags(card.id)
        dx, dy = new_coords
        self.game_canvas.itemconfig(
            card.id, tags=(to_stack, tags[1], f"{dx}-{dy}"))
        # delete cards from origin stack
        Logic.TABLEAU_CARDS[from_stack].pop(-1)
        # add cards to destination stack
        new_card = Card(card.id, "tableau-card", card.value, "visible")
        Logic.TABLEAU_CARDS[to_stack].append(new_card)

    def check_if_card_can_go_to_destination(from_coord, to_coord, card):
        if from_coord == to_coord:
            return True
        if Logic.TABLEAU_CARDS[to_coord] == []:
            return True

        last_card_on_destination_stack = Logic.TABLEAU_CARDS[to_coord][-1]
        moved_card_value = card.value
        last_destination_card_value = last_card_on_destination_stack.value
        return last_destination_card_value - 1 == moved_card_value

    def show_underlying_cards_if_any(self):
        stack_from = Logic.move_parameters["from"]
        stack_to = Logic.move_parameters["to"]
        values_in_origin = Logic.TABLEAU_CARDS[stack_from]
        values_in_destination = Logic.TABLEAU_CARDS[stack_to]

        if values_in_origin:
            last_card = values_in_origin[-1]
            if last_card.status == "hidden":
                card_name = f"{Logic.suit_dict.get(last_card.value, last_card.value)}_of_{Logic.SUIT_TYPE}"
                card_image = self.card_suit_images[card_name]
                self.game_canvas.itemconfig(last_card.id, image=card_image)
                last_card.status = "visible"

        if values_in_destination:
            last_card = values_in_destination[-1]
            if last_card.status == "hidden":
                card_name = f"{Logic.suit_dict.get(last_card.value, last_card.value)}_of_{Logic.SUIT_TYPE}"
                card_image = self.card_suit_images[card_name]
                self.game_canvas.itemconfig(last_card.id, image=card_image)
                last_card.status = "visible"

    def check_available_stack_card_can_move_to(self, card_value, from_stack):
        """ checks if there are free stack to move card to """

        positions = []
        empty_tableau = []
        for key, card in Logic.TABLEAU_CARDS.items():
            # exclude the origin stack from search
            if key != from_stack:
                if card == []:
                    empty_tableau.append(key)
                else:
                    topmost_card = card[-1]
                    if topmost_card.value - 1 == card_value:
                        positions.append(key)

        return positions if positions else empty_tableau

    def get_topmost_positons(self):
        positions = []
        for key, card in Logic.TABLEAU_CARDS.items():
            if card == []:
                x, y = Logic.STACK_STARTING_POSITIONS[key]
                positions.append((x, y))
            else:
                topmost_card = card[-1]
                card_id = topmost_card.id
                widget = self.game_canvas.find_withtag(f"card-{str(card_id)}")
                widget_position = self.game_canvas.coords(widget)
                new_x, new_y = widget_position[0], widget_position[1] + 25
                positions.append((new_x, new_y))

        return positions

    def check_complete_stack():
        complete_stacks = []
        for key, val in Logic.TABLEAU_CARDS.items():
            open_values = []

            for v in val:
                if v.status == "visible":
                    # add the values of each card to open_values list
                    open_values.append(v.value)

            # if last 13 values in the list is [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            if open_values[-13:] == [i for i in range(13, 0, -1)]:
                # add it to the complete_stacks list
                complete_stacks.append(key)

        return complete_stacks

    def check_if_any_card_can_be_moved():
        topmosts = []
        open_values = []

        # Get the open cards and the topmost cards
        for val in Logic.TABLEAU_CARDS.values():
            if val == []:
                topmosts.append([])
                continue
            else:
                topmosts.append(val[-1].value)

            open_values.append([int(i.value)
                               for i in val if i.status == "visible"])

        # If there's an empty stack,
        # any card can be moved there
        if [] in topmosts:
            return False

        movables = []
        last_legal_card = 0

        # add the last movable cards to the movable list
        for lst in open_values:
            lst = lst[::-1]
            if len(lst) == 1:
                movables.append(lst[0])
            else:
                for num in range(len(lst) - 1):
                    if lst[num] + 1 == lst[num + 1]:
                        last_legal_card = lst[num + 1]
                    else:
                        last_legal_card = lst[num]
                        break

                movables.append(last_legal_card)
                last_legal_card = 0

        # check if any of the movable cards can go to another stack
        can_move_bool = []
        for card in movables:
            can_move_bool.append(card+1 in topmosts)

        return not any(can_move_bool) and Logic.STOCK_PILE_CARDS == []

    def check_if_card_can_be_moved(id, stack):
        stack = Logic.TABLEAU_CARDS[stack]

        for idx, card in enumerate(stack):
            if card.id == int(id):
                if card.status == "hidden":
                    return False
                break

        cards_under = stack[idx:]
        if len(cards_under) == 1:
            Logic.cards_moved = cards_under
            return True
        else:
            the_numbers = [i.value for i in cards_under]
            Logic.cards_moved = cards_under
            return Logic.check_numbers_are_in_order(the_numbers)

    def remove_cards_from_tableau(self, complete_stack):
        for stack in complete_stack:
            complete_card_ids = [
                i.id for i in Logic.TABLEAU_CARDS[stack][-13:]]
            for ids in complete_card_ids[:-1]:
                self.game_canvas.delete(ids)
            last_card = complete_card_ids[-1]
            target_x, target_y = Logic.FOUNDATION_POSITION[Logic.FOUNDATION_COUNT]
            Logic.animate_card(self, last_card, target_x, target_y)

            self.game_canvas.tag_unbind(last_card, "<Button-1>")
            Logic.FOUNDATION_COUNT += 1

        for stack in complete_stack:
            for _ in range(13):
                Logic.TABLEAU_CARDS[stack].pop(-1)

        Logic.show_underlying_cards_if_any(self)
        game_is_over = Logic.check_if_game_over()
        outcome = {"moves_count": Logic.MOVES_COUNT}
        if game_is_over:
            self.reveal_game_outcome(outcome)

    def animate_card(self, card, target_x, target_y):
        cur_x, cur_y = self.game_canvas.coords(card)
        dx = target_x - cur_x
        dy = target_y - cur_y
        pixel_step = 3

        if abs(dx) > pixel_step or abs(dy) > pixel_step:
            Logic.animation_is_done = False
            move_x = min(abs(dx), pixel_step) * \
                (1 if dx > 0 else -1 if dx < 0 else 0)
            move_y = min(abs(dy), pixel_step) * \
                (1 if dy > 0 else -1 if dy < 0 else 0)

            self.game_canvas.move(card, move_x, move_y)
            self.master.after(
                2, Logic.animate_card, self, card, target_x, target_y)
        else:
            Logic.animation_is_done = True
            self.game_canvas.coords(card, target_x, target_y)

    def check_numbers_are_in_order(lst):
        highest = lst[0]
        for number in lst[1:]:
            if highest - number != 1:
                return False
            highest = number

        return True

    def check_card_is_single(idx, stack):
        last_card = Logic.TABLEAU_CARDS[stack][-1]
        return last_card.id == idx

    def check_if_game_over():
        return Logic.FOUNDATION_COUNT == 8

    def remove_card_from_pile(id):
        for idx, card in enumerate(Logic.STOCK_PILE_CARDS):
            if card.id == int(id):
                return Logic.STOCK_PILE_CARDS.pop(idx)

    def get_card_value(id):
        for card in Logic.STOCK_PILE_CARDS:
            if card.id == int(id):
                return card.value
