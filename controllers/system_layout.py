from layouts import system_layout
from page_controller import PageController
from config.pages import PAGES

class SystemLayoutController:
    @staticmethod
    def load_main_system(root):
        systemLayout = system_layout.SystemLayout(root)
        pageContainer = systemLayout.get_page_container()
        pageController = PageController(pageContainer)
        systemLayout.create_sidebar_buttons(PAGES, pageController)

        for page in PAGES:
            pageController.register_page(page["className"])

        for idx, page in enumerate(PAGES):
            if page["default"] == True:
                pageController.display_page(idx)
                break
