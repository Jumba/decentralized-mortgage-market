from PyQt5.QtWidgets import *


class ProfileController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.current_profile = None
        self.payload = {}

        # Add listener to the save profile button
        self.mainwindow.profile_save_pushbutton.clicked.connect(self.save_form)

    def setup_view(self):
        # Check if user already has a role, if so load the right data. Otherwise show an empty profile
        if self.mainwindow.app.user.role_id:
            self.current_profile = self.mainwindow.api.load_profile(self.mainwindow.app.user)
            if self.current_profile:
                self.mainwindow.profile_firstname_lineedit.setText(self.current_profile.first_name)
                self.mainwindow.profile_lastname_lineedit.setText(self.current_profile.last_name)
                self.mainwindow.profile_email_lineedit.setText(self.current_profile.email)
                self.mainwindow.profile_iban_lineedit.setText(self.current_profile.iban)
                self.mainwindow.profile_phonenumber_lineedit.setText(self.current_profile.phone_number)

                if self.mainwindow.app.user.role_id == 1:
                    self.mainwindow.profile_borrower_radiobutton.setChecked(True)
                    self.mainwindow.profile_postcode_lineedit.setText(self.current_profile.current_postal_code)
                    self.mainwindow.profile_housenumber_lineedit.setText(self.current_profile.current_house_number)
                else:
                    self.mainwindow.profile_investor_radiobutton.setChecked(True)
            else:
                print 'Profile: Current profile is empty'

    def save_form(self):
        # Get the data from the forms
        self.payload = {'role': 2, 'first_name': unicode(self.mainwindow.profile_firstname_lineedit.text()),
                        'last_name': unicode(self.mainwindow.profile_lastname_lineedit.text()),
                        'email': str(self.mainwindow.profile_email_lineedit.text()),
                        'iban': str(self.mainwindow.profile_iban_lineedit.text()),
                        'phonenumber': str(self.mainwindow.profile_phonenumber_lineedit.text())}

        if self.mainwindow.profile_borrower_radiobutton.isChecked():
            self.payload['role'] = 1
            self.payload['current_postalcode'] = str(self.mainwindow.profile_postcode_lineedit.text())
            self.payload['current_housenumber'] = str(self.mainwindow.profile_housenumber_lineedit.text())
            # TODO Add missing 'documents_list': self.documentsTable
            self.payload['documents_list'] = []

        # Show a popup window when the profile has been saved
        if self.mainwindow.api.create_profile(self.mainwindow.app.user, self.payload):
            QMessageBox.about(self.mainwindow, "Profile saved", 'Your profile has been saved.')
        self.mainwindow.app.user.update(self.mainwindow.api.db)
        self.update_navigation_bar()

    def update_navigation_bar(self):
        # Check which role the user currently has, and adjust the navigation bar accordingly
        user_role = self.mainwindow.app.user.role_id
        if user_role == 1:
            self.mainwindow.navigation.set_borrower_navigation()
        elif user_role == 2:
            self.mainwindow.navigation.set_investor_navigation()
