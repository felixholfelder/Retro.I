from enum import Enum

import flet as ft

from helper.RevisionHelper import RevisionHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
revision_helper = RevisionHelper()


class RevisionType(Enum):
    BRANCH = "BRANCH"
    TAG = "TAG"


class SettingsUpdateDialog(ft.AlertDialog):
    branches_list = ft.ListView()
    tags_list = ft.ListView()

    def __init__(self):
        super().__init__()
        # TODO - bold title (or maybe only bold revision)
        self.title = ft.Text(f"Aktueller Stand: {self.get_current_revision()}")
        # TODO - check if scrolling works with more items
        self.content = ft.Column(
            width=500,
            tight=True,
            controls=[
                ft.Divider(),
                ft.Tabs(
                    animation_duration=300,
                    tabs=[
                        # TODO - strech tabs for complete width
                        ft.Tab(
                            text="Branches",
                            content=self.branches_list,
                        ),
                        ft.Tab(
                            text="Tags",
                            content=self.tags_list,
                        ),
                    ],
                    expand=True,
                ),
            ],
        )

    def open_dialog(self):
        self.fill_branches_list()
        self.fill_tags_list()
        self.open = True
        self.update()

    def fill_branches_list(self):
        branches = revision_helper.get_branches()

        self.branches_list.controls.clear()
        self.branches_list.controls = self._get_items(branches, RevisionType.BRANCH)
        self.branches_list.update()

    def fill_tags_list(self):
        tags = revision_helper.get_tags()

        self.tags_list.controls.clear()
        self.tags_list.controls = self._get_items(tags, RevisionType.TAG)
        self.tags_list.update()

    def _get_items(self, revisions: list, revision_type: RevisionType):
        return [
            ft.TextButton(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.DONE, visible=(r == self.get_current_revision())),
                            ft.Text(
                                r,
                                size=18,
                                # TODO - remove BOLD
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                ),
                on_click=lambda e, revision=r: self.on_revision_click(revision, revision_type),
            )
            for r in revisions
        ]

    def on_revision_click(self, revision, revision_type):
        # TODO - what happens when revision clicked
        print(f"You clicked {revision_type} {revision}")
        pass

    def get_current_revision(self):
        return revision_helper.get_current_revision()
