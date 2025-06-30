from nicegui import ui
from pages.login import login_page
from pages.background import page as background_page
from pages.calibration import page as calibration_page
from pages.acquisition import page as acquisition_page
# from pages.scope import scope_page

from pages.background_sampling import page as background_sampling_page
from pages.calibration_sampling import page as calibration_sampling_page
from pages.acquisition_sampling import page as acquisition_sampling_page
from pages.database import page as database_page


def create_all_pages() -> None:
    ui.page('/login')(login_page)
    ui.page("/background")(background_page)
    ui.page("/calibration")(calibration_page)
    ui.page("/acquisition")(acquisition_page)
    # ui.page("/scope")(scope_page)

    ui.page("/background_sampling")(background_sampling_page)
    ui.page("/calibration_sampling")(calibration_sampling_page)
    ui.page("/acquisition_sampling")(acquisition_sampling_page)
    ui.page("/database")(database_page)

if __name__ == '__main__':
    create_all_pages()