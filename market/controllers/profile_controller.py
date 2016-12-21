from PyQt5.QtWidgets import *


class ProfileController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.current_profile = None
        self.msg = QMessageBox
        # Add listener to the save profile button
        self.mainwindow.profile_save_pushbutton.clicked.connect(self.save_form)

    def setup_view(self):
        # Check if user already has a role, if so load the right data. Otherwise show an empty profile
        if self.mainwindow.app.user.role_id:
            self.current_profile = self.mainwindow.api.load_profile(self.mainwindow.app.user)
            if self.current_profile:
                self.update_form(self.current_profile)
            else:
                print 'Profile: Current profile is empty'

    def save_form(self):
        try:
            # Get the data from the forms
            payload = {'role': 2, 'first_name': unicode(self.mainwindow.profile_firstname_lineedit.text()),
                            'last_name': unicode(self.mainwindow.profile_lastname_lineedit.text()),
                            'email': str(self.mainwindow.profile_email_lineedit.text()),
                            'iban': str(self.mainwindow.profile_iban_lineedit.text()),
                            'phonenumber': str(self.mainwindow.profile_phonenumber_lineedit.text())}

            if self.mainwindow.profile_borrower_radiobutton.isChecked():
                payload['role'] = 1
                payload['current_postalcode'] = str(self.mainwindow.profile_postcode_lineedit.text())
                payload['current_housenumber'] = str(self.mainwindow.profile_housenumber_lineedit.text())
                payload['current_address'] = str(self.mainwindow.profile_address_lineedit.text())
                # TODO Add missing 'documents_list': self.documentsTable
                payload['documents_list'] = []

            # Check if all fields are filled out
            for _, value in payload.iteritems():
                if value == '':
                    raise ValueError

            # Check if the user can switch roles
            if self.check_role_switch():
                # Show a popup window when the profile has been saved
                if self.mainwindow.api.create_profile(self.mainwindow.app.user, payload):
                    self.msg.about(self.mainwindow, "Profile saved", 'Your profile has been saved.')
                    self.mainwindow.app.user.update(self.mainwindow.api.db)
                    self.update_navigation_bar()
                else:
                    self.msg.about(self.mainwindow, "Profile error",
                                      'Your profile could not be saved. Try again later.')
            else:
                self.msg.about(self.mainwindow, "Role switch failed",
                                  'It is not possible to change your role at this time')
        except ValueError:
            self.msg.about(self.mainwindow, "Profile error", 'You didn\'t enter all of the required information.')

    def update_form(self, profile):
        # if self.current_profile:
        self.mainwindow.profile_firstname_lineedit.setText(profile.first_name)
        self.mainwindow.profile_lastname_lineedit.setText(profile.last_name)
        self.mainwindow.profile_email_lineedit.setText(profile.email)
        self.mainwindow.profile_iban_lineedit.setText(profile.iban)
        self.mainwindow.profile_phonenumber_lineedit.setText(profile.phone_number)
        self.mainwindow.profile_investor_radiobutton.setChecked(True)

        # Add additional info if the user is a borrower
        if self.mainwindow.app.user.role_id == 1:
            self.mainwindow.profile_borrower_radiobutton.setChecked(True)
            self.mainwindow.profile_postcode_lineedit.setText(profile.current_postal_code)
            self.mainwindow.profile_housenumber_lineedit.setText(profile.current_house_number)
            self.mainwindow.profile_address_lineedit.setText(profile.current_address)


    def update_navigation_bar(self):
        # Check which role the user currently has, and adjust the navigation bar accordingly
        user_role = self.mainwindow.app.user.role_id
        if user_role == 1:
            self.mainwindow.navigation.set_borrower_navigation()
        elif user_role == 2:
            self.mainwindow.navigation.set_investor_navigation()

    def check_role_switch(self):
        # Check if the user still has an open loan request or investments
        # If not, they can switch roles
        user = self.mainwindow.app.user
        if user.loan_request_ids or user.investment_ids:
            return False
        return True
