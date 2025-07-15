from typing import Optional, Tuple
import discord
from discord import Embed, Interaction
from discord.ui import Button, View, Select

from utils.Debuggin import get_current_file_and_line


class Page:
    def __init__(self, embed: Embed, view: Optional[View] = None):
        self.embed = embed
        self.view = view or View(timeout=None)

    def __iter__(self):
        yield from [self.embed, self.view]

class PageNavigationButton(Button):
    def __init__(self, label: str, pages: 'Pages', current_page: Page, is_prev: bool = False):
        self.pages = pages
        self.current_page = current_page
        self.is_prev = is_prev
        disabled = self._is_disabled()
        super().__init__(label=label, style = discord.ButtonStyle.grey, disabled=disabled)

    def _is_disabled(self) -> bool:
        if not self.pages or not self.current_page:
            return True
        idx = self.pages.pages.index(self.current_page)
        return idx == 0 if self.is_prev else idx == len(self.pages.pages) - 1

    async def callback(self, interaction: Interaction):
        try:
            idx = self.pages.pages.index(self.current_page)
            next_idx = idx - 1 if self.is_prev else idx + 1
            next_page = self.pages.pages[next_idx]
            self.pages.current_page = next_page

            for item in next_page.view.children:
                if isinstance(item, PageNavigationButton):
                    item.disabled = item._is_disabled()

            await interaction.response.edit_message(embed=next_page.embed, view=next_page.view)
        except (ValueError, IndexError):
            await interaction.response.send_message(
                f"{'◀️' if self.is_prev else '▶️'} 페이지가 없습니다.", ephemeral=True
            )

class SelectNavigationButton(Button):
    ##TODO : 여기서 실질적 작동을 구현 해야함.

    def __init__(self, label: str, pages: 'Pages', current_page: Page, is_prev: bool = False):
        self.pages = pages
        self.current_page = current_page
        self.is_prev = is_prev
        disabled = self._is_disabled()
        super().__init__(label=label, style = discord.ButtonStyle.grey, disabled=disabled)

        get_current_file_and_line()
    def _is_disabled(self) -> bool:
        get_current_file_and_line()

        if not self.pages or not self.current_page:
            return True

        idx = self.pages.pages.index(self.current_page)
        get_current_file_and_line()
        if self.is_prev and idx == 0:
            get_current_file_and_line()
            return True
        if not self.is_prev and idx == len(self.pages.pages) - 1:
            get_current_file_and_line()
            return True

        for _item in self.current_page.view.children:
            get_current_file_and_line()

            if isinstance(_item, Select) and len(_item.options) > 25:
                get_current_file_and_line()
                return True
        return False


class Pages:

    def __init__(self, *pages: Page, page_prev_button_label: str = "◀️", page_next_button_label: str = "▶️"):
        self.pages: Tuple[Page, ...] = pages
        self.current_page: Page = pages[0] if pages else None
        self.page_prev_button_label = page_prev_button_label
        self.page_next_button_label = page_next_button_label

        get_current_file_and_line()

        for page in self.pages:
            get_current_file_and_line()
            in_Select = False



            for _item in page.view.children :
                if isinstance(_item, Select):
                    in_Select = True
                    get_current_file_and_line()

            self.page_prev_button = PageNavigationButton(self.page_prev_button_label, self, page, is_prev=True)
            self. page_next_button = PageNavigationButton(self.page_next_button_label, self, page, is_prev=False)
            get_current_file_and_line()

            if in_Select:
                get_current_file_and_line()
                self.select_prev_button = SelectNavigationButton("tset1", self, page, is_prev=True)
                self.select_next_button = SelectNavigationButton("tset2", self, page, is_prev=False)

            old_children = list(page.view.children) if page.view else []
            page.view.clear_items()
            get_current_file_and_line()

            if in_Select:
                page.view.add_item(self.select_prev_button)
            page.view.add_item(self.page_prev_button)
            get_current_file_and_line()

            for item in old_children:
                page.view.add_item(item)
            page.view.add_item(self.page_next_button)

            if in_Select:
                page.view.add_item(self.select_next_button)