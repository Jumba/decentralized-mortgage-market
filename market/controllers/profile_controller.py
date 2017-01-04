import os
import ntpath

from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QFileDialog, qApp
from PyQt5.QtWidgets import QPushButton, QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem


DOCUMENT_NAMES = ['Example Document 1', 'Example Document 2', 'Example Document 3']


class ProfileController:
    """
    Create a ProfileController object that performs tasks on the Profile section of the gui.
    Takes a MainWindowController object during construction.
    """

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.current_profile = None
        self.focused_button = None
        self.documents = dict.fromkeys(DOCUMENT_NAMES)
        # Add listener to the save profile button
        self.mainwindow.profile_save_pushbutton.clicked.connect(self.save_form)
        self.table = self.mainwindow.profile_documents_table
        self.prepare_table()

    def prepare_table(self):
        rows = len(DOCUMENT_NAMES)
        l = []
        for i in range(0, rows):
            self.table.insertRow(i)
            edit_button = QPushButton('Browse')
            edit_button.setText('Browse')
            edit_button.index = i
            edit_button.clicked.connect(self.browse)
            self.table.setItem(i, 0, QTableWidgetItem(str(DOCUMENT_NAMES[i])))
            self.table.setCellWidget(i, 2, edit_button)
            l.append(edit_button)

    def browse(self):
        index = self.mainwindow.sender().index
        path, _ = QFileDialog.getOpenFileName(self.mainwindow, 'Open File', os.getenv('HOME'))

        if QFile.exists(path):
            document_name = self.table.item(index, 0).text()
            self.documents[document_name] = path
            self.table.setItem(index, 1, QTableWidgetItem(str(ntpath.basename(path))))

    def setup_view(self):
        """
        Setup the profile screen with up-to-date data.
        """
        # Check if user already has a role, if so load the right data. Otherwise show an empty profile
        if self.mainwindow.app.user.role_id:
            self.current_profile = self.mainwindow.api.load_profile(self.mainwindow.app.user)
            if self.current_profile:
                self.update_form(self.current_profile)

    def save_form(self):
        """
        Create a profile with the data from the form.

        Shows a "Profile saved" alert if saving a new profile or switching to a new profile is successful.
        Shows a "Role switch failed" alert if switching to a new profile is not possible at this time.
        Shows a "Profile error" alert if the user failed to fill in the form correctly or, saving a new profile
        or switching to a new profile was not successful.

        """

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
                # TODO Add missing 'documents_list'
                # payload['documents_list'] = self.documents #The document payload as a dictionary.
                payload['documents_list'] = map(lambda key: self.documents[key], sorted(self.documents))

            # Check if all fields are filled out
            for _, value in payload.iteritems():
                if value == '':
                    raise ValueError

            # Check if the user can switch roles
            if self.check_role_switch():
                # Show a popup window when the profile has been saved
                if self.mainwindow.api.create_profile(self.mainwindow.app.user, payload):
                    self.mainwindow.show_dialog("Profile saved", 'Your profile has been saved.')
                    self.mainwindow.app.user.update(self.mainwindow.api.db)
                    self.update_navigation_bar()
                else:
                    self.mainwindow.show_dialog("Profile error",
                                                'Your profile could not be saved. Try again later.')
            else:
                self.mainwindow.show_dialog("Role switch failed",
                                            'It is not possible to change your role at this time')
        except ValueError:
            self.mainwindow.show_dialog("Profile error", 'You didn\'t enter all of the required information.')

    def update_form(self, profile):
        """
        Populate the view's form with a profile object.

        :param profile: Profile object used to populate form
        """
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
        """
        Updates the navigation bar if the user switches roles when he updates his profile.
        """
        # Check which role the user currently has, and adjust the navigation bar accordingly
        user_role = self.mainwindow.app.user.role_id
        if user_role == 1:
            self.mainwindow.navigation.set_borrower_navigation()
        elif user_role == 2:
            self.mainwindow.navigation.set_investor_navigation()

    def check_role_switch(self):
        """
        Checks if the user is allowed to switch roles.
        If the user has any active investments or loan requests, then the user is not allowed to do switch roles.
        :return: Returns True if the user is allowed to switch roles. Otherwise returns False
        """
        # Check if the user still has an open loan request or investments
        # If not, they can switch roles
        user = self.mainwindow.app.user
        if user.loan_request_ids or user.investment_ids:
            return False
        return True
