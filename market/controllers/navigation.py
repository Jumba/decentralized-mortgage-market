class NavigateUser:
    """
    Create a NavigateUser object that controls the navigation buttons on the screen.
    Takes a MainWindowController object during construction.
    """
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.set_navigation_visible(False, 0)

    def user_screen_navigation(self):
        """
        Set the navigation bar depending on the role of the user.
        """
        user_role = self.mainwindow.app.user.role_id
        # user_role = 3    # The user you want to be. Only used for testing.
        if user_role:
            if user_role == 1:
                self.set_borrower_navigation()
            elif user_role == 2:
                self.set_investor_navigation()
            elif user_role == 3:
                self.set_bank_navigation()
        else:
            self.switch_to_profile()

    def set_borrower_navigation(self):
        """
        Sets the navigation bar and sets up the screens for the user with a borrower role.
        """
        self.mainwindow.navigation_pushbutton_1.setText('Profile')
        self.mainwindow.navigation_pushbutton_1.clicked.connect(self.switch_to_profile)
        self.mainwindow.navigation_pushbutton_2.setText('Portfolio')
        self.mainwindow.navigation_pushbutton_2.clicked.connect(self.switch_to_borrowers_portfolio)
        self.mainwindow.navigation_pushbutton_3.setText('Place Loan Request')
        self.mainwindow.navigation_pushbutton_3.clicked.connect(self.switch_to_bplr)
        self.mainwindow.navigation_pushbutton_4.setText('Open Market')
        self.mainwindow.navigation_pushbutton_4.clicked.connect(self.switch_to_openmarket)
        self.mainwindow.bplr_controller.setup_view()
        self.set_navigation_visible(True, 1)

    def set_investor_navigation(self):
        """
        Sets the navigation bar and sets up the screens for the user with a investor role.
        """
        self.mainwindow.navigation_pushbutton_1.setText('Profile')
        self.mainwindow.navigation_pushbutton_1.clicked.connect(self.switch_to_profile)
        self.mainwindow.navigation_pushbutton_2.setText('Portfolio')
        self.mainwindow.navigation_pushbutton_2.clicked.connect(self.switch_to_investors_portfolio)
        self.mainwindow.navigation_pushbutton_3.setText('Open Market')
        self.mainwindow.navigation_pushbutton_3.clicked.connect(self.switch_to_openmarket)
        self.mainwindow.navigation_pushbutton_4.setVisible(False)
        self.set_navigation_visible(True, 2)
        self.mainwindow.ip_controller.setup_view()

    def set_bank_navigation(self):
        """
        Sets the navigation bar and sets up the screens for the user with a bank role.
        """
        self.mainwindow.navigation_pushbutton_1.setText('Portfolio')
        self.mainwindow.navigation_pushbutton_1.clicked.connect(self.switch_to_banks_portfolio)
        self.mainwindow.navigation_pushbutton_2.setText('Loan Requests')
        self.mainwindow.navigation_pushbutton_2.clicked.connect(self.switch_to_fiplr)
        self.mainwindow.navigation_pushbutton_3.setText('Open Market')
        self.mainwindow.navigation_pushbutton_3.clicked.connect(self.switch_to_openmarket)
        self.mainwindow.navigation_pushbutton_4.setVisible(False)
        self.set_navigation_visible(True, 3)
        self.mainwindow.fip_controller.setup_view()
        self.mainwindow.fiplr1_controller.setup_view()
        # self.mainwindow.fiplr2_controller.setup_view()

    def switch_to_bplr(self):
        """
        Switch to the Place Loan Request page.
        """
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.bplr_page)

    def switch_to_borrowers_portfolio(self):
        """
        Switch to the Borrower's Portfolio page. Contains overview of all loan offers.
        """
        self.mainwindow.bp_controller.setup_view()
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.bp_page)

    def switch_to_investors_portfolio(self):
        """
        Switch to the Investor's Portfolio page. Contains overview of all investments made by the user.
        """
        self.mainwindow.ip_controller.setup_view()
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.ip_page)

    def switch_to_banks_portfolio(self):
        """
        Switch to the Bank's Portfolio page. Contains overview of all loan requests.
        """
        self.mainwindow.fip_controller.setup_view()
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.fip_page)

    def switch_to_openmarket(self):
        """
        Switch to the Open Market page. Contains overview of all active campaigns.
        """
        self.mainwindow.openmarket_controller.setup_view()
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.openmarket_page)

    def switch_to_profile(self):
        """
        Switch to the Profile page. Contains user details.
        """
        self.mainwindow.profile_controller.setup_view()
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.profile_page)

    def switch_to_fiplr(self):
        """
        Switch to the Pending Loan Requests 1 page. Contains overview of all loan requests.
        """
        self.mainwindow.fiplr1_controller.setup_view()
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.fiplr1_page)

    def switch_to_fiplr2(self):
        """
        Switch to the Pending Loan Requests 2 page. Shows details of a single loan request.
        From this screen the bank can reject the request or create a mortgage offer.
        """
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.fiplr2_page)

    def switch_to_campaign_bids(self, mortgage_id):
        """
        Switch to the Campaign Bids page. Contains details and placed bids of a single campaign.
        """
        self.mainwindow.cb_controller.setup_view(mortgage_id)
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.icb_page)

    def set_navigation_visible(self, boolean, role):
        """
        Hides or shows the navigation buttons for a user
        :param boolean: True to show the needed navigation buttons. False to hide all buttons.
        :param role: The role id of the user.
        """
        self.mainwindow.navigation_pushbutton_1.setVisible(boolean)
        self.mainwindow.navigation_pushbutton_2.setVisible(boolean)
        self.mainwindow.navigation_pushbutton_3.setVisible(boolean)
        if role == 1:
            self.mainwindow.navigation_pushbutton_4.setVisible(True)
        else:
            self.mainwindow.navigation_pushbutton_4.setVisible(False)
