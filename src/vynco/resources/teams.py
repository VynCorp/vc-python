from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._response import Response, ResponseMeta
from vynco.types.teams import BillingSummary, Invitation, JoinTeamResponse, Team, TeamMember

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncTeams:
    """Async team operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def me(self) -> Response[Team]:
        """Get the current team."""
        return await self._client._request_model(
            "GET",
            "/v1/teams/me",
            response_type=Team,
        )

    async def create(self, *, name: str | None = None) -> Response[Team]:
        """Create a new team."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        return await self._client._request_model(
            "POST",
            "/v1/teams",
            json=body,
            response_type=Team,
        )

    async def members(self) -> Response[_list[TeamMember]]:
        """List all team members."""
        return await self._client._request_model(
            "GET",
            "/v1/teams/me/members",
            response_type=list[TeamMember],
        )

    async def invite_member(
        self,
        *,
        email: str,
        role: str | None = None,
    ) -> Response[Invitation]:
        """Invite a user to join the team."""
        body: dict[str, Any] = {"email": email}
        if role is not None:
            body["role"] = role
        return await self._client._request_model(
            "POST",
            "/v1/teams/me/members",
            json=body,
            response_type=Invitation,
        )

    async def update_member_role(self, id: str, *, role: str) -> Response[TeamMember]:
        """Update a team member's role."""
        return await self._client._request_model(
            "PUT",
            f"/v1/teams/me/members/{id}",
            json={"role": role},
            response_type=TeamMember,
        )

    async def remove_member(self, id: str) -> ResponseMeta:
        """Remove a team member."""
        return await self._client._request_empty(
            "DELETE",
            f"/v1/teams/me/members/{id}",
        )

    async def billing_summary(self) -> Response[BillingSummary]:
        """Get team billing summary for the current period."""
        return await self._client._request_model(
            "GET",
            "/v1/teams/me/billing-summary",
            response_type=BillingSummary,
        )

    async def join(self, *, token: str) -> Response[JoinTeamResponse]:
        """Join a team via invitation token."""
        return await self._client._request_model(
            "POST",
            "/v1/teams/join",
            json={"token": token},
            response_type=JoinTeamResponse,
        )


class Teams:
    """Sync team operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def me(self) -> Response[Team]:
        """Get the current team."""
        return self._client._request_model(
            "GET",
            "/v1/teams/me",
            response_type=Team,
        )

    def create(self, *, name: str | None = None) -> Response[Team]:
        """Create a new team."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        return self._client._request_model(
            "POST",
            "/v1/teams",
            json=body,
            response_type=Team,
        )

    def members(self) -> Response[_list[TeamMember]]:
        """List all team members."""
        return self._client._request_model(
            "GET",
            "/v1/teams/me/members",
            response_type=list[TeamMember],
        )

    def invite_member(
        self,
        *,
        email: str,
        role: str | None = None,
    ) -> Response[Invitation]:
        """Invite a user to join the team."""
        body: dict[str, Any] = {"email": email}
        if role is not None:
            body["role"] = role
        return self._client._request_model(
            "POST",
            "/v1/teams/me/members",
            json=body,
            response_type=Invitation,
        )

    def update_member_role(self, id: str, *, role: str) -> Response[TeamMember]:
        """Update a team member's role."""
        return self._client._request_model(
            "PUT",
            f"/v1/teams/me/members/{id}",
            json={"role": role},
            response_type=TeamMember,
        )

    def remove_member(self, id: str) -> ResponseMeta:
        """Remove a team member."""
        return self._client._request_empty(
            "DELETE",
            f"/v1/teams/me/members/{id}",
        )

    def billing_summary(self) -> Response[BillingSummary]:
        """Get team billing summary for the current period."""
        return self._client._request_model(
            "GET",
            "/v1/teams/me/billing-summary",
            response_type=BillingSummary,
        )

    def join(self, *, token: str) -> Response[JoinTeamResponse]:
        """Join a team via invitation token."""
        return self._client._request_model(
            "POST",
            "/v1/teams/join",
            json={"token": token},
            response_type=JoinTeamResponse,
        )
