from idlelib.textview import ViewFrame
from operator import index
from typing import Optional

import discord
from discord import Embed
from discord.ui import Button, View, Select, item

class Page:
    def __init__(self, embed : Embed, *items : item):
        self.embed = embed
        self.view = None
        if items :
            view = View()
            for _item in items :
                view.add_item(_item)
            self.view = view

    def __iter__(self):
        yield from [self.embed, self.view]

class Pages:
    def __init__(self, *pages : Page,current_page = None ,prev_button_label : str = "이전", next_button_label : str = "다음"):
        self.pages = pages

        if current_page :
            self.current_page = current_page
        else :
            self.current_page = self.pages[0]


        # pages에서 받아온 page들을 순회함
        for _page in self.pages:
            prevButton = PrevButton(prev_button_label, pages=self, current_page=_page)
            nextButton = NextButton(next_button_label, pages=self, current_page=_page)
            # _page.view가 존재 한다면 _page.view의 children을 한칸씩 밀어서 맨 앞엔 prevButton, 맨 뒤엔 nextButton이 들어가게 함
            if _page.view:
                old_children = list(_page.view.children)
                _page.view.clear_items()
                _page.view.add_item(prevButton)

                for _item in old_children:
                    _page.view.add_item(_item)

                _page.view.add_item(nextButton)
            else :
                _page.view = View()
                _page.view.add_item(prevButton)
                _page.view.add_item(nextButton)


class PrevButton(Button):
    def __init__(self, label: str, pages, current_page=None):
        self.pages = pages
        self.current_page = current_page
        if self.pages and current_page :
            if not self.pages.pages[0] is current_page :
                super().__init__(label=label, disabled= False)
            else:
                super().__init__(label=label, disabled= True)

    async def callback(self, interaction: discord.Interaction):
        try:
            idx = self.pages.pages.index(self.current_page)
            print(idx)
            next_page = self.pages.pages[idx - 1]

            self.pages.current_page = next_page

            await interaction.response.edit_message(
                embed=next_page.embed,
                view=next_page.view
            )

        except (ValueError, IndexError):
            await interaction.response.send_message(
                "이전 페이지가 없습니다.", ephemeral=True
            )

class NextButton(Button):
    def __init__(self, label: str, pages, current_page=None):
        self.pages = pages
        self.current_page = current_page
        if self.pages and current_page :
            if not self.pages.pages[len(self.pages.pages) - 1] is current_page :
                super().__init__(label=label, disabled= False)
            else:
                super().__init__(label=label, disabled= True)

    async def callback(self, interaction: discord.Interaction):
        try:
            idx = self.pages.pages.index(self.current_page)
            next_page = self.pages.pages[idx + 1]

            self.pages.current_page = next_page

            await interaction.response.edit_message(
                embed=next_page.embed,
                view=next_page.view
            )

        except (ValueError, IndexError):
            await interaction.response.send_message(
                "다음 페이지가 없습니다.", ephemeral=True
            )