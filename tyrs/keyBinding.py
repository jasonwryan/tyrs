import curses
import editBox

class KeyBinding:

    def __init__ (self, ui, conf, api):
        self.conf = conf
        self.ui = ui
        self.api = api

    def resizeEvent (self):
        self.ui.resize_event = False
        curses.endwin()
        self.ui.maxyx = self.ui.screen.getmaxyx()
        curses.doupdate()

    def moveDown (self):
        if self.ui.status['current'] < self.ui.status['count'] - 1:
            if self.ui.status['current'] >= self.ui.status['last']:
            # We need to be sure it will have enough place to
            # display the next tweet, otherwise we still stay
            # to the current tweet
            # This is due to the dynamic height of a tweet.

            # height_first_status = self.getSizeStatus(self.statuses[self.status['first']])
            # next_status = self.status['last'] + 1
            # height_next_status  = self.getSizeStatus(self.statuses[next_status])
            # height_left = self.current_y - self.maxyx[0]-1
            # if height_next_status['height'] > (height_left + height_first_status['height']):
            #     self.status['current'] -=

                self.ui.status['first'] += 1


            self.ui.status['current'] += 1

    def moveUp (self):
        if self.ui.status['current'] > 0:
            # if we need to move up the list to display
            if self.ui.status['current'] == self.ui.status['first']:
                self.ui.status['first'] -= 1
            self.ui.status['current'] -= 1

    def tweet (self):
        params = {'char': 200, 'width': 80, 'header': "What's up ?"}
        self.ui.refresh_token = True
        box = editBox.EditBox(self.ui.screen, params)
        if box.confirm:
            try:
                self.api.postTweet(box.getTweet())
                self.ui.flash = ['Tweet has been send successfully.', "info"]
            except:
                self.ui.flash = ["Couldn't send the tweet.", "warning"]
        self.ui.refresh_token = False

    def retweet (self):
        status = self.ui.statuses[self.ui.status['current']]
        try:
            self.api.retweet(status.GetId())
            self.ui.flash = ['Retweet has been send successfully.', 'info']
        except:
            self.ui.flash = ["Couldn't send the retweet.", 'warning']

    def clear (self):
        self.ui.clearStatuses()

    def update (self):
        self.ui.updateHomeTimeline()

    def followSelected (self):
        status = self.ui.getCurrentStatus()
        try:
            if self.ui.isRetweet(status):
                pseudo = self.ui.originOfRetweet(status)
                self.api.CreateFriendship(pseudo)
            else:
                pseudo = status.user.screen_name
                self.api.CreateFriendship(pseudo)
            self.ui.flash = ["You are now following %s" % pseudo, 'info']
        except:
            self.ui.flash = ["Couldn't follow %s" % pseudo, 'warning']

    def unfollowSelected (self):
        pseudo = self.ui.getCurrentStatus().user.screen_name
        try:
            self.api.DestroyFriendship(pseudo)
            self.ui.flash = ["You have unfollowed %s" % pseudo, "info"]
        except:
            self.ui.flash = ["Failed to unfollow %s" % pseudo, "warning"]

    def handleKeyBinding(self):
        '''Should have all keybinding handle here'''
        while True:

            ch = self.ui.screen.getch()

            if self.ui.resize_event:
                self.resizeEvent()

            # Down and Up key must act as a menu, and should navigate
            # throught every tweets like an item.
            #
            if ch == ord(self.conf.keys_down) or ch == curses.KEY_DOWN:
                self.moveDown()

            elif ch == ord(self.conf.keys_up) or ch == curses.KEY_UP:
                self.moveUp()

            elif ch == ord(self.conf.keys_tweet):
                self.tweet()

            elif ch == ord(self.conf.keys_retweet):
                self.retweet()

            elif ch == ord(self.conf.keys_clear):
                self.clear()

            elif ch == ord(self.conf.keys_update):
                self.update()

            elif ch == ord(self.conf.keys_follow_selected):
                self.followSelected()

            elif ch == ord(self.conf.keys_unfollow_selected):
                self.unfollowSelected()

            # QUIT
            # 27 corresponding to the ESC, couldn't find a KEY_* corresponding
            elif ch == ord(self.conf.keys_quit) or ch == 27:
                break

            self.ui.displayHomeTimeline()
