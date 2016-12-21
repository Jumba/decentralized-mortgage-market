from PyQt5.QtWidgets import QMessageBox


class CampaignBidsController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.mortgage_id = None
        self.table = self.mainwindow.icb_current_bids_table
        self.mainwindow.icb_place_bid_pushbutton.clicked.connect(self.place_bid)
        self.set_place_bid_visible(False)
        self.msg = QMessageBox

    def setup_view(self, mortgage_id):
        self.table.setRowCount(0)
        self.mortgage_id = mortgage_id
        self.mainwindow.icb_place_bid_pushbutton.disconnect()
        self.mainwindow.icb_place_bid_pushbutton.clicked.connect(self.place_bid)
        bids, house, campaign = self.mainwindow.api.load_bids({'mortgage_id': mortgage_id})
        self.mainwindow.icb_property_address_lineedit.setText(house.address + ' ' + house.house_number + ' , ' + house.postal_code)
        self.mainwindow.icb_remaining_amount_lineedit.setText(str(campaign.amount))
        for investment in bids:
            self.mainwindow.insert_row(self.table, [investment.amount, investment.duration, investment.interest_rate, investment.status.name])
        if self.mainwindow.app.user.role_id == 2:
            self.set_place_bid_visible(True)

    def place_bid(self):
        try:
            payload = {'amount': int(self.mainwindow.icb_amount_lineedit.text()),
                       'duration': int(self.mainwindow.icb_duration_lineedit.text()),
                       'interest_rate': float(self.mainwindow.icb_interest_lineedit.text()),
                       'mortgage_id': self.mortgage_id}
            if self.mainwindow.api.place_loan_offer(self.mainwindow.app.user, payload):
                self.msg.about(self.mainwindow, "Offer placed",
                                  'Your bid has been placed.')
                self.setup_view(self.mortgage_id)
        except ValueError:
            self.msg.about(self.mainwindow, "Bid error",
                              'You didn\'t enter all of the required information.')

    def set_place_bid_visible(self, boolean):
        self.mainwindow.icb_place_bid_label.setVisible(boolean)
        self.mainwindow.icb_place_bid_pushbutton.setVisible(boolean)
        self.mainwindow.icb_amount_label.setVisible(boolean)
        self.mainwindow.icb_amount_lineedit.setVisible(boolean)
        self.mainwindow.icb_duration_label.setVisible(boolean)
        self.mainwindow.icb_duration_lineedit.setVisible(boolean)
        self.mainwindow.icb_interest_label.setVisible(boolean)
        self.mainwindow.icb_interest_lineedit.setVisible(boolean)
