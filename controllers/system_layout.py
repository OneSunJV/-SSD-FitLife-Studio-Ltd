from layouts import system_layout
from page_controller import PageController
from config.pages import PAGES

class SystemLayoutController:
    @staticmethod
    def load_main_system(root):
        systemLayout = system_layout.SystemLayout(root)
        pageContainer = systemLayout.get_page_container()
        pageController = PageController(pageContainer)
        system_layout.SystemLayout.create_sidebar_buttons(PAGES, pageController)
        for page in PAGES:
            pageController.register_page(page["className"])
        pageController.display_page(next(filter(PAGES, lambda page: page["default"] == True))["className"])