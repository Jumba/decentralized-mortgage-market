

class CampaignBidsController:
    """
    Create a CampaignBidsController object that performs tasks on the Campaign Bids section of the gui.
    Takes a MainWindowController object during construction.
    Redirected from the open market page.
    """
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.mortgage_id = None
        self.table = self.mainwindow.icb_current_bids_table
        self.mainwindow.icb_place_bid_pushbutton.clicked.connect(self.place_bid)
        self.set_place_bid_visible(False)

    def setup_view(self, mortgage_id):
        """
        Show up-to-date information about the chosen campaign on the screen.
        :param mortgage_id: Mortgage UUID of the campaign
        """
        self.table.setRowCount(0)
        self.mortgage_id = mortgage_id
        self.mainwindow.icb_place_bid_pushbutton.disconnect()
        self.mainwindow.icb_place_bid_pushbutton.clicked.connect(self.place_bid)
        bids, house, campaign = self.mainwindow.api.load_bids({'mortgage_id': mortgage_id})
        self.mainwindow.icb_property_address_lineedit.setText(house.address + ' '
                                                              + house.house_number + ', ' + house.postal_code)
        self.mainwindow.icb_remaining_amount_lineedit.setText(str(campaign.amount))
        for investment in bids:
            self.mainwindow.insert_row(self.table, [investment.amount, investment.duration, investment.interest_rate,
                                                    investment.status.name])
        if self.mainwindow.app.user.role_id == 2:
            self.set_place_bid_visible(True)

    def place_bid(self):
        """
        Place an investment offer on the currently viewed campaign.
        Shows a "Offer placed" alert if the offer was places successfully.
        Shows a "Bid error" alert if the form was not filled in correctly.
        """
        try:
            payload = {'amount': int(self.mainwindow.icb_amount_lineedit.text()),
                       'duration': int(self.mainwindow.icb_duration_lineedit.text()),
                       'interest_rate': float(self.mainwindow.icb_interest_lineedit.text()),
                       'mortgage_id': self.mortgage_id}
            if self.mainwindow.api.place_loan_offer(self.mainwindow.app.user, payload):
                self.mainwindow.show_dialog("Offer placed",
                                            'Your bid has been placed.')
                self.setup_view(self.mortgage_id)
        except ValueError:
            self.mainwindow.show_dialog("Bid error",
                                        'You didn\'t enter all of the required information.')

    def set_place_bid_visible(self, boolean):
        """
        Sets the visibility of the form used for investing.
        :param boolean: True to turn on the visibility of the form, False to turn hide the form.
        """
        self.mainwindow.icb_place_bid_label.setVisible(boolean)
        self.mainwindow.icb_place_bid_pushbutton.setVisible(boolean)
        self.mainwindow.icb_amount_label.setVisible(boolean)
        self.mainwindow.icb_amount_lineedit.setVisible(boolean)
        self.mainwindow.icb_duration_label.setVisible(boolean)
        self.mainwindow.icb_duration_lineedit.setVisible(boolean)
        self.mainwindow.icb_interest_label.setVisible(boolean)
        self.mainwindow.icb_interest_lineedit.setVisible(boolean)
