class CampaignBidsController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.set_place_bid_visible(False)

    def setup_view(self, mortgage_id):
        print 'mortgage_id'
        print mortgage_id
        # print self.mainwindow.api.load_bids({'mortgage_id': mortgage_id})
        if self.mainwindow.app.user.role_id == 2:
            self.set_place_bid_visible(True)

    def set_place_bid_visible(self, boolean):
        self.mainwindow.icb_place_bid_label.setVisible(boolean)
        self.mainwindow.icb_place_bid_pushbutton.setVisible(boolean)
        self.mainwindow.icb_amount_label.setVisible(boolean)
        self.mainwindow.icb_amount_lineedit.setVisible(boolean)
        self.mainwindow.icb_duration_label.setVisible(boolean)
        self.mainwindow.icb_duration_lineedit.setVisible(boolean)
        self.mainwindow.icb_interest_label.setVisible(boolean)
        self.mainwindow.icb_interest_lineedit.setVisible(boolean)
