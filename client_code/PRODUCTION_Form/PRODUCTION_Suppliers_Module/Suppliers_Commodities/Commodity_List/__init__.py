from ._anvil_designer import Commodity_ListTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import component_cache

class Commodity_List(Commodity_ListTemplate):
  def __init__(self, supplier_id = None,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id
    

    # Any code you write here will run before the form opens.
    commodities = component_cache.get_commodities(self.supplier_id)
    self.commodity_repeating_panel.items = commodities


    
