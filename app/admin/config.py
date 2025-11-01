from gettext import gettext
from typing import Any

from fastapi import Request
from starlette_admin import link_row_action, row_action
from starlette_admin.contrib.sqla import ModelView

ADMIN_ICON = {
    "user": "icon-user",
    "admin": "icon-shield",
}

def setup_admin_defaults():

    setup_row_actions()


def setup_row_actions():
    @link_row_action(
        name="view",
        text="View",
        icon_class="icon-eye",
        exclude_from_detail=True,
    )
    def row_action_1_view(self, request: Request, pk: Any) -> str:
        route_name = request.app.state.ROUTE_NAME
        return str(
            request.url_for(route_name + ":detail", identity=self.identity, pk=pk)
        )

    @link_row_action(
        name="edit",
        text="Edit",
        icon_class="icon-pencil",
        action_btn_class="btn-primary",
    )
    def row_action_2_edit(self, request: Request, pk: Any) -> str:
        route_name = request.app.state.ROUTE_NAME
        return str(request.url_for(route_name + ":edit", identity=self.identity, pk=pk))

    @row_action(
        name="delete",
        text="Delete",
        confirmation="Are you sure you want to delete this item?",
        icon_class="icon-trash",
        submit_btn_text="Yes, delete",
        submit_btn_class="btn-danger",
        action_btn_class="btn-danger",
    )
    async def row_action_3_delete(self, request: Request, pk: Any) -> str:
        await self.delete(request, [pk])
        return gettext("Item was successfully deleted")

    ModelView.row_action_1_view = row_action_1_view
    ModelView.row_action_2_edit = row_action_2_edit
    ModelView.row_action_3_delete = row_action_3_delete