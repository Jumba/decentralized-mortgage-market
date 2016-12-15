from market.views.main_view import Ui_MainWindow

# The user you want to be. Only used for testing.
USER = 1

class NavigateUser:
    def __init__(self, mainwindow):
        # self.mainwindow = Ui_MainWindow
        self.mainwindow = mainwindow
        self.mainwindow.navigation_pushbutton_1.setVisible(False)
        self.mainwindow.navigation_pushbutton_2.setVisible(False)
        self.mainwindow.navigation_pushbutton_3.setVisible(False)
        self.mainwindow.navigation_pushbutton_4.setVisible(False)

    def prepare_views_for_user(self):
        # check page permissions
        self.mainwindow.navigation_pushbutton_1.setVisible(True)
        self.mainwindow.navigation_pushbutton_2.setVisible(True)
        self.mainwindow.navigation_pushbutton_3.setVisible(True)
        self.mainwindow.navigation_pushbutton_4.setVisible(True)
        self.user_screen_navigation()
        self.mainwindow.navigation_pushbutton_1.click()
        # self.mainwindow.profile_controller.setup_view()
        # self.mainwindow.next_screen()

    def user_screen_navigation(self):
        user_role = self.mainwindow.app.user.role_id
        #user_role = USER
        if user_role:
            if user_role == 1:
                print 'User logged in as: borrower'
                self.set_borrower_navigation()
            elif user_role == 2:
                print 'User logged in as: investor'
                self.set_investor_navigation()
            elif user_role == 3:
                print 'User logged in as: financial institution'
                self.set_bank_navigation()
        else:
            print 'User has no recognized role.'
            self.mainwindow.navigation_pushbutton_1.setVisible(False)
            self.mainwindow.navigation_pushbutton_2.setVisible(False)
            self.mainwindow.navigation_pushbutton_3.setVisible(False)
            self.mainwindow.navigation_pushbutton_4.setVisible(False)
            self.switch_to_profile()

    def set_borrower_navigation(self):
        self.mainwindow.navigation_pushbutton_1.setText('Profile')
        self.mainwindow.navigation_pushbutton_1.clicked.connect(self.switch_to_profile)
        self.mainwindow.navigation_pushbutton_2.setText('Portfolio')
        self.mainwindow.navigation_pushbutton_2.clicked.connect(self.switch_to_borrowers_portfolio)
        self.mainwindow.navigation_pushbutton_3.setText('Place Loan Request')
        self.mainwindow.navigation_pushbutton_3.clicked.connect(self.switch_to_bplr)
        self.mainwindow.navigation_pushbutton_4.setText('Open Market')
        self.mainwindow.navigation_pushbutton_4.clicked.connect(self.switch_to_openmarket)
        # self.mainwindow.profile_controller.setup_view()
        self.mainwindow.openmarket_controller.setup_view()
        self.mainwindow.bplr_controller.setup_view()
        # self.mainwindow.portfolio_controller.setup_view()


    def set_investor_navigation(self):
        self.mainwindow.navigation_pushbutton_1.setText('Profile')
        self.mainwindow.navigation_pushbutton_1.clicked.connect(self.switch_to_profile)
        self.mainwindow.navigation_pushbutton_2.setText('Portfolio')
        self.mainwindow.navigation_pushbutton_2.clicked.connect(self.switch_to_investors_portfolio)
        self.mainwindow.navigation_pushbutton_3.setText('Open market')
        self.mainwindow.navigation_pushbutton_3.clicked.connect(self.switch_to_openmarket)
        self.mainwindow.navigation_pushbutton_4.setVisible(False)

    def set_bank_navigation(self):
        self.mainwindow.navigation_pushbutton_1.setText('Portfolio')
        self.mainwindow.navigation_pushbutton_1.clicked.connect(self.switch_to_banks_portfolio)
        self.mainwindow.navigation_pushbutton_2.setText('Loan Requests')
        self.mainwindow.navigation_pushbutton_2.clicked.connect(self.switch_to_fiplr)
        self.mainwindow.navigation_pushbutton_3.setText('Open Market')
        self.mainwindow.navigation_pushbutton_3.clicked.connect(self.switch_to_openmarket)
        self.mainwindow.navigation_pushbutton_4.setVisible(False)

    def switch_to_bplr(self):
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.bplr_page)

    def switch_to_borrowers_portfolio(self):
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.bp_page)

    def switch_to_investors_portfolio(self):
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.ip_page)

    def switch_to_banks_portfolio(self):
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.fip_page)

    def switch_to_openmarket(self):
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.openmarket_page)

    def switch_to_profile(self):
        self.mainwindow.profile_controller.setup_view()
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.profile_page)

    def switch_to_fiplr(self):
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.fiplr1_page)

    def switch_to_view_campaign(self):
        self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.fiplr1_page)

