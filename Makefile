###### EDIT ##################### 
#Directory with ui and resource files
RESOURCE_DIR = ui
 
#Directory for compiled resources
COMPILED_DIR = market/views
 
#UI files to compile
UI_FILES = banksportfolio.ui investorsportfolio.ui openmarket.ui place_loan_request.ui requested_loans_1.ui borrowersportfolio.ui login.ui place_loan_offer.ui profile.ui requested_loans_2.ui

PYUIC = pyuic5
 
#################################
# DO NOT EDIT FOLLOWING
 
COMPILED_UI = $(UI_FILES:%.ui=$(COMPILED_DIR)/ui_%.py)
COMPILED_RESOURCES = $(RESOURCES:%.qrc=$(COMPILED_DIR)/%_rc.py)
 
 
all : $(COMPILED_UI)
 
$(COMPILED_DIR)/ui_%.py : $(RESOURCE_DIR)/%.ui
	$(PYUIC) $< -o $@
 
$(COMPILED_DIR)/%_rc.py : $(RESOURCE_DIR)/%.qrc
	$(PYRCC) $< -o $@
 
clean : 
	$(RM) $(COMPILED_UI) $(COMPILED_RESOURCES) $(COMPILED_UI:.py=.pyc) $(COMPILED_RESOURCES:.py=.pyc)  
